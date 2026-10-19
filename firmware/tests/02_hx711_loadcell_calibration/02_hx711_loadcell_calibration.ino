/*==========================================================
  TEST 02: LOAD CELL 5KG & HX711 INTERACTIVE CALIBRATION
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Menguji komunikasi ADC 24-bit HX711 dengan ESP32.
  2. Melakukan kalibrasi timbangan interaktif via Serial Monitor.
  3. Mendapatkan nilai `LOADCELL_FAKTOR` yang tepat untuk firmware utama.

  Wiring:
  - HX711 VCC  -> 5V (Step-down / Pin VIN)
  - HX711 GND  -> GND ESP32
  - HX711 DT   -> ESP32 GPIO 5
  - HX711 SCK  -> ESP32 GPIO 4

  Warna Kabel Load Cell ke Modul HX711:
  - Merah  -> E+ (Excitation +)
  - Hitam  -> E- (Excitation -)
  - Putih  -> A- (Signal -)
  - Hijau  -> A+ (Signal +)
==========================================================*/

#include <HX711.h>

#define PIN_HX711_DOUT 5
#define PIN_HX711_SCK  4

HX711 scale;
float calibration_factor = 0.42; // Nilai awal simulasi Wokwi (satuan gram)

void printMenu() {
  Serial.println("\n--- PERINTAH KALIBRASI INTERAKTIF ---");
  Serial.println("  't' : Tare (Nol-kan timbangan saat kosong)");
  Serial.println("  '+' : Naikkan faktor kalibrasi (+0.02)");
  Serial.println("  '-' : Turunkan faktor kalibrasi (-0.02)");
  Serial.println("  'c' : Masukkan beban kalibrasi standar (misal botol 500g / 1000g)");
  Serial.println("-------------------------------------");
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 02: LOAD CELL 5KG + HX711 CALIBRATION");
  Serial.println("==========================================");
  Serial.flush();

  Serial.println("[1] Memeriksa koneksi modul HX711...");
  Serial.printf("    Konfigurasi pin: DOUT=GPIO %d, SCK=GPIO %d\n", PIN_HX711_DOUT, PIN_HX711_SCK);
  Serial.flush();

  // Konfigurasi pin awal secara aman untuk membangunkan chip HX711
  pinMode(PIN_HX711_SCK, OUTPUT);
  digitalWrite(PIN_HX711_SCK, LOW); // SCK LOW = mode aktif (bukan power-down)
  pinMode(PIN_HX711_DOUT, INPUT_PULLUP);

  // Tunggu respon pin data (HX711 akan menarik DOUT ke LOW saat siap)
  unsigned long startCheck = millis();
  bool sensorReady = false;
  while (millis() - startCheck < 2500) {
    if (digitalRead(PIN_HX711_DOUT) == LOW) {
      sensorReady = true;
      break;
    }
    delay(20);
    yield(); // Mencegah watchdog reset pada ESP32
  }

  if (sensorReady) {
    scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);
    Serial.println("   [OK] HX711 terdeteksi dan siap!");
  } else {
    Serial.println("   [ERROR] HX711 TIDAK MERESPONS!");
    Serial.println("   -------------------------------------------------");
    Serial.println("   Penyebab yang sering terjadi:");
    Serial.println("   1. Pin DT & SCK tertukar:");
    Serial.printf("      - Pastikan kabel DT modul ke GPIO %d\n", PIN_HX711_DOUT);
    Serial.printf("      - Pastikan kabel SCK modul ke GPIO %d\n", PIN_HX711_SCK);
    Serial.println("   2. Kabel VCC (5V) atau GND longgar.");
    Serial.println("   3. 4 kabel Load Cell ke HX711 belum terpasang.");
    Serial.println("   -------------------------------------------------");
    Serial.flush();
    while (1) {
      delay(1000);
      yield(); // Tetap jalan tanpa merestart ESP32
    }
  }

  Serial.println("[2] Melakukan TARE awal (pastikan sensor kosong tanpa beban)...");
  scale.set_scale();
  scale.tare();
  scale.set_scale(calibration_factor);
  Serial.println("   [OK] Tare selesai!");

  printMenu();
}

void loop() {
  if (scale.is_ready()) {
    float reading = scale.get_units(5); // Rata-rata 5 pembacaan
    Serial.printf("Berat: %6.1f gram  |  Faktor Kalibrasi: %.2f\n", reading, calibration_factor);
  } else {
    Serial.println("[WARNING] Sensor sibuk / tidak terbaca...");
  }

  // Cek input dari Serial Monitor
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch == 't' || ch == 'T') {
      Serial.println(">> Melakukan TARE... sensor di-nolkan.");
      scale.tare();
    } else if (ch == '+') {
      calibration_factor += 0.02;
      scale.set_scale(calibration_factor);
      Serial.printf(">> Faktor kalibrasi dinaikkan: %.2f\n", calibration_factor);
    } else if (ch == '-') {
      calibration_factor -= 0.02;
      scale.set_scale(calibration_factor);
      Serial.printf(">> Faktor kalibrasi diturunkan: %.2f\n", calibration_factor);
    } else if (ch == 'c' || ch == 'C') {
      Serial.println("\n>> PROSEDUR HITUNG OTOMATIS:");
      Serial.println("   1. Pastikan beban kalibrasi sudah ada di atas sensor (misal gula/botol).");
      Serial.println("   2. Ketik berat beban sebenarnya dalam gram (contoh: 500 atau 1000) lalu ENTER:");
      while (!Serial.available()) delay(50);
      float known_weight = Serial.parseFloat();
      if (known_weight > 0) {
        long raw = scale.get_value(10);
        calibration_factor = (float)raw / known_weight;
        scale.set_scale(calibration_factor);
        Serial.printf("   [BERHASIL!] Nilai faktor baru: %.2f\n", calibration_factor);
        Serial.printf("   Salin nilai ini ke mesin_tempe.ino pada: #define LOADCELL_FAKTOR %.1f\n\n", calibration_factor);
      }
    }
  }

  delay(600);
}