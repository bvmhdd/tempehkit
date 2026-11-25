/*=============================================================================
  WOKWI FULL SIMULATION — MESIN PENCETAK TEMPE OTOMATIS (TempehKit v9)
  ─────────────────────────────────────────────────────────────────────────────
  Simulasi Mekatronika Lengkap:
  - Motor DC 12V Worm Gearbox + Driver L298N (GPIO 25 & 26)
  - Micro Limit Switch V-156-1C25: Posisi ATAS (GPIO 32) & BAWAH (GPIO 33)
  - Stepper NEMA 23 + TB6600: Pembalik Cetakan 180° (GPIO 12 STEP, GPIO 14 DIR)
  - Solenoid Elektromagnet 12V: Pengunci Tutup Mold (Relay GPIO 13)
  - Solenoid Gate 12V: Pintu Geser Dosing Hopper (Relay GPIO 27)
  - Load Cell 20kg + HX711: Penimbang Dosing Kedelai (GPIO 4 DOUT, GPIO 5 SCK)
  - Tombol Fisik: START (GPIO 34) & STOP / EMERGENCY (GPIO 35)
  - Indikator Visual & Audio: LED Hijau (GPIO 2), LED Merah (GPIO 15), Buzzer (GPIO 23)
=============================================================================*/

#include <HX711.h>
#include <AccelStepper.h>

// ── Pinout Hardware Sesuai Desain TempehKit ──────────────────────────────────
#define PIN_HX711_DOUT    4
#define PIN_HX711_SCK     5
#define PIN_STEPPER_STEP 12
#define PIN_STEPPER_DIR  14
#define PIN_RELAY_MAGNET 13
#define PIN_MOTOR_IN1    25   // L298N IN1: Press TURUN
#define PIN_MOTOR_IN2    26   // L298N IN2: Press NAIK
#define PIN_RELAY_GATE   27   // Solenoid Pintu Corong Dosing
#define PIN_LIMIT_ATAS   32   // Limit Switch Posisi HOME (V-156 NO ke GND)
#define PIN_LIMIT_BAWAH  33   // Limit Switch Posisi PRESS PENUH (V-156 NO ke GND)
#define PIN_BTN_START    34   // Tombol Hijau START (Pull-Down 10k)
#define PIN_BTN_STOP     35   // Tombol Merah STOP / EMERGENCY (Pull-Down 10k)
#define PIN_LED_OK        2   // LED Hijau: Status Mesin Berjalan
#define PIN_LED_ALARM    15   // LED Merah: Indikator Peringatan / Alarm
#define PIN_BUZZER       23   // Buzzer Notifikasi

// ── Konstanta Kinematika & Parameter Operasi ────────────────────────────────
#define STEPS_180DEG        2400     // 200 step * 8 microstep * rasio 3 / 2 = 180°
#define TARGET_BERAT_GRAM   1800.0   // 6 slot x 300 gram = 1.8 kg kedelai
#define WAKTU_TAHAN_PRESS   5000     // Durasi menahan tekanan = 5 detik
#define TIMEOUT_PRESS_MS    25000    // Batas aman motor/aktuator turun (25 detik)
#define TIMEOUT_HOMING_MS   25000    // Batas aman motor/aktuator naik (25 detik)

// ── State Machine Siklus Otomatis ───────────────────────────────────────────
enum MachineState {
  ST_IDLE,          // Siap / Standby menunggu START
  ST_DOSING,        // Buka gate hopper & menimbang kedelai
  ST_PRESS_DOWN,    // Motor DC turun sampai Limit Switch Bawah tersentuh
  ST_PRESS_HOLD,    // Motor mati, menahan pemadatan selama 5 detik
  ST_PRESS_UP,      // Motor DC naik sampai Limit Switch Atas tersentuh
  ST_LOCK_MOLD,     // Elektromagnet aktif mengunci tutup cetakan
  ST_FLIP_MOLD,     // NEMA 23 memutar cetakan 180° ke ancak bambu
  ST_UNLOCK_DROP,   // Elektromagnet mati, tempe lepas jatuh ke ancak
  ST_RETURN_MOLD,   // NEMA 23 kembali ke posisi 0°
  ST_CYCLE_DONE,    // Siklus selesai, update counter & notifikasi
  ST_EMERGENCY      // Kondisi darurat / STOP ditekan
};

MachineState state = ST_IDLE;
unsigned long stateTimer = 0;
unsigned long holdCountdown = 0;
int totalPapanCetak = 0;
float beratSimulasi = 0.0;

HX711 scale;
AccelStepper stepper(AccelStepper::DRIVER, PIN_STEPPER_STEP, PIN_STEPPER_DIR);

// ── Helper Kendali Motor & Indikator ────────────────────────────────────────
void motorStop()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, LOW);  }
void motorTurun() { digitalWrite(PIN_MOTOR_IN1, HIGH); digitalWrite(PIN_MOTOR_IN2, LOW);  }
void motorNaik()  { digitalWrite(PIN_MOTOR_IN1, LOW);  digitalWrite(PIN_MOTOR_IN2, HIGH); }

void buzz(int count, int durOn = 80, int durOff = 80) {
  for (int i = 0; i < count; i++) {
    digitalWrite(PIN_BUZZER, HIGH); delay(durOn);
    digitalWrite(PIN_BUZZER, LOW);  delay(durOff);
  }
}

// Pembacaan Limit Switch (Micro Switch V-156-1C25: NO tersambung ke GND saat tertekan)
bool isLimitAtasPressed()  { return digitalRead(PIN_LIMIT_ATAS)  == LOW; }
bool isLimitBawahPressed() { return digitalRead(PIN_LIMIT_BAWAH) == LOW; }

// Pembacaan Tombol Fisik (Pull-down: HIGH saat ditekan)
bool isStartPressed() { return digitalRead(PIN_BTN_START) == HIGH; }
bool isStopPressed()  { return digitalRead(PIN_BTN_STOP)  == HIGH; }

void printMenu() {
  Serial.println("\n┌────────────────────────────────────────────────────────┐");
  Serial.println("│        TEMPEHKIT v9 - WOKWI SIMULATION CONSOLE         │");
  Serial.println("├────────────────────────────────────────────────────────┤");
  Serial.println("│  KONTROL INTERAKTIF:                                   │");
  Serial.println("│  [BTN START (Hijau)]  : Mulai 1 Siklus Cetak Otomatis  │");
  Serial.println("│  [BTN STOP (Merah)]   : Emergency Stop / Batal Siklus  │");
  Serial.println("│  [Limit SW Bawah]     : Sentuh saat Motor Press TURUN  │");
  Serial.println("│  [Limit SW Atas]      : Sentuh saat Motor Press NAIK   │");
  Serial.println("│                                                        │");
  Serial.println("│  PERINTAH SERIAL MONITOR (Ketik huruf lalu Enter):    │");
  Serial.println("│   's' : Trigger Tombol START                           │");
  Serial.println("│   'e' : Trigger EMERGENCY STOP                         │");
  Serial.println("│   'd' : Manual Motor TURUN                             │");
  Serial.println("│   'u' : Manual Motor NAIK                              │");
  Serial.println("│   'o' : Manual Motor STOP                              │");
  Serial.println("│   'f' : Uji Rotasi Stepper NEMA23 180°                │");
  Serial.println("│   'l' : Cek Status Limit Switch Realtime               │");
  Serial.println("│   '?' : Tampilkan menu bantuan ini lagi                │");
  Serial.println("└────────────────────────────────────────────────────────┘\n");
}

// ═════════════════════════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  delay(500);
  printMenu();

  // Inisialisasi Output
  pinMode(PIN_LED_OK,        OUTPUT);
  pinMode(PIN_LED_ALARM,     OUTPUT);
  pinMode(PIN_BUZZER,        OUTPUT);
  pinMode(PIN_RELAY_MAGNET,  OUTPUT);
  pinMode(PIN_RELAY_GATE,    OUTPUT);
  pinMode(PIN_MOTOR_IN1,     OUTPUT);
  pinMode(PIN_MOTOR_IN2,     OUTPUT);

  // Inisialisasi Input
  pinMode(PIN_BTN_START,     INPUT);          // Pull-down eksternal 10k
  pinMode(PIN_BTN_STOP,      INPUT);          // Pull-down eksternal 10k
  pinMode(PIN_LIMIT_ATAS,    INPUT_PULLUP);   // Internal pull-up (V-15 ke GND)
  pinMode(PIN_LIMIT_BAWAH,   INPUT_PULLUP);   // Internal pull-up (V-15 ke GND)

  // Matikan semua aktuator di awal
  motorStop();
  digitalWrite(PIN_RELAY_MAGNET, LOW);
  digitalWrite(PIN_RELAY_GATE,   LOW);
  digitalWrite(PIN_LED_OK,       LOW);
  digitalWrite(PIN_LED_ALARM,    LOW);
  digitalWrite(PIN_BUZZER,       LOW);

  // Inisialisasi Sensor & Stepper
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);
  stepper.setMaxSpeed(800.0);
  stepper.setAcceleration(400.0);

  // Nada pembuka sistem siap
  buzz(2, 60, 60);
  Serial.println(">> [SISTEM SIAP] Mesin dalam posisi STANDBY.");
  Serial.println(">> Tekan tombol hijau START di diagram Wokwi untuk memulai!\n");
}

// ═════════════════════════════════════════════════════════════════════════════
void loop() {
  // ── Interlock Emergency Stop Kapan Saja ──────────────────────────────────
  if (isStopPressed() && state != ST_EMERGENCY) {
    motorStop();
    digitalWrite(PIN_RELAY_MAGNET, LOW);
    digitalWrite(PIN_RELAY_GATE,   LOW);
    digitalWrite(PIN_LED_OK,       LOW);
    digitalWrite(PIN_LED_ALARM,    HIGH);
    buzz(1, 400, 100);
    state = ST_EMERGENCY;
    Serial.println("\n⛔ [EMERGENCY STOP DIAKTIFKAN!]");
    Serial.println(">> Semua motor dan solenoid dimatikan seketika!");
    Serial.println(">> Tekan Tombol START atau ketik 's' untuk reset kembali ke IDLE.\n");
    return;
  }

  // ── Input Perintah Serial Monitor ─────────────────────────────────────────
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 's' || cmd == 'S') {
      if (state == ST_IDLE || state == ST_EMERGENCY) {
        Serial.println(">> [SERIAL] Tombol START ditekan via Serial!");
        state = ST_DOSING;
        stateTimer = millis();
        beratSimulasi = 0.0;
        buzz(1, 100, 50);
      }
    } else if (cmd == 'e' || cmd == 'E') {
      motorStop();
      digitalWrite(PIN_RELAY_MAGNET, LOW);
      digitalWrite(PIN_RELAY_GATE,   LOW);
      state = ST_EMERGENCY;
      digitalWrite(PIN_LED_ALARM, HIGH);
      digitalWrite(PIN_LED_OK, LOW);
      Serial.println("\n⛔ [SERIAL] EMERGENCY STOP!");
    } else if (cmd == 'd' || cmd == 'D') {
      Serial.println(">> [MANUAL] Motor DC TURUN...");
      motorTurun();
    } else if (cmd == 'u' || cmd == 'U') {
      Serial.println(">> [MANUAL] Motor DC NAIK...");
      motorNaik();
    } else if (cmd == 'o' || cmd == 'O') {
      Serial.println(">> [MANUAL] Motor DC STOP.");
      motorStop();
    } else if (cmd == 'f' || cmd == 'F') {
      Serial.println(">> [MANUAL] Uji putar NEMA23 180°...");
      stepper.moveTo(STEPS_180DEG);
    } else if (cmd == 'l' || cmd == 'L') {
      Serial.printf(">> Status Limit Switch: ATAS=%s | BAWAH=%s\n",
                    isLimitAtasPressed() ? "TERTEKAN (LOW)" : "BEBAS (HIGH)",
                    isLimitBawahPressed() ? "TERTEKAN (LOW)" : "BEBAS (HIGH)");
    } else if (cmd == '?') {
      printMenu();
    }
  }

  // ── Mesin Keadaan (State Machine) Siklus Produksi ──────────────────────────
  switch (state) {

    // ────────────────────────────────────────────────────────────────────────
    case ST_IDLE:
      // Heartbeat LED Hijau berkedip santai saat standby
      digitalWrite(PIN_LED_OK, (millis() / 800) % 2 == 0);
      digitalWrite(PIN_LED_ALARM, LOW);

      if (isStartPressed()) {
        delay(50); // Debounce
        if (isStartPressed()) {
          Serial.println("\n══════════════════════════════════════════════════════════");
          Serial.println("▶▶ MEMULAI SIKLUS PENCETAKAN TEMPE (6 SLOT SIMULTAN) ◀◀");
          Serial.println("══════════════════════════════════════════════════════════");
          buzz(1, 120, 50);
          state = ST_DOSING;
          stateTimer = millis();
          beratSimulasi = 0.0;
        }
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_DOSING:
      digitalWrite(PIN_LED_OK, HIGH);
      digitalWrite(PIN_RELAY_GATE, HIGH); // Buka pintu hopper kedelai

      // Simulasi aliran kedelai masuk ke cetakan secara bertahap
      beratSimulasi += 150.0;
      Serial.printf("  [DOSING] Solenoid Gate BUKA... Timbangan: %.0f gram / %.0f gram\n",
                    beratSimulasi, TARGET_BERAT_GRAM);
      delay(300);

      if (beratSimulasi >= TARGET_BERAT_GRAM) {
        digitalWrite(PIN_RELAY_GATE, LOW); // Tutup pintu hopper
        Serial.println("  [DOSING SELESAI] Target 1800 gram tercapai! Gate ditutup.");
        buzz(1, 100, 50);

        Serial.println("\n----------------------------------------------------------");
        Serial.println("▼ TAHAP 1: PENGEPRESAN (PRESS TURUN)");
        Serial.println("  Motor DC 12V L298N mulai berputar TURUN.");
        Serial.println("  >> KLIK tombol [Limit Switch BAWAH (GPIO 33)] di Wokwi");
        Serial.println("     untuk simulasi pelat telah menyentuh batas kedelai!");
        Serial.println("----------------------------------------------------------");

        motorTurun();
        state = ST_PRESS_DOWN;
        stateTimer = millis();
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_PRESS_DOWN:
      // Berhenti jika Limit Switch Bawah tersentuh atau timeout pengaman
      if (isLimitBawahPressed()) {
        motorStop();
        Serial.println("\n  ✔ [LIMIT BAWAH AKTIF!] Pelat penekan sampai pada posisi padat.");
        Serial.println("  ✔ Motor DC STOP seketika!");
        Serial.println("\n----------------------------------------------------------");
        Serial.println("⏳ TAHAP 2: MENAHAN TEKANAN (PRESS HOLD 5 DETIK)");
        Serial.println("  Mekanisme Worm Gear menahan posisi secara mekanik.");
        Serial.println("----------------------------------------------------------");
        buzz(1, 100, 50);
        state = ST_PRESS_HOLD;
        stateTimer = millis();
        holdCountdown = 5;
      } else if (millis() - stateTimer > TIMEOUT_PRESS_MS) {
        motorStop();
        Serial.println("\n  ⚠ [TIMEOUT SAFETY] Limit bawah tidak tersentuh dalam 20 detik!");
        Serial.println("  Motor dihentikan otomatis demi keamanan.");
        state = ST_PRESS_HOLD;
        stateTimer = millis();
        holdCountdown = 5;
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_PRESS_HOLD:
      {
        unsigned long elapsed = millis() - stateTimer;
        int remaining = 5 - (elapsed / 1000);
        if (remaining != (int)holdCountdown && remaining >= 0) {
          holdCountdown = remaining;
          Serial.printf("  Menahan pemadatan... %d detik\n", remaining);
          digitalWrite(PIN_BUZZER, HIGH); delay(20); digitalWrite(PIN_BUZZER, LOW);
        }

        if (elapsed >= WAKTU_TAHAN_PRESS) {
          Serial.println("  ✔ Pemadatan 5 detik selesai! Struktur tempe telah rata.");
          Serial.println("\n----------------------------------------------------------");
          Serial.println("▲ TAHAP 3: LIFT-OFF / HOMING (PRESS NAIK)");
          Serial.println("  Motor DC 12V L298N berputar NAIK kembali ke posisi awal.");
          Serial.println("  >> KLIK tombol [Limit Switch ATAS (GPIO 32)] di Wokwi");
          Serial.println("     untuk simulasi pelat telah kembali ke posisi HOME!");
          Serial.println("----------------------------------------------------------");

          motorNaik();
          state = ST_PRESS_UP;
          stateTimer = millis();
        }
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_PRESS_UP:
      if (isLimitAtasPressed()) {
        motorStop();
        Serial.println("\n  ✔ [LIMIT ATAS AKTIF!] Pelat penekan kembali ke posisi HOME.");
        Serial.println("  ✔ Motor DC STOP.");
        Serial.println("\n----------------------------------------------------------");
        Serial.println("🔄 TAHAP 4: ROTASI PEMBALIKAN CETAKAN (FLIP 180°)");
        Serial.println("  Elektromagnet 12V ON mengunci tutup cetakan.");
        Serial.println("  Motor Stepper NEMA 23 mulai memutar cetakan 180°...");
        Serial.println("----------------------------------------------------------");

        digitalWrite(PIN_RELAY_MAGNET, HIGH); // Kunci tutup cetakan
        delay(400);

        stepper.setCurrentPosition(0);
        stepper.moveTo(STEPS_180DEG);
        state = ST_FLIP_MOLD;
      } else if (millis() - stateTimer > TIMEOUT_HOMING_MS) {
        motorStop();
        Serial.println("\n  ⚠ [TIMEOUT SAFETY] Limit atas tercapai via batas waktu.");
        digitalWrite(PIN_RELAY_MAGNET, HIGH);
        delay(400);
        stepper.setCurrentPosition(0);
        stepper.moveTo(STEPS_180DEG);
        state = ST_FLIP_MOLD;
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_FLIP_MOLD:
      stepper.run();
      if (stepper.distanceToGo() == 0) {
        Serial.println("  ✔ Rotasi 180° selesai! Cetakan kini menghadap ke bawah (ke ancak).");
        Serial.println("  ✔ Melepas Elektromagnet -> Tutup cetakan terbuka!");
        Serial.println("  ✔ 6 balok tempe meluncur mulus ke rak ancak bambu.");
        buzz(2, 80, 80);

        digitalWrite(PIN_RELAY_MAGNET, LOW); // Lepas kunci tutup mold
        delay(1200);

        Serial.println("\n----------------------------------------------------------");
        Serial.println("↩ TAHAP 5: PENGEMBALIAN POSISI CETAKAN (RETURN 0°)");
        Serial.println("  NEMA 23 berputar balik ke posisi tegak semula...");
        Serial.println("----------------------------------------------------------");

        stepper.moveTo(0);
        state = ST_RETURN_MOLD;
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_RETURN_MOLD:
      stepper.run();
      if (stepper.distanceToGo() == 0) {
        Serial.println("  ✔ Cetakan kembali ke posisi awal (0°).");
        state = ST_CYCLE_DONE;
      }
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_CYCLE_DONE:
      totalPapanCetak++;
      Serial.println("\n==========================================================");
      Serial.println("🎉 SIKLUS PENCETAKAN BERHASIL LENGKAP!");
      Serial.printf("   Total Produksi Hari Ini: %d Papan (%d Batang Tempe)\n",
                    totalPapanCetak, totalPapanCetak * 6);
      Serial.println("==========================================================\n");

      digitalWrite(PIN_LED_OK, HIGH);
      digitalWrite(PIN_LED_ALARM, LOW);
      buzz(3, 100, 80);
      delay(2000);

      Serial.println(">> Mesin kembali ke posisi STANDBY. Tekan START untuk siklus berikutnya!\n");
      state = ST_IDLE;
      break;

    // ────────────────────────────────────────────────────────────────────────
    case ST_EMERGENCY:
      // LED Merah berkedip cepat menandakan status darurat
      digitalWrite(PIN_LED_ALARM, (millis() / 200) % 2 == 0);
      digitalWrite(PIN_LED_OK, LOW);

      if (isStartPressed()) {
        delay(50);
        if (isStartPressed()) {
          Serial.println(">> [RESET] Status darurat dibatalkan. Kembali ke STANDBY.\n");
          digitalWrite(PIN_LED_ALARM, LOW);
          buzz(2, 60, 60);
          state = ST_IDLE;
        }
      }
      break;
  }
}
