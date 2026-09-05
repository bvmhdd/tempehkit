/*==========================================================
  TEST 04: PUSH BUTTONS & LIMIT SWITCHES TEST
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Menguji tombol fisik START (GPIO 34) dan STOP (GPIO 35).
  2. Menguji Limit Switch Posisi Atas (GPIO 32) dan Bawah (GPIO 33).
  3. Memverifikasi LED status Hijau (GPIO 2) dan Merah (GPIO 15).

  Wiring:
  - Tombol START -> GPIO 34 (Wajib resistor eksternal 10k ohm pull-up ke 3.3V, tombol ke GND)
  - Tombol STOP  -> GPIO 35 (Wajib resistor eksternal 10k ohm pull-up ke 3.3V, tombol ke GND)
    * Alasan: GPIO 34 & 35 adalah pin input-only pada ESP32 tanpa internal pull-up!
  - Limit Switch ATAS  -> GPIO 32 (Menggunakan INPUT_PULLUP internal ESP32, switch ke GND)
  - Limit Switch BAWAH -> GPIO 33 (Menggunakan INPUT_PULLUP internal ESP32, switch ke GND)
  - LED Hijau (OK)     -> GPIO 2 (seri resistor 220 ohm ke GND)
  - LED Merah (ALARM)  -> GPIO 15 (seri resistor 220 ohm ke GND)
==========================================================*/

#define PIN_BTN_START   34
#define PIN_BTN_STOP    35
#define PIN_LIMIT_ATAS  32
#define PIN_LIMIT_BAWAH 33
#define PIN_LED_OK       2
#define PIN_LED_ALARM   15

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 04: TOMBOL & LIMIT SWITCH TEST");
  Serial.println("==========================================");

  // Pin output LED
  pinMode(PIN_LED_OK, OUTPUT);
  pinMode(PIN_LED_ALARM, OUTPUT);

  // Pin Limit Switch (Internal Pull-Up)
  pinMode(PIN_LIMIT_ATAS, INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);

  // Pin Tombol (Input biasa - butuh pull-up resistor 10k fisik)
  pinMode(PIN_BTN_START, INPUT);
  pinMode(PIN_BTN_STOP, INPUT);

  // Tes kedip LED awal
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_ALARM, HIGH);
  delay(500);
  digitalWrite(PIN_LED_OK, LOW);
  digitalWrite(PIN_LED_ALARM, LOW);

  Serial.println("[OK] Siap! Tekan tombol START/STOP atau sentuh limit switch...");
  Serial.println("     Logika: Tombol ditekan = LOW (0), dilepas = HIGH (1)");
}

bool lastStart = HIGH;
bool lastStop  = HIGH;
bool lastLimUp = HIGH;
bool lastLimDn = HIGH;

void loop() {
  bool btnStart = digitalRead(PIN_BTN_START);
  bool btnStop  = digitalRead(PIN_BTN_STOP);
  bool limUp    = digitalRead(PIN_LIMIT_ATAS);
  bool limDn    = digitalRead(PIN_LIMIT_BAWAH);

  // Deteksi event tekan tombol START
  if (btnStart == LOW && lastStart == HIGH) {
    Serial.println(">> [EVENT] Tombol START DITEKAN! -> LED Hijau Menyala");
    digitalWrite(PIN_LED_OK, HIGH);
    delay(50); // Debounce
  } else if (btnStart == HIGH && lastStart == LOW) {
    digitalWrite(PIN_LED_OK, LOW);
  }

  // Deteksi event tekan tombol STOP
  if (btnStop == LOW && lastStop == HIGH) {
    Serial.println(">> [EVENT] Tombol STOP DITEKAN! -> LED Merah Menyala");
    digitalWrite(PIN_LED_ALARM, HIGH);
    delay(50);
  } else if (btnStop == HIGH && lastStop == LOW) {
    digitalWrite(PIN_LED_ALARM, LOW);
  }

  // Deteksi Limit Switch Atas
  if (limUp == LOW && lastLimUp == HIGH) {
    Serial.println(">> [LIMIT] Limit Switch ATAS Tertekan! (Posisi Home Tercapai)");
  }

  // Deteksi Limit Switch Bawah
  if (limDn == LOW && lastLimDn == HIGH) {
    Serial.println(">> [LIMIT] Limit Switch BAWAH Tertekan! (Posisi Maksimal Press Tercapai)");
  }

  lastStart = btnStart;
  lastStop  = btnStop;
  lastLimUp = limUp;
  lastLimDn = limDn;

  delay(20);
}
