/*==========================================================
  TEST 02: LOAD CELL 10KG & HX711 INTERACTIVE CALIBRATION
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Menguji komunikasi ADC 24-bit HX711 dengan ESP32.
  2. Melakukan kalibrasi timbangan interaktif via Serial Monitor.
  3. Mendapatkan nilai `LOADCELL_FAKTOR` yang tepat untuk firmware utama.

  Wiring:
  - HX711 VCC  -> 5V (Step-down / Pin VIN)
  - HX711 GND  -> GND ESP32
  - HX711 DT   -> ESP32 GPIO 4
  - HX711 SCK  -> ESP32 GPIO 5

  Warna Kabel Load Cell ke Modul HX711:
  - Merah  -> E+ (Excitation +)
  - Hitam  -> E- (Excitation -)
  - Putih  -> A- (Signal -)
  - Hijau  -> A+ (Signal +)
==========================================================*/

#include <HX711.h>

#define PIN_HX711_DOUT 4
#define PIN_HX711_SCK  5

HX711 scale;
float calibration_factor = 420.0; // Nilai awal perkiraan

void printMenu() {
  Serial.println("\n--- PERINTAH KALIBRASI INTERAKTIF ---");
  Serial.println("  't' : Tare (Nol-kan timbangan saat kosong)");
  Serial.println("  '+' : Naikkan faktor kalibrasi (+10)");
  Serial.println("  '-' : Turunkan faktor kalibrasi (-10)");
  Serial.println("  'c' : Masukkan beban kalibrasi standar (misal botol 500g / 1000g)");
  Serial.println("-------------------------------------");
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 02: LOAD CELL 10KG + HX711 CALIBRATION");
  Serial.println("==========================================");

  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);

  Serial.println("[1] Memeriksa koneksi HX711...");
  if (scale.wait_ready_timeout(2000)) {
    Serial.println("   [OK] HX711 terdeteksi dan siap!");
  } else {
    Serial.println("   [ERROR] HX711 tidak merespons!");
    Serial.println("   Periksa kabel DOUT (GPIO 4), SCK (GPIO 5), VCC (5V), GND.");
    while (1) delay(1000);
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
      calibration_factor += 10.0;
      scale.set_scale(calibration_factor);
      Serial.printf(">> Faktor kalibrasi dinaikkan: %.2f\n", calibration_factor);
    } else if (ch == '-') {
      calibration_factor -= 10.0;
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
