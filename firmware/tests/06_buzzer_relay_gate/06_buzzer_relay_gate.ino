/*==========================================================
  TEST 06: BUZZER & RELAY GATE HOPPER TEST
  Mesin Pencetak Tempe Otomatis
  ──────────────────────────────────────────────────────────
  Tujuan:
  1. Menguji fungsi nada buzzer aktif 5V (GPIO 23).
  2. Menguji aktivasi relay gate hopper (GPIO 27).

  Wiring:
  - Buzzer VCC -> 5V (atau GPIO 23 jika buzzer mini dengan arus <12mA)
  - Buzzer GND -> GND ESP32
  - Relay IN   -> ESP32 GPIO 27
  - Relay VCC  -> 5V
  - Relay GND  -> GND ESP32
==========================================================*/

#define PIN_BUZZER     23
#define PIN_RELAY_GATE 27

void beepPendek(int count) {
  for (int i = 0; i < count; i++) {
    digitalWrite(PIN_BUZZER, HIGH);
    delay(100);
    digitalWrite(PIN_BUZZER, LOW);
    delay(100);
  }
}

void beepPanjang(int ms) {
  digitalWrite(PIN_BUZZER, HIGH);
  delay(ms);
  digitalWrite(PIN_BUZZER, LOW);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==========================================");
  Serial.println("  TEST 06: BUZZER & RELAY GATE TEST");
  Serial.println("==========================================");

  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_RELAY_GATE, OUTPUT);

  // Relay biasanya Active LOW
  digitalWrite(PIN_RELAY_GATE, HIGH); // Relay OFF (standar)
  digitalWrite(PIN_BUZZER, LOW);

  Serial.println("[OK] Modul diinisialisasi.");
  Serial.println("\n--- PERINTAH SERIAL ---");
  Serial.println("  '1' : Bunyikan Beep Pendek (Konfirmasi OK)");
  Serial.println("  '2' : Bunyikan Beep Panjang (Alarm Error)");
  Serial.println("  'r' : Toggle Relay Gate Hopper (ON / OFF)");
  Serial.println("-----------------------");
}

bool relayState = false;

void loop() {
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch == '1') {
      Serial.println(">> Beep 2x: Siklus Mulai / Selesai");
      beepPendek(2);
    } else if (ch == '2') {
      Serial.println(">> Beep Panjang: Alarm Hopper Kosong / Error");
      beepPanjang(1000);
    } else if (ch == 'r' || ch == 'R') {
      relayState = !relayState;
      // Modul relay 5V optocoupler umumnya Active-LOW:
      // LOW = Relay ON (kontak tertutup), HIGH = Relay OFF (kontak terbuka)
      digitalWrite(PIN_RELAY_GATE, relayState ? LOW : HIGH);
      Serial.printf(">> Relay Gate Hopper: %s\n", relayState ? "BUKA / AKTIF (ON)" : "TUTUP / NONAKTIF (OFF)");
    }
  }
  delay(50);
}
