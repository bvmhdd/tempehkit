/*==========================================================
  TEST 07: BENCHTOP INTEGRATED DRY-RUN TEST
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  Uji coba integrasi MEKATRONIKA LENGKAP di atas meja (Breadboard)
  sebelum mesin dirakit ke rangka besi oleh tukang las.

  Alur Simulasi 1 Siklus Cetak di Meja:
  1. Layar LCD menampilkan: "READY - TEKAN START"
  2. Operator menekan Tombol START (GPIO 34).
  3. Relay gate aktif sejenak (simulasi isi kedelai).
  4. Motor berputar TURUN (Arah Press).
  5. Operator menyentuh Limit Switch BAWAH (GPIO 33) dengan jari.
  6. Motor langsung STOP, menahan selama 3 detik (simulasi pemadatan tempe).
  7. Motor berputar NAIK (Arah Lift-Off & Homing).
  8. Operator menyentuh Limit Switch ATAS (GPIO 32) dengan jari.
  9. Motor STOP. Buzzer berbunyi beep 2x. Counter bertambah +1.
  10. Kembali ke status READY.
==========================================================*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <HX711.h>

// Pin Mapping
#define PIN_HX711_DOUT   4
#define PIN_HX711_SCK    5
#define PIN_TRIG        18
#define PIN_ECHO        19
#define PIN_SDA         21
#define PIN_SCL         22
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

LiquidCrystal_I2C lcd(0x27, 16, 2); // Ubah ke 0x3F jika diperlukan
HX711 scale;

enum Step {
  STEP_IDLE,
  STEP_DOSING,
  STEP_PRESS_DOWN,
  STEP_PRESS_HOLD,
  STEP_LIFT_UP,
  STEP_DONE
};

Step stepState = STEP_IDLE;
int  totalPapan = 0;
unsigned long holdTimer = 0;

void motorStop()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, LOW);  }
void motorTurun() { digitalWrite(PIN_MOTOR_IN1, HIGH); digitalWrite(PIN_MOTOR_IN2, LOW);  }
void motorNaik()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, HIGH); }

void beep(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(PIN_BUZZER, HIGH);
    delay(80);
    digitalWrite(PIN_BUZZER, LOW);
    delay(80);
  }
}

void updateLCD(const char* line1, const char* line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 07: BENCHTOP INTEGRATED DRY-RUN");
  Serial.println("==========================================");

  // Inisialisasi Pin
  pinMode(PIN_MOTOR_IN1, OUTPUT);
  pinMode(PIN_MOTOR_IN2, OUTPUT);
  motorStop();

  pinMode(PIN_RELAY_GATE, OUTPUT);
  digitalWrite(PIN_RELAY_GATE, HIGH); // Off

  pinMode(PIN_LED_OK, OUTPUT);
  pinMode(PIN_LED_ALARM, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  pinMode(PIN_LIMIT_ATAS, INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);
  pinMode(PIN_BTN_START, INPUT);
  pinMode(PIN_BTN_STOP, INPUT);

  // Inisialisasi LCD
  Wire.begin(PIN_SDA, PIN_SCL);
  lcd.init();
  lcd.backlight();
  updateLCD("BENCH TEST v1.0", "Inisialisasi...");

  // Inisialisasi Sensor Berat
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);
  if (scale.wait_ready_timeout(1000)) {
    scale.set_scale(420.0);
    scale.tare();
  }

  delay(1000);
  digitalWrite(PIN_LED_OK, HIGH);
  updateLCD("MESIN TEMPE READY", "TEKAN START >>");
  Serial.println("[SIAP] Silakan tekan tombol START (GPIO 34) untuk memulai simulasi 1 siklus!");
}

void loop() {
  bool btnStart = (digitalRead(PIN_BTN_START) == LOW);
  bool btnStop  = (digitalRead(PIN_BTN_STOP)  == LOW);
  bool limAtas  = (digitalRead(PIN_LIMIT_ATAS)  == LOW);
  bool limBawah = (digitalRead(PIN_LIMIT_BAWAH) == LOW);

  // Emergency Stop kapan saja
  if (btnStop) {
    motorStop();
    digitalWrite(PIN_RELAY_GATE, HIGH);
    digitalWrite(PIN_LED_ALARM, HIGH);
    digitalWrite(PIN_LED_OK, LOW);
    updateLCD("EMERGENCY STOP!", "Tekan Reset...");
    Serial.println("[STOP] Emergency stop ditekan!");
    stepState = STEP_IDLE;
    delay(500);
    return;
  }

  switch (stepState) {
    case STEP_IDLE:
      if (btnStart) {
        Serial.println("\n--- [SIKLUS DIMULAI] ---");
        beep(1);
        stepState = STEP_DOSING;
        updateLCD("1. MENGISI KEDELAI", "Buka Gate...");
        digitalWrite(PIN_RELAY_GATE, LOW); // Gate buka
        delay(1500); // Simulasi isi
        digitalWrite(PIN_RELAY_GATE, HIGH); // Gate tutup
        stepState = STEP_PRESS_DOWN;
        updateLCD("2. PRESS TURUN", "Menekan 6 Slot");
        Serial.println(">> Motor mulai TURUN. Sentuh Limit Switch BAWAH untuk simulasi press sampai!");
        motorTurun();
      }
      break;

    case STEP_PRESS_DOWN:
      if (limBawah) {
        motorStop();
        Serial.println(">> Limit Switch BAWAH aktif! Motor STOP. Mulai TAHAN PRESS 3 detik...");
        updateLCD("3. TAHAN TEKANAN", "Pemadatan 3s...");
        holdTimer = millis();
        stepState = STEP_PRESS_HOLD;
      }
      break;

    case STEP_PRESS_HOLD:
      if (millis() - holdTimer >= 3000) {
        Serial.println(">> Tahan selesai! Mulai LIFT-OFF (Motor NAIK ke posisi Home)...");
        updateLCD("4. LIFT-OFF FRAME", "Motor Naik...");
        motorNaik();
        stepState = STEP_LIFT_UP;
      }
      break;

    case STEP_LIFT_UP:
      if (limAtas) {
        motorStop();
        totalPapan++;
        Serial.printf(">> Limit Switch ATAS aktif! Siklus Selesai. Total Cetak: %d papan (%d tempe)\n",
                      totalPapan, totalPapan * 6);
        beep(2);
        char buf[17];
        snprintf(buf, sizeof(buf), "HASIL: %d PAPAN", totalPapan);
        updateLCD("SIKLUS SUKSES!", buf);
        delay(2500);
        updateLCD("MESIN TEMPE READY", "TEKAN START >>");
        stepState = STEP_IDLE;
      }
      break;
  }

  delay(20);
}
