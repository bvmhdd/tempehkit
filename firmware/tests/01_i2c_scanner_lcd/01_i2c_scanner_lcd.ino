/*==========================================================
  TEST 01: I2C SCANNER & LCD 16x2 TEST
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Memindai bus I2C untuk mengetahui alamat LCD (biasanya 0x27 atau 0x3F).
  2. Menampilkan teks pada LCD 16x2 dengan backlight.

  Wiring:
  - ESP32 GPIO 21 (SDA) -> LCD I2C Module SDA
  - ESP32 GPIO 22 (SCL) -> LCD I2C Module SCL
  - ESP32 VIN / 5V       -> LCD I2C Module VCC (5V)
  - ESP32 GND            -> LCD I2C Module GND
==========================================================*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define PIN_SDA 21
#define PIN_SCL 22

LiquidCrystal_I2C *lcd = nullptr;
byte i2c_addr = 0x00;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 01: I2C SCANNER & LCD 16x2");
  Serial.println("==========================================");

  Wire.begin(PIN_SDA, PIN_SCL);

  // 1. Scan I2C
  Serial.println("[1] Memindai alamat I2C pada GPIO 21 (SDA) & 22 (SCL)...");
  int nDevices = 0;
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("   -> Perangkat I2C ditemukan pada alamat: 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      i2c_addr = address;
      nDevices++;
    }
  }

  if (nDevices == 0) {
    Serial.println("   [ERROR] Tidak ada perangkat I2C ditemukan!");
    Serial.println("   Periksa kabel VCC (5V), GND, SDA (21), SCL (22).");
  } else {
    Serial.printf("   [OK] Ditemukan %d perangkat. Menggunakan alamat 0x%02X\n", nDevices, i2c_addr);

    // Inisialisasi LCD
    lcd = new LiquidCrystal_I2C(i2c_addr, 16, 2);
    lcd->init();
    lcd->backlight();
    lcd->clear();

    lcd->setCursor(0, 0);
    lcd->print("TEST LCD I2C OK!");
    lcd->setCursor(0, 1);
    lcd->printf("Addr: 0x%02X", i2c_addr);

    Serial.println("[2] Teks berhasil dikirim ke layar LCD.");
    Serial.println("    Jika layar menyala tapi tidak ada teks, putar potensiometer (kontras) biru di belakang modul I2C!");
  }
}

int counter = 0;
void loop() {
  if (lcd != nullptr) {
    lcd->setCursor(11, 1);
    lcd->printf("#%04d", counter++);
    delay(1000);
  } else {
    delay(2000);
  }
}
