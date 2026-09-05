# 📐 Spesifikasi Dimensi Mekanik — Mesin Pencetak Tempe
### Modular & Upgrade-Ready Design

> **Prinsip desain:** Frame dibuat SEKALI, upgrade dilakukan dengan MENAMBAH komponen — bukan membongkar ulang.

---

## 🗺️ Peta Upgrade (Roadmap Mekanik)

```
┌─────────────────────────────────────────────────────────────────┐
│  V1 — SEKARANG           V2 — UPGRADE 1        V3 — UPGRADE 2  │
│  (Manual Geser)          (Auto Geser)           (Auto Balik)    │
│                                                                 │
│  Press otomatis    ──►   + Stepper NEMA17  ──►  + Motor flip   │
│  Geser tangan            + Timing belt          + Sensor papan  │
│  Balik tangan            Balik tangan           Full otomatis   │
│                                                                 │
│  Frame yang dibuat sekarang sudah menyediakan mount point       │
│  untuk V2 dan V3 — tinggal PASANG, tidak perlu LAS ulang       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📏 Dimensi Cetakan Referensi (JANGAN UBAH)

```
Cetakan tempe (sudah ada, tidak dibuat ulang):
  Panjang total : 50.5 cm
  Lebar total   : 24.0 cm
  5 slot @ 21.3 × 6.6 cm, jarak sekat 1 cm
  Pitch antar slot: 7.6 cm
  Total jarak slot 1 ke slot 5: 30.4 cm

Ancak bambu:
  Panjang : 50.5 cm
  Lebar   : 7.0 cm
```

---

## 🏗️ BAGIAN 1 — FRAME UTAMA

```
Material     : Besi siku 40×40×4 mm (atau 50×50×4mm untuk lebih kuat)
Finishing    : Cat anti karat / galvanis
Tinggi total : 90 cm  (ergonomis operator berdiri)
Lebar total  : 70 cm  (50.5cm cetakan + 10cm kanan-kiri buffer)
Kedalaman    : 45 cm

TAMPAK DEPAN:
   ←──────── 70 cm ────────→
   │                        │  ↑
   │   [AREA HOPPER]        │  │ 40cm
   │                        │  │
   ├────────────────────────┤ ─┤ ← Titik press (tinggi 50cm dari lantai)
   │                        │  │
   │   [AREA REL GESER]     │  │ 20cm
   │   [PLATFORM CETAKAN]   │  │
   ├────────────────────────┤ ─┤ ← Tinggi platform = 30cm dari lantai
   │                        │  │
   │   [KAKI FRAME]         │  │ 30cm
   │                        │  │
   └────────────────────────┘  ↓

KAKI:
  4 kaki besi siku, masing-masing beri baut leveling M10
  (agar bisa datar meski lantai pabrik tidak rata)
  Beri 2 caster/roda di belakang (agar bisa dipindah)
```

---

## 🏗️ BAGIAN 2 — SISTEM REL GESER ⭐ (Bagian Paling Modular)

> Rel dibuat dari awal untuk mendukung V1 (manual) dan V2 (otomatis) **tanpa modifikasi frame**.

### 2.1 Rel Linear

```
SPESIFIKASI REL:
  Tipe      : Linear rail MGW12 ATAU rel aluminium profil V-slot 2040
  Panjang   : 65 cm  (cetakan 50.5cm + 7cm buffer kiri + 7cm buffer kanan)
  Jumlah    : 2 buah (kiri dan kanan, sejajar)
  Jarak antar rel : 22 cm (menyesuaikan lebar cetakan 24cm)

CARRIAGE / PLATFORM GESER:
  Material  : Plat besi 3mm atau aluminium 5mm
  Ukuran    : 52 cm × 26 cm (lebih besar dari cetakan 50.5×24cm)
  Lubang baut cetakan : 4 titik M6 (agar cetakan terkunci, tidak geser)
  Handle manual : Las 2 pegangan pipa Ø16mm di kiri-kanan
                  (dipakai di V1, tetap berguna di V2 untuk manual override)
```

### 2.2 Pembatas Posisi Slot (V1)

```
Las 6 buah stopper baut M8 di body rel, bisa digeser-kencangkan
Posisi preset  : Slot 1, 2, 3, 4, 5 (jarak 7.6cm antar stopper)
Fungsi V1      : Operator geser cetakan sampai "mentok" ke stopper
               → Presisi tanpa sensor, tanpa motor
```

### 2.3 Pre-weld untuk Upgrade V2 (Auto Geser) 🟡

```
Las sekarang, pasang motor nanti:

BRACKET MOTOR NEMA 17 (ujung KIRI rel):
  Plat bracket L 60×60×5mm
  4 lubang M3 jarak 31mm × 31mm (standar NEMA 17)
  Posisi : ujung kiri rel, mengarah ke sumbu belt

BRACKET IDLER PULLEY (ujung KANAN rel):
  Plat bracket dengan lubang Ø5mm untuk as pulley
  Adjustable slot untuk tensioner belt

T-NUT SLOT di bawah carriage:
  Tidak perlu las — buat alur geser untuk clamp belt
  Carriage bisa clamp timing belt tanpa modifikasi las

END-STOP SWITCH HOLES:
  Bor 2× lubang M3 di ujung KIRI rel (home position)
  Bor 2× lubang M3 di ujung KANAN rel (batas maksimum)
  Pasang kabel conduit Ø16mm dari titik ini ke panel kontrol
  (kabel bisa kosong dulu, conduit sudah terpasang)
```

### 2.4 Diagram Rel (Tampak Atas)

```
← 65 cm total ──────────────────────────────────────────→
←7cm→←──────── 50.5 cm (area cetakan) ────────────→←7cm→

[END-STOP]  S1   S2   S3   S4   S5  [END-STOP]
    ●────┼────┼────┼────┼────┼────●
    │    7.6  7.6  7.6  7.6  cm   │
[BRACKET                      [BRACKET]
MOTOR V2]                    IDLER V2]
(pre-weld)                   (pre-weld)

↑ Handle manual (V1)    ↑ Handle manual (V1)

Kabel conduit bawah rel (sudah terpasang dari sekarang)
```

---

## 🏗️ BAGIAN 3 — MEKANISME PRESS VERTIKAL

### 3.1 Kolom Press

```
KOLOM VERTIKAL:
  Material  : Besi hollow/kotak 40×40×3mm
  Jumlah    : 2 buah (kiri-kanan)
  Tinggi    : 40 cm (dari permukaan platform ke atas)
  Posisi    : Tepat di atas titik nozzle (slot 1 = home position)

SLIDER PRESS:
  Material  : Plat besi 5mm + bushing linear Ø40mm
  Fungsi    : Bergerak naik-turun di dalam kolom

MOTOR PRESS:
  Tipe      : Motor DC 12V + Gearbox, torsi min 15 kg.cm
  Mekanisme : Lead screw M8 atau rack & pinion
  Mount     : Lubang center Ø10mm di crossbar atas kolom

PISTON / PLAT PRESS:
  Material  : Plat aluminium 10mm atau besi 5mm
  Ukuran    : 6.0 cm × 21.0 cm (masuk ke slot 6.6×21.3cm)
  Baut ke slider : 4× M6 — bisa ganti piston jika ukuran slot berubah
  Lapisan bawah  : Karet 3mm (tekanan lebih merata)

LIMIT SWITCH MOUNT:
  Las rel micro switch adjustable di sisi kolom
  Bisa digeser atas-bawah ±5cm untuk sesuaikan stroke press
  Titik ATAS  : batas press sudah naik penuh
  Titik BAWAH : batas press sudah menekan penuh
```

### 3.2 Upgrade Path Press

```
V1 → Motor DC + relay ON/OFF (kontrol limit switch)
V2 → Ganti relay ke L298N + PWM (kecepatan halus)
V3 → Ganti motor ke servo linear / pneumatik
     (mount titik sama, cukup ganti aktuator)
```

---

## 🏗️ BAGIAN 4 — HOPPER KEDELAI

```
DIMENSI HOPPER:
  Bentuk    : Corong persegi (mudah dibuat tukang las)
  Mulut atas: 40cm × 30cm
  Mulut bawah (nozzle): 6cm × 6cm
  Tinggi    : 30cm
  Volume    : ± 8 Liter (~5kg kedelai)
  Material  : Plat besi 2mm ATAU stainless 1.5mm (lebih higienis)

GATE / PINTU NOZZLE:
  Tipe V1   : Plat geser manual (operator tarik-dorong)
              Slot T-groove di kiri-kanan nozzle, lebar 2mm
  Upgrade V2: Ganti plat manual → servo 20kg atau solenoid
  Pre-drill  : 2 lubang M3 di sisi kiri-kanan nozzle untuk servo mount

POSISI HOPPER:
  Nozzle tepat di atas slot 1 cetakan (home position)
  Jarak nozzle ke cetakan : 3-5 cm (ada ruang untuk plastik)

MOUNT HOPPER KE FRAME:
  4 baut M8 adjustable (bisa naik-turun ±5cm)
  → Menyesuaikan jika ketebalan cetakan berubah
```

---

## 🏗️ BAGIAN 5 — SISTEM BALIK CETAKAN (Pre-weld untuk Upgrade V3) 🔵

> V1 & V2: balik manual. Tapi frame sudah disiapkan titik pivot & motor mount untuk V3.

```
KONSEP V3 — MEKANISME BALIK:
  Cetakan penuh (5 slot) → diangkat gripper → putar 180° → 
  diletakkan ke conveyor/rak dengan ancak di bawah

PERSIAPAN DI FRAME SEKARANG:
  Las 2 buah bracket pivot Ø20mm di SISI KIRI frame
  Ketinggian : 55cm dari lantai
  Plat penguat: 10×10cm di sekitar titik pivot
  Las motor mount plate 10×10×5mm di dekat pivot (untuk worm gear V3)
  Bor lubang kabel conduit Ø16mm dari area pivot ke panel kontrol

PENANDA:
  Cat kuning SEMUA titik upgrade V2 dan V3
  Tulis "V2" dan "V3" dengan stamp/stiker tahan air
  → Mempermudah saat upgrade, langsung tahu titik mana yang dipakai
```

---

## 🏗️ BAGIAN 6 — PANEL KONTROL

```
PANEL BOX:
  Ukuran    : 30cm × 20cm × 15cm
  Material  : ABS plastik atau besi 1mm
  Posisi    : Sisi kanan frame, ketinggian 75cm
  Mount     : 4 baut M6, bisa dipindah ke sisi lain

LAYOUT PANEL (V1):
  ┌─────────────────────────────┐
  │  [LCD 16×2]                 │
  │                             │
  │  [●START] [●STOP] [●RESET]  │
  │  (hijau)  (merah) (kuning)  │
  │                             │
  │  [LED OK] [LED ALARM]       │
  └─────────────────────────────┘

CABLE CONDUIT (pasang sekarang, isi kabel belakangan):
  Conduit Ø16mm → Area rel geser (end-stop V2 + stepper V2)
  Conduit Ø16mm → Area press (limit switch)
  Conduit Ø16mm → Area hopper (ultrasonic + gate servo V2)
  Conduit Ø16mm → Area pivot (motor flip V3)
```

---

## ✅ CHECKLIST UNTUK TUKANG LAS

### Wajib Dibuat Sekarang (V1)

| # | Item | Spesifikasi |
|---|---|---|
| 1 | Frame utama 4 kaki | Besi siku 40×40, T=90cm, L=70cm, D=45cm |
| 2 | Baut leveling 4 kaki | Baut M10 di tiap kaki |
| 3 | 2 roda caster belakang | Ø5cm, dengan pengunci |
| 4 | 2 rel linear kanan-kiri | 65cm, jarak 22cm, tinggi 30cm dari lantai |
| 5 | Platform carriage geser | Plat 52×26cm, 2 handle pipa, 4 lubang M6 |
| 6 | 6 stopper manual di rel | Baut M8 adjustable, preset jarak 7.6cm |
| 7 | 2 kolom press vertikal | Hollow 40×40, tinggi 40cm |
| 8 | Crossbar atas + lubang lead screw | Lubang center Ø10mm |
| 9 | Slider press + bushing | Plat 5mm + bushing Ø40mm |
| 10 | Piston press 6×21cm | Plat 5mm, baut M6 ke slider, lapisan karet |
| 11 | Hopper 40×30→6×6, tinggi 30cm | Plat 2mm, gate geser manual |
| 12 | Panel kontrol mount kanan | Ketinggian 75cm, 4 baut M6 |
| 13 | 4 kabel conduit Ø16mm | Ke rel, press, hopper, pivot area |

### Wajib Pre-weld untuk Upgrade V2 🟡

| # | Item | Keterangan |
|---|---|---|
| 14 | Bracket NEMA 17 ujung kiri rel | 4 lubang M3 jarak 31×31mm |
| 15 | Bracket idler pulley ujung kanan | Lubang Ø5mm + slot tensioner |
| 16 | 2 lubang end-stop kiri & kanan | Lubang M3 di ujung rel |
| 17 | 2 lubang gate servo di nozzle | Lubang M3 di kiri-kanan nozzle |

### Wajib Pre-weld untuk Upgrade V3 🔵

| # | Item | Keterangan |
|---|---|---|
| 18 | 2 bracket pivot Ø20mm | Sisi kiri frame, tinggi 55cm, penguat 10×10cm |
| 19 | Motor mount plate di dekat pivot | Plat 10×10×5mm |
| 20 | Cat kuning semua titik upgrade | Stiker "V2" dan "V3" tahan air |

---

## 💡 Pesan untuk Tukang Las

> *"Pak, tolong semua lubang baut dibuat presisi pakai bor, jangan dibakar. Yang dikasih tanda kuning itu titik untuk pasang motor nanti — tolong dilas bracketnya sekarang tapi belum perlu pasang motornya. Nanti kalau mau upgrade tinggal pasang motor ke bracket yang sudah ada, tidak perlu las lagi."*

**Tips material:**
- Gunakan **besi hollow** untuk kolom press — lebih ringan, tetap kuat
- **Cat anti karat** sebelum dipakai — lingkungan pabrik tempe lembab
- Semua **baut yang kena air pakai stainless** — tahan kedelai basah

---

## 📊 Estimasi Biaya Mekanik per Fase

| Komponen | V1 (Sekarang) | Tambahan V2 | Tambahan V3 |
|---|---|---|---|
| Frame + kaki + rel | Rp 200.000 | — | — |
| Press mechanism | Rp 100.000 | — | — |
| Hopper | Rp 80.000 | — | — |
| Pre-weld mount V2 | Rp 30.000 | Motor+belt: Rp 150.000 | — |
| Pre-weld mount V3 | Rp 20.000 | — | Motor flip: Rp 300.000 |
| Cat + finishing | Rp 50.000 | — | — |
| Jasa las | Rp 150.000 | Rp 50.000 | Rp 80.000 |
| **Total per fase** | **~Rp 630.000** | **+Rp 200.000** | **+Rp 380.000** |

> ✅ **Dengan menambah hanya Rp 50.000 di jasa las sekarang**, kamu menghemat bongkar-pasang seharga ratusan ribu di upgrade V2 & V3 nanti.
