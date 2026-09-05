# 🧩 Brainstorming Desain Cetakan Tempe Baru
### Eliminasi Proses Balik — Ancak Jadi Alas Permanen

> **Masalah yang diselesaikan:** Proses balik cetakan 3-4kg itu berat, berbahaya, dan sulit diotomasi. Solusinya: **rancang ulang cetakan** agar tempe sudah ada di posisi benar sejak awal — tidak perlu dibalik.

---

## 🔑 Prinsip Baru Cetakan

```
LAMA (cetakan existing):                BARU (desain ulang):
─────────────────────                   ────────────────────
Kedelai diisi dari atas      VS         Kedelai diisi dari atas ✅
Ancak ditaruh di atas                   Ancak jadi ALAS dari awal ✅
Seluruh unit DIBALIK         ❌          Cetakan DIBUKA / DILEPAS ✅
Berat ~3-4kg dibalik manual             Tempe tinggal di ancak otomatis ✅
```

---

## 💡 KONSEP 1 — Split-Side Clamshell (Buka Kanan-Kiri)

```
POSISI ISI:                    POSISI PRESS:              POSISI BUKA:
─────────────                  ──────────────             ────────────
     TERBUKA                    [PRESS PLATE]                 ╔══╗
    ╔══╗  ╔══╗                  ════════════                  ║  ║
    ║  ║  ║  ║    ← tutup →     ║  kedelai  ║    → buka →    ║  ║
    ║  ║  ║  ║                  ╠══════════╣                  ╚══╝
    ╚══╝  ╚══╝                  ║  ancak   ║               [ancak + tempe]
   [ancak dulu]                 ╚══════════╝               tinggal di bawah

Cara kerja:
1. Dua sisi cetakan dibuka ke kiri-kanan (engsel/pivot)
2. Taruh ancak di bawah, plastik melapisi dinding
3. Tutup kedua sisi → mold terbentuk
4. Isi kedelai dari atas → press dari atas
5. Buka kedua sisi → tempe + ancak tinggal di platform
```

| ✅ Keunggulan | ❌ Kelemahan |
|---|---|
| Mudah dibayangkan | Engsel kiri-kanan bisa kotor/macet |
| Tempe mudah dilepas | Butuh 2 aktuator/solenoid untuk buka sisi |
| Tidak perlu flip | Celah antar sisi bisa bocor kedelai |

---

## 💡 KONSEP 2 — Lift-Off Frame (Rangka Terangkat) ⭐ DIREKOMENDASIKAN

```
TAHAP 1 — SIAPKAN:       TAHAP 2 — ISI & PRESS:    TAHAP 3 — LEPAS:
──────────────────        ───────────────────         ──────────────
  [FRAME TURUN]           [PRESS PLATE turun]         [FRAME NAIK]
  ┌──────────┐            ════════════                 ┌──────────┐
  │          │            ║  kedelai  ║     ↑ naik     │          │
  │ plastik  │            ╠══════════╣                 │          │ ← frame terangkat
  │ di dalam │            ║ plastik  ║                 └──────────┘
  │          │            ╠══════════╣
  └──────────┘            ║  ancak   ║            [ancak + tempe]
  [ancak di bawah]        ╚══════════╝             tinggal di bawah ✅
  [platform]              [platform]               Operator ambil!

Cara kerja:
1. Frame (hanya dinding, tanpa alas/atap) turun ke posisi press
2. Operator taruh ancak di platform, plastik dimasukkan ke frame
3. Isi kedelai dari atas yang terbuka
4. Press plate turun dari atas → menekan kedelai
5. Press plate naik → frame terangkat → tempe + ancak tinggal di platform
6. Operator ambil ancak + tempe → taruh frame baru → ulang

KUNCI: Frame dan press plate BERGERAK BERSAMA — 1 motor saja!
       Frame turun → isi → press turun → tekan → press+frame naik bersama
```

| ✅ Keunggulan | ❌ Kelemahan |
|---|---|
| **Mekanisme paling sederhana** | Frame dan press harus sinkron |
| **1 motor untuk frame + press** | Platform harus rata & bersih |
| Tidak ada engsel yang macet | Perlu sensor posisi frame |
| Integrasi langsung dengan sistem press yang sudah direncanakan | — |
| Ancak bisa diganti tanpa alat | — |
| **Tidak perlu mekanisme balik SAMA SEKALI** | — |

---

## 💡 KONSEP 3 — Hinged Lid Press (Tutup Engsel Atas)

```
POSISI BUKA:               POSISI TUTUP & PRESS:
──────────────             ─────────────────────
     ╔════╗                ╔════╗
  ╔══╝    ╚══╗ ← lid       ║    ║ ← press plate di dalam lid
  ║  TERBUKA  ║            ║════║ ← menekan kedelai
  ║           ║            ║    ║
  ║  kedelai  ║            ║kedelai║
  ╠═══════════╣            ╠════════╣
  ║  ancak    ║            ║ ancak  ║
  ╚═══════════╝            ╚════════╝

Cara kerja:
1. Buka lid (engsel di sisi kiri), taruh plastik + ancak di dasar
2. Isi kedelai
3. Tutup lid → motor dorong lid ke bawah = sekaligus press
4. Buka lid → tempe di atas ancak → ambil
```

| ✅ Keunggulan | ❌ Kelemahan |
|---|---|
| Lid = press plate (satu komponen) | Engsel harus kuat menahan gaya press |
| Visualnya intuitif | Motor harus di sisi, bukan di atas |
| Tidak perlu flip | Posisi motor lebih kompleks |

---

## 💡 KONSEP 4 — Sliding Drawer (Laci Geser)

```
POSISI PRESS:              POSISI GESER KELUAR:
──────────────             ─────────────────────
[PRESS dari atas]          [laci berisi tempe geser keluar →]
════════════
║          ║               ══════╗
║ kedelai  ║               ║tempe╠══════════→  [tempe keluar]
╠══════════╣               ╚══════╝
║  ancak   ║ ← laci
╚══════════╝
  [rel laci]

Cara kerja:
1. Laci ditarik masuk → isi plastik + kedelai dari atas
2. Press dari atas → menekan kedelai
3. Press naik → laci didorong keluar → tempe + ancak geser ke area pengambilan
```

| ✅ Keunggulan | ❌ Kelemahan |
|---|---|
| Alur produksi linier (masuk-keluar) | Gesekan laci bisa menekan tempe |
| Bisa kombinasi dengan conveyor | Tempe bisa bergeser saat laci ditarik |
| Bagus untuk skala besar | Lebih kompleks dari konsep 2 |

---

## 🏆 Perbandingan 4 Konsep

| | Konsep 1 | **Konsep 2 ⭐** | Konsep 3 | Konsep 4 |
|---|---|---|---|---|
| Kerumitan mekanik | Sedang | **Rendah** | Sedang | Tinggi |
| Jumlah motor | 2 | **1** | 1 | 2 |
| Risiko macet | Sedang | **Rendah** | Sedang | Sedang |
| Biaya tambahan | +Rp 100rb | **+Rp 50rb** | +Rp 80rb | +Rp 150rb |
| Integrasi ke plan existing | Modifikasi | **Minimal** | Modifikasi | Besar |
| Tidak perlu flip | ✅ | ✅ | ✅ | ✅ |
| **Rekomendasi** | Backup | **✅ PILIH** | Backup | Skip |

---

## ✅ Detail Konsep 2 — Lift-Off Frame (Yang Direkomendasikan)

### Dimensi Cetakan Baru (Satu Slot)

```
FRAME (dinding saja, tanpa alas & tutup):
  Panjang dalam : 21.3 cm  (sama dengan slot existing)
  Lebar dalam   : 6.6 cm   (sama dengan slot existing)
  Tinggi frame  : 8-10 cm  (ruang isi kedelai + press)
  Tebal dinding : 3mm besi plat atau 5mm aluminium
  Material      : Stainless steel (tahan lembab + mudah dibersihkan)

PLATFORM BAWAH (tempat ancak diletakkan):
  Ukuran        : 25 cm × 10 cm (lebih besar dari ancak 21.3×7cm)
  Material      : Plat besi 5mm
  Stop/pembatas : 4 sudut L-bracket kecil supaya ancak tidak geser

PRESS PLATE (turun dari atas):
  Ukuran        : 21.0 cm × 6.3 cm (sedikit lebih kecil dari dalam frame)
  Material      : Aluminium 10mm + lapisan karet 3mm di bawah
  Baut ke slider: 4× M6 (sama dengan desain existing)

MEKANISME GERAK FRAME:
  Frame diangkat oleh press plate (dikaitkan)
  Saat motor turun → press plate & frame turun bersama
  Saat plastik + ancak siap → press plate turun lebih jauh dari frame
  Saat motor naik → frame & press plate naik bersama → tempe bebas
```

### Mekanisme Sinkronisasi Frame + Press (1 Motor)

```
DETAIL MEKANIK — Spring-loaded coupling:

   Motor shaft (naik-turun)
        │
   ┌────┴────┐
   │ SLIDER  │
   └────┬────┘
        │
   ┌────┴──────────────────────┐
   │ PRESS PLATE (bawah slider) │
   └────────────────────────────┘
        │ ← spring + pin coupling
   ┌────┴──────────────────────┐
   │ FRAME (dinding cetakan)   │
   └────────────────────────────┘
        ↕ bisa bergerak independen 10cm (spring range)

Cara kerja:
• Motor turun: Frame + press plate turun bersama
• Frame menyentuh platform → frame berhenti
• Motor terus turun: press plate turun sendiri (spring meregang) → PRESS
• Motor naik: press plate naik → spring menarik frame naik → LIFT OFF
• Tidak perlu 2 motor atau 2 aktuator!
```

### Integrasi ke Mesin (Tidak perlu ubah frame besar)

```
SEBELUM (desain lama):           SESUDAH (desain baru):
─────────────────────            ──────────────────────
Cetakan existing (5 slot)        Frame baru 1 slot per stasiun
di atas rel geser                (frame naik-turun, platform tetap)

Butuh:                           Cukup:
- Rel geser horizontal ✅        - Press motor (sudah ada) ✅
- Stepper geser ✅               - Modifikasi piston → frame+press
- Balik manual/otomatis ❌       - Platform statis di bawah
                                 - Tidak perlu geser horizontal ✅
                                 (satu stasiun per slot)
```

> [!NOTE]
> Dengan Konsep 2, **rel geser horizontal bisa disederhanakan** atau bahkan dihilangkan untuk V1. Operator cukup meletakkan dan mengambil ancak di satu titik yang sama. Rel bisa ditambahkan kembali di V2 jika produksi membutuhkan multi-stasiun.

---

## 🔄 Alur Kerja Baru dengan Konsep 2

```
SIKLUS SATU TEMPE:

1. [IDLE] Operator taruh ancak di platform
          Masukkan kantong plastik ke dalam frame
          Tekan START

2. [DOSING] Gate hopper buka → kedelai masuk kantong
            HX711 timbang sampai target berat
            Gate tutup

3. [PRESSING] Motor turun → frame + press turun ke platform
              Frame mentok → press terus turun → menekan kedelai
              Tahan 3 detik → press padat

4. [LIFT-OFF] Motor naik → press + frame terangkat
              Tempe + ancak tinggal di platform
              Buzzer 1x

5. [AMBIL] Operator ambil ancak + tempe
           Ikat/seal plastik manual (2 detik)
           Taruh ke rak fermentasi
           Kembali ke langkah 1

TOTAL WAKTU PER TEMPE: ~15-20 detik (estimasi)
THROUGHPUT: ~180-240 tempe/jam = ~3-4 papan/menit 🚀
```

---

## 📋 Update BOM (Perubahan dari Plan Sebelumnya)

| Item | Plan Lama | Plan Baru |
|---|---|---|
| Cetakan existing (5 slot) | Dipakai | **Tidak dipakai** (diganti frame baru) |
| Rel geser horizontal 65cm | Wajib | **Opsional** (bisa skip di V1) |
| Stepper NEMA 17 + belt | Rp 90.000 | **Bisa skip di V1** |
| Driver A4988 | Rp 20.000 | **Bisa skip di V1** |
| Frame cetakan baru (stainless) | — | **+Rp 80.000** (tukang las) |
| Spring coupling | — | **+Rp 15.000** |
| **Penghematan V1** | | **~Rp 95.000 lebih hemat** |

---

## ❓ Yang Perlu Dikonfirmasi Sebelum Lanjut

> [!IMPORTANT]
> **Pertanyaan untuk kamu:**
>
> 1. **Satu stasiun atau multi-stasiun?**
>    Apakah mesin punya 1 titik press (operator bolak-balik di satu titik)?
>    Atau tetap ingin 5 stasiun sekaligus seperti cetakan lama?
>
> 2. **Ancak per-tempe atau per-papan?**
>    Dari gambar, ancak bamboo ukurannya 50.5×7cm (cukup untuk 1 tempe).
>    Apakah setiap tempe punya ancak sendiri, atau satu ancak untuk 5 tempe?
>
> 3. **Plastik: kantong atau lembaran?**
>    Apakah plastiknya kantong yang dimasukkan ke dalam frame?
>    Atau lembaran plastik yang dilipat mengelilingi kedelai?
