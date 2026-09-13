# Mesin Pencetak Tempe Semi-Otomatis — Tier 2 ESP32 WiFi
## Implementation Plan FINAL v8 — 5 SLOT SERENTAK
### Semua slot diproses bersamaan, tanpa mekanisme geser

> **Tanggal**: 13 September 2026  
> **Status**: FINAL v8 — Revisi arsitektur: 5 slot sekaligus  
> **Tier**: 2 — ESP32 WiFi + Local Web Dashboard  
> **Perubahan dari v7**: Hilangkan sliding mechanism → tambah long hopper + dual fold bar + wide press plate

---

## 1. RINGKASAN SISTEM

Mesin semi-otomatis untuk mencetak tempe. Seluruh 5 slot diproses **secara bersamaan** dalam 1 siklus.

**Alur kerja**:
1. Operator pasang 5 plastik ke 5 slot sekaligus
2. Tekan START
3. Hopper dosi semua 5 slot sekaligus
4. Fold bar lipat semua 5 plastik sekaligus
5. Press plate tekan semua 5 slot sekaligus
6. Buzzer bunyi → operator angkat cetakan → balik ke ancak

**Kapasitas target**: ~1 menit/papan (5 slot) → ±60 papan/jam  
*(jauh lebih cepat dari sequential 3 menit/papan!)*

---

## 📸 MULTI-ANGLE CAD DESIGN (TIER 2 — 5 SLOT SERENTAK)

| 1. Isometric 3D View | 2. Front Elevation View |
| :---: | :---: |
| ![Isometric View](../assets/tier2_isometric_view.jpg) | ![Front View](../assets/tier2_front_view.jpg) |
| *Perspektif 3D mesin lengkap dengan hopper 5 nozzle & controller box* | *Tampak depan: 5 slot serentak (50.5cm), lead screw, dan fold bar* |

| 3. Side View (Folding & Press Mechanism) | 4. Top Plan View (Mold & Rails) |
| :---: | :---: |
| ![Side Folding View](../assets/tier2_side_folding.jpg) | ![Top View](../assets/tier2_top_view.jpg) |
| *Detail mekanisme lintasan lipat plastik dan stroke penekanan vertikal* | *Tampak atas: dimensi 5 slot (21.3x6.6cm), bar lipat 52cm, dan gate hopper* |

---

## 2. PERBANDINGAN ARSITEKTUR

```
v7 (Sequential per-slot):           v8 (Simultan 5 slot):
──────────────────────────────       ──────────────────────────────
Mold geser kanan tiap slot           Mold DIAM (tidak bergerak)
1 nozzle hopper kecil                1 hopper panjang 5 lubang
2 servo arm kecil per slot           2 fold bar panjang 50cm
1 press plate kecil per slot         1 press plate panjang 50cm
NEMA17 + belt + rail                 TIDAK ADA (dihilangkan)
Siklus ~3 menit/papan                Siklus ~45-60 detik/papan
```

### Komponen yang DIHILANGKAN (hemat Rp 319.000):
- ~~NEMA17 Stepper (Rp 80K)~~
- ~~Driver A4988 (Rp 18K)~~
- ~~GT2 Belt + Pulley (Rp 35K)~~
- ~~Linear Rail MGR12 × 2 (Rp 170K)~~
- ~~Idler Pulley (Rp 16K)~~

---

## 3. GEOMETRI CETAKAN (orientasi penting!)

```
TAMPAK ATAS CETAKAN (50.5 × 24cm):

← 50.5cm →
┌──────────────────────────────────────────────────────────┐
│6.75cm│S1 6.6│1│S2 6.6│1│S3 6.6│1│S4 6.6│1│S5 6.6│6.75cm│ 24cm
│      │21.3cm│ │21.3cm│ │21.3cm│ │21.3cm│ │21.3cm│      │
└──────────────────────────────────────────────────────────┘
         ↑ slot panjangnya ke arah 24cm (depan-belakang)
         ↑ kelebihan plastik 4-5cm ada di sisi DEPAN dan BELAKANG tiap slot

POSISI FOLD BAR:
  Bar DEPAN: memanjang sepanjang 50.5cm, di sisi depan mold (y = 0)
  Bar BELAKANG: memanjang sepanjang 50.5cm, di sisi belakang mold (y = 24cm)
  → Kedua bar angkat semua 5 kelebihan plastik depan dan belakang sekaligus
```

---

## 4. MEKANISME PROVEN — REFERENSI & BEST PRACTICE

### 4.1 Dosing: Hopper Panjang 5 Nozzle + 1 Load Cell Total

**Proven di**: Mesin packaging biji-bijian multi-lane (grain bagging multi-head), feed dispenser ternak multi-slot.

```
HOPPER SS304 PANJANG (tampak depan):
┌────────────────────────────────────────────────────────┐
│                  Hopper SS304                           │
│               Lebar 50.5cm (full mold)                  │
│  ╲_________________________________________/            │
│     ○       ○       ○       ○       ○                  │  ← 5 lubang nozzle
│    N1      N2      N3      N4      N5                   │
│    |        |       |       |       |                   │
└────────────────────────────────────────────────────────┘
     ▼       ▼       ▼       ▼       ▼
  [S1]    [S2]    [S3]    [S4]    [S5]   ← 5 slot mold

Gate: 1 servo MG996R membuka/menutup seluruh 5 lubang sekaligus
      via 1 plat gate sliding horizontal (digeser servo 1x)

Load Cell: 1 buah di bawah SELURUH MOLD
           Baca total berat → target = 5 × target_per_slot
           Contoh: target 200g/slot → gate tutup saat total ≥ 990g (offset 10g)
```

**Desain Gate Hopper**:
- 1 plat aluminium sliding (panjang 52cm, lebar 4cm) menutupi semua 5 lubang sekaligus
- Digerakkan oleh 1 servo MG996R dengan pushrod/linkage ke gate sliding
- Alternatif lebih sederhana: gate "engsel" → 1 servo angkat flap plat dari bawah nozzle
- Nozzle Ø35mm per slot → volume flow dapat diatur dengan ukuran lubang

**Kelemahan yang harus diantisipasi**:
- Distribusi tidak 100% merata antar slot (bisa beda ±10–15g antar slot)
- Mitigasi: kalibrasi ukuran lubang nozzle (yang di tengah mungkin perlu lebih kecil)
- Bisa diterima untuk produksi tempe (tidak butuh presisi farmasi)

### 4.2 Folding Plastik: Dual Fold Bar (Long Bar Mechanism)

**Proven di**: Mesin box folder industri (carton folding machine), pizza box folding, flat-pack packaging folder — semua menggunakan long bar hinge mechanism.

```
MEKANISME FOLD BAR (tampak sisi pendek = 24cm):

POSISI REST (bar rebah ke luar):    POSISI FOLD (bar tegak ke atas):

         Slot                              ╔════╗
         ╔══════════╗                      ║    ║ ← kelebihan plastik
         ║  kedelai ║                      ║    ║   terdorong ke atas
         ╚══════════╝                   ╔══╝    ║
  ───────╗                             ──║ slot ║──
  [BAR]──╝                              ╚═══════╝
  servo=0° (bar horizontal)           [BAR] servo=90° (bar vertikal)

IMPLEMENTASI:
- Fold bar DEPAN: aluminium bar (Ø20mm / 20×20mm profil) panjang 50–52cm
  Dipasang horizontal di DEPAN mold, engsel di dasar (pivot point)
  Diangkat oleh: 2x servo MG996R (kiri dan kanan bar) via lengan 8cm
  → gerakan angkat dari 0° ke 90° (bar dari rebah ke tegak)

- Fold bar BELAKANG: identik, sisi belakang mold
  Juga digerakkan 2x servo MG996R

Total servo untuk folding: 4x MG996R
```

**Mengapa 2 servo per bar (bukan 1 servo center)?**
- Bar panjang 50cm yang diangkat dari 1 titik tengah → ujung-ujung bar lentur (flex)
- 2 servo di ujung kiri dan kanan bar → bar terangkat rata tanpa flex
- Proven: mesin industri folder selalu drive dari 2 sisi untuk bar panjang

**Alternatif lebih murah (jika 4 servo terlalu mahal)**:
- 1 motor DC 12V dengan crank + 2 pushrod (proven di mesin carton folder sederhana)
- Crank memutar 0° → 90° → motor berhenti (limit switch)
- Biaya: motor DC Rp 65K vs 2 servo Rp 70K → hampir sama, tapi motor lebih torsi

### 4.3 Press: Wide Press Plate (Full 5-Slot Coverage)

**Proven di**: Mesin press tofu/tahu (paling mirip secara fungsi), buku/kertas press, flat panel laminator.

```
PRESS PLATE DESIGN (tampak depan):

  ← 50.5cm →
  ┌──────────────────────────────────────────────────────┐
  │             Press Plate Aluminium 6061                │ ← satu plat panjang
  │  [pad1] [pad2] [pad3] [pad4] [pad5]                  │   dengan 5 pad menonjol
  └──────────────────────────────────────────────────────┘
       ↓       ↓       ↓       ↓       ↓
    [S1]    [S2]    [S3]    [S4]    [S5]

OPSI 1 (RECOMMENDED): Plat datar panjang 48cm × 5cm
  - Satu plat aluminium rata yang menekan SELURUH permukaan mold atas
  - Simpel, mudah dibuat, merata
  - Pastikan plat cukup kaku (min 5mm tebal) agar tidak melengkung saat tekan

OPSI 2: 5 pad terpisah pada 1 gantry bar
  - 5 pad aluminium 6cm × 5cm dipasang ke 1 bar horizontal
  - Lebih mahal tapi menghindari tekanan ke dinding antar slot

MEKANISME TURUN:
  - 2x Lead Screw T8 (kiri dan kanan press plate) untuk tekanan merata
  - 1 Motor DC Gearbox 12V (torsi besar) putar 1 shaft → 2 lead screw via chain/belt
  - ATAU: 2 motor DC gearbox, sync via firmware (lebih simpel kawat, sedikit beda waktu)
  - RECOMMENDED: 1 motor → 1 shaft → 2 lead screw via coupler (mekanis sync, tidak drift)
```

### 4.4 ESP32 WiFi Local Dashboard (tidak berubah dari v7)

Library: `ESPAsyncWebServer` + `ArduinoJson`. Dashboard HTML real-time, no cloud.

---

## 5. DESAIN MEKANIK FRAME FINAL

```
TAMPAK DEPAN (80cm lebar × 130cm tinggi):

┌─────────────────────────────────────────────────────────┐
│             [HOPPER SS304 PANJANG 50.5cm]               │ h=130cm
│             /─────────────────────────────\             │
│            / ○  ○  ○  ○  ○  servo-gate    \            │
├─────────────────────────────────────────────────────────┤ h=100cm
│  [L-SCREW]  [PRESS PLATE PANJANG 50cm]  [R-SCREW]      │
│      │              ↕                       │            │ h=85cm
│    [MOTOR DC GEARBOX + SHAFT COUPLER]                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [BAR BELAKANG]  [MOLD 5-SLOT DIAM]  [BAR DEPAN]       │ h=60cm
│     servo↑       ═════════════════     servo↑           │
│                  cetakan 50.5×24cm                      │
│                  [1 LOAD CELL BAWAH]                    │
├─────────────────────────────────────────────────────────┤ h=30cm
│           [FRAME BESI HOLLOW 40×40mm]                   │
│           [PANEL KONTROL - KANAN]                       │
└─────────────────────────────────────────────────────────┘

Lebar frame: 80cm | Tinggi: 130cm | Depth: 40cm
```

```
TAMPAK SAMPING (40cm depth):

              [HOPPER]
              ╲_____/
               |   |   ← nozzle gate (servo)
               |   |
         ──────────────── h=85cm  ← cross bar
         [PRESS PLATE] ↕ (naik/turun)
         ──────────────── h=65cm
    ↗[FOLD BAR DEPAN]  [MOLD]  [FOLD BAR BELAKANG]↖
         ──────────────── h=55cm  ← dudukan mold
         [LOAD CELL]
         ──────────────── h=30cm
```

---

## 6. BILL OF MATERIALS v8 (REVISI)

### 6.1 Elektronik

| No | Komponen                | Spesifikasi                       | Qty | Harga  | Total      |
|----|-------------------------|-----------------------------------|-----|--------|------------|
| 1  | ESP32 DevKit V1         | 38-pin, WiFi built-in             | 1   | 65K    | Rp 65.000  |
| 2  | Load Cell 20kg + HX711  | 20kg (total 5 slot × ≤300g/slot = 1.5kg, pakai 20kg untuk presisi) | 1 | 35K | Rp 35.000 |
| 3  | Servo MG996R            | Metal gear, 9.4kg.cm, 180°        | **5** | 35K  | **Rp 175.000** |
|    | *(1 gate + 2 bar depan + 2 bar belakang)* | | | | |
| 4  | Motor DC Gearbox 12V    | RPM 60, torsi ≥50kg.cm (lebih berat = 5 slot) | 1 | 75K | Rp 75.000 |
| 5  | ~~NEMA17 Stepper~~      | **DIHILANGKAN**                   | 0   | -      | -          |
| 6  | Driver L298N            | Dual H-bridge 2A/ch               | 1   | 22K    | Rp 22.000  |
| 7  | ~~Driver A4988~~        | **DIHILANGKAN**                   | 0   | -      | -          |
| 8  | HC-SR04 Ultrasonic      | Level sensor hopper               | 1   | 10K    | Rp 10.000  |
| 9  | LCD 16×2 I2C            | HD44780 + PCF8574                 | 1   | 18K    | Rp 18.000  |
| 10 | Limit Switch (micro)    | NC/NO, 5A                         | **4** | 5K   | Rp 20.000  |
| 11 | Buzzer aktif 5V         | 95dB                              | 1   | 5K     | Rp 5.000   |
| 12 | Push Button 16mm        | START / STOP / RESET              | 3   | 8K     | Rp 24.000  |
| 13 | PSU 12V 10A             | Switching, 120W                   | 1   | 90K    | Rp 90.000  |
| 14 | Buck Converter LM2596   | 12V→5V, 3A                        | 1   | 12K    | Rp 12.000  |
| 15 | Kabel + terminal        | Berbagai ukuran                   | -   | 30K    | Rp 30.000  |
| 16 | Kotak panel ABS         | 200×150×100mm                     | 1   | 25K    | Rp 25.000  |
| 17 | LED 5mm (R/G/Y)         | Indikator                         | 3   | 1K     | Rp 3.000   |
| **TOTAL ELEKTRONIK v8** | | | | | **Rp 609.000** |

### 6.2 Mekanik & Struktural

| No | Komponen                | Spesifikasi                       | Qty | Harga  | Total      |
|----|-------------------------|-----------------------------------|-----|--------|------------|
| 1  | Besi Hollow 40×40mm     | Tebal 2mm, total ~8m              | -   | -      | Rp 600.000 |
| 2  | ~~Linear Rail MGR12~~   | **DIHILANGKAN**                   | 0   | -      | -          |
| 3  | Lead Screw T8 + Nut     | 300mm, pitch 2mm                  | **2** | 45K  | **Rp 90.000** |
| 4  | Shaft coupler + pulley  | Coupler motor ke 2 lead screw    | 1   | 35K    | Rp 35.000  |
| 5  | ~~GT2 Belt + Pulley~~   | **DIHILANGKAN**                   | 0   | -      | -          |
| 6  | Bearing 608ZZ           | Lead screw support (4) + fold bar pivot (4) | 8 | 5K | Rp 40.000 |
| 7  | Aluminium profile 20×20mm | Fold bar × 2 batang × 55cm    | 2   | 25K    | Rp 50.000  |
| 8  | Aluminium plate 5mm     | Press plate 50cm × 5cm           | 1   | 120K   | Rp 120.000 |
| 9  | Aluminium plate 3mm     | Gate hopper + arm bracket         | 1   | 60K    | Rp 60.000  |
| 10 | Hopper SS304 (custom)   | Panjang 50.5cm, lebar 20cm, 5 lubang Ø35mm | 1 | 250K | Rp 250.000 |
| 11 | Stainless rod/pivot     | As pivot fold bar kiri+kanan (Ø8mm × 55cm) | 2 | 20K | Rp 40.000 |
| 12 | Baut + mur set          | M5, M3, berbagai ukuran           | -   | 45K    | Rp 45.000  |
| 13 | Kaki karet M10          | Anti-slip                         | 4   | 8K     | Rp 32.000  |
| 14 | Cat epoxy food-grade    | Primer + topcoat                  | 1   | 45K    | Rp 45.000  |
| 15 | Ongkos las + fabrikasi  | Frame + bracket + pivot           | -   | -      | Rp 400.000 |
| **TOTAL MEKANIK v8** | | | | | **Rp 1.807.000** |

### 6.3 Total Biaya v8

| Kategori              | v7 (sequential) | v8 (simultan) | Selisih |
|-----------------------|-----------------|---------------|---------|
| Elektronik            | Rp 625.000      | Rp 609.000    | -16K    |
| Mekanik + Fabrikasi   | Rp 1.603.000    | Rp 1.807.000  | +204K   |
| Buffer 10%            | Rp 223.000      | Rp 242.000    | +19K    |
| **GRAND TOTAL**       | **Rp 2.451.000** | **Rp 2.658.000** | **+207K** |

> Sedikit lebih mahal (~Rp 207K) tapi **lebih cepat 3× lipat** (60 detik vs 3 menit per papan).  
> Nilai lebih: desain lebih simpel (tidak ada sliding mechanism), lebih reliable, lebih mudah dirawat.

---

## 7. PIN MAPPING ESP32 (REVISI v8)

```
GPIO │ Komponen                    │ Keterangan
─────┼──────────────────────────────┼──────────────────────────────────
  4  │ HX711 DOUT                  │ Load cell data
  5  │ HX711 SCK                   │ Load cell clock
 18  │ HC-SR04 TRIG                │ Ultrasonic trigger (level hopper)
 19  │ HC-SR04 ECHO                │ Ultrasonic echo
 21  │ I2C SDA (LCD)               │ LCD 16×2 data
 22  │ I2C SCL (LCD)               │ LCD 16×2 clock
 25  │ L298N IN1 (press)           │ Motor press TURUN
 26  │ L298N IN2 (press)           │ Motor press NAIK
 27  │ Servo GATE hopper           │ PWM gate dosing (buka/tutup)
 33  │ Servo FOLD BAR DEPAN KIRI   │ PWM fold bar depan kiri
 32  │ Servo FOLD BAR DEPAN KANAN  │ PWM fold bar depan kanan
 14  │ Servo FOLD BAR BELAKANG KIRI│ PWM fold bar belakang kiri
 12  │ Servo FOLD BAR BELAKANG KANAN│ PWM fold bar belakang kanan
 35  │ Limit SW PRESS BAWAH        │ INPUT_PULLUP eksternal 10kΩ
 34  │ Limit SW PRESS ATAS         │ INPUT_PULLUP eksternal 10kΩ
  0  │ Tombol START                │ INPUT_PULLUP, LOW=pressed
 15  │ Tombol STOP/PAUSE           │ INPUT_PULLUP, LOW=pressed
 16  │ Tombol RESET                │ INPUT_PULLUP, LOW=pressed
  2  │ LED onboard (biru)          │ Heartbeat
 23  │ Buzzer aktif                │ HIGH=bunyi

CATATAN:
- GPIO 34, 35 = INPUT ONLY → pullup eksternal 10kΩ ke 3.3V WAJIB
- Semua 4 servo fold bar: sync PWM output, gerak bersamaan
- Load cell mengukur TOTAL berat (target = 5 × berat_per_slot)
```

---

## 8. STATE MACHINE (REVISI v8 — jauh lebih simpel!)

```
[POWER ON] → HOMING (press plate ke atas) → IDLE

IDLE:
  LCD: "PASANG 5 PLASTIK, TEKAN START"
  Operator pasang 5 plastik ke 5 slot
  Tekan START
  ↓
CEK_HOPPER:
  HC-SR04 ukur level kedelai
  JIKA kosong → ALARM_HOPPER
  ↓
DOSING (semua 5 slot sekaligus):
  Tare load cell (berat mold + plastik = 0 referensi)
  Gate servo buka → kedelai mengalir ke semua 5 slot bersamaan
  HX711 baca berat TOTAL setiap 50ms
  Target total = 5 × target_per_slot (default: 5 × 200g = 1000g)
  Saat total ≥ (target - offset) → gate tutup
  Tunggu 500ms settling → validasi total berat
  ↓
FOLDING (semua 5 slot sekaligus):
  4 servo fold bar gerak 0° → 90° bersamaan (500ms)
  Tunggu 300ms (stabilize)
  ↓
PRESSING (semua 5 slot sekaligus):
  Motor press TURUN (L298N forward) sampai limit SW bawah
  Tahan 1500ms (lebih lama karena 5 slot)
  4 servo fold bar kembali 90° → 0° (arm keluar, 500ms)
  Tunggu 200ms (arm clear)
  Motor press NAIK (L298N backward) sampai limit SW atas
  ↓
PAPAN_PENUH:
  Buzzer 3x panjang
  LCD: "PAPAN PENUH - BALIK KE ANCAK"
  Dashboard push: "Batch #N selesai, Total: Xg"
  Tunggu operator angkat mold → tekan START lagi
  batch_counter++
  → IDLE
```

**Catatan**: Tidak ada lagi state GESER, tidak ada stepper, tidak ada homing ke posisi slot. Jauh lebih simpel!

---

## 9. TANTANGAN DESAIN & SOLUSI

### 9.1 Distribusi Kedelai Tidak Merata Antar Slot

**Masalah**: Kedelai di hopper mungkin lebih banyak ke slot tengah (gravitasi, pressure).  
**Solusi**:
- Desain hopper dengan pemisah internal (divider plate di dalam hopper)
- Setiap "chamber" hopper terpisah untuk 1 slot → flow lebih terkontrol
- Ukuran lubang nozzle dapat di-adjust: lubang tengah lebih kecil, ujung lebih besar
- Kalibrasi awal: ukur berat masing-masing slot dengan scale manual (bukan load cell mesin)

### 9.2 Press Plate Lentur di Tengah (Span 50cm)

**Masalah**: Plat aluminium 50cm panjang → bisa melengkung/melentur saat tekan.  
**Solusi**:
- Gunakan plat tebal: **min 8mm** atau **profil C-channel aluminium** (lebih kaku)
- Atau tambah support bar di tengah plat (pantograph linkage dari 2 lead screw)
- 2 lead screw (kiri dan kanan) → tekanan merata, tidak ada momen lentur di tengah

### 9.3 Fold Bar Lentur (Span 50cm)

**Masalah**: Fold bar 50cm diangkat 2 servo di ujung → bar bisa flex di tengah.  
**Solusi**:
- Pilih material yang kaku: **besi kotak 20×20mm** (bukan aluminium tipis)
- ATAU tambah 1 titik support di tengah bar (servo ketiga per bar) → tapi jadi 6 servo total
- ATAU desain bar dengan **bracing diagonal** di tengah
- Rekomendasi: **besi hollow 20×20mm tebal 2mm** untuk fold bar → kaku, ringan, murah

### 9.4 Sinkronisasi Fold Bar Depan & Belakang

**Masalah**: Bar depan dan belakang harus lipat bersamaan, tidak boleh satu lebih dulu.  
**Solusi**: Firmware: `servoFoldDepanKiri.write(angle); servoFoldDepanKanan.write(angle); servoFoldBelakangKiri.write(angle); servoFoldBelakangKanan.write(angle);` → panggil bersamaan dalam 1 blok kode → ESP32 update semua PWM dalam 1 loop iteration → sync otomatis.

---

## 10. DIMENSI MEKANIK UNTUK TUKANG LAS (v8)

```
FRAME UTAMA (Besi Hollow 40×40mm, tebal 2mm):

KAKI VERTIKAL: 4 buah × 100cm
Jarak kaki kiri-kanan: 80cm
Jarak kaki depan-belakang: 40cm

CROSS BAR BAWAH (h=30cm): dudukan mold + load cell
  2 batang 80cm (kiri-kanan) + 2 batang 40cm (depan-belakang)
  Di tengahnya: plat besi untuk dudukan load cell + mold
  
CROSS BAR TENGAH (h=55cm): dudukan pivot fold bar
  2 batang 80cm (kiri-kanan)
  Bracket pivot fold bar: las di ujung depan dan belakang

CROSS BAR ATAS (h=85cm): dudukan press mechanism
  2 batang 80cm (kiri-kanan)
  Plate motor press: las di tengah (di antara 2 lead screw)
  Bracket lead screw atas: 2 titik (x=15cm dan x=65cm dari kiri)

TOP FRAME (h=130cm): dudukan hopper
  2 batang 80cm (kiri-kanan)
  Bracket hopper: 2 titik kiri-kanan

PIVOT FOLD BAR:
  As besi Ø8mm × 55cm panjang
  Dipasang horizontal di sisi depan (y=0) dan belakang (y=40cm) mold
  Tinggi pivot: h=58cm (sedikit di atas tepi mold ~55cm)
  Fold bar besi hollow 20×20mm 55cm dipasang ke as pivot
  Servo MG996R bracket di ujung kiri dan kanan as → angkat bar via lengan 8cm
```

---

## 11. TIMELINE IMPLEMENTASI (tidak berubah dari v7)

### Sprint 0 (Minggu 0): Procurement
- Order elektronik, beli besi, pesan hopper SS304 custom (panjang 50.5cm)

### Sprint 1 (Minggu 1–2): Mekanik
- Frame, pivot fold bar, lead screw press, dudukan mold + load cell

### Sprint 2 (Minggu 2–3): Elektronik Unit Test
- Test HX711 (total weight), 4 servo fold bar, motor press, LCD, buzzer

### Sprint 3 (Minggu 3–4): Firmware
- State machine v8 (tanpa stepper), web dashboard

### Sprint 4 (Minggu 4–5): System Test
- Dry run → test dengan kedelai → kalibrasi distribusi per slot

### Sprint 5 (Minggu 5+): Produksi
- Target: ≥50 papan/jam (jauh lebih tinggi dari v7!)

---

## 12. CHECKLIST SEBELUM PRODUKSI

- [ ] Load cell baca total berat 5 slot dengan akurasi ±15g total (±3g/slot)
- [ ] 4 fold bar servo sync: semua lipat plastik bersamaan, tidak ada yang lebih lambat
- [ ] Press plate turun merata di 5 slot (tidak miring kiri-kanan)
- [ ] Distribusi kedelai: setiap slot ±10-15% dari rata-rata (cek dengan timbang manual)
- [ ] Hopper gate buka/tutup mulus untuk 5 lubang sekaligus
- [ ] STOP button interrupt langsung berfungsi
- [ ] WiFi dashboard akses dari HP
- [ ] Cycle time papan: < 90 detik (target 60 detik)

---

*Revisi: v8 — 13 September 2026 — Arsitektur 5 slot simultan, tanpa sliding mechanism*  
*Selanjutnya: Gambar desain multi-angle (pending quota reset) + firmware skeleton v8*
