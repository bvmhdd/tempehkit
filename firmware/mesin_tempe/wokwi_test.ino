/*==========================================================
  WOKWI TEST SKETCH — TempehKit v9
  ──────────────────────────────────────────────────────────
  Tujuan: Verifikasi wiring semua komponen di Wokwi.
  Firmware ini TIDAK menggunakan WiFi/SPIFFS/Web Dashboard.
  Tekan BTN START untuk menjalankan urutan test otomatis.
  Tekan BTN STOP untuk reset ke IDLE.
  ──────────────────────────────────────────────────────────
  Pin Map (sesuai firmware utama):
  GPIO 4  → HX711 DOUT          GPIO 25 → Motor Press IN1
  GPIO 5  → HX711 SCK           GPIO 26 → Motor Press IN2
  GPIO 12 → NEMA23 STEP         GPIO 27 → Relay Gate Solenoid
  GPIO 14 → NEMA23 DIR          GPIO 32 → Limit Switch ATAS
  GPIO 13 → Relay Elektromagnet GPIO 33 → Limit Switch BAWAH
  GPIO 2  → LED Hijau            GPIO 34 → Tombol START
  GPIO 15 → LED Merah            GPIO 35 → Tombol STOP
  GPIO 23 → Buzzer
==========================================================*/

#include <HX711.h>
#include <AccelStepper.h>

// ── Pin Mapping ─────────────────────────────────────────
#define PIN_HX711_DOUT    4
#define PIN_HX711_SCK     5
#define PIN_STEPPER_STEP 12
#define PIN_STEPPER_DIR  14
#define PIN_RELAY_MAGNET 13
#define PIN_MOTOR_IN1    25
#define PIN_MOTOR_IN2    26
#define PIN_RELAY_GATE   27
#define PIN_LIMIT_ATAS   32
#define PIN_LIMIT_BAWAH  33
#define PIN_BTN_START    34
#define PIN_BTN_STOP     35
#define PIN_LED_OK        2
#define PIN_LED_ALARM    15
#define PIN_BUZZER       23

// ── State Machine ────────────────────────────────────────
enum State {
  ST_IDLE,
  ST_TEST_LED,
  ST_TEST_BUZZER,
  ST_TEST_RELAY,
  ST_TEST_MOTOR,
  ST_TEST_STEPPER,
  ST_TEST_LOADCELL,
  ST_DONE
};

State state = ST_IDLE;
unsigned long stateTimer = 0;

HX711 scale;
AccelStepper stepper(AccelStepper::DRIVER, PIN_STEPPER_STEP, PIN_STEPPER_DIR);

// ── Helper ───────────────────────────────────────────────
void buzz(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_BUZZER, HIGH); delay(150);
    digitalWrite(PIN_BUZZER, LOW);  delay(100);
  }
}

bool readBtn(int pin) {
  // tombol GPIO 34/35 adalah INPUT_ONLY (no pullup), pakai pull-down eksternal 10k
  return digitalRead(pin) == HIGH;
}

// ════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  Serial.println("=== TempehKit v9 — Wokwi Test Mode ===");

  // Output pins
  pinMode(PIN_LED_OK,        OUTPUT);
  pinMode(PIN_LED_ALARM,     OUTPUT);
  pinMode(PIN_BUZZER,        OUTPUT);
  pinMode(PIN_RELAY_MAGNET,  OUTPUT);
  pinMode(PIN_RELAY_GATE,    OUTPUT);
  pinMode(PIN_MOTOR_IN1,     OUTPUT);
  pinMode(PIN_MOTOR_IN2,     OUTPUT);

  // Input pins
  pinMode(PIN_BTN_START,     INPUT);   // pull-down eksternal 10k
  pinMode(PIN_BTN_STOP,      INPUT);   // pull-down eksternal 10k
  pinMode(PIN_LIMIT_ATAS,    INPUT);   // pull-down eksternal 10k
  pinMode(PIN_LIMIT_BAWAH,   INPUT);   // pull-down eksternal 10k

  // Default OFF
  digitalWrite(PIN_LED_OK,       LOW);
  digitalWrite(PIN_LED_ALARM,    LOW);
  digitalWrite(PIN_BUZZER,       LOW);
  digitalWrite(PIN_RELAY_MAGNET, LOW);
  digitalWrite(PIN_RELAY_GATE,   LOW);
  digitalWrite(PIN_MOTOR_IN1,    LOW);
  digitalWrite(PIN_MOTOR_IN2,    LOW);

  // HX711
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);

  // Stepper
  stepper.setMaxSpeed(800);
  stepper.setAcceleration(400);

  // Startup indicator
  buzz(2);
  Serial.println("[IDLE] Tekan BTN START (GPIO34) untuk mulai test otomatis.");
}

// ════════════════════════════════════════════════════════
void loop() {

  // STOP button → reset kapanpun
  if (readBtn(PIN_BTN_STOP) && state != ST_IDLE) {
    Serial.println("[STOP] Reset ke IDLE.");
    state = ST_IDLE;
    digitalWrite(PIN_LED_OK,       LOW);
    digitalWrite(PIN_LED_ALARM,    LOW);
    digitalWrite(PIN_RELAY_MAGNET, LOW);
    digitalWrite(PIN_RELAY_GATE,   LOW);
    digitalWrite(PIN_MOTOR_IN1,    LOW);
    digitalWrite(PIN_MOTOR_IN2,    LOW);
    buzz(1);
    return;
  }

  switch (state) {

    // ────────────────────────────────────────────────────
    case ST_IDLE:
      if (readBtn(PIN_BTN_START)) {
        Serial.println("[TEST 1] LED & Indikator...");
        state = ST_TEST_LED;
        stateTimer = millis();
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_LED:
      // LED Hijau ON, Merah OFF → flip setiap 500ms selama 2 detik
      {
        unsigned long t = millis() - stateTimer;
        digitalWrite(PIN_LED_OK,    (t / 300) % 2 == 0);
        digitalWrite(PIN_LED_ALARM, (t / 300) % 2 == 1);
        if (t >= 2000) {
          digitalWrite(PIN_LED_OK,    LOW);
          digitalWrite(PIN_LED_ALARM, LOW);
          Serial.println("[TEST 2] Buzzer...");
          state = ST_TEST_BUZZER;
          stateTimer = millis();
        }
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_BUZZER:
      if (millis() - stateTimer < 100) buzz(3);
      if (millis() - stateTimer > 1500) {
        Serial.println("[TEST 3] Relay Elektromagnet & Gate Solenoid...");
        state = ST_TEST_RELAY;
        stateTimer = millis();
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_RELAY:
      {
        unsigned long t = millis() - stateTimer;
        if (t < 800) {
          digitalWrite(PIN_RELAY_MAGNET, HIGH);
          digitalWrite(PIN_RELAY_GATE,   LOW);
          Serial.println("  Relay Elektromagnet: ON | Gate: OFF");
        } else if (t < 1600) {
          digitalWrite(PIN_RELAY_MAGNET, LOW);
          digitalWrite(PIN_RELAY_GATE,   HIGH);
          Serial.println("  Relay Elektromagnet: OFF | Gate: ON");
        } else if (t < 2400) {
          digitalWrite(PIN_RELAY_MAGNET, HIGH);
          digitalWrite(PIN_RELAY_GATE,   HIGH);
          Serial.println("  Relay Elektromagnet: ON | Gate: ON");
        } else {
          digitalWrite(PIN_RELAY_MAGNET, LOW);
          digitalWrite(PIN_RELAY_GATE,   LOW);
          Serial.println("[TEST 4] Motor DC Press (L298N)...");
          state = ST_TEST_MOTOR;
          stateTimer = millis();
        }
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_MOTOR:
      {
        unsigned long t = millis() - stateTimer;
        if (t < 1500) {
          digitalWrite(PIN_MOTOR_IN1, HIGH);
          digitalWrite(PIN_MOTOR_IN2, LOW);
          Serial.println("  Motor Press: TURUN");
        } else if (t < 3000) {
          digitalWrite(PIN_MOTOR_IN1, LOW);
          digitalWrite(PIN_MOTOR_IN2, HIGH);
          Serial.println("  Motor Press: NAIK");
        } else {
          digitalWrite(PIN_MOTOR_IN1, LOW);
          digitalWrite(PIN_MOTOR_IN2, LOW);
          Serial.println("[TEST 5] Stepper NEMA23 (Rotary Flip 180°)...");
          stepper.moveTo(2400); // 180 derajat
          state = ST_TEST_STEPPER;
          stateTimer = millis();
        }
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_STEPPER:
      stepper.run();
      if (stepper.distanceToGo() == 0) {
        Serial.println("  NEMA23: 180° tercapai. Balik ke 0°...");
        delay(500);
        stepper.moveTo(0);
        while (stepper.distanceToGo() != 0) stepper.run();
        Serial.println("[TEST 6] Load Cell (HX711)...");
        state = ST_TEST_LOADCELL;
        stateTimer = millis();
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_TEST_LOADCELL:
      if (scale.is_ready()) {
        long raw = scale.read();
        Serial.printf("  HX711 Raw: %ld\n", raw);
      }
      if (millis() - stateTimer > 3000) {
        Serial.println("[DONE] Semua test selesai! LED Hijau menyala.");
        state = ST_DONE;
      }
      break;

    // ────────────────────────────────────────────────────
    case ST_DONE:
      digitalWrite(PIN_LED_OK,    HIGH);
      digitalWrite(PIN_LED_ALARM, LOW);
      buzz(3);
      delay(3000);
      Serial.println("[IDLE] Tekan BTN START untuk test ulang.");
      state = ST_IDLE;
      digitalWrite(PIN_LED_OK, LOW);
      break;
  }

  // ── Monitor Limit Switch secara real-time ─────────────
  static bool lastAtas = false, lastBawah = false;
  bool atas   = digitalRead(PIN_LIMIT_ATAS)  == HIGH;
  bool bawah  = digitalRead(PIN_LIMIT_BAWAH) == HIGH;
  if (atas  != lastAtas)  { Serial.printf("  Limit Switch ATAS : %s\n",  atas  ? "TERTEKAN" : "BEBAS"); lastAtas  = atas; }
  if (bawah != lastBawah) { Serial.printf("  Limit Switch BAWAH: %s\n", bawah ? "TERTEKAN" : "BEBAS"); lastBawah = bawah; }
}
