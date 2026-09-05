# 🧩 Desain Cetakan Baru — Final Konfirmasi
### 6 Slot · Press Simultan · Lift-Off Frame · Plastik Lembaran

---

## ✅ Rekap Konfirmasi Data

| Pertanyaan | Jawaban | Dampak Desain |
|---|---|---|
| Jumlah slot | **6 slot** (koreksi dari 5) | Semua kalkulasi pitch diperbarui |
| Press simultan? | **Ya, 6 slot bersamaan** | 1 press plate besar menggantikan 1 slot kecil |
| Ancak per apa? | **Per papan** (1 papan = 6 slot) | Ancak = alas seluruh frame 6 slot |
| Ukuran ancak | **50.5 × 7 cm** (dari data awal) | Ancak per slot, 6 ancak per papan |
| Jenis plastik | **Lembaran 12 × 35 cm, berlubang** | Perlu mekanisme lipat sebelum insert |

> [!NOTE]
> **Clarifikasi ancak:** Dari foto dan dimensi (50.5cm panjang = cetakan, 7cm ≈ lebar 1 slot), disimpulkan **1 ancak = 1 slot tempe** dan butuh **6 ancak per papan produksi**. Ancak dijejer bersisian saat fermentasi.

---

## 📦 Analisis Plastik Lembaran 12 × 35 cm

```
PLASTIK: 12cm × 35cm berlubang (sudah dipisah per lembar)
SLOT   : 6.6cm lebar × 21.3cm dalam × ~6cm tinggi

CARA PLASTIK MASUK KE SLOT (tampak atas):

  Plastik 12cm    Slot 6.6cm
  ───────────     ──────────
  │←──12cm──→│
  │           │     ┌─ 6.6cm ─┐
  │           │     │         │ ← Plastik dilipat masuk
  └───────────┘     └─────────┘

  Sisa kiri-kanan = (12 - 6.6) / 2 = 2.7 cm per sisi
  → Plastik NAIK ke dinding kiri-kanan slot ✅

CARA PLASTIK MASUK KE SLOT (tampak samping/panjang):

  Plastik 35cm      Slot 21.3cm dalam
  ────────────      ──────────────────
  │←── 35cm ───→│
  │              │  ┌──── 21.3cm ────┐
  │              │  │                │
  └──────────────┘  └────────────────┘

  Sisa panjang = 35 - 21.3 = 13.7cm
  → 13.7cm dibagi dua: ~7cm naik ke dinding depan, ~7cm ke belakang ✅

KESIMPULAN: Plastik 12×35 cm pas untuk slot 6.6×21.3cm dengan lipatan
yang naik ke semua 4 dinding slot. Ini SUDAH BENAR dari desain pabrik ✅
```

**Cara operator memasukkan plastik ke slot baru (sebelum mesin jalan):**

```
1. Ambil lembaran plastik 12×35cm
2. Lipat sisi 12cm ke atas (buat "U" shape, lebar 6.6cm)
3. Masukkan dari atas ke dalam slot (seperti melapisi loyang kue)
4. Sisi 35cm akan terlipat naik di depan dan belakang slot
5. Ulangi untuk 6 slot → baru tekan START
```

---

## 🔧 Desain Cetakan Baru — 6 Slot Simultan

### Konsep Terpilih: Lift-Off Frame (Dimodifikasi untuk 6 Slot)

```
TAMPAK DEPAN — Mekanisme Press 6 Slot Simultan:

POSISI SIAP ISI:           POSISI PRESS:              POSISI LIFT-OFF:
────────────────           ─────────────              ────────────────
                           ║ PRESS PLATE ║
                           ║ 48cm × 20cm║
                           ╠═╦═╦═╦═╦═╦═╣  ← 1 plat
  ┌─┬─┬─┬─┬─┬─┐           ║ ║ ║ ║ ║ ║ ║    besar
  │ │ │ │ │ │ │           ║ ║ ║ ║ ║ ║ ║
  │1│2│3│4│5│6│           ║1║2║3║4║5║6║     ↑ TERANGKAT
  │ │ │ │ │ │ │           ╚═╩═╩═╩═╩═╩═╝
  └─┴─┴─┴─┴─┴─┘           ─────────────    ┌─┬─┬─┬─┬─┬─┐
  [ancak di bawah]        [ancak di bawah]  └─┴─┴─┴─┴─┴─┘ ← frame naik
                                            [tempe di ancak]
                                            [operator ambil]
```

### Dimensi Frame Baru (6 Slot)

```
REKAP DIMENSI SLOT (dari data nyata):
  Jumlah slot    : 6
  Lebar tiap slot: 6.6 cm
  Sekat antar slot: 1.0 cm
  Panjang slot   : 21.3 cm

KALKULASI FRAME:
  Lebar total dalam = (6 × 6.6) + (5 × 1.0) = 39.6 + 5.0 = 44.6 cm
  Lebar total luar  = 44.6 + (2 × dinding 3mm) = ~45.2 cm
  Panjang dalam     = 21.3 cm
  Panjang luar      = 21.3 + (2 × 3mm) = ~21.9 cm
  Tinggi frame      = 8 cm  (ruang isi + sedikit lebih dari tebal tempe)

  Pitch antar slot  = 6.6 + 1.0 = 7.6 cm (sama seperti sebelumnya)

PRESS PLATE (satu plat untuk 6 slot bersamaan):
  Lebar  : 44.0 cm  (masuk ke dalam frame, 3mm clearance tiap sisi)
  Panjang: 20.8 cm  (masuk ke dalam frame)
  Tebal  : 8-10mm besi / 12mm aluminium
  Permukaan bawah: dilapisi karet 3mm (merata, tidak merusak plastik)
  Struktur: bisa solid plat ATAU grid (lebih ringan, tetap rata)

ANCAK (per slot):
  Ukuran  : 50.5 cm × 7 cm (sesuai data)
  Material: Anyaman bambu existing (tidak perlu beli baru)
  Posisi  : Diletakkan satu per satu di platform bawah tiap slot

PLATFORM BAWAH FRAME:
  Ukuran  : 47 cm × 24 cm (dengan 4 pembatas L-bracket sudut)
  Material: Plat besi 5mm atau stainless
  Permukaan: bisa berlubang-lubang (agar sisa kedelai mudah dibersihkan)
```

---

## ⚙️ Kalkulasi Gaya Press & Rekomendasi Motor

```
LUAS PRESS TOTAL:
  1 slot = 6.6 × 21.3 = 140.6 cm²
  6 slot = 140.6 × 6  = 843.6 cm²

TEKANAN YANG DIBUTUHKAN:
  Tempe tidak butuh tekanan besar — hanya membentuk & memadatkan
  Estimasi: 0.05 – 0.1 kg/cm²
  Total gaya = 843.6 × 0.075 = ~63 kg  (rata-rata)

REKOMENDASI AKTUATOR:
```

| Opsi | Spesifikasi | Biaya | Keunggulan | Kelemahan |
|---|---|---|---|---|
| **Lead Screw M10** + DC Motor 12V Gearbox | Gear ratio 1:50, gaya output ~80kg | Rp 120.000 | Mudah dapat, kontrol presisi | Kecepatan agak lambat |
| **Motor DC + Rack Gear 1:30** | Pinion + rack 1m | Rp 100.000 | Lebih cepat | Torsi lebih rendah |
| **Hydraulic Jack Manual + Solenoid trigger** | Jack 2 ton + solenoid release | Rp 150.000 | Gaya sangat besar, murah | Tidak bisa kontrol presisi |
| **Linear Actuator 12V** | Stroke 10cm, 500N force | Rp 250.000 | Plug-and-play | Lebih mahal |

> [!TIP]
> **Rekomendasi: Lead Screw M10 + Motor DC 12V Gearbox** — paling terjangkau, gaya cukup, bisa dikontrol presisi via limit switch. Lead screw M10 (pitch 1.5mm, 1 putaran = 1.5mm gerak) dengan motor 60rpm + gearbox 1:50 → kecepatan turun ~0.5cm/detik, lebih dari cukup.

---

## 🔄 Alur Kerja Baru (Tanpa Flip!)

```
═══════════════════════════════════════════════════════════
SATU SIKLUS = 6 TEMPE BERSAMAAN
═══════════════════════════════════════════════════════════

[PERSIAPAN — Manual oleh Operator, ~60 detik]
  1. Taruh 6 ancak di platform (satu per slot)
  2. Lipat & masukkan plastik 12×35 ke tiap slot (6x)
  3. Tekan START

[DOSING — Otomatis, ~20–30 detik]
  4. Gate hopper buka → kedelai mengisi slot 1–6 bersamaan
     (pakai hopper dengan 6 outlet atau 1 outlet lebar)
  5. HX711 timbang total berat → gate tutup saat target (6×berat per slot)

[PRESSING — Otomatis, ~10 detik]
  6. Motor lead screw turun → press plate turun ke frame
  7. Frame menyentuh platform → berhenti
  8. Press plate terus turun → menekan 6 kedelai sekaligus
  9. Tahan 5 detik → press plate naik

[LIFT-OFF — Otomatis, ~5 detik]
  10. Motor naik → frame terangkat bersama press plate
  11. 6 tempe dalam plastik tinggal di atas 6 ancak
  12. Buzzer bunyi → LCD: "6 TEMPE SIAP!"

[FINISHING — Manual oleh Operator, ~30 detik]
  13. Operator lipat/tutup plastik di tiap tempe (ikat/seal)
  14. Susun 6 tempe + ancak ke rak fermentasi
  15. Kembali ke langkah 1

TOTAL WAKTU OTOMATIS  : ~40–45 detik
TOTAL WAKTU 1 SIKLUS  : ~2.5 menit (termasuk persiapan operator)
THROUGHPUT ESTIMASI   : ~24 siklus/jam = 144 tempe/jam 🚀
```

---

## 🏗️ Desain Hopper untuk 6 Slot

```
OPSI A — Hopper Satu Outlet Lebar (Lebih Sederhana):
  Satu nozzle lebar 44cm × 3cm yang menutupi semua 6 slot
  Kedelai mengalir merata ke semua slot via gravity
  ⚠️ Distribusi tidak merata mungkin — perlu deflector di dalam hopper

OPSI B — Hopper 6 Outlet Terpisah (Lebih Merata):
  6 nozzle kecil masing-masing 4×4cm tepat di atas tiap slot
  1 gate besar yang buka-tutup semua 6 outlet serentak
  ✅ Distribusi lebih merata — direkomendasikan

OPSI C — Screw Feeder Per Slot (V2):
  6 screw feeder kecil, dosing presisi per slot
  Mahal dan kompleks — skip untuk V1

DESAIN OPSI B (Direkomendasikan):
  ┌────────────────────────────────────────────────────┐
  │              HOPPER VOLUME ~15 liter               │
  │           (cukup untuk ~1 siklus produksi)         │
  └─────────────────────────┬──────────────────────────┘
                            │ Gate plat geser (1 gate buka semua)
             ┌──┬──┬──┬──┬──┼──┐
             │  │  │  │  │  │  │ ← 6 outlet @ 4×4cm
             ▼  ▼  ▼  ▼  ▼  ▼
           [slot1-2-3-4-5-6 frame]
```

---

## 📐 Revisi Dimensi Mekanik (Update dari 5 → 6 Slot)

```
YANG BERUBAH vs PLAN SEBELUMNYA:
─────────────────────────────────
❌ 5 slot, press per-slot, rel geser horizontal
✅ 6 slot, press simultan, TANPA rel geser horizontal

ITEM          | LAMA               | BARU
──────────────|────────────────────|──────────────────────
Jumlah slot   | 5                  | 6
Press plate   | 6×21cm (1 slot)    | 44×21cm (6 slot)
Rel geser     | Wajib (65cm)       | TIDAK DIPERLUKAN ✅
Stepper motor | Wajib              | TIDAK DIPERLUKAN ✅
Lead screw    | M8 (1 slot)        | M10 (beban 6 slot)
Hopper outlet | 1 nozzle kecil     | 6 outlet atau 1 lebar
Frame cetakan | Existing (5 slot)  | Baru dibuat (6 slot)
Load cell     | Berat 1 slot       | Berat 6 slot (0-5kg)
```

---

## 💰 Revisi BOM Final

| No | Komponen | Spesifikasi | Harga |
|---|---|---|---|
| 1 | ESP32 DevKit V1 | — | Rp 55.000 |
| 2 | Load Cell **10kg** + HX711 | 6 slot sekaligus, ~3-4kg total | Rp 45.000 |
| 3 | Ultrasonic HC-SR04 | Level hopper | Rp 15.000 |
| 4 | Limit Switch × 2 | Atas & bawah press | Rp 10.000 |
| 5 | Motor DC 12V + Gearbox **1:50** | Press lead screw, torsi tinggi | Rp 110.000 |
| 6 | Lead Screw M10 + Nut 15cm | Aktuator press | Rp 50.000 |
| 7 | Driver L298N | Motor DC | Rp 20.000 |
| 8 | Relay Module 4ch | Gate hopper | Rp 25.000 |
| 9 | LCD 16×2 + I2C | Display lokal | Rp 30.000 |
| 10 | Buzzer + LED + Tombol | — | Rp 20.000 |
| 11 | Power Supply 12V 5A | — | Rp 80.000 |
| 12 | Step-down LM2596 5V | — | Rp 15.000 |
| 13 | Kabel + protoboard + konektor | — | Rp 75.000 |
| | **Total Elektronik** | | **~Rp 550.000** |
| | Frame 6-slot baru (stainless/besi, tukang las) | Frame + press plate + hopper + platform | Rp 400.000–550.000 |
| | **TOTAL** | | **Rp 950.000–1.100.000** ✅ |

> [!TIP]
> **Lebih hemat Rp 130.000** dari plan sebelumnya karena:
> Hapus stepper NEMA17 (Rp 55rb) + driver A4988 (Rp 20rb) + timing belt+rel (Rp 115rb) = hemat Rp 190rb
> Tambah lead screw M10 (Rp 50rb) + upgrade load cell 10kg (Rp 10rb) = tambah Rp 60rb
> **Net saving: -Rp 130.000** 🎉

---

## 🔁 Perbandingan: Desain Lama vs Baru

| Aspek | Desain Lama (5 slot, geser) | **Desain Baru (6 slot, simultan)** |
|---|---|---|
| Press per siklus | 1 tempe | **6 tempe sekaligus** |
| Waktu per papan | ~5–8 menit | **~2.5 menit** |
| Throughput | ~7–12 papan/jam | **~24 papan/jam = 144 tempe/jam** |
| Rel geser | Diperlukan | **Tidak diperlukan** |
| Flip cetakan | Diperlukan | **Tidak diperlukan** |
| Jumlah motor | 2 (press + stepper) | **1 (press saja)** |
| Kerumitan sistem | Sedang | **Rendah** ✅ |
| Biaya total | ~Rp 1.050.000–1.235.000 | **~Rp 950.000–1.100.000** ✅ |

---

## 📌 Langkah Selanjutnya

> [!IMPORTANT]
> Dengan desain ini sudah terkonfirmasi, langkah berikutnya adalah:
>
> 1. **Konfirmasi tinggi frame** — Berapa tinggi tempe yang diinginkan setelah press? Ini menentukan tinggi frame cetakan (estimasi: 5–8 cm).
> 2. **Konfirmasi berat target per slot** — Berapa gram kedelai per tempe? Ini untuk kalibrasi load cell.
>
> Jika sudah, saya langsung generate:
> - `mesin_tempe.ino` — Firmware ESP32 lengkap
> - `index.html` — Dashboard web monitoring
> - Spesifikasi dimensi mekanik final untuk tukang las
