/*==========================================================
  TEST 03: ULTRASONIC HC-SR04 (LEVEL KEDELAI HOPPER)
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Mengukur jarak pantul ultrasonik (2 - 400 cm).
  2. Menguji deteksi level persediaan kedelai di corong penampung (hopper).
  3. Memvalidasi threshold alarm ketika stok kedelai menipis.

  Wiring:
  - HC-SR04 VCC   -> 5V
  - HC-SR04 GND   -> GND ESP32
  - HC-SR04 TRIG  -> ESP32 GPIO 18
  - HC-SR04 ECHO  -> ESP32 GPIO 19
    * Catatan: ECHO mengeluarkan sinyal 5V. Disarankan menggunakan
      voltage divider (resistor 1k ke GPIO 19, lalu 2k ke GND)
      agar aman bagi pin ESP32 yang bertegangan kerja 3.3V.
==========================================================*/

#define PIN_TRIG 18
#define PIN_ECHO 19

// Ambang batas level hopper (cm)
// Jarak sensor ke permukaan kedelai saat kosong = misal 25 cm
// Saat kedelai penuh = 5 cm
// Batas alarm habis = > 18 cm
const float DISTANCE_FULL_CM  = 5.0;
const float DISTANCE_EMPTY_CM = 25.0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 03: ULTRASONIC HC-SR04 HOPPER TEST");
  Serial.println("==========================================");

  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  digitalWrite(PIN_TRIG, LOW);
  delay(50);
  Serial.println("[OK] Pin Trig & Echo siap. Mengukur jarak...");
}

float bacaJarakCM() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duration = pulseIn(PIN_ECHO, HIGH, 30000); // Timeout 30ms (~5 meter)
  if (duration == 0) return -1.0; // Tidak ada pantulan / out of range

  return (duration * 0.0343) / 2.0;
}

void loop() {
  float distance = bacaJarakCM();

  if (distance < 0 || distance > 400) {
    Serial.println("[WARNING] Sensor di luar jangkauan (Out of Range / No Echo)");
  } else {
    // Estimasi persentase isi kedelai di hopper
    float persenIsi = (DISTANCE_EMPTY_CM - distance) / (DISTANCE_EMPTY_CM - DISTANCE_FULL_CM) * 100.0;
    if (persenIsi < 0) persenIsi = 0;
    if (persenIsi > 100) persenIsi = 100;

    Serial.printf("Jarak: %5.1f cm  |  Kapasitas Hopper: %3.0f%%  |  Status: ", distance, persenIsi);
    if (persenIsi < 20) {
      Serial.println("[ALARM: KEDELAI HAMPIR HABIS!]");
    } else if (persenIsi > 80) {
      Serial.println("[PENUH / OPTIMAL]");
    } else {
      Serial.println("[NORMAL]");
    }
  }

  delay(800);
}
