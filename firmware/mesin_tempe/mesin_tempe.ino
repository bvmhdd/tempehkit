/*==========================================================
  MESIN PENCETAK TEMPE OTOMATIS v9.0 (LEAN ARSITEKTUR)
  ──────────────────────────────────────────────────
  Hardware : ESP32 DevKit V1 (38-pin)
  Cetakan  : 6 slot simultan (lebar mold 59.1 cm)
  Rotasi   : NEMA23 + Driver TB6600 + Timing Belt HTD3M 1:3 (2400 steps = 180°)
  Pengunci : Solenoid Elektromagnet 12V x2 (Relay GPIO 13)
  Press    : Motor DC 12V + Driver L298N + Dual Lead Screw T8
  Dosing   : Solenoid Gate 12V (Relay GPIO 27) + Load Cell 20kg (HX711)
  UI       : Web Dashboard WiFi (ESP32) + LED Hijau/Merah + Buzzer + Tombol START/STOP
  ──────────────────────────────────────────────────
  PIN MAP:
  GPIO 4  → HX711 DOUT          GPIO 25 → Motor Press IN1 (L298N)
  GPIO 5  → HX711 SCK           GPIO 26 → Motor Press IN2 (L298N)
  GPIO 12 → NEMA23 STEP         GPIO 27 → Relay Gate Solenoid (Hopper)
  GPIO 14 → NEMA23 DIR          GPIO 32 → Limit Switch ATAS
  GPIO 13 → Relay Elektromagnet GPIO 33 → Limit Switch BAWAH
  GPIO 2  → LED Hijau (OK/RUN)  GPIO 34 → Tombol Fisik START
  GPIO 15 → LED Merah (ALARM)   GPIO 35 → Tombol Fisik STOP
  GPIO 23 → Buzzer Aktif 5V
  Bebas   : GPIO 18, 19, 21, 22 (Spare pin)
==========================================================*/

// ════════════════════════════════════════════════════════
// SECTION 1 — Library & Feature Flags
// ════════════════════════════════════════════════════════
#define USE_LCD      0       // 0 = Tanpa LCD (Web Dashboard WiFi), 1 = dengan LCD 16x2
#define USE_HCSR04   0       // 0 = Tanpa Ultrasonik (pantau visual), 1 = dengan HC-SR04

#include <WiFi.h>
#include <WebServer.h>
#include <SPIFFS.h>
#include <HX711.h>
#include <Wire.h>
#if USE_LCD
#include <LiquidCrystal_I2C.h>
#endif
#include <Preferences.h>
#include <ArduinoJson.h>
#include <AccelStepper.h>

// ════════════════════════════════════════════════════════
// SECTION 2 — Konfigurasi & Pin Mapping
// ════════════════════════════════════════════════════════

// ── WiFi ──────────────────────────────────────────────
const char* WIFI_SSID     = "NAMA_WIFI_KAMU";     // ← ganti
const char* WIFI_PASSWORD = "PASSWORD_WIFI_KAMU"; // ← ganti

// ── Pin Mapping ───────────────────────────────────────
#define PIN_HX711_DOUT   4
#define PIN_HX711_SCK    5
#define PIN_MOTOR_IN1   25
#define PIN_MOTOR_IN2   26
#define PIN_RELAY_GATE  27
#define PIN_LIMIT_ATAS  32
#define PIN_LIMIT_BAWAH 33
#define PIN_BTN_START   34
#define PIN_BTN_STOP    35
#define PIN_LED_OK       2
#define PIN_LED_ALARM   15
#define PIN_BUZZER      23
#define PIN_RELAY_MAGNET 13
#define PIN_STEPPER_DIR 14
#define PIN_STEPPER_STEP 12

// ── Konstanta Mekanik & Rotasi (JANGAN UBAH) ──────────
#define SLOT_COUNT           6       // Jumlah slot cetakan
#define TINGGI_FRAME_CM      3.6     // Tinggi frame cetakan (cm)
#define STEPS_180DEG         2400    // 200 step × 8 microstep × 3 gear_ratio / 2 = 2400 step (180°)
#define NEMA23_MAX_SPEED     800.0   // step/detik
#define NEMA23_ACCELERATION  400.0   // step/detik²
#define TIMEOUT_HOMING_MS    15000   // Max waktu homing (ms)
#define TIMEOUT_PRESSING_MS  25000   // Max waktu press turun (ms)
#define TIMEOUT_DOSING_MS    90000   // Max waktu dosing (ms)
#define DEBOUNCE_MS          50      // Debounce tombol (ms)

// ── Default Parameter (bisa diubah via dashboard) ─────
#define BERAT_DEFAULT        0.0     // gram (0 = mode manual/isi tangan)
#define WAKTU_TAHAN_DEFAULT  5000    // ms (tahan press = 5 detik)
#define LEVEL_ALARM_DEFAULT  8.0     // cm (jarak sensor ke kedelai saat hampir habis)
#define LOADCELL_FAKTOR      420.0   // ← KALIBRASI DULU! (lihat catatan di bawah)

// ════════════════════════════════════════════════════════
// SECTION 3 — Variabel Global & State Machine
// ════════════════════════════════════════════════════════

enum State {
  ST_HOMING,        // Press naik ke atas (posisi referensi awal)
  ST_IDLE,          // Menunggu tombol START
  ST_CEK_HOPPER,    // Cek level kedelai di hopper
  ST_TUNGGU_SIAP,   // Tunggu operator pasang plastik
  ST_DOSING,        // Mengisi kedelai ke cetakan
  ST_PRESSING,      // Press turun + tahan
  ST_LIFT_OFF,      // Press + frame naik → tempe bebas di ancak
  ST_LOCK_LID,      // Kunci tutup cetakan dengan elektromagnet
  ST_ROTATE_MOLD,   // Putar cetakan 180 derajat untuk membalik
  ST_UNLOCK_LID,    // Buka kunci elektromagnet
  ST_RETURN_MOLD,   // Putar cetakan kembali ke posisi semula (0 derajat)
  ST_SELESAI,       // Siklus selesai, counter update
  ST_ALARM_HOPPER,  // Kedelai hampir habis
  ST_ALARM_ERROR    // Error mekanik (timeout)
};

State  currentState = ST_HOMING;
String stateStr     = "HOMING";

float beratSaatIni  = 0.0;
float levelHopper   = 0.0;

// Konfigurasi (disimpan di flash, bisa diubah via dashboard)
float beratTarget   = BERAT_DEFAULT;
int   waktuTahan    = WAKTU_TAHAN_DEFAULT;
float levelAlarm    = LEVEL_ALARM_DEFAULT;

// Counter produksi
int counterHariIni  = 0;
int counterTotal    = 0;

// Timing
unsigned long lastSensorUpdate = 0;
unsigned long lastBlinkTime    = 0;
bool          ledBlinkState    = false;

// Objects
HX711             scale;
#if USE_LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);
#endif
WebServer         server(80);
Preferences       prefs;
AccelStepper      stepper(AccelStepper::DRIVER, PIN_STEPPER_STEP, PIN_STEPPER_DIR);

bool magnetActive = false;

// ════════════════════════════════════════════════════════
// SECTION 4 — Fungsi Sensor
// ════════════════════════════════════════════════════════

float bacaBerat() {
  if (!scale.is_ready()) return -1.0;
  float val = scale.get_units(5);
  return (val < 0) ? 0.0 : val;
}

float bacaHopper() {
#if USE_HCSR04
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  long dur = pulseIn(PIN_ECHO, HIGH, 30000UL);
  if (dur == 0) return 999.0; // tidak ada respons = hopper kosong
  return (dur * 0.0343f) / 2.0f;
#else
  return 5.0f; // Mode visual: selalu normal (tidak memicu alarm)
#endif
}

bool limitAtas()  { return digitalRead(PIN_LIMIT_ATAS)  == LOW; }
bool limitBawah() { return digitalRead(PIN_LIMIT_BAWAH) == LOW; }

bool tombolStart() {
  if (digitalRead(PIN_BTN_START) == LOW) {
    delay(DEBOUNCE_MS);
    return digitalRead(PIN_BTN_START) == LOW;
  }
  return false;
}

bool tombolStop() {
  if (digitalRead(PIN_BTN_STOP) == LOW) {
    delay(DEBOUNCE_MS);
    return digitalRead(PIN_BTN_STOP) == LOW;
  }
  return false;
}

// ════════════════════════════════════════════════════════
// SECTION 5 — Fungsi Aktuator & UI
// ════════════════════════════════════════════════════════

void motorNaik()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, HIGH); }
void motorTurun() { digitalWrite(PIN_MOTOR_IN1, HIGH); digitalWrite(PIN_MOTOR_IN2, LOW);  }
void motorStop()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, LOW);  }
void bukaGate()   { digitalWrite(PIN_RELAY_GATE, HIGH); }
void tutupGate()  { digitalWrite(PIN_RELAY_GATE, LOW);  }

void setMagnet(bool active) {
  magnetActive = active;
  digitalWrite(PIN_RELAY_MAGNET, active ? HIGH : LOW);
}

void setLED(bool ok, bool alarm) {
  digitalWrite(PIN_LED_OK,    ok    ? HIGH : LOW);
  digitalWrite(PIN_LED_ALARM, alarm ? HIGH : LOW);
}

void buzzer(int kali, int durMs = 150, int jedaMs = 100) {
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

String progressBar(float val, float maxVal, int len = 10) {
  int filled = (maxVal > 0) ? constrain((int)(val / maxVal * len), 0, len) : 0;
  String bar = "[";
  for (int i = 0; i < len; i++) bar += (i < filled) ? "#" : ".";
  return bar + "]";
}

// ════════════════════════════════════════════════════════
// SECTION 6 — Finite State Machine
// ════════════════════════════════════════════════════════

void changeState(State next) {
  const char* names[] = {
    "HOMING","IDLE","CEK_HOPPER","TUNGGU_SIAP",
    "DOSING","PRESSING","LIFT_OFF",
    "LOCK_LID","ROTATE_MOLD","UNLOCK_LID","RETURN_MOLD","SELESAI",
    "ALARM_HOPPER","ALARM_ERROR"
  };
  currentState = next;
  stateStr = names[next];
  Serial.printf("[FSM] → %s\n", stateStr.c_str());
}

// ── HOMING ────────────────────────────────────────────
void handleHoming() {
  lcdPrint("HOMING...", "Naik ke atas");
  setLED(false, false);
  motorNaik();
  unsigned long t0 = millis();
  while (!limitAtas()) {
    server.handleClient();
    if (millis() - t0 > TIMEOUT_HOMING_MS) {
      motorStop();
      changeState(ST_ALARM_ERROR); return;
    }
    delay(10);
  }
  motorStop();
  lcdPrint("Homing selesai", "Tekan START");
  buzzer(1, 200);
  changeState(ST_IDLE);
}

// ── IDLE ──────────────────────────────────────────────
void handleIdle() {
  if (millis() - lastBlinkTime > 700) {
    ledBlinkState = !ledBlinkState;
    digitalWrite(PIN_LED_OK, ledBlinkState);
    lastBlinkTime = millis();
  }
  digitalWrite(PIN_LED_ALARM, LOW);

  String mode = (beratTarget > 0)
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

// ── CEK_HOPPER ────────────────────────────────────────
void handleCekHopper() {
  lcdPrint("Cek kedelai...", "");
  levelHopper = bacaHopper();
  Serial.printf("[HOPPER] %.1f cm (alarm > %.1f cm)\n", levelHopper, levelAlarm);
  if (levelHopper > levelAlarm) {
    changeState(ST_ALARM_HOPPER); return;
  }
  changeState(ST_TUNGGU_SIAP);
}

// ── TUNGGU_SIAP ───────────────────────────────────────
void handleTungguSiap() {
  setLED(true, false);
  lcdPrint("Pasang plastik", "START=lanjut");
  scale.tare(); // nol sebelum isi
  while (true) {
    server.handleClient();
    if (tombolStop())  { changeState(ST_IDLE);    return; }
    if (tombolStart()) { changeState(ST_DOSING);  return; }
    delay(50);
  }
}

// ── DOSING ────────────────────────────────────────────
void handleDosing() {
  // Mode Manual
  if (beratTarget <= 0) {
    lcdPrint("ISI KEDELAI", "START=press");
    while (true) {
      server.handleClient();
      beratSaatIni = bacaBerat();
      lcdPrint("Berat:" + String((int)beratSaatIni) + "g", "START=lanjut press");
      if (tombolStop())  { changeState(ST_IDLE);     return; }
      if (tombolStart()) { changeState(ST_PRESSING); return; }
      delay(200);
    }
  }

  // Mode Otomatis
  bukaGate();
  Serial.printf("[DOSING] Target: %.0fg (total 6 slot)\n", beratTarget);
  unsigned long t0 = millis();

  while (millis() - t0 < (unsigned long)TIMEOUT_DOSING_MS) {
    server.handleClient();
    beratSaatIni = bacaBerat();
    float toleransi = 5.0 * SLOT_COUNT; // 5g per slot

    lcdPrint(
      "Isi:" + String((int)beratSaatIni) + "/" + String((int)beratTarget) + "g",
      progressBar(beratSaatIni, beratTarget, 12)
    );

    if (beratSaatIni >= beratTarget - toleransi) {
      tutupGate();
      delay(800);
      beratSaatIni = bacaBerat();
      Serial.printf("[DOSING] Selesai: %.0fg\n", beratSaatIni);
      changeState(ST_PRESSING); return;
    }
    if (tombolStop()) { tutupGate(); changeState(ST_IDLE); return; }
    delay(100);
  }

  tutupGate();
  Serial.println("[ERR] Dosing timeout!");
  changeState(ST_ALARM_ERROR);
}

// ── PRESSING ──────────────────────────────────────────
void handlePressing() {
  setLED(true, false);
  lcdPrint("PRESSING...", "Harap tunggu");
  motorTurun();

  unsigned long t0 = millis();
  while (!limitBawah()) {
    server.handleClient();
    if (millis() - t0 > TIMEOUT_PRESSING_MS) {
      motorStop(); changeState(ST_ALARM_ERROR); return;
    }
    if (tombolStop()) { motorStop(); changeState(ST_HOMING); return; }
    delay(10);
  }
  motorStop();

  // Tahan posisi press
  unsigned long holdStart = millis();
  while (millis() - holdStart < (unsigned long)waktuTahan) {
    server.handleClient();
    int sisa = (waktuTahan - (int)(millis() - holdStart)) / 1000 + 1;
    lcdPrint("Tahan press:", String(sisa) + " detik...");
    delay(200);
  }

  changeState(ST_LIFT_OFF);
}

// ── LIFT_OFF ──────────────────────────────────────────
void handleLiftOff() {
  lcdPrint("Naik...", "Melepas frame");
  motorNaik();

  unsigned long t0 = millis();
  while (!limitAtas()) {
    server.handleClient();
    if (millis() - t0 > TIMEOUT_HOMING_MS) {
      motorStop(); changeState(ST_ALARM_ERROR); return;
    }
    delay(10);
  }
  motorStop();
  changeState(ST_LOCK_LID); // Lanjut ke penguncian tutup sebelum putar
}

// ── LOCK_LID ──────────────────────────────────────────
void handleLockLid() {
  lcdPrint("Mengunci Tutup", "Magnet Aktif...");
  setMagnet(true);
  delay(1000); // Tunggu magnet mengunci kuat
  changeState(ST_ROTATE_MOLD);
}

// ── ROTATE_MOLD ───────────────────────────────────────
void handleRotateMold() {
  lcdPrint("Memutar Cetakan", "Awas menjauh...");
  stepper.enableOutputs();
  // Asumsi putaran 180 derajat (perlu disesuaikan dengan rasio pulley dan microstepping)
  // Contoh: 200 step/rev * 8 microstep * 3 (gear ratio 1:3) / 2 (180 deg) = 2400 steps
  long targetPos = 2400; 
  stepper.moveTo(targetPos); 
  
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    server.handleClient();
    if (tombolStop()) { stepper.stop(); changeState(ST_ALARM_ERROR); return; }
  }
  changeState(ST_UNLOCK_LID);
}

// ── UNLOCK_LID ────────────────────────────────────────
void handleUnlockLid() {
  lcdPrint("Buka Tutup", "Ambil Tempe...");
  setMagnet(false);
  buzzer(3, 200, 100);
  
  // Tunggu operator mengambil cetakan / tempe jatuh ke ancak
  lcdPrint("Tempe Selesai", "START = Lanjut");
  while (true) {
    server.handleClient();
    if (tombolStart()) { changeState(ST_RETURN_MOLD); return; }
    if (tombolStop())  { changeState(ST_HOMING); return; }
    delay(50);
  }
}

// ── RETURN_MOLD ───────────────────────────────────────
void handleReturnMold() {
  lcdPrint("Posisi Semula...", "");
  stepper.moveTo(0);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    server.handleClient();
    if (tombolStop()) { stepper.stop(); changeState(ST_ALARM_ERROR); return; }
  }
  stepper.disableOutputs(); // Matikan arus agar motor tidak panas
  changeState(ST_SELESAI);
}

// ── SELESAI ───────────────────────────────────────────
void handleSelesai() {
  counterHariIni += SLOT_COUNT;
  counterTotal   += SLOT_COUNT;
  prefs.putInt("counterTotal", counterTotal);
  prefs.putInt("counterHari",  counterHariIni);

  setLED(true, false);
  buzzer(2, 300, 150);

  lcdPrint(
    String(SLOT_COUNT) + " TEMPE SIAP!",
    "Hari:" + String(counterHariIni) + " Tot:" + String(counterTotal)
  );
  Serial.printf("[DONE] Siklus selesai! Hari:%d Total:%d\n",
                counterHariIni, counterTotal);
  delay(3000);
  changeState(ST_CEK_HOPPER); // loop otomatis
}

// ── ALARM_HOPPER ──────────────────────────────────────
void handleAlarmHopper() {
  setLED(false, true);
  lcdPrint("! KEDELAI HABIS", "Isi & tekan STP");
  buzzer(3, 400, 200);
  delay(2000);
  if (tombolStop()) { delay(DEBOUNCE_MS); changeState(ST_IDLE); }
}

// ── ALARM_ERROR ───────────────────────────────────────
void handleAlarmError() {
  setLED(false, true);
  lcdPrint("! ERROR MEKANIK", "STOP = restart");
  buzzer(5, 150, 80);
  delay(2000);
  if (tombolStop()) { delay(DEBOUNCE_MS); ESP.restart(); }
}

// ── Runner ────────────────────────────────────────────
void runFSM() {
  // STOP global override
  if (tombolStop() &&
      currentState != ST_IDLE &&
      currentState != ST_ALARM_HOPPER &&
      currentState != ST_ALARM_ERROR) {
    tutupGate(); motorStop();
    changeState(ST_HOMING); return;
  }

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
// SECTION 7 — Web Server & REST API
// ════════════════════════════════════════════════════════

void handleApiStatus() {
  StaticJsonDocument<512> doc;
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
  doc["stepperPos"]     = stepper.currentPosition();
  doc["modeDosing"]     = (beratTarget > 0) ? "otomatis" : "manual";
  doc["ipAddress"]      = WiFi.localIP().toString();
  String out; serializeJson(doc, out);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", out);
}

void handleApiControl() {
  if (!server.hasArg("plain")) {
    server.send(400, "application/json", "{\"error\":\"No body\"}"); return;
  }
  StaticJsonDocument<128> doc;
  deserializeJson(doc, server.arg("plain"));
  String cmd = doc["cmd"] | "";
  String msg = "ok";

  if (cmd == "START") {
    if (currentState == ST_IDLE) {
#if USE_HCSR04
      changeState(ST_CEK_HOPPER);
#else
      changeState(ST_DOSING);
#endif
    }
    else msg = "Mesin sedang berjalan";
  } else if (cmd == "STOP") {
    tutupGate(); motorStop(); changeState(ST_HOMING);
  } else if (cmd == "RESET_HARI") {
    counterHariIni = 0; prefs.putInt("counterHari", 0);
    msg = "Counter harian direset";
  } else if (cmd == "TOGGLE_MAGNET") {
    setMagnet(!magnetActive);
    msg = magnetActive ? "Magnet Aktif" : "Magnet Mati";
  } else if (cmd == "ROTATE_TEST") {
    stepper.enableOutputs();
    stepper.moveTo(stepper.currentPosition() == 0 ? 2400 : 0);
    msg = "Rotasi dijalankan (Non-blocking)";
  } else if (cmd == "RESTART") {
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200, "application/json", "{\"ok\":true}");
    delay(500); ESP.restart(); return;
  } else {
    msg = "Perintah tidak dikenal";
  }

  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", "{\"ok\":true,\"msg\":\"" + msg + "\"}");
}

void handleApiConfig() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");

  if (server.method() == HTTP_OPTIONS) { server.send(204); return; }

  if (server.method() == HTTP_POST && server.hasArg("plain")) {
    StaticJsonDocument<256> doc;
    deserializeJson(doc, server.arg("plain"));
    if (doc.containsKey("beratTarget")) {
      beratTarget = doc["beratTarget"].as<float>();
      prefs.putFloat("beratTarget", beratTarget);
    }
    if (doc.containsKey("waktuTahan")) {
      waktuTahan = doc["waktuTahan"].as<int>() * 1000;
      prefs.putInt("waktuTahan", waktuTahan);
    }
    if (doc.containsKey("levelAlarm")) {
      levelAlarm = doc["levelAlarm"].as<float>();
      prefs.putFloat("levelAlarm", levelAlarm);
    }
    server.send(200, "application/json", "{\"ok\":true,\"msg\":\"Tersimpan!\"}");
    return;
  }

  // GET config
  StaticJsonDocument<256> doc;
  doc["beratTarget"] = beratTarget;
  doc["waktuTahan"]  = waktuTahan / 1000;
  doc["levelAlarm"]  = levelAlarm;
  String out; serializeJson(doc, out);
  server.send(200, "application/json", out);
}

void handleApiCalibrate() {
  scale.tare();
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json",
    "{\"ok\":true,\"msg\":\"Load cell di-nol-kan (tare)\"}");
}

void handleRoot() {
  if (SPIFFS.exists("/index.html")) {
    File f = SPIFFS.open("/index.html", "r");
    server.streamFile(f, "text/html");
    f.close();
  } else {
    server.send(200, "text/html",
      "<h2 style='font-family:sans-serif;color:#e74c3c'>"
      "⚠ Dashboard tidak ditemukan!<br><br>"
      "<small>Upload <b>index.html</b> ke SPIFFS ESP32 dulu.</small></h2>");
  }
}

void setupWebServer() {
  server.on("/",             HTTP_GET,     handleRoot);
  server.on("/api/status",   HTTP_GET,     handleApiStatus);
  server.on("/api/control",  HTTP_POST,    handleApiControl);
  server.on("/api/config",   HTTP_GET,     handleApiConfig);
  server.on("/api/config",   HTTP_POST,    handleApiConfig);
  server.on("/api/config",   HTTP_OPTIONS, handleApiConfig);
  server.on("/api/calibrate",HTTP_POST,    handleApiCalibrate);
  server.begin();
  Serial.println("[WEB] Server → http://" + WiFi.localIP().toString());
}

// ════════════════════════════════════════════════════════
// SECTION 8 — Setup
// ════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  Serial.println("\n╔════════════════════════════╗");
  Serial.println("║  MESIN TEMPE OTOMATIS v1.0 ║");
  Serial.println("║  6 slot · press simultan   ║");
  Serial.println("║  Tinggi frame: 3.6 cm      ║");
  Serial.println("╚════════════════════════════╝\n");

  // Pin setup
  pinMode(PIN_MOTOR_IN1,   OUTPUT);
  pinMode(PIN_MOTOR_IN2,   OUTPUT);
  pinMode(PIN_RELAY_GATE,  OUTPUT);
  pinMode(PIN_LED_OK,      OUTPUT);
  pinMode(PIN_LED_ALARM,   OUTPUT);
  pinMode(PIN_BUZZER,      OUTPUT);
  pinMode(PIN_TRIG,        OUTPUT);
  pinMode(PIN_ECHO,        INPUT);
  pinMode(PIN_RELAY_MAGNET,OUTPUT);
  pinMode(PIN_LIMIT_ATAS,  INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);
  pinMode(PIN_BTN_START,   INPUT_PULLUP);
  pinMode(PIN_BTN_STOP,    INPUT_PULLUP);

  motorStop(); tutupGate();
  setMagnet(false);
  setLED(false, false);
  digitalWrite(PIN_BUZZER, LOW);
  
  // Setup Stepper
  stepper.setMaxSpeed(NEMA23_MAX_SPEED);
  stepper.setAcceleration(NEMA23_ACCELERATION);
  stepper.disableOutputs();

  // LCD (opsional)
#if USE_LCD
  Wire.begin(PIN_SDA, PIN_SCL);
  lcd.init(); lcd.backlight();
  lcdPrint("MESIN TEMPE v9.0", "Memulai...");
#else
  Serial.println("[SYSTEM] Mesin Tempe v9.0 Memulai (Web Dashboard Mode)");
#endif

  // Load Cell
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);
  scale.set_scale(LOADCELL_FAKTOR);
  scale.tare();
  Serial.println("[HX711] Siap");

  // SPIFFS
  if (!SPIFFS.begin(true)) Serial.println("[SPIFFS] ERROR!");
  else Serial.println("[SPIFFS] OK");

  // Flash storage
  prefs.begin("tempe-cfg", false);
  beratTarget    = prefs.getFloat("beratTarget", BERAT_DEFAULT);
  waktuTahan     = prefs.getInt("waktuTahan",    WAKTU_TAHAN_DEFAULT);
  levelAlarm     = prefs.getFloat("levelAlarm",  LEVEL_ALARM_DEFAULT);
  counterTotal   = prefs.getInt("counterTotal",  0);
  counterHariIni = prefs.getInt("counterHari",   0);
  Serial.printf("[CFG] Berat:%.0fg | Tahan:%ds | Alarm:%.0fcm\n",
                beratTarget, waktuTahan/1000, levelAlarm);

  // WiFi
  lcdPrint("Connecting WiFi", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries++ < 20) {
    delay(500); Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    String ip = WiFi.localIP().toString();
    Serial.println("\n[WiFi] OK: " + ip);
    lcdPrint("WiFi OK!", ip);
    delay(2500);
  } else {
    Serial.println("\n[WiFi] GAGAL - offline mode");
    lcdPrint("WiFi GAGAL", "Mode Offline");
    delay(2000);
  }

  setupWebServer();
  buzzer(2, 100, 80);
  Serial.println("[SETUP] Selesai → HOMING\n");
}

// ════════════════════════════════════════════════════════
// SECTION 9 — Loop Utama
// ════════════════════════════════════════════════════════
void loop() {
  server.handleClient();

  // Update sensor saat IDLE / ALARM (non-blocking)
  if (currentState == ST_IDLE || currentState == ST_ALARM_HOPPER) {
    if (millis() - lastSensorUpdate > 500) {
      float b = bacaBerat();
      beratSaatIni = (b < 0) ? 0 : b;
      levelHopper  = bacaHopper();
      lastSensorUpdate = millis();
    }
  }

  runFSM();
  delay(5);
}

/*==========================================================
  📌 CATATAN KALIBRASI LOAD CELL
  ──────────────────────────────
  1. Pastikan platform kosong (tidak ada beban apapun)
  2. Upload firmware → buka Serial Monitor (115200 baud)
  3. Jalankan: scale.get_units(10) — catat nilai RAW
  4. Letakkan beban DIKETAHUI (contoh: 1000g / 1kg)
  5. LOADCELL_FAKTOR = nilai_raw / berat_sebenarnya
  6. Update konstanta LOADCELL_FAKTOR → upload ulang
  7. Verifikasi dengan benda lain → selesai ✅

  📌 LIBRARY YANG HARUS DIINSTALL (Arduino Library Manager)
  ──────────────────────────────────────────────────────────
  - "AccelStepper" by Mike McCauley (untuk Stepper NEMA23)
  - "HX711" by bogde (versi 0.7.5+)
  - "ArduinoJson" by Benoit Blanchon (versi 6.x)
  - "LiquidCrystal I2C" by Frank de Brabander (opsional, hanya jika USE_LCD 1)
  - ESP32 board: Tools → Board → ESP32 Dev Module

  📌 CARA UPLOAD index.html KE SPIFFS
  ──────────────────────────────────
  1. Install plugin: Arduino ESP32 Filesystem Uploader
  2. Buat folder "data" di dalam folder sketch ini
  3. Taruh index.html di dalam folder data/
  4. Tools → ESP32 Sketch Data Upload
==========================================================*/
