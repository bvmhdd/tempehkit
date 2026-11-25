/*==========================================================
  UJI COBA NEMA 23 + TB6600 (KELISTRIKAN USB LAPTOP + PSU 12V)
  ──────────────────────────────────────────────────────────
  Proyek      : Mesin Pencetak Tempe Otomatis v9 (Rotary Flip 180°)
  
  KELISTRIKAN SISTEM (SANGAT AMAN UNTUK LAPTOP):
    - ESP32       : Ditenagai LANGSUNG dari kabel USB Laptop (5V)
    - TB6600      : Ditenagai LANGSUNG dari PSU 12V 10A (VCC & GND)
    - Step-Down   : TIDAK DIPAKAI (Dilepas dari ESP32)
    - Micro Switch: TIDAK DIPAKAI (Berhenti presisi via pulsa)

  KONEKSI KABEL:
    - ESP32 GPIO 12 -> TB6600 PUL+ (Pulsa Langkah)
    - ESP32 GPIO 14 -> TB6600 DIR+ (Arah Putar)
    - ESP32 GND     -> TB6600 PUL- & DIR- & GND PSU 12V (Common GND)
    - TB6600 ENA    -> KOSONG (Default aktif mengunci torsi)
    - TB6600 A/B    -> 4 Kabel Motor Stepper NEMA 23
  ──────────────────────────────────────────────────────────
  KONTROL SERIAL MONITOR (115200 Baud):
    [ 1 ] Ketik '1' lalu Enter -> Putar Flip 180° (Menuang tempe)
    [ 0 ] Ketik '0' lalu Enter -> Putar Balik ke 0° (Posisi awal)
    [ a ] Ketik 'a' lalu Enter -> Mode Auto Loop Bolak-Balik
    [ s ] Ketik 's' lalu Enter -> Emergency STOP (Berhenti seketika)
==========================================================*/

#include <AccelStepper.h>

// ── Pinout ESP32 ─────────────────────────────────────────
#define PIN_STEPPER_STEP  12
#define PIN_STEPPER_DIR   14
#define PIN_LED_BUILDIN    2   // LED biru bawaan ESP32 (indikator gerak)

// ── Parameter Perhitungan Pulsa Stepper ──────────────────
// NEMA 23 (200 step) × 8 microstep × 3 gear_ratio / 2 = 2400 step (180°)
const long STEPS_180_DEG = 2400;

// Inisialisasi library AccelStepper (mode driver 2-kabel: STEP & DIR)
AccelStepper stepper(AccelStepper::DRIVER, PIN_STEPPER_STEP, PIN_STEPPER_DIR);

bool posisiTerbalik = false;
bool sedangBergerak = false;
bool modeOtomatis   = false;
unsigned long waktuJedaAuto = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  // Setel LED indikator
  pinMode(PIN_LED_BUILDIN, OUTPUT);
  digitalWrite(PIN_LED_BUILDIN, LOW);

  // Setel Kecepatan & Akselerasi Halus (Bebas Hentakan & Torsi Kuat)
  stepper.setMaxSpeed(1000.0);      // Kecepatan maksimal (step/detik)
  stepper.setAcceleration(500.0);   // Akselerasi bertahap
  stepper.setCurrentPosition(0);

  Serial.println("\n========================================================");
  Serial.println("  MESIN TEMPE v9 — TEST BENCH NEMA 23 & TB6600");
  Serial.println("========================================================");
  Serial.println("[STATUS] ESP32      : Aktif via USB Laptop (Aman)");
  Serial.println("[STATUS] Daya Motor : PSU 12V 10A aktif di TB6600");
  Serial.println("[STATUS] Torsi Motor: MENGUNCI KOKOH (Holding Active)");
  Serial.println("--------------------------------------------------------");
  Serial.println("PERINTAH KONTROL SERIAL MONITOR:");
  Serial.println("  Ketik '1' + Enter -> Putar Flip 180° (Menuang)");
  Serial.println("  Ketik '0' + Enter -> Putar Balik ke 0° (Semula)");
  Serial.println("  Ketik 'a' + Enter -> Mode AUTO LOOP (Bolak-balik)");
  Serial.println("  Ketik 's' + Enter -> STOP Darurat");
  Serial.println("========================================================\n");
}

void loop() {
  // Generator pulsa motor AccelStepper
  stepper.run();

  // Deteksi ketika motor selesai berputar mencapai target
  if (sedangBergerak && stepper.distanceToGo() == 0) {
    sedangBergerak = false;
    digitalWrite(PIN_LED_BUILDIN, LOW); // Matikan LED saat motor diam

    Serial.print("[SUKSES] Motor berhenti di: ");
    Serial.print(stepper.currentPosition());
    Serial.print(" step -> ");
    Serial.println(posisiTerbalik ? "CETAKAN TERBALIK 180°" : "POSISI AWAL 0°");

    if (modeOtomatis) {
      waktuJedaAuto = millis();
    }
  }

  // Logika Mode Otomatis (jika diaktifkan dengan 'a')
  if (modeOtomatis && !sedangBergerak) {
    if (millis() - waktuJedaAuto > 2500) { // Jeda diam 2.5 detik
      if (posisiTerbalik) {
        jalanKe(0);
        posisiTerbalik = false;
      } else {
        jalanKe(STEPS_180_DEG);
        posisiTerbalik = true;
      }
    }
  }

  // Membaca ketikan perintah dari Serial Monitor
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == '1' && !sedangBergerak) {
      modeOtomatis = false;
      Serial.println("\n>> Memutar FLIP 180°...");
      jalanKe(STEPS_180_DEG);
      posisiTerbalik = true;
    }
    else if (cmd == '0' && !sedangBergerak) {
      modeOtomatis = false;
      Serial.println("\n>> Memutar BALIK ke Posisi Semula 0°...");
      jalanKe(0);
      posisiTerbalik = false;
    }
    else if (cmd == 'a' || cmd == 'A') {
      modeOtomatis = true;
      Serial.println("\n>> Mode AUTO LOOP Aktif! (Motor akan bolak-balik otomatis)...");
      jalanKe(STEPS_180_DEG);
      posisiTerbalik = true;
    }
    else if (cmd == 's' || cmd == 'S') {
      modeOtomatis = false;
      stepper.stop();
      sedangBergerak = false;
      digitalWrite(PIN_LED_BUILDIN, LOW);
      Serial.println("\n>> [EMERGENCY STOP] Motor dihentikan mendadak!");
    }
  }
}

void jalanKe(long targetLangkah) {
  sedangBergerak = true;
  digitalWrite(PIN_LED_BUILDIN, HIGH); // LED menyala saat motor aktif bergerak
  stepper.moveTo(targetLangkah);
}
