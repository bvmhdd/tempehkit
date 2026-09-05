# 🫘 Mesin Pencetak Tempe Otomatis — Implementation Plan FINAL v4

> Berdasarkan gambar & dimensi nyata cetakan dari pabrik

---

## 📸 Referensi Objek Nyata

![Cetakan tempe dan ancak bambu](C:\Users\muhib\.gemini\antigravity-ide\brain\79d9e287-90e4-49e3-aa23-e5342b96ecba\cetakan_tempe.jpeg)

**Analisis dari gambar:**
- **Bawah (Cetakan logam)**: Terbuat dari besi/aluminium, 5 slot bersekat, dasar terbuka — kantong plastik dimasukkan dari bawah kemudian diisi kedelai dari atas
- **Atas (Ancak/Alas anyaman bambu)**: Berfungsi sebagai alas saat cetakan dibalik — tempe duduk di atas anyaman bamboo untuk sirkulasi udara saat fermentasi

---

## 📐 Dimensi Nyata (Terukur)

```
CETAKAN TEMPE (besi/aluminium):
┌─────────────────────────────────────────────────────┐
│ Panjang total : 50.5 cm                             │
│ Lebar total   : 24.0 cm                             │
│                                                     │
│  ┌──────┐ 1cm ┌──────┐ 1cm ┌──────┐ 1cm ┌──────┐  │
│  │ Slot │     │ Slot │     │ Slot │     │ Slot │  │
│  │  1   │     │  2   │     │  3   │     │  4   │  │
│  │21.3cm│     │21.3cm│     │21.3cm│     │21.3cm│  │
│  │ 6.6cm│     │ 6.6cm│     │ 6.6cm│     │ 6.6cm│  │
│  └──────┘     └──────┘     └──────┘     └──────┘  │
│  (slot ke-5 ada di ujung kanan, total 5 slot)       │
└─────────────────────────────────────────────────────┘

Pitch per slot = 6.6 + 1.0 = 7.6 cm  ← jarak geser stepper

ANCAK / ALAS (anyaman bambu):
┌─────────────────────────────────────────────────────┐
│ Panjang : 50.5 cm  (sama dengan cetakan)            │
│ Lebar   : 7.0 cm   (sedikit lebih lebar dari slot)  │
└─────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Insight penting dari dimensi:**
> Lebar ancak (7.0 cm) ≈ lebar slot + sekat (6.6 + 0.4 cm). Artinya saat cetakan dibalik, tiap slot tempe tepat berdiri di atas satu ancak. Desain mekanik harus menjaga akurasi posisi ±2mm.

---

## 🔄 Alur Proses Lengkap (Berdasarkan Kondisi Nyata)

```
TAHAP MANUAL (sebelum mesin):
  Operator siapkan kantong plastik → masukkan ke tiap slot cetakan dari bawah

TAHAP OTOMATIS (mesin):
  ┌─────────────────────────────────────────────────────────┐
  │  Siklus 1: Slot 1 di bawah nozzle → DOSING → PRESS     │
  │  Geser otomatis 7.6cm → Slot 2                          │
  │  Siklus 2: Slot 2 di bawah nozzle → DOSING → PRESS     │
  │  Geser otomatis 7.6cm → Slot 3                          │
  │  ... (sampai slot 5)                                    │
  │  Siklus 5: Slot 5 selesai → BUZZER PANJANG              │
  └─────────────────────────────────────────────────────────┘

TAHAP MANUAL (sesudah mesin):
  Operator ambil cetakan → taruh ancak di atas → balik → 
  tempe kini duduk di atas ancak → susun ke rak fermentasi
```

---

## 🗂️ KATEGORI 1 — PENGAMBILAN DATA

### 1.1 Parameter Sensor Final

| Parameter | Sensor | Titik Ukur | Fungsi |
|---|---|---|---|
| Berat kedelai per slot | Load Cell 5kg + HX711 | Platform di bawah nozzle | Dosing presisi sesuai berat target |
| Level kedelai di hopper | HC-SR04 Ultrasonic | Di dalam hopper, arah bawah | Alarm saat kedelai hampir habis |
| Posisi press ATAS | Limit Switch #1 | Rel press vertikal, titik atas | Tanda press sudah naik penuh |
| Posisi press BAWAH | Limit Switch #2 | Rel press vertikal, titik bawah | Tanda press sudah menekan penuh |
| Posisi papan (homing) | End-stop Switch | Ujung kiri rel horizontal | Titik referensi (home position) |
| Counter slot & papan | Software | Di ESP32 | Tracking progress 1/5 s.d 5/5 |

### 1.2 Kalkulasi Mekanik dari Dimensi Nyata

```
PITCH GESER = Lebar slot + Jarak sekat = 6.6 + 1.0 = 7.6 cm

TOTAL JARAK GESER = Pitch × (5-1) slot = 7.6 × 4 = 30.4 cm

STEPPER MOTOR (NEMA 17, 200 step/rev):
  Gunakan timing belt GT2 (2mm pitch) + pulley 20T
  Pulley keliling = 20 × 2mm = 40mm = 4.0 cm/rev
  Step per cm = 200 / 4.0 = 50 steps/cm
  Step per 1 slot = 7.6 cm × 50 = 380 steps ← nilai di firmware

DIMENSI REL GESER:
  Panjang rel minimal = 50.5 + buffer 10cm = ~60 cm
  Lebar platform geser = 24 cm (sama dengan cetakan)

NOZZLE PRESS:
  Lebar nozzle = 6.0 cm (sedikit lebih kecil dari slot 6.6cm)
  Tinggi press stroke = tinggi cetakan + 2cm clearance
```

---

## 🗂️ KATEGORI 2 — PERANCANGAN SISTEM

### 2.1 Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    ESP32 DevKit V1                       │
│          WiFi Web Server + State Machine                 │
└────┬──────────┬───────────┬──────────────┬──────────────┘
     │          │           │              │
[SENSOR]   [MOTOR A]   [MOTOR B]       [UI LAYER]
─────────  ─────────   ─────────       ──────────
Load Cell  Motor DC    Stepper          LCD 16x2 I2C
HX711      Vertikal    NEMA 17          Tombol START
HC-SR04    (Press)     Horizontal       Tombol STOP
Limit Sw2  L298N drv   (Geser)          LED Hijau/Merah
End-stop   Relay 4ch   A4988 drv        Buzzer
     │
     └──────── WiFi ────► Dashboard HP (browser)
                          status slot, counter, berat
```

### 2.2 Desain Mekanik Rinci

```
TAMPAK SAMPING — Mekanisme Press Vertikal:

   [HOPPER KEDELAI]
         │
    [Nozzle/Gate]──── Servo/solenoid buka-tutup
         │
   ══════╪══════  ← Titik press (tetap, diam)
         │
   [PISTON PRESS] ──── Motor DC + rack gear / lead screw
         ↕ (naik-turun)
   [CETAKAN] ←──────── Ini yang bergerak horizontal
   ─────────────── ← Platform rel
      ↔ Geser kiri-kanan via Stepper + timing belt


TAMPAK ATAS — Rel Geser Cetakan:

  Home  S1    S2    S3    S4    S5   End
  │◄───────────── 30.4 cm ────────────►│
  ●     │7.6cm│7.6cm│7.6cm│7.6cm│     ●
  (end  [  ][  ][  ][  ][  ]         (end
  stop                               stop
  kiri)                              kanan)

  Cetakan berjalan dari kiri ke kanan,
  slot 1 mulai di titik nozzle (posisi home),
  setiap siklus selesai → geser 7.6cm ke kanan
```

### 2.3 Finite State Machine — Detail 5 Slot

```
                    ┌──────────┐
           BOOT     │          │
         ──────────►│  HOMING  │── Stepper gerak ke kiri sampai end-stop
                    │          │── Set posisi = slot 1
                    └────┬─────┘
                         │ Selesai homing
                         ▼
                    ┌──────────┐
                    │   IDLE   │── LCD: "READY - Tekan START"
                    │          │── LED Hijau kedip
                    └────┬─────┘
                         │ START ditekan
                         ▼
                    ┌──────────┐  level < 5cm
                    │ CEK_HOPP │──────────────► [ALARM_HOPPER]
                    │   -ER    │               Buzzer panjang 3x
                    └────┬─────┘               LCD: "HOPPER KOSONG!"
                         │ level OK            LED Merah nyala
                         ▼
                    ┌──────────┐
                    │  DOSING  │── Buka gate/nozzle
                    │          │── Baca HX711 terus-menerus
                    │          │── Tutup gate saat berat = target ±5g
                    └────┬─────┘── LCD: "Isi: XXXg / YYYg"
                         │ Berat tercapai
                         ▼
                    ┌──────────┐
                    │ PRESSING │── Motor press turun
                    │          │── Tunggu limit switch bawah
                    └────┬─────┘── Tahan 3 detik → Motor naik
                         │ Limit switch atas aktif
                         ▼
                    ┌──────────┐
                    │  slot_count < 5?  │
                    └────┬──────────────┘
                         │ YES              NO
                         ▼                  ▼
                    ┌──────────┐      ┌──────────────┐
                    │  GESER   │      │  PAPAN_PENUH │
                    │          │      │  Buzzer 5x   │
                    │ +380step │      │  LCD: "BALIK!│
                    └────┬─────┘      │  Tekan START"│
                         │            └──────┬───────┘
                    kembali ke               │ START ditekan
                    CEK_HOPPER          kembali ke HOMING
```

### 2.4 Pin Mapping ESP32 Lengkap

```
╔══════════════════════════════════════════════════════════╗
║  GPIO  │ Fungsi                  │ Komponen              ║
╠════════╪═════════════════════════╪═══════════════════════╣
║   4    │ HX711 DOUT              │ Load Cell data        ║
║   5    │ HX711 SCK               │ Load Cell clock       ║
║  18    │ HC-SR04 TRIG            │ Ultrasonic hopper     ║
║  19    │ HC-SR04 ECHO            │ Ultrasonic hopper     ║
║  21    │ SDA                     │ LCD 16x2 I2C          ║
║  22    │ SCL                     │ LCD 16x2 I2C          ║
║  25    │ Motor Press IN1         │ L298N channel A       ║
║  26    │ Motor Press IN2         │ L298N channel A       ║
║  27    │ Gate/Nozzle relay       │ Relay module ch1      ║
║  14    │ Stepper DIR             │ A4988 driver          ║
║  12    │ Stepper STEP            │ A4988 driver          ║
║  13    │ Stepper ENABLE          │ A4988 driver          ║
║  32    │ Limit Switch ATAS       │ Press, active LOW     ║
║  33    │ Limit Switch BAWAH      │ Press, active LOW     ║
║  34    │ End-stop Kiri (HOME)    │ Rel, active LOW       ║
║  35    │ End-stop Kanan          │ Rel, active LOW       ║
║  36    │ Tombol START            │ Push button           ║
║  39    │ Tombol STOP             │ Push button           ║
║   2    │ LED Built-in / Hijau    │ Status OK             ║
║  15    │ LED Merah               │ Status ALARM          ║
║  23    │ Buzzer                  │ Aktif buzzer 5V       ║
╚════════╧═════════════════════════╧═══════════════════════╝

Power Supply:
  PSU 12V 5A → L298N (motor press) + Stepper (via A4988)
  LM2596 step-down → 5V untuk ESP32, LCD, relay, sensor
  ESP32 3.3V pin → HX711, HC-SR04, limit switches
```

---

## 🗂️ KATEGORI 3 — PEMBUATAN SISTEM

### 3.1 Struktur File Terintegrasi

```
📁 IOT_Tempe/
│
├── 📄 firmware/
│   └── mesin_tempe/
│       ├── mesin_tempe.ino          ← FIRMWARE UTAMA (1 file)
│       └── data/
│           └── index.html           ← Dashboard (upload SPIFFS)
│
├── 📄 docs/
│   ├── wiring_diagram.md            ← Diagram wiring lengkap
│   ├── BOM_belanja.md               ← Link beli Tokopedia/Shopee
│   └── panduan_operator.md          ← SOP kakak (simpel + foto)
│
└── 📄 hardware/
    └── dimensi_mekanik.md           ← Drawing untuk tukang las (MODULAR V1→V3)
```

> 📄 **Dokumen mekanik sudah dibuat:** [dimensi_mekanik.md](file:///C:/Users/muhib/.gemini/antigravity-ide/brain/79d9e287-90e4-49e3-aa23-e5342b96ecba/dimensi_mekanik.md)
> Berisi spesifikasi lengkap frame modular dengan titik upgrade V2 (auto-slide) dan V3 (auto-balik) yang sudah di-pre-weld dari awal.

### Roadmap Upgrade Mekanik

| Fase | Apa yang Ditambah | Biaya Tambahan | Las Ulang? |
|---|---|---|---|
| **V1 (sekarang)** | Frame + press + rel manual | ~Rp 630.000 | — |
| **V2 (nanti)** | Pasang stepper + belt ke bracket yang sudah ada | +Rp 200.000 | ❌ Tidak perlu |
| **V3 (masa depan)** | Pasang motor flip ke pivot yang sudah ada | +Rp 380.000 | ❌ Tidak perlu |

### 3.2 Isi Firmware `mesin_tempe.ino` (Struktur)

```cpp
/*==========================================================
  MESIN PENCETAK TEMPE OTOMATIS v1.0
  Kapasitas: 5 slot / papan | Cetakan: 50.5×24cm
  Slot: 21.3×6.6cm | Pitch: 7.6cm | Steps/slot: 380
  Hardware: ESP32 + NEMA17 + L298N + HX711 + HC-SR04
  By: [Nama Kamu] | IOT Pabrik Tempe [Nama Pabrik]
==========================================================*/

// ── SECTION 1: Library & Konfigurasi WiFi/Web ──────────
// ── SECTION 2: Pin Mapping & Konstanta Mekanik ─────────
//    #define STEPS_PER_SLOT  380
//    #define SLOT_COUNT      5
//    #define BERAT_TARGET    500  // gram, adjustable
//    #define WAKTU_PRESS     3000 // ms
// ── SECTION 3: Variabel State Machine ──────────────────
//    enum State { HOMING, IDLE, CEK_HOPPER, DOSING,
//                 PRESSING, GESER, PAPAN_PENUH, ALARM }
// ── SECTION 4: Fungsi Sensor ───────────────────────────
//    float bacaBerat()      // HX711
//    float bacaHopper()     // HC-SR04 cm
//    bool limitAtas()       // digitalRead
//    bool limitBawah()      // digitalRead
// ── SECTION 5: Fungsi Aktuator ─────────────────────────
//    void pressDown()       // motor turun
//    void pressUp()         // motor naik
//    void geserSlot()       // stepper 380 steps
//    void homing()          // stepper ke end-stop kiri
//    void bukaGate()        // relay ON
//    void tutupGate()       // relay OFF
// ── SECTION 6: FSM Handler ─────────────────────────────
//    void runFSM()          // dipanggil di loop()
// ── SECTION 7: Web Server & API ────────────────────────
//    GET  /            → index.html dari SPIFFS
//    GET  /api/status  → JSON semua data real-time
//    POST /api/control → {"cmd":"START"/"STOP"/"RESET"}
//    GET  /api/config  → baca parameter
//    POST /api/config  → set BERAT_TARGET, WAKTU_PRESS, dll
// ── SECTION 8: Setup & Loop ────────────────────────────
```

### 3.3 Dashboard Web — Fitur

```
┌──────────────────────────────────────────┐
│  🫘 MESIN TEMPE — Dashboard              │
├──────────────────────────────────────────┤
│  Status: ██ DOSING                       │
│                                          │
│  Slot aktif: ●●●○○  (3 / 5)            │
│  Papan selesai: 12                       │
│  Total tempe hari ini: 60                │
│                                          │
│  Berat saat ini: ████░░░ 342g / 500g    │
│  Level hopper:   ██████░ 15cm           │
│                                          │
│  [▶ START]  [⏹ STOP]  [⟳ RESET]        │
│                                          │
│  ⚙ Konfigurasi                          │
│  Berat target: [500] g                  │
│  Waktu press:  [3]   detik              │
│  [Simpan]                               │
└──────────────────────────────────────────┘
Mobile-friendly, auto-refresh setiap 1 detik
```

### 3.4 BOM Final — Opsi B (Termasuk Geser Otomatis)

| No | Komponen | Spesifikasi | Estimasi Harga |
|---|---|---|---|
| 1 | ESP32 DevKit V1 | 38-pin | Rp 55.000 |
| 2 | Load Cell 5kg + HX711 | Set lengkap | Rp 35.000 |
| 3 | Ultrasonic HC-SR04 | — | Rp 15.000 |
| 4 | Limit Switch | x4 (2 press + 2 end-stop) | Rp 20.000 |
| 5 | Motor DC 12V + Gearbox | Torsi ≥ 10kg.cm untuk press | Rp 95.000 |
| 6 | Stepper Motor NEMA 17 | 1.8°/step, 200step/rev | Rp 55.000 |
| 7 | Driver L298N | Motor DC press | Rp 20.000 |
| 8 | Driver A4988 | Stepper NEMA 17 | Rp 20.000 |
| 9 | Relay Module 4ch | Gate nozzle | Rp 25.000 |
| 10 | LCD 16x2 + I2C | Display lokal | Rp 30.000 |
| 11 | Buzzer + LED + Tombol | x2 tombol, x2 LED | Rp 20.000 |
| 12 | Timing Belt GT2 + Pulley 20T | Transmisi geser | Rp 35.000 |
| 13 | Linear Rail / Rel aluminium 60cm | Jalur geser cetakan | Rp 100.000 |
| 14 | Power Supply 12V 5A | — | Rp 80.000 |
| 15 | Step-down LM2596 ke 5V | — | Rp 15.000 |
| 16 | Kabel, protoboard, konektor | — | Rp 75.000 |
| | **Total Elektronik** | | **~Rp 700.000** |
| | **Frame besi + mold press (tukang las)** | Rel, frame, piston, platform | Rp 350.000 – 500.000 |
| | **TOTAL KESELURUHAN** | | **Rp 1.050.000 – 1.200.000** ✅ |

### 3.5 Dimensi untuk Tukang Las (Drawing Spec)

```
FRAME UTAMA:
  Tinggi total       : ~80 cm (ergonomis berdiri)
  Lebar frame        : 60 cm (lebih lebar dari cetakan 50.5cm)
  Kedalaman frame    : 35 cm

REL GESER HORIZONTAL:
  Panjang rel        : 60 cm
  Lebar platform     : 25 cm (lebih dari lebar cetakan 24cm)
  Material           : Besi siku 3cm × 3cm

MEKANISME PRESS VERTIKAL:
  Stroke press       : 15 cm (cukup masuk ke slot cetakan)
  Piston / plat press: 6.0 cm × 21.0 cm (masuk ke satu slot)
  Lead screw / rack  : Panjang 20 cm
  Material piston    : Plat besi 5mm

HOPPER:
  Volume hopper      : ~10 Liter (kapasitas kedelai)
  Nozzle outlet      : Diameter 4-5 cm dengan gate (buka-tutup)
  Posisi nozzle      : Tepat di atas titik press
```

### 3.6 Timeline 6 Minggu

```
MINGGU 1 — Persiapan & Order
  ├── Order semua komponen elektronik (Tokopedia/Shopee)
  ├── Buat drawing spek untuk tukang las (dari docs di atas)
  └── Koordinasi dengan tukang las, estimasi biaya & waktu

MINGGU 2 — Mekanik Selesai & Uji Sensor
  ├── Frame dari tukang las selesai
  ├── Wiring semua sensor ke ESP32 (breadboard dulu)
  ├── Uji HX711: kalibrasi dengan timbangan referensi
  └── Uji HC-SR04: uji deteksi level hopper

MINGGU 3 — Firmware Dasar
  ├── Coding FSM skeleton (semua state)
  ├── Implementasi homing stepper
  ├── Uji geser 1 slot = 380 steps (verifikasi presisi)
  └── Uji motor press + limit switch

MINGGU 4 — Firmware Lengkap + Dashboard
  ├── Integrasi dosing (HX711 + gate relay)
  ├── Siklus penuh 1 slot (dosing → press → geser)
  ├── Coding Web Server + API
  └── Coding index.html dashboard

MINGGU 5 — Trial Produksi
  ├── Dry-run 5 slot tanpa kedelai (cek presisi geser)
  ├── Trial dengan kedelai nyata (1 papan = 5 tempe)
  ├── Kalibrasi berat target per slot
  └── Fine-tuning timing press & kecepatan dosing

MINGGU 6 — Deployment & Training
  ├── Instalasi permanen di pabrik
  ├── Training kakak: cara pakai + troubleshoot
  ├── Cetak & tempel panduan operator di mesin
  └── Monitoring 1 minggu pertama + penyesuaian
```

---

## ✅ Verification Plan

| Test | Metode | Kriteria Lulus |
|---|---|---|
| Akurasi dosing | Timbang 10 slot, bandingkan ke timbangan dapur | Error < ±5 gram |
| Presisi geser stepper | Ukur posisi slot dengan penggaris setelah homing | Offset < ±2 mm |
| Cycle time | Stopwatch 1 papan penuh (5 slot) | Target < 5 menit/papan |
| Throughput | Hitung papan/jam selama 1 jam produksi | ≥ 12 papan/jam (60 tempe) |
| Alarm hopper | Kosongkan hopper sampai batas → cek buzzer | Bunyi + LCD muncul |
| Dashboard | Akses dari HP kakak via WiFi | Semua data update, kontrol berfungsi |

---

## 📌 Siap Eksekusi — File yang Akan Dibuat

Setelah plan ini disetujui:

| File | Isi |
|---|---|
| `mesin_tempe.ino` | Firmware ESP32 lengkap, siap upload |
| `data/index.html` | Dashboard web cantik, upload ke SPIFFS |
| `docs/wiring_diagram.md` | Diagram wiring + foto referensi |
| `docs/BOM_belanja.md` | Link produk Tokopedia/Shopee per item |
| `hardware/dimensi_mekanik.md` | Drawing spec untuk tukang las |
| `docs/panduan_operator.md` | SOP bergambar untuk kakak |
