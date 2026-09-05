/*==========================================================
  TEST 05: MOTOR DC 12V + DRIVER L298N & SAFETY LIMIT CUT-OFF
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Menguji arah putaran motor DC (Turun/Press & Naik/Homing).
  2. Menguji interlock keamanan: motor wajib langsung berhenti jika
     Limit Switch tersentuh!

  Wiring Driver L298N:
  - 12V Terminal L298N -> Adaptor Positif (+12V DC)
  - GND Terminal L298N -> Adaptor Negatif (GND) & GND ESP32 (WAJIB COMMON GND!)
  - 5V Terminal L298N  -> Biarkan terbuka (atau lepas jumper jika pakai tegangan >12V)
  - IN1                -> ESP32 GPIO 25
  - IN2                -> ESP32 GPIO 26
  - OUT1 & OUT2        -> 2 Kabel ke Motor DC 12V
  - Limit Switch Atas  -> GPIO 32 (ke GND)
  - Limit Switch Bawah -> GPIO 33 (ke GND)

  PERINGATAN KESELAMATAN:
  Pastikan GND Adaptor 12V tersambung ke GND ESP32 agar referensi logika sama!
==========================================================*/

#define PIN_MOTOR_IN1   25
#define PIN_MOTOR_IN2   26
#define PIN_LIMIT_ATAS  32
#define PIN_LIMIT_BAWAH 33

void motorStop() {
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, LOW);
}

void motorTurun() {
  // Arah press turun
  digitalWrite(PIN_MOTOR_IN1, HIGH);
  digitalWrite(PIN_MOTOR_IN2, LOW);
}

void motorNaik() {
  // Arah homing naik
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, HIGH);
}

void printMenu() {
  Serial.println("\n--- PERINTAH KONTROL MOTOR DC VIA SERIAL ---");
  Serial.println("  'd' : Putar MOTOR TURUN (Arah Press)");
  Serial.println("  'u' : Putar MOTOR NAIK  (Arah Homing)");
  Serial.println("  's' : MOTOR STOP (Berhenti Seketika)");
  Serial.println("--------------------------------------------");
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 05: MOTOR DC 12V + L298N DRIVER");
  Serial.println("==========================================");

  pinMode(PIN_MOTOR_IN1, OUTPUT);
  pinMode(PIN_MOTOR_IN2, OUTPUT);
  motorStop();

  pinMode(PIN_LIMIT_ATAS, INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);

  Serial.println("[OK] Driver L298N diinisialisasi pada GPIO 25 & 26.");
  printMenu();
}

enum MotorState { M_STOP, M_DOWN, M_UP };
MotorState mState = M_STOP;

void loop() {
  // Cek Input Serial
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'd' || cmd == 'D') {
      if (digitalRead(PIN_LIMIT_BAWAH) == LOW) {
        Serial.println("[BLOCKED] Tidak bisa turun! Limit Switch BAWAH sedang aktif!");
      } else {
        Serial.println(">> Motor bergerak TURUN (Pressing)...");
        motorTurun();
        mState = M_DOWN;
      }
    } else if (cmd == 'u' || cmd == 'U') {
      if (digitalRead(PIN_LIMIT_ATAS) == LOW) {
        Serial.println("[BLOCKED] Tidak bisa naik! Limit Switch ATAS sedang aktif!");
      } else {
        Serial.println(">> Motor bergerak NAIK (Homing)...");
        motorNaik();
        mState = M_UP;
      }
    } else if (cmd == 's' || cmd == 'S') {
      Serial.println(">> Motor STOP.");
      motorStop();
      mState = M_STOP;
    }
  }

  // INTERLOCK SAFETY: Cut-off otomatis jika limit switch tersentuh
  if (mState == M_DOWN && digitalRead(PIN_LIMIT_BAWAH) == LOW) {
    motorStop();
    mState = M_STOP;
    Serial.println("\n[SAFETY CUT-OFF!] Limit switch BAWAH tersentuh -> Motor DIMATIKAN OTOMATIS!");
  }

  if (mState == M_UP && digitalRead(PIN_LIMIT_ATAS) == LOW) {
    motorStop();
    mState = M_STOP;
    Serial.println("\n[SAFETY CUT-OFF!] Limit switch ATAS tersentuh -> Motor DIMATIKAN OTOMATIS!");
  }

  delay(20);
}
