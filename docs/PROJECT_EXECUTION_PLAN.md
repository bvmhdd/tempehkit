# 🏭 Project Execution Plan — Mesin Pencetak Tempe Tier 2
## End-to-End: Dari Nol sampai Produksi

> **Framework**: Hardware Agile Sprint (5 Sprint × 1 Minggu)  
> **Status Tracking**: Gunakan GitHub Projects / Notion / Trello / kertas (pilih satu!)  
> **Estimasi Total**: 5–6 Minggu kerja paruh waktu

---

## FRAMEWORK YANG DIGUNAKAN

```
Hardware Agile Sprint Method:
┌──────────────────────────────────────────────────────────┐
│ SPRINT 0: Procurement & Persiapan          (Minggu 0–1)  │
│ SPRINT 1: Mekanik & Frame                  (Minggu 1–2)  │
│ SPRINT 2: Elektronik & Unit Test           (Minggu 2–3)  │
│ SPRINT 3: Firmware & Integrasi             (Minggu 3–4)  │
│ SPRINT 4: System Test & Kalibrasi          (Minggu 4–5)  │
│ SPRINT 5: Produksi & Fine-tuning           (Minggu 5–6)  │
└──────────────────────────────────────────────────────────┘

Setiap Sprint punya: TASK LIST + ACCEPTANCE CRITERIA (Definition of Done)
```

> **Tools yang direkomendasikan**: Notion (gratis, mobile-friendly) → buat database task  
> Alternatif: Google Sheets dengan kolom [Task | Status | Due | Notes]  
> Alternatif paling simpel: Buku tulis dengan checklist ✓

---

## SPRINT 0: PROCUREMENT & PERSIAPAN
### Target: Semua bahan tersedia, dokumen siap
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 0

#### S0-1: Buat Shopping List Final
- [ ] Print/buka `docs/implementation_plan_final.md`
- [ ] Pisahkan BOM ke 3 kelompok:
  - **A**: Tokopedia/Shopee → order online (elektronik)
  - **B**: Toko besi lokal → beli langsung (hollow, plat)
  - **C**: Bengkel/tukang → custom (hopper SS304, nozzle)
- [ ] Konfirmasi harga terkini (harga bisa beda dari estimasi)

#### S0-2: Order Elektronik (Online)
- [ ] **Order Batch 1** (kritis, harus ada duluan):
  - ESP32 DevKit V1 ×1
  - Load Cell 5kg + HX711 ×1
  - Servo MG996R ×3
  - NEMA17 42mm 2A ×1
  - Driver A4988 ×1
  - Driver L298N ×1
  - HC-SR04 ×1
  - LCD 16×2 I2C ×1
  - Limit Switch micro ×6 (beli lebih, harga murah)
  
- [ ] **Order Batch 2** (bisa menyusul):
  - PSU 12V 10A ×1
  - Buck Converter LM2596 ×1
  - Linear Rail MGR12 600mm ×2
  - Lead Screw T8 300mm + Nut ×1
  - GT2 Belt 1m + Pulley 20T ×2
  - Idler Pulley GT2 ×2
  - Bearing 608ZZ ×4

- [ ] **Order Batch 3** (untuk protoboard):
  - Kabel jumper male-female 40cm ×40
  - Protoboard / PCB stripboard
  - Terminal block screw 2-pin ×20
  - Heatshrink tube set
  - Kapasitor 470μF 10V ×3
  - Resistor 10kΩ ×10 (pullup)
  - Push button 16mm ×3 + LED 5mm ×5

#### S0-3: Beli Material Mekanik (Toko Besi Lokal)
- [ ] Besi Hollow 40×40mm tebal 2mm — beli ~10m (minta potong)
- [ ] Plat aluminium 3mm — minimal 30×30cm (untuk press plate + arm)
- [ ] Baut M5×20 + mur ×30 set
- [ ] Baut M3×10 + mur ×50 set
- [ ] Kaki karet M10 ×4

#### S0-4: Pesan Custom Parts
- [ ] Hubungi bengkel las/stainless:
  - Hopper kerucut SS304 (20×20cm atas, nozzle outlet Ø40mm, tebal 0.8mm)
  - Minta gambar teknik sederhana: [tinggi 25cm, sudut kerucut 60°]
  - Estimasi biaya: Rp 100.000–200.000
- [ ] Hopper bisa ditambahkan setelah frame siap (tidak kritis di awal)

#### S0-5: Persiapan Tools & Workspace
- [ ] Pastikan tersedia: solder + timah, multimeter, tang, obeng set
- [ ] Download Arduino IDE + install ESP32 board support
- [ ] Install library yang dibutuhkan:
  ```
  Arduino IDE → Library Manager:
  - HX711 by bogde
  - ESP32Servo by Kevin Harrington
  - LiquidCrystal_I2C by Frank de Brabander
  - ArduinoJson by Benoit Blanchon
  - ESPAsyncWebServer by lacamera
  - AsyncTCP by me-no-dev
  - AccelStepper by Mike McCauley
  ```
- [ ] Clone/buka folder firmware di Arduino IDE
- [ ] Pastikan firmware test yang ada bisa compile:
  - `02_hx711_loadcell_calibration.ino` → compile OK
  - `03_hcsr04_ultrasonic.ino` → compile OK

#### ✅ DEFINITION OF DONE — Sprint 0
- [ ] Semua komponen elektronik sudah diorder (konfirmasi pembayaran)
- [ ] Material besi hollow sudah dibeli atau konfirmasi toko
- [ ] Arduino IDE bisa compile semua firmware test
- [ ] Hopper SS304 sudah dipesan ke bengkel
- [ ] Ada workspace/meja kerja yang bersih untuk assembly

---

## SPRINT 1: MEKANIK & FRAME
### Target: Frame berdiri, rel terpasang, mold bisa slide manual
### Durasi: 5–7 hari (bergantung ketersediaan tukang las)

---

### 📋 TASK LIST SPRINT 1

#### S1-1: Buat Gambar Teknik untuk Tukang Las
- [ ] Print `docs/dimensi_mekanik_final.md` (atau buat terpisah)
- [ ] Siapkan sketsa dimensi untuk tukang las:
  ```
  Frame utama: 80×40×130cm
  Cross bar posisi: 20cm, 60cm, 90cm, 130cm dari lantai
  Lubang-lubang bracket yang perlu dibuat
  ```
- [ ] Diskusikan dengan tukang las: estimasi hari kerja + ongkos

#### S1-2: Fabrikasi Frame (di Tukang Las)
- [ ] Kaki vertikal ×4 @ 100cm
- [ ] Cross bar bawah (h=20cm): 2 batang 80cm + 2 batang 40cm
- [ ] Cross bar tengah (h=60cm): 2 batang 80cm
- [ ] Cross bar atas (h=90cm): 2 batang 80cm + plate motor press
- [ ] Top frame (h=130cm): 2 batang 80cm + bracket hopper
- [ ] Semua bracket untuk: linear rail, servo arm, motor
- [ ] **Cek**: Siku semua sambungan sebelum las final!

#### S1-3: Finishing Frame
- [ ] Grinding + amplas semua permukaan
- [ ] Cat primer (epoxy primer 1 lapis)
- [ ] Cat topcoat (epoxy food-grade, warna sesuai selera)
- [ ] Tunggu kering 24 jam

#### S1-4: Pasang Linear Rail
- [ ] Bersihkan permukaan dudukan rail dengan WD-40
- [ ] Pasang MGR12 rail ×2 ke cross bar bawah dengan baut M5
- [ ] **Pastikan**: kedua rail PARALEL (ukur dengan penggaris)
- [ ] Toleransi paralel: <1mm gap di seluruh panjang 600mm
- [ ] Pasang carriage block ke rail, cek smooth sliding

#### S1-5: Pasang Mold ke Carriage
- [ ] Buat adapter plate (aluminium 3mm) untuk sambung mold ke carriage
- [ ] Baut mold ke adapter plate + adapter plate ke carriage
- [ ] Test: geser mold dengan tangan → harus MULUS, tidak goyang

#### S1-6: Pasang Stepper + Belt Drive
- [ ] Pasang NEMA17 ke bracket di salah satu ujung rel
- [ ] Pasang pulley 20T ke shaft NEMA17
- [ ] Pasang idler pulley di ujung rel lainnya
- [ ] Pasang GT2 belt: sambungkan ke carriage + tensikan belt
- [ ] Test putar NEMA17 manual (pakai obeng) → mold harus bergerak

#### S1-7: Pasang Press Mechanism
- [ ] Pasang lead screw T8 vertikal ke frame (bearing atas + bawah)
- [ ] Pasang motor DC gearbox ke coupling lead screw di atas
- [ ] Pasang press plate aluminium ke nut T8
- [ ] **Pastikan**: press plate bergerak lurus vertikal, tidak miring
- [ ] Pasang 2 limit switch: atas (h=90cm) dan bawah (h=60cm)

#### ✅ DEFINITION OF DONE — Sprint 1
- [ ] Frame berdiri kokoh, tidak goyang (cek dengan tangan)
- [ ] Mold bisa digeser manual di rel dengan halus, tidak ada gesekan berat
- [ ] Belt drive terpasang, mold bergerak saat NEMA17 diputar manual
- [ ] Press plate bisa naik/turun manual di lead screw
- [ ] Semua limit switch sudah posisi benar
- [ ] Cat sudah kering, frame bersih

---

## SPRINT 2: ELEKTRONIK & UNIT TEST
### Target: Setiap komponen elektronik sudah ditest & bekerja sendiri-sendiri
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 2

#### S2-1: Buat Protoboard/Wiring Sementara
- [ ] Pasang ESP32 di protoboard besar / breadboard
- [ ] Wiring PSU 12V → Buck converter → 5V rail
- [ ] Ukur output buck: HARUS 5.00–5.10V (adjust potensiometer)
- [ ] Sambungkan jalur GND bersama (common ground)

#### S2-2: Unit Test Load Cell + HX711
- [ ] Wire HX711: DOUT→GPIO4, SCK→GPIO5, VCC→3.3V, GND
- [ ] Upload `02_hx711_loadcell_calibration.ino`
- [ ] Ikuti prosedur kalibrasi:
  - Tare kosong
  - Taruh batu timbang 200g → catat calibration factor
  - Taruh 500g → verifikasi
- [ ] **LULUS jika**: error < ±5g untuk berat 200–500g
- [ ] Catat calibration_factor: __________ (simpan di config.h)

#### S2-3: Unit Test HC-SR04 (Sensor Hopper)
- [ ] Wire: TRIG→GPIO18, ECHO→GPIO19, VCC→5V, GND
- [ ] Upload `03_hcsr04_ultrasonic.ino`
- [ ] Ukur jarak 5cm, 10cm, 20cm dengan penggaris
- [ ] **LULUS jika**: error < ±2cm untuk jarak 5–30cm

#### S2-4: Unit Test Limit Switch & Tombol
- [ ] Wire 4 limit switch + 3 tombol ke GPIO yang sesuai
- [ ] Pullup eksternal 10kΩ untuk GPIO 34, 35, 36
- [ ] Upload `04_buttons_and_limitswitches.ino`
- [ ] Test setiap switch/tombol → Serial Monitor harus respon

#### S2-5: Unit Test Motor DC Press + L298N
- [ ] Wire L298N: IN1→GPIO25, IN2→GPIO26, VCC→12V, GND bersama
- [ ] Upload `05_motor_l298n_leadscrew.ino`
- [ ] Test naik dan turun press plate
- [ ] **LULUS jika**: motor berhenti saat limit switch aktif (tulis kode test)
- [ ] Ukur kecepatan: target ~5–10mm/detik untuk press plate

#### S2-6: Unit Test Servo MG996R
- [ ] Wire 3 servo ke GPIO27 (kiri), GPIO33 (kanan), GPIO17 (gate)
- [ ] Power servo dari 5V buck (BUKAN dari 3.3V ESP32!)
- [ ] Pasang kapasitor 470μF di jalur 5V servo (dekat konektor)
- [ ] Upload sketch test servo:
  ```cpp
  #include <ESP32Servo.h>
  Servo servoKiri, servoKanan, servoGate;
  void setup() {
    servoKiri.attach(27); servoKanan.attach(33); servoGate.attach(17);
    servoGate.write(0);   // gate tutup
    delay(1000);
    servoGate.write(90);  // gate buka
    delay(2000);
    servoGate.write(0);   // gate tutup lagi
    servoKiri.write(0);  servoKanan.write(0);   // arm rest
    delay(1000);
    servoKiri.write(110); servoKanan.write(70);  // arm fold
    // Note: kanan mungkin mirror (sesuaikan sudut)
    delay(2000);
    servoKiri.write(0);  servoKanan.write(0);   // arm balik
  }
  void loop(){}
  ```
- [ ] Cek: servo gate buka/tutup mulus, tidak ada getaran berlebihan
- [ ] Cek: arm kiri dan kanan lipat plastik dengan benar (test dengan plastik)
- [ ] **Catat**: sudut exact yang benar untuk fold & unfold (mungkin bukan tepat 110°)

#### S2-7: Unit Test NEMA17 + A4988
- [ ] Wire A4988: DIR→GPIO14, STEP→GPIO12, EN→GPIO13
- [ ] MS1+MS2+MS3 untuk 1/8 step (cek datasheet A4988: MS1=H, MS2=H, MS3=L)
- [ ] Set current limit A4988: putar potensiometer → Vref ≈ 0.8V (= 2A × 0.4 resistor)
- [ ] Upload AccelStepper test:
  ```cpp
  #include <AccelStepper.h>
  AccelStepper stepper(AccelStepper::DRIVER, 12, 14);
  void setup() {
    pinMode(13, OUTPUT); digitalWrite(13, LOW); // enable
    stepper.setMaxSpeed(2000); stepper.setAcceleration(500);
    stepper.moveTo(1520); // geser 1 slot = 7.6cm
  }
  void loop() { stepper.run(); }
  ```
- [ ] Ukur: apakah mold bergerak ±7.6cm?
- [ ] Fine-tune steps_per_cm jika perlu

#### S2-8: Unit Test LCD I2C
- [ ] Wire: SDA→GPIO21, SCL→GPIO22, VCC→5V
- [ ] Cek I2C address dengan `01_i2c_scanner_lcd.ino`
- [ ] Tampilkan "MESIN TEMPE\nv1.0 READY"
- [ ] Pastikan kontras OK (adjust potensiometer di modul I2C)

#### S2-9: Test Buzzer & LED
- [ ] Wire buzzer aktif 5V ke GPIO23 (via transistor NPN atau langsung jika drive cukup)
- [ ] Wire LED merah GPIO, hijau GPIO2
- [ ] Test berbunyi dan nyala

#### ✅ DEFINITION OF DONE — Sprint 2
- [ ] Load cell akurasi ±5g → calibration_factor tersimpan
- [ ] HC-SR04 baca jarak akurat
- [ ] Semua limit switch dan tombol merespons
- [ ] Motor press naik/turun sesuai perintah + berhenti di limit switch
- [ ] Servo gate buka/tutup, arm lipat ke atas dengan benar
- [ ] NEMA17 gerak sesuai langkah (diverifikasi dengan penggaris)
- [ ] LCD tampilkan teks dengan benar
- [ ] Buzzer berbunyi, LED menyala

---

## SPRINT 3: FIRMWARE & INTEGRASI
### Target: State machine berjalan end-to-end, dashboard WiFi aktif
### Durasi: 5–7 hari

---

### 📋 TASK LIST SPRINT 3

#### S3-1: Tulis `config.h`
- [ ] Definisikan semua pin
- [ ] Definisikan semua konstanta default (target_weight, dll)
- [ ] Definisikan calibration_factor load cell (dari S2-2)
- [ ] Definisikan servo angles yang benar (dari S2-6)

#### S3-2: Implementasi Modul Dosing
- [ ] `dosing.h/.cpp`: fungsi `startDosing()`, `isDoseComplete()`, `getWeight()`
- [ ] Implementasi pre-close offset (cutoff gate lebih awal)
- [ ] Implementasi tare otomatis sebelum setiap dosing
- [ ] Test modul dosing secara isolated

#### S3-3: Implementasi Modul Folding
- [ ] `folding.h/.cpp`: fungsi `foldPlastic()`, `unfoldArms()`
- [ ] Kedua servo gerak bersamaan (timing sync)
- [ ] Smooth motion: gunakan loop increment angle (tidak langsung jump ke 110°)

#### S3-4: Implementasi Modul Pressing
- [ ] `pressing.h/.cpp`: fungsi `pressDown()`, `pressUp()`, `isAtBottom()`, `isAtTop()`
- [ ] Interrupt atau polling limit switch
- [ ] Timeout safety: jika 10 detik belum sampai limit → ERROR state

#### S3-5: Implementasi Modul Slider
- [ ] `slider.h/.cpp`: fungsi `moveToNextSlot()`, `homePosition()`
- [ ] Gunakan AccelStepper untuk gerakan smooth (ada accelerasi)
- [ ] HOMING: gerak kiri sampai endstop → set position = 0

#### S3-6: Implementasi State Machine Utama
- [ ] `mesin_tempe.ino`: enum states + switch-case state machine
- [ ] Implementasi semua transisi state (lihat diagram state machine di plan)
- [ ] Implementasi STOP button sebagai interrupt (bisa ditekan kapanpun)
- [ ] Test: jalankan state machine tanpa kedelai (dry run mekanik)

#### S3-7: Implementasi Web Dashboard
- [ ] Setup WiFi (mode AP atau STA — pilih STA jika ada WiFi rumah)
- [ ] Buat `data/index.html` simpan ke SPIFFS
  - Tampilkan: status mesin, slot ke-N, berat terakhir, batch counter
  - Tombol: START, STOP, RESET
  - Form: setting target berat
- [ ] Implementasi `GET /status` → return JSON
- [ ] Test: akses dari HP → dashboard tampil

#### S3-8: Test Integrasi Penuh (Dry Run)
- [ ] Jalankan 1 siklus penuh tanpa kedelai (plastik doang):
  - HOMING → IDLE → START → CEK_HOPPER → DOSING (skip) → FOLDING → PRESSING → GESER → ...
- [ ] Amati setiap transisi state di LCD + Serial Monitor
- [ ] Catat bug/masalah → fix

#### ✅ DEFINITION OF DONE — Sprint 3
- [ ] State machine berjalan 1 siklus penuh tanpa crash
- [ ] Semua 5 slot diproses, buzzer bunyi di akhir
- [ ] STOP button berfungsi kapanpun
- [ ] Dashboard WiFi tampil di HP, data real-time ter-update
- [ ] Setting target berat bisa diubah dari dashboard dan tersimpan

---

## SPRINT 4: SYSTEM TEST & KALIBRASI
### Target: Mesin bekerja dengan kedelai sungguhan, akurasi terpenuhi
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 4

#### S4-1: Kalibrasi Load Cell Final
- [ ] Tare dengan mold kosong
- [ ] Isi 200g kedelai manual, verifikasi baca sensor
- [ ] Fine-tune pre_close_offset → target error akhir < ±5g
- [ ] Uji 10x dosing → catat berat setiap slot:
  ```
  Slot 1: ___g, Slot 2: ___g, ..., Slot 10: ___g
  Rata-rata: ___g, Std deviasi: ___g
  ```

#### S4-2: Kalibrasi Servo Folding
- [ ] Test folding dengan plastik PE sesungguhnya (lembaran 6×30cm)
- [ ] Cek: plastik terlipat ke atas dengan sempurna, tidak robek
- [ ] Jika robek/terlalu kencang: kurangi fold_angle (misal 100°)
- [ ] Jika tidak menutup penuh: tambah fold_angle (misal 115°)

#### S4-3: Test Pressing dengan Kedelai
- [ ] Isi slot dengan kedelai terfolding
- [ ] Jalankan press: amati tekanan, waktu tahan
- [ ] Cek hasil: kedelai terpadatkan? Plastik tidak robek?
- [ ] Tuning press_hold_ms (default 1000ms, coba 1500ms jika kurang padat)

#### S4-4: Test Siklus Penuh 1 Papan
- [ ] Operator: pasang 5 plastik → START
- [ ] Amati: 5 slot selesai, buzzer bunyi
- [ ] Operator: balik ke ancak secara manual
- [ ] Evaluasi: tempe bentuknya sesuai? Padat? Plastik terbungkus rapi?

#### S4-5: Test Daya Tahan (5 Papan Berturut)
- [ ] Jalankan 5 papan berturut-turut tanpa henti
- [ ] Catat: ada panas berlebih? Ada slip belt? Ada servo lemah?
- [ ] Catat waktu per papan (target < 3 menit)

#### S4-6: Test WiFi Dashboard Saat Produksi
- [ ] Monitor dashboard dari HP saat mesin berjalan
- [ ] Cek: update real-time, tidak lag, tidak disconnect
- [ ] Test setting berat dari dashboard → perubahan langsung berlaku

#### ✅ DEFINITION OF DONE — Sprint 4
- [ ] Akurasi dosing: mean error < ±5g, tidak ada outlier >15g
- [ ] Folding: 100% plastik terlipat, 0% robek
- [ ] Pressing: semua slot terpadatkan dengan baik
- [ ] Cycle time per papan (5 slot): < 3 menit
- [ ] 5 papan berturut tanpa error mekanik atau firmware crash
- [ ] Dashboard WiFi stabil selama sesi produksi

---

## SPRINT 5: PRODUKSI & FINE-TUNING
### Target: Mesin siap digunakan rutin untuk produksi
### Durasi: Ongoing (minggu ke-6+)

---

### 📋 TASK LIST SPRINT 5

#### S5-1: Buat SOP Operator
- [ ] Tulis prosedur 1 halaman untuk operator:
  1. Nyalakan mesin → tunggu LCD "READY"
  2. Pastikan hopper terisi kedelai
  3. Pasang plastik ke 5 slot
  4. Tekan START
  5. Saat buzzer bunyi → ambil cetakan → balik ke ancak
  6. Letakkan ancak ke rak fermentasi
  7. Pasang plastik baru → ulangi
  8. Shutdown: tekan STOP → matikan PSU

#### S5-2: Pasang Label & Keamanan
- [ ] Label tombol: START (hijau), STOP (merah), RESET (kuning)
- [ ] Label LCD: penjelasan tampilan
- [ ] Emergency stop yang mudah dijangkau
- [ ] Cover pelindung untuk bagian bergerak (optional untuk V1)

#### S5-3: Produksi Pertama (Official)
- [ ] Jalankan produksi normal 1 hari
- [ ] Catat: jumlah papan, waktu total, masalah yang muncul
- [ ] Bandingkan dengan kapasitas manual sebelumnya

#### S5-4: Monitoring & Logging via Dashboard
- [ ] Aktifkan logging batch di ESP32 (simpan data ke EEPROM atau Serial)
- [ ] Monitor dari HP: trend berat per slot, alarm rate
- [ ] Identifikasi pola masalah (misalnya slot ke-3 selalu overshoot)

#### S5-5: Iterative Fine-tuning
- [ ] Tuning parameter berdasarkan data produksi
- [ ] Update firmware via OTA (Over-The-Air) jika perlu: gunakan `ArduinoOTA`
- [ ] Dokumentasikan parameter final yang optimal

#### S5-6: Rencana Upgrade V2 (Future)
- [ ] Evaluasi: apakah perlu auto-flip ke ancak?
- [ ] Evaluasi: apakah perlu plastik roll?
- [ ] Dokumentasi semua perbaikan untuk V2

#### ✅ DEFINITION OF DONE — Sprint 5 / PROJECT SELESAI
- [ ] Mesin digunakan operator secara mandiri (tanpa bantuan teknisi)
- [ ] Produksi berjalan ≥5 hari kerja tanpa insiden
- [ ] Kapasitas terpenuhi: ≥15 papan/jam
- [ ] Dokumentasi lengkap tersimpan di folder docs/

---

## RINGKASAN TIMELINE

```
MINGGU    SPRINT        MILESTONE
────────────────────────────────────────────────────────
  0       Sprint 0      Semua komponen diorder / dibeli
  1       Sprint 1      Frame berdiri, mold bisa slide manual
  2       Sprint 2      Semua komponen lulus unit test
  3       Sprint 3      Firmware berjalan dry run, WiFi aktif
  4       Sprint 4      Test produksi kedelai, kalibrasi OK
  5–6+    Sprint 5      Produksi rutin, mesin mandiri
```

---

## CHECKLIST MITIGASI RISIKO GLOBAL

| Risiko                          | Tanda Peringatan Dini        | Tindakan                           |
|---------------------------------|------------------------------|------------------------------------|
| Komponen datang cacat           | Unit test gagal              | Klaim garansi toko, order ulang    |
| Frame tidak siku                | Mold oblak di rel            | Grinding ulang sambungan di tukang las |
| Load cell drift                 | Berat tidak konsisten hari ke-2 | Re-tare, re-kalibrasi           |
| Servo overheat                  | Servo panas saat disentuh    | Turunkan duty cycle, tambah cooling time |
| WiFi tidak bisa connect         | Dashboard tidak muncul       | Switch ke AP mode (hotspot sendiri) |
| Belt slip                       | Mold geser kurang dari 7.6cm | Kencangkan belt tensioner           |

---

## REFERENSI FILE PROJECT

```
c:\Users\muhib\OneDrive\Dokumen\IOT Tempe\
├── docs/
│   ├── implementation_plan_final.md   ← BOM + PIN MAP + STATE MACHINE
│   ├── implementation_plan_v6.md      ← Versi sebelumnya (referensi)
│   ├── panduan_uji_hardware.md        ← Panduan unit test hardware
│   └── PROJECT_EXECUTION_PLAN.md     ← File ini
├── firmware/
│   └── tests/                         ← Firmware unit test sudah ada
│       ├── 02_hx711_loadcell_calibration/
│       ├── 03_hcsr04_ultrasonic/
│       ├── 04_buttons_and_limitswitches/
│       ├── 05_motor_l298n_leadscrew/
│       └── 06_buzzer_relay_gate/
└── assets/
    ├── slide_stages_corrected.jpg     ← Diagram lipat plastik
    └── servo_arm_return_mechanism.jpg ← Urutan arm return
```

---

*Dibuat: 13 September 2026*  
*Next action: Mulai Sprint 0 — buat shopping list dan order komponen*
