/*==========================================================
  UJI 05: LINEAR ACTUATOR 12V (1500N) + DRIVER L298N + LIMIT SWITCH
  ──────────────────────────────────────────────────────────
  Proyek      : Mesin Pencetak Tempe Otomatis v9
  Deskripsi   : Pengujian penggerak penekan 6-slot (turun & naik)
                serta pengujian interlock keamanan (Safety Cut-Off).
  
  KELISTRIKAN & PINOUT:
    - L298N 12V & GND   -> Langsung dari PSU 12V 10A (Baut ke Baut)
    - L298N OUT1 & OUT2 -> Ke 2 Kabel Linear Actuator 12V
    - L298N IN1         -> ESP32 GPIO 25 (Perintah Dorong Turun)
    - L298N IN2         -> ESP32 GPIO 26 (Perintah Tarik Naik)
    - L298N GND         -> Jumper ke Rel GND (-) Breadboard (Common GND)
    
    - Limit Switch Atas : Kaki NO -> GPIO 32, Kaki COM -> Rel GND
    - Limit Switch Bawah: Kaki NO -> GPIO 33, Kaki COM -> Rel GND
    - ESP32             : Ditenagai kabel USB Laptop
  ──────────────────────────────────────────────────────────
  KONTROL SERIAL MONITOR (115200 Baud):
    [ d ] : Dorong Aktuator TURUN (Arah Pengepresan)
    [ u ] : Tarik Aktuator NAIK   (Arah Homing / Istirahat)
    [ s ] : STOP Seketika
    [ t ] : Tes Sensor Limit Switch (Cek apakah switch terbaca)
==========================================================*/

// Definisi Pin Kontrol L298N
#define PIN_ACTUATOR_IN1  25
#define PIN_ACTUATOR_IN2  26

// Definisi Pin Sensor Limit Switch
#define PIN_LIMIT_ATAS    32
#define PIN_LIMIT_BAWAH   33

// LED Indikator internal ESP32
#define PIN_LED_BUILDIN    2

enum ActuatorState { ACT_STOP, ACT_DOWN, ACT_UP };
ActuatorState statusAktuator = ACT_STOP;

void aktuatorStop() {
  digitalWrite(PIN_ACTUATOR_IN1, LOW);
  digitalWrite(PIN_ACTUATOR_IN2, LOW);
  digitalWrite(PIN_LED_BUILDIN, LOW);
  statusAktuator = ACT_STOP;
}

void aktuatorTurun() {
  // Arah piston memanjang keluar (menekan ke bawah)
  digitalWrite(PIN_ACTUATOR_IN1, HIGH);
  digitalWrite(PIN_ACTUATOR_IN2, LOW);
  digitalWrite(PIN_LED_BUILDIN, HIGH);
  statusAktuator = ACT_DOWN;
}

void aktuatorNaik() {
  // Arah piston memendek ke dalam (menarik ke atas)
  digitalWrite(PIN_ACTUATOR_IN1, LOW);
  digitalWrite(PIN_ACTUATOR_IN2, HIGH);
  digitalWrite(PIN_LED_BUILDIN, HIGH);
  statusAktuator = ACT_UP;
}

void cetakMenu() {
  Serial.println("\n--------------------------------------------------");
  Serial.println("  PERINTAH PENGUJIAN LINEAR ACTUATOR:");
  Serial.println("   [ d ] -> Dorong Piston TURUN (Pressing)");
  Serial.println("   [ u ] -> Tarik Piston NAIK   (Homing)");
  Serial.println("   [ s ] -> STOP Seketika");
  Serial.println("   [ t ] -> Tes Status Kedua Limit Switch");
  Serial.println("--------------------------------------------------");
}

void cekStatusSensor() {
  Serial.println("\n[TES SENSOR LIMIT SWITCH]:");
  Serial.print(" - Limit Switch ATAS  (GPIO 32): ");
  if (digitalRead(PIN_LIMIT_ATAS) == LOW) {
    Serial.println("TERTEKAN / TERSENTUH (LOW) [OK]");
  } else {
    Serial.println("BEBAS / TERBUKA (HIGH)");
  }

  Serial.print(" - Limit Switch BAWAH (GPIO 33): ");
  if (digitalRead(PIN_LIMIT_BAWAH) == LOW) {
    Serial.println("TERTEKAN / TERSENTUH (LOW) [OK]");
  } else {
    Serial.println("BEBAS / TERBUKA (HIGH)");
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(PIN_LED_BUILDIN, OUTPUT);
  digitalWrite(PIN_LED_BUILDIN, LOW);

  // Inisialisasi pin driver L298N
  pinMode(PIN_ACTUATOR_IN1, OUTPUT);
  pinMode(PIN_ACTUATOR_IN2, OUTPUT);
  aktuatorStop(); // Pastikan mati saat pertama kali menyala

  // Inisialisasi limit switch dengan internal pull-up ESP32
  pinMode(PIN_LIMIT_ATAS, INPUT_PULLUP);
  pinMode(PIN_LIMIT_BAWAH, INPUT_PULLUP);

  Serial.println("\n========================================================");
  Serial.println("  MESIN TEMPE v9 — TEST UJI 5: LINEAR ACTUATOR 12V");
  Serial.println("========================================================");
  Serial.println("[INFO] Driver L298N terhubung ke GPIO 25 & GPIO 26");
  Serial.println("[INFO] Limit Switch terhubung ke GPIO 32 (Atas) & 33 (Bawah)");
  Serial.println("[INFO] Sistem Safety Interlock: AKTIF OTOMATIS");
  cetakMenu();
}

void loop() {
  // ── 1. BACA INPUT DARI SERIAL MONITOR ────────────────
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'd' || cmd == 'D') {
      // Cek apakah switch bawah sedang tersentuh
      if (digitalRead(PIN_LIMIT_BAWAH) == LOW) {
        Serial.println("\n[DITOLAK!] Tidak bisa turun! Limit Switch BAWAH sedang tertekan.");
      } else {
        Serial.println("\n>> Aktuator bergerak TURUN (Mendorong Pelat Press)...");
        aktuatorTurun();
      }
    }
    else if (cmd == 'u' || cmd == 'U') {
      // Cek apakah switch atas sedang tersentuh
      if (digitalRead(PIN_LIMIT_ATAS) == LOW) {
        Serial.println("\n[DITOLAK!] Tidak bisa naik! Limit Switch ATAS sedang tertekan.");
      } else {
        Serial.println("\n>> Aktuator bergerak NAIK (Menarik Pelat Press)...");
        aktuatorNaik();
      }
    }
    else if (cmd == 's' || cmd == 'S') {
      Serial.println("\n>> Aktuator dihentikan (STOP).");
      aktuatorStop();
    }
    else if (cmd == 't' || cmd == 'T') {
      cekStatusSensor();
    }
  }

  // ── 2. SISTEM SAFETY INTERLOCK (CUT-OFF OTOMATIS) ─────
  // Jika aktuator sedang turun lalu menyentuh limit switch bawah -> MATIKAN SEKETIKA!
  if (statusAktuator == ACT_DOWN && digitalRead(PIN_LIMIT_BAWAH) == LOW) {
    aktuatorStop();
    Serial.println("\n⚠️ [SAFETY CUT-OFF!] Limit Switch BAWAH tersentuh! Aktuator MATI SEKETIKA!");
  }

  // Jika aktuator sedang naik lalu menyentuh limit switch atas -> MATIKAN SEKETIKA!
  if (statusAktuator == ACT_UP && digitalRead(PIN_LIMIT_ATAS) == LOW) {
    aktuatorStop();
    Serial.println("\n⚠️ [SAFETY CUT-OFF!] Limit Switch ATAS tersentuh! Aktuator MATI SEKETIKA!");
  }

  delay(20);
}
