/*==========================================================
  MESIN PENCETAK TEMPE OTOMATIS v10.0 (BUG-FIXED & READY)
  ──────────────────────────────────────────────────────────
  Perbaikan menyeluruh dari v9.0:
  1. FIX Error Compile: PIN_TRIG & PIN_ECHO dibungkus #if USE_HCSR04.
  2. FIX Gate Hopper: Mendukung Servo MG996R (GATE_USE_SERVO 1)
     DAN Relay Solenoid (GATE_USE_SERVO 0) + opsi RELAY_ACTIVE_LOW.
  3. FIX GPIO 34 & 35: Menggunakan pinMode(..., INPUT) sesuai hardware
     ESP32 input-only dengan resistor pull-up eksternal 10kΩ.
  4. FIX ROTATE_TEST Dashboard: stepper.run() selalu dipanggil di loop().
  5. FIX Safety Interlock: Aktuator mengecek Limit Switch sebelum gerak
     & delay panjang non-blocking agar Web Dashboard & STOP selalu responsif.
  6. FITUR BARU: Serial Bench Dry-Run Console (ketik '?' di Serial Monitor)
     untuk menguji seluruh modul + 1 siklus penuh di meja sebelum pasang rangka!

  PIN MAP ESP32 DevKit V1 (38-pin):
    GPIO  4  -> HX711 DOUT (Data Load Cell 20 kg)
    GPIO  5  -> HX711 SCK  (Clock Load Cell 20 kg)
    GPIO 12  -> TB6600 PUL+ (STEP NEMA 23 Flip 180°)
    GPIO 14  -> TB6600 DIR+ (DIR NEMA 23)
    GPIO 13  -> Relay Elektromagnet 12V (Kunci Tutup Cetakan)
    GPIO 25  -> L298N IN1 (Linear Actuator Press TURUN)
    GPIO 26  -> L298N IN2 (Linear Actuator Press NAIK)
    GPIO 27  -> Servo Gate MG996R (PWM) / Relay Gate Hopper
    GPIO 32  -> Limit Switch ATAS (INPUT_PULLUP, aktif LOW)
    GPIO 33  -> Limit Switch BAWAH (INPUT_PULLUP, aktif LOW)
    GPIO 34  -> Tombol Fisik START (INPUT, ext pull-up 10k, aktif LOW)
    GPIO 35  -> Tombol Fisik STOP  (INPUT, ext pull-up 10k, aktif LOW)
    GPIO  2  -> LED Hijau (OK / RUN)
    GPIO 15  -> LED Merah (ALARM)
    GPIO 23  -> Buzzer Aktif 5V
==========================================================*/

// ════════════════════════════════════════════════════════
// SECTION 1 — Feature Flags & Konfigurasi Hardware
// ════════════════════════════════════════════════════════
#define USE_LCD           0   // 0 = Tanpa LCD (Web Dashboard WiFi), 1 = LCD 16x2 I2C
#define USE_HCSR04        0   // 0 = Pantau visual, 1 = Sensor ultrasonik HC-SR04
#define GATE_USE_SERVO    1   // 1 = Servo MG996R (GPIO 27), 0 = Relay Solenoid Gate
#define RELAY_ACTIVE_LOW  1   // 1 = Modul relay optocoupler aktif LOW, 0 = aktif HIGH

#include <WiFi.h>
#include <WebServer.h>
#include <SPIFFS.h>
#include <HX711.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <AccelStepper.h>

#if GATE_USE_SERVO
  #include <ESP32Servo.h>
#endif

#if USE_LCD
  #include <Wire.h>
  #include <LiquidCrystal_I2C.h>
#endif

// ════════════════════════════════════════════════════════
// SECTION 2 — Konfigurasi WiFi, Pinout & Konstanta Mekanik
// ════════════════════════════════════════════════════════
const char* WIFI_SSID     = "NAMA_WIFI_KAMU";     // ← Ganti dengan WiFi lokalmu
const char* WIFI_PASSWORD = "PASSWORD_WIFI_KAMU"; // ← Ganti dengan password WiFi

// Pin Mapping Utama (sesuai Panduan Uji Hardware v9/v10)
#define PIN_HX711_DOUT    4
#define PIN_HX711_SCK     5
#define PIN_STEPPER_STEP 12
#define PIN_RELAY_MAGNET 13
#define PIN_STEPPER_DIR  14
#define PIN_MOTOR_IN1    25
#define PIN_MOTOR_IN2    26
#define PIN_GATE         27
#define PIN_LIMIT_ATAS   32
#define PIN_LIMIT_BAWAH  33
#define PIN_BTN_START    34
#define PIN_BTN_STOP     35
#define PIN_LED_OK        2
#define PIN_LED_ALARM    15
#define PIN_BUZZER       23

#if USE_HCSR04
  #define PIN_TRIG       18
  #define PIN_ECHO       19
#endif

#if USE_LCD
  #define PIN_SDA        21
  #define PIN_SCL        22
#endif

// Konfigurasi Servo Gate (jika GATE_USE_SERVO == 1)
#define SERVO_ANGLE_TUTUP     0
#define SERVO_ANGLE_BUKA     90

// Konstanta Mekanik v10
#define SLOT_COUNT            6
#define STEPS_180DEG       2400       // 200 step * 8 ustep * rasio 3 / 2 = 2400 step
#define NEMA23_MAX_SPEED    800.0f    // step/detik
#define NEMA23_ACCEL        400.0f    // step/detik^2
#define TIMEOUT_HOMING_MS  35000UL    // Aman untuk stroke 200 mm @ 6 mm/s (~33 dtk)
#define TIMEOUT_PRESS_MS   35000UL    // Aman untuk stroke 200 mm @ 6 mm/s
#define TIMEOUT_DOSING_MS  90000UL    // Max waktu dosing 90 detik
#define DEBOUNCE_MS           40

// Default Parameter (bisa diubah dari Web Dashboard)
#define BERAT_DEFAULT         0.0f    // 0 = Mode Manual, >0 = Mode Otomatis (misal 900g)
#define WAKTU_TAHAN_DEFAULT  5000     // ms (5 detik)
#define LEVEL_ALARM_DEFAULT   8.0f    // cm
#define LOADCELL_FAKTOR     420.0f    // ← Ganti dengan hasil kalibrasi Uji 3!

// Helper level logika relay
#if RELAY_ACTIVE_LOW
  #define RELAY_ON  LOW
  #define RELAY_OFF HIGH
#else
  #define RELAY_ON  HIGH
  #define RELAY_OFF LOW
#endif

// ════════════════════════════════════════════════════════
// SECTION 3 — State Machine & Variabel Global
// ════════════════════════════════════════════════════════
enum State {
  ST_HOMING,
  ST_IDLE,
  ST_CEK_HOPPER,
  ST_TUNGGU_SIAP,
  ST_DOSING,
  ST_PRESSING,
  ST_LIFT_OFF,
  ST_LOCK_LID,
  ST_ROTATE_MOLD,
  ST_UNLOCK_LID,
  ST_RETURN_MOLD,
  ST_SELESAI,
  ST_ALARM_HOPPER,
  ST_ALARM_ERROR
};

State  currentState    = ST_HOMING;
String stateStr        = "HOMING";
bool   webStartRequest = false;
bool   webStopRequest  = false;

float beratSaatIni     = 0.0f;
float levelHopper      = 5.0f;

float beratTarget      = BERAT_DEFAULT;
int   waktuTahan       = WAKTU_TAHAN_DEFAULT;
float levelAlarm       = LEVEL_ALARM_DEFAULT;

int   counterHariIni   = 0;
int   counterTotal     = 0;

bool  magnetActive     = false;
bool  gateOpen         = false;

unsigned long lastSensorUpdate = 0;
unsigned long lastBlinkTime    = 0;
bool          ledBlinkState    = false;

HX711        scale;
WebServer    server(80);
Preferences  prefs;
AccelStepper stepper(AccelStepper::DRIVER, PIN_STEPPER_STEP, PIN_STEPPER_DIR);

#if GATE_USE_SERVO
  Servo gateServo;
#endif

#if USE_LCD
  LiquidCrystal_I2C lcd(0x27, 16, 2);
#endif

// ════════════════════════════════════════════════════════
// SECTION 4 — Fungsi Sensor & Tombol
// ════════════════════════════════════════════════════════
float bacaBerat() {
  if (!scale.is_ready()) return beratSaatIni;
  float val = scale.get_units(3);
  return (val < 0.0f) ? 0.0f : val;
}

float bacaHopper() {
#if USE_HCSR04
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  long dur = pulseIn(PIN_ECHO, HIGH, 30000UL);
  if (dur == 0) return 999.0f;
  return (dur * 0.0343f) / 2.0f;
#else
  return 5.0f;
#endif
}

bool limitAtas()  { return digitalRead(PIN_LIMIT_ATAS)  == LOW; }
bool limitBawah() { return digitalRead(PIN_LIMIT_BAWAH) == LOW; }

bool tombolStart() {
  if (webStartRequest) { webStartRequest = false; return true; }
  if (digitalRead(PIN_BTN_START) == LOW) {
    delay(DEBOUNCE_MS);
    if (digitalRead(PIN_BTN_START) == LOW) {
      while (digitalRead(PIN_BTN_START) == LOW) { server.handleClient(); delay(10); }
      return true;
    }
  }
  return false;
}

bool tombolStop() {
  if (webStopRequest) { webStopRequest = false; return true; }
  if (digitalRead(PIN_BTN_STOP) == LOW) {
    delay(DEBOUNCE_MS);
    if (digitalRead(PIN_BTN_STOP) == LOW) {
      return true;
    }
  }
  return false;
}

// ════════════════════════════════════════════════════════
// SECTION 5 — Fungsi Aktuator (dengan Safety Interlock)
// ════════════════════════════════════════════════════════
void motorStop() {
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, LOW);
}

void motorTurun() {
  if (limitBawah()) { motorStop(); return; }
  digitalWrite(PIN_MOTOR_IN1, HIGH);
  digitalWrite(PIN_MOTOR_IN2, LOW);
}

void motorNaik() {
  if (limitAtas()) { motorStop(); return; }
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, HIGH);
}

void setGate(bool buka) {
  gateOpen = buka;
#if GATE_USE_SERVO
  gateServo.write(buka ? SERVO_ANGLE_BUKA : SERVO_ANGLE_TUTUP);
#else
  digitalWrite(PIN_GATE, buka ? RELAY_ON : RELAY_OFF);
#endif
  Serial.printf("[GATE] %s\n", buka ? "BUKA" : "TUTUP");
}

void setMagnet(bool active) {
  magnetActive = active;
  digitalWrite(PIN_RELAY_MAGNET, active ? RELAY_ON : RELAY_OFF);
  Serial.printf("[MAGNET] %s\n", active ? "TERKUNCI (ON)" : "LEPAS (OFF)");
}

void setLED(bool ok, bool alarm) {
  digitalWrite(PIN_LED_OK,    ok    ? HIGH : LOW);
  digitalWrite(PIN_LED_ALARM, alarm ? HIGH : LOW);
}

void buzzer(int kali, int durMs = 120, int jedaMs = 90) {
  for (int i = 0; i < kali; i++) {
    digitalWrite(PIN_BUZZER, HIGH); delay(durMs);
    digitalWrite(PIN_BUZZER, LOW);  delay(jedaMs);
  }
}

void lcdPrint(const String& b1, const String& b2) {
#if USE_LCD
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print(b1.substring(0, 16));
  lcd.setCursor(0, 1); lcd.print(b2.substring(0, 16));
#else
  static String lastB1 = "", lastB2 = "";
  if (b1 != lastB1 || b2 != lastB2) {
    Serial.printf("[DISPLAY] %s | %s\n", b1.c_str(), b2.c_str());
    lastB1 = b1;
    lastB2 = b2;
  }
#endif
}

// Delay non-blocking: tetap melayani Web Server, Stepper, dan deteksi STOP
bool smartDelay(unsigned long ms, bool allowStop = true) {
  unsigned long t0 = millis();
  while (millis() - t0 < ms) {
    server.handleClient();
    stepper.run();
    if (allowStop && tombolStop()) return false;
    delay(5);
  }
  return true;
}

void emergencyHalt(const char* reason) {
  motorStop();
  setGate(false);
  stepper.stop();
  setLED(false, true);
  Serial.printf("[EMERGENCY] %s\n", reason);
  buzzer(3, 180, 100);
}

// ════════════════════════════════════════════════════════
// SECTION 6 — Finite State Machine (v10 Clean Flow)
// ════════════════════════════════════════════════════════
void changeState(State next) {
  const char* names[] = {
    "HOMING", "IDLE", "CEK_HOPPER", "TUNGGU_SIAP",
    "DOSING", "PRESSING", "LIFT_OFF",
    "LOCK_LID", "ROTATE_MOLD", "UNLOCK_LID", "RETURN_MOLD", "SELESAI",
    "ALARM_HOPPER", "ALARM_ERROR"
  };
  currentState = next;
  stateStr = names[next];
  Serial.printf("[FSM] -> %s\n", stateStr.c_str());
}

void handleHoming() {
  lcdPrint("HOMING...", "Aktuator naik");
  setLED(false, false);

  if (!limitAtas()) {
    motorNaik();
    unsigned long t0 = millis();
    while (!limitAtas()) {
      server.handleClient();
      if (tombolStop()) {
        emergencyHalt("STOP saat HOMING");
        changeState(ST_IDLE);
        return;
      }
      if (millis() - t0 > TIMEOUT_HOMING_MS) {
        emergencyHalt("Timeout HOMING (Limit Atas tidak tersentuh)");
        changeState(ST_ALARM_ERROR);
        return;
      }
      delay(10);
    }
    motorStop();
  }

  lcdPrint("Homing Selesai", "Tekan START");
  buzzer(1, 180);
  changeState(ST_IDLE);
}

void handleIdle() {
  if (millis() - lastBlinkTime > 700) {
    ledBlinkState = !ledBlinkState;
    digitalWrite(PIN_LED_OK, ledBlinkState);
    lastBlinkTime = millis();
  }
  digitalWrite(PIN_LED_ALARM, LOW);

  String mode = (beratTarget > 0.0f)
    ? "Target:" + String((int)beratTarget) + "g"
    : "Mode: Manual";
  lcdPrint("READY - START", mode);

  if (tombolStart()) {
#if USE_HCSR04
    changeState(ST_CEK_HOPPER);
#else
    changeState(ST_DOSING);
#endif
  }
}

void handleCekHopper() {
  lcdPrint("Cek kedelai...", "");
  levelHopper = bacaHopper();
  if (levelHopper > levelAlarm) {
    changeState(ST_ALARM_HOPPER);
    return;
  }
  changeState(ST_TUNGGU_SIAP);
}

void handleTungguSiap() {
  setLED(true, false);
  lcdPrint("Pasang plastik", "START=lanjut");
  if (scale.is_ready()) scale.tare();
  while (true) {
    server.handleClient();
    if (tombolStop())  { changeState(ST_IDLE);   return; }
    if (tombolStart()) { changeState(ST_DOSING); return; }
    delay(25);
  }
}

void handleDosing() {
  setLED(true, false);

  // Mode Manual (beratTarget == 0)
  if (beratTarget <= 0.0f) {
    lcdPrint("ISI KEDELAI", "START=press");
    while (true) {
      server.handleClient();
      beratSaatIni = bacaBerat();
      if (tombolStop())  { changeState(ST_IDLE);     return; }
      if (tombolStart()) { changeState(ST_PRESSING); return; }
      delay(80);
    }
  }

  // Mode Otomatis (Weigh-Box Load Cell 20 kg)
  if (scale.is_ready()) scale.tare();
  setGate(true);
  Serial.printf("[DOSING] Target: %.0f g (6 slot)\n", beratTarget);
  unsigned long t0 = millis();
  const float inFlightOffset = 20.0f; // kompensasi kedelai yang masih jatuh

  while (millis() - t0 < TIMEOUT_DOSING_MS) {
    server.handleClient();
    beratSaatIni = bacaBerat();

    if (beratSaatIni >= (beratTarget - inFlightOffset)) {
      setGate(false);
      if (!smartDelay(700)) { changeState(ST_IDLE); return; }
      beratSaatIni = bacaBerat();
      Serial.printf("[DOSING] Selesai: %.0f g\n", beratSaatIni);
      changeState(ST_PRESSING);
      return;
    }
    if (tombolStop()) {
      setGate(false);
      changeState(ST_IDLE);
      return;
    }
    delay(60);
  }

  setGate(false);
  emergencyHalt("Timeout DOSING");
  changeState(ST_ALARM_ERROR);
}

void handlePressing() {
  setLED(true, false);
  lcdPrint("PRESSING...", "Aktuator turun");

  if (!limitBawah()) {
    motorTurun();
    unsigned long t0 = millis();
    while (!limitBawah()) {
      server.handleClient();
      if (millis() - t0 > TIMEOUT_PRESS_MS) {
        emergencyHalt("Timeout PRESSING (Limit Bawah tidak tersentuh)");
        changeState(ST_ALARM_ERROR);
        return;
      }
      if (tombolStop()) {
        motorStop();
        changeState(ST_HOMING);
        return;
      }
      delay(10);
    }
    motorStop();
  }

  // Tahan posisi pemadatan
  unsigned long holdStart = millis();
  while (millis() - holdStart < (unsigned long)waktuTahan) {
    server.handleClient();
    if (tombolStop()) { changeState(ST_HOMING); return; }
    int sisa = (waktuTahan - (int)(millis() - holdStart)) / 1000 + 1;
    lcdPrint("Tahan press:", String(sisa) + " detik...");
    delay(50);
  }

  changeState(ST_LIFT_OFF);
}

void handleLiftOff() {
  lcdPrint("LIFT-OFF...", "Naik ke HOME");
  if (!limitAtas()) {
    motorNaik();
    unsigned long t0 = millis();
    while (!limitAtas()) {
      server.handleClient();
      if (millis() - t0 > TIMEOUT_HOMING_MS) {
        emergencyHalt("Timeout LIFT_OFF (Limit Atas tidak tersentuh)");
        changeState(ST_ALARM_ERROR);
        return;
      }
      if (tombolStop()) {
        motorStop();
        changeState(ST_IDLE);
        return;
      }
      delay(10);
    }
    motorStop();
  }
  changeState(ST_LOCK_LID);
}

void handleLockLid() {
  // Interlock keselamatan v10: JANGAN putar jika press belum di HOME (Limit Atas)!
  if (!limitAtas()) {
    emergencyHalt("Interlock! Press belum di posisi HOME sebelum Flip 180°");
    changeState(ST_ALARM_ERROR);
    return;
  }
  lcdPrint("Kunci Tutup", "Magnet Aktif...");
  setMagnet(true);
  if (!smartDelay(800)) { setMagnet(false); changeState(ST_IDLE); return; }
  changeState(ST_ROTATE_MOLD);
}

void handleRotateMold() {
  lcdPrint("Flip 180 deg", "Awas menjauh...");
  stepper.moveTo(STEPS_180DEG);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    server.handleClient();
    if (tombolStop()) {
      emergencyHalt("STOP saat ROTATE_MOLD");
      changeState(ST_ALARM_ERROR);
      return;
    }
  }
  changeState(ST_UNLOCK_LID);
}

void handleUnlockLid() {
  lcdPrint("Lepas Tempe", "Magnet OFF...");
  setMagnet(false);
  buzzer(3, 160, 90);
  lcdPrint("Tempe Siap!", "START = Balik 0");

  while (true) {
    server.handleClient();
    if (tombolStart()) { changeState(ST_RETURN_MOLD); return; }
    if (tombolStop())  { changeState(ST_IDLE);        return; }
    delay(25);
  }
}

void handleReturnMold() {
  lcdPrint("Balik 0 deg...", "");
  stepper.moveTo(0);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    server.handleClient();
    if (tombolStop()) {
      emergencyHalt("STOP saat RETURN_MOLD");
      changeState(ST_ALARM_ERROR);
      return;
    }
  }
  changeState(ST_SELESAI);
}

void handleSelesai() {
  counterHariIni += SLOT_COUNT;
  counterTotal   += SLOT_COUNT;
  prefs.putInt("counterTotal", counterTotal);
  prefs.putInt("counterHari",  counterHariIni);

  setLED(true, false);
  buzzer(2, 240, 120);
  lcdPrint(String(SLOT_COUNT) + " TEMPE SIAP!",
           "Hari:" + String(counterHariIni) + " Tot:" + String(counterTotal));
  Serial.printf("[DONE] Siklus selesai! Hari:%d Total:%d\n", counterHariIni, counterTotal);

  smartDelay(2000, false);
  changeState(ST_IDLE); // Kembali aman ke IDLE (fix v10)
}

void handleAlarmHopper() {
  setLED(false, true);
  lcdPrint("! KEDELAI HABIS", "Isi & tekan STOP");
  if (!smartDelay(1200)) {
    changeState(ST_IDLE);
  }
}

void handleAlarmError() {
  setLED(false, true);
  lcdPrint("! ERROR MEKANIK", "STOP = reset IDLE");
  if (!smartDelay(1200)) {
    setLED(false, false);
    changeState(ST_HOMING);
  }
}

void runFSM() {
  switch (currentState) {
    case ST_HOMING:       handleHoming();      break;
    case ST_IDLE:         handleIdle();        break;
    case ST_CEK_HOPPER:   handleCekHopper();   break;
    case ST_TUNGGU_SIAP:  handleTungguSiap();  break;
    case ST_DOSING:       handleDosing();      break;
    case ST_PRESSING:     handlePressing();    break;
    case ST_LIFT_OFF:     handleLiftOff();     break;
    case ST_LOCK_LID:     handleLockLid();     break;
    case ST_ROTATE_MOLD:  handleRotateMold();  break;
    case ST_UNLOCK_LID:   handleUnlockLid();   break;
    case ST_RETURN_MOLD:  handleReturnMold();  break;
    case ST_SELESAI:      handleSelesai();     break;
    case ST_ALARM_HOPPER: handleAlarmHopper(); break;
    case ST_ALARM_ERROR:  handleAlarmError();  break;
  }
}

// ════════════════════════════════════════════════════════
// SECTION 7 — Serial Bench Dry-Run Console (Baru di v10!)
// ════════════════════════════════════════════════════════
void printSerialHelp() {
  Serial.println("\n┌────────────────────────────────────────────────┐");
  Serial.println("│  TEMPEHKIT v10 — SERIAL BENCH DRY-RUN CONSOLE  │");
  Serial.println("├────────────────────────────────────────────────┤");
  Serial.println("│  's' : Trigger START (mulai/lanjut siklus)     │");
  Serial.println("│  'x' : Trigger STOP / EMERGENCY                │");
  Serial.println("│  'g' : Toggle Gate Hopper (Servo/Relay)        │");
  Serial.println("│  'm' : Toggle Elektromagnet Pengunci           │");
  Serial.println("│  'r' : Test Rotasi NEMA 23 (0° <-> 180°)       │");
  Serial.println("│  'u' : Manual Aktuator NAIK (cek LS Atas)      │");
  Serial.println("│  'd' : Manual Aktuator TURUN (cek LS Bawah)    │");
  Serial.println("│  'o' : Manual Aktuator STOP                    │");
  Serial.println("│  't' : Tare (nol-kan) Timbangan Load Cell      │");
  Serial.println("│  'i' : Info Status Sensor & State Realtime     │");
  Serial.println("│  '?' : Tampilkan menu ini                      │");
  Serial.println("└────────────────────────────────────────────────┘\n");
}

void handleSerialConsole() {
  if (!Serial.available()) return;
  char c = Serial.read();
  if (c == '\n' || c == '\r') return;

  switch (c) {
    case 's': case 'S': webStartRequest = true; Serial.println("[CMD] START dikirim"); break;
    case 'x': case 'X': webStopRequest  = true; Serial.println("[CMD] STOP dikirim");  break;
    case 'g': case 'G': setGate(!gateOpen);     break;
    case 'm': case 'M': setMagnet(!magnetActive); break;
    case 'r': case 'R': {
      long target = (stepper.currentPosition() < (STEPS_180DEG / 2)) ? STEPS_180DEG : 0;
      stepper.moveTo(target);
      Serial.printf("[CMD] NEMA 23 menuju %ld step\n", target);
      break;
    }
    case 'u': case 'U': motorNaik();  Serial.println("[CMD] Aktuator NAIK");  break;
    case 'd': case 'D': motorTurun(); Serial.println("[CMD] Aktuator TURUN"); break;
    case 'o': case 'O': motorStop();  Serial.println("[CMD] Aktuator STOP");  break;
    case 't': case 'T':
      if (scale.is_ready()) scale.tare();
      Serial.println("[CMD] Load Cell Tare OK");
      break;
    case 'i': case 'I':
      Serial.printf("[INFO] State=%s | Berat=%.1fg | LS_Atas=%d | LS_Bawah=%d | Gate=%d | Magnet=%d | Step=%ld\n",
                    stateStr.c_str(), bacaBerat(), limitAtas(), limitBawah(),
                    gateOpen, magnetActive, stepper.currentPosition());
      break;
    case '?': printSerialHelp(); break;
  }
}

// ════════════════════════════════════════════════════════
// SECTION 8 — Web Server & REST API
// ════════════════════════════════════════════════════════
void sendCorsHeaders() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}

void handleApiStatus() {
  StaticJsonDocument<512> doc;
  doc["version"]        = "v10.0";
  doc["state"]          = stateStr;
  doc["beratSaatIni"]   = (int)beratSaatIni;
  doc["beratTarget"]    = (int)beratTarget;
  doc["levelHopper"]    = levelHopper;
  doc["counterHariIni"] = counterHariIni;
  doc["counterTotal"]   = counterTotal;
  doc["waktuTahan"]     = waktuTahan / 1000;
  doc["slotCount"]      = SLOT_COUNT;
  doc["limitAtas"]      = limitAtas();
  doc["limitBawah"]     = limitBawah();
  doc["magnetActive"]   = magnetActive;
  doc["gateOpen"]       = gateOpen;
  doc["stepperPos"]     = stepper.currentPosition();
  doc["modeDosing"]     = (beratTarget > 0.0f) ? "otomatis" : "manual";
  doc["ipAddress"]      = (WiFi.status() == WL_CONNECTED) ? WiFi.localIP().toString() : "Offline";
  String out;
  serializeJson(doc, out);
  sendCorsHeaders();
  server.send(200, "application/json", out);
}

void handleApiControl() {
  sendCorsHeaders();
  if (server.method() == HTTP_OPTIONS) { server.send(204); return; }
  if (!server.hasArg("plain")) {
    server.send(400, "application/json", "{\"ok\":false,\"msg\":\"No body\"}");
    return;
  }
  StaticJsonDocument<128> doc;
  deserializeJson(doc, server.arg("plain"));
  String cmd = doc["cmd"] | "";
  String msg = "OK";

  if (cmd == "START") {
    webStartRequest = true;
    msg = "Perintah START diterima";
  } else if (cmd == "STOP") {
    webStopRequest = true;
    motorStop();
    setGate(false);
    msg = "Perintah STOP diterima";
  } else if (cmd == "RESET_HARI") {
    counterHariIni = 0;
    prefs.putInt("counterHari", 0);
    msg = "Counter harian direset";
  } else if (cmd == "TOGGLE_MAGNET") {
    setMagnet(!magnetActive);
    msg = magnetActive ? "Magnet TERKUNCI" : "Magnet LEPAS";
  } else if (cmd == "TOGGLE_GATE") {
    setGate(!gateOpen);
    msg = gateOpen ? "Gate Hopper BUKA" : "Gate Hopper TUTUP";
  } else if (cmd == "ROTATE_TEST") {
    if (!limitAtas()) {
      msg = "Ditolak! Pastikan Press di posisi HOME (Limit Atas) dulu";
    } else {
      long target = (stepper.currentPosition() < (STEPS_180DEG / 2)) ? STEPS_180DEG : 0;
      stepper.moveTo(target);
      msg = (target == STEPS_180DEG) ? "Memutar ke 180°..." : "Kembali ke 0°...";
    }
  } else if (cmd == "RESTART") {
    server.send(200, "application/json", "{\"ok\":true,\"msg\":\"Restarting...\"}");
    delay(400);
    ESP.restart();
    return;
  } else {
    msg = "Perintah tidak dikenal";
  }

  server.send(200, "application/json", "{\"ok\":true,\"msg\":\"" + msg + "\"}");
}

void handleApiConfig() {
  sendCorsHeaders();
  if (server.method() == HTTP_OPTIONS) { server.send(204); return; }

  if (server.method() == HTTP_POST && server.hasArg("plain")) {
    StaticJsonDocument<256> doc;
    deserializeJson(doc, server.arg("plain"));
    if (doc.containsKey("beratTarget")) {
      beratTarget = doc["beratTarget"].as<float>();
      prefs.putFloat("beratTarget", beratTarget);
    }
    if (doc.containsKey("waktuTahan")) {
      waktuTahan = max(1, doc["waktuTahan"].as<int>()) * 1000;
      prefs.putInt("waktuTahan", waktuTahan);
    }
    if (doc.containsKey("levelAlarm")) {
      levelAlarm = doc["levelAlarm"].as<float>();
      prefs.putFloat("levelAlarm", levelAlarm);
    }
    server.send(200, "application/json", "{\"ok\":true,\"msg\":\"Konfigurasi tersimpan!\"}");
    return;
  }

  StaticJsonDocument<256> doc;
  doc["beratTarget"] = beratTarget;
  doc["waktuTahan"]  = waktuTahan / 1000;
  doc["levelAlarm"]  = levelAlarm;
  String out;
  serializeJson(doc, out);
  server.send(200, "application/json", out);
}

void handleApiCalibrate() {
  sendCorsHeaders();
  if (scale.is_ready()) scale.tare();
  server.send(200, "application/json", "{\"ok\":true,\"msg\":\"Load cell di-nol-kan (Tare)\"}");
}

void handleRoot() {
  if (SPIFFS.exists("/index.html")) {
    File f = SPIFFS.open("/index.html", "r");
    server.streamFile(f, "text/html");
    f.close();
  } else {
    server.send(200, "text/html",
      "<h2 style='font-family:sans-serif;color:#dc2626'>"
      "Dashboard index.html belum diupload ke SPIFFS ESP32!</h2>");
  }
}

void setupWebServer() {
  server.on("/",              HTTP_GET,     handleRoot);
  server.on("/api/status",    HTTP_GET,     handleApiStatus);
  server.on("/api/control",   HTTP_POST,    handleApiControl);
  server.on("/api/control",   HTTP_OPTIONS, handleApiControl);
  server.on("/api/config",    HTTP_GET,     handleApiConfig);
  server.on("/api/config",    HTTP_POST,    handleApiConfig);
  server.on("/api/config",    HTTP_OPTIONS, handleApiConfig);
  server.on("/api/calibrate", HTTP_POST,    handleApiCalibrate);
  server.begin();
}

// ════════════════════════════════════════════════════════
// SECTION 9 — Setup & Loop Utama
// ════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  delay(400);
  Serial.println("\n╔══════════════════════════════════════╗");
  Serial.println("║  TEMPEHKIT v10.0 — ZERO-COLLISION    ║");
  Serial.println("║  6-Slot • Press 200mm • Flip 180°    ║");
  Serial.println("╚══════════════════════════════════════╝");

  // Output pins
  pinMode(PIN_MOTOR_IN1,    OUTPUT);
  pinMode(PIN_MOTOR_IN2,    OUTPUT);
  pinMode(PIN_LED_OK,       OUTPUT);
  pinMode(PIN_LED_ALARM,    OUTPUT);
  pinMode(PIN_BUZZER,       OUTPUT);
  pinMode(PIN_RELAY_MAGNET, OUTPUT);

#if GATE_USE_SERVO
  gateServo.attach(PIN_GATE);
#else
  pinMode(PIN_GATE, OUTPUT);
#endif

#if USE_HCSR04
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
#endif

  // Input pins (FIX v10: GPIO 34 & 35 pakai INPUT karena input-only + ext 10k pull-up)
  pinMode(PIN_LIMIT_ATAS,  INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);
  pinMode(PIN_BTN_START,   INPUT);
  pinMode(PIN_BTN_STOP,    INPUT);

  motorStop();
  setGate(false);
  setMagnet(false);
  setLED(false, false);
  digitalWrite(PIN_BUZZER, LOW);

  // Stepper NEMA 23 + TB6600
  stepper.setMaxSpeed(NEMA23_MAX_SPEED);
  stepper.setAcceleration(NEMA23_ACCEL);
  stepper.setCurrentPosition(0);

#if USE_LCD
  Wire.begin(PIN_SDA, PIN_SCL);
  lcd.init();
  lcd.backlight();
#endif

  // Load Cell HX711
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);
  scale.set_scale(LOADCELL_FAKTOR);
  if (scale.wait_ready_timeout(1000)) {
    scale.tare();
    Serial.println("[HX711] OK & Tare selesai");
  } else {
    Serial.println("[HX711] Tidak terdeteksi (lanjut mode aman)");
  }

  // SPIFFS & Preferences
  Serial.println(SPIFFS.begin(true) ? "[SPIFFS] OK" : "[SPIFFS] ERROR");
  prefs.begin("tempe-cfg", false);
  beratTarget    = prefs.getFloat("beratTarget", BERAT_DEFAULT);
  waktuTahan     = prefs.getInt("waktuTahan",    WAKTU_TAHAN_DEFAULT);
  levelAlarm     = prefs.getFloat("levelAlarm",  LEVEL_ALARM_DEFAULT);
  counterTotal   = prefs.getInt("counterTotal",  0);
  counterHariIni = prefs.getInt("counterHari",   0);

  // WiFi (timeout cepat 8 detik agar mode offline tetap lancar)
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.printf("[WiFi] Menghubungkan ke %s", WIFI_SSID);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries++ < 16) {
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Terhubung! Dashboard -> http://" + WiFi.localIP().toString());
  } else {
    Serial.println("\n[WiFi] Mode Offline (Tombol fisik & Serial Console tetap aktif)");
  }

  setupWebServer();
  buzzer(2, 90, 70);
  printSerialHelp();
  changeState(ST_HOMING);
}

void loop() {
  server.handleClient();
  stepper.run();          // FIX v10: memastikan ROTATE_TEST & perintah manual stepper selalu jalan!
  handleSerialConsole();  // Console uji meja v10

  // Safety cut-off global saat kontrol manual via Serial
  if (currentState == ST_IDLE) {
    if (limitAtas() && digitalRead(PIN_MOTOR_IN2) == HIGH) motorStop();
    if (limitBawah() && digitalRead(PIN_MOTOR_IN1) == HIGH) motorStop();
  }

  if (currentState == ST_IDLE || currentState == ST_ALARM_HOPPER) {
    if (millis() - lastSensorUpdate > 500) {
      beratSaatIni = bacaBerat();
      levelHopper  = bacaHopper();
      lastSensorUpdate = millis();
    }
  }

  runFSM();
  delay(5);
}
