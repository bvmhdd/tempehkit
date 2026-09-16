# 📐 Spesifikasi Dimensi Mekanik — Mesin Pencetak Tempe
## Desain Final v9 — 6-Slot Simultan, Flip Rotari 180°

> **Status Dokumen**: FINAL v9  
> **Konsep Mekanik**: 6 Slot Cetak Serentak, Pembalikan Rotari 180° (Flip Mold), Dual Lead Screw Pressing, Rangka Lebar 90 cm.

---

## 1. Rangkuman Dimensi Utama

| Elemen Mesin | Panjang / Lebar | Tinggi | Kedalaman | Keterangan |
|---|:---:|:---:|:---:|---|
| **Rangka Utama (Frame)** | 90.0 cm | 130.0 cm | 40.0 cm | Besi hollow 40×40×2.0 mm |
| **Cetakan 6-Slot (SS304)** | 59.1 cm | 3.6 cm | 24.0 cm | 6 rongga @ 21.3 × 6.6 cm |
| **Poros As Rotasi Cetakan** | 65.0 cm | Ø 20 mm | — | As baja/stainless pejal Ø20mm |
| **Pelat Gantry Penekan** | 59.0 cm | 5.0 mm | 15.0 cm | Plat aluminium 5mm (6 pad) |
| **Corong Hopper Kedelai** | 60.0 cm | 30.0 cm | 25.0 cm | Plat SS304 1.0mm, 6 cabang nozzle |
| **Ancak Bambu Penampung** | 65.0 cm | — | 25.0 cm | Diletakkan di rak bawah (h=30cm) |

---

## 2. Geometri Cetakan 6-Slot (Mold Assembly)

```
TAMPAK ATAS CETAKAN (59.1 cm × 24.0 cm):

←─────────────────────────────────── 59.1 cm ───────────────────────────────────→
┌───────────────────────────────────────────────────────────────────────────────┐
│ 6.75 │ S1: 6.6 │ 1 │ S2: 6.6 │ 1 │ S3: 6.6 │ 1 │ S4: 6.6 │ 1 │ S5: 6.6 │ 1 │ S6: 6.6 │ 6.75 │ 24.0
│  cm  │  21.3cm │cm │  21.3cm │cm │  21.3cm │cm │  21.3cm │cm │  21.3cm │cm │  21.3cm │  cm  │  cm
└───────────────────────────────────────────────────────────────────────────────┘
       ▲         ▲   ▲         ▲   ▲         ▲   ▲         ▲   ▲         ▲   ▲
       └─Nozzle 1─┘   └─Nozzle 2─┘   └─Nozzle 3─┘   └─Nozzle 4─┘   └─Nozzle 5─┘   └─Nozzle 6─┘
       ◄────────────── Pitch Antar Lubang Nozzle = 8.5 cm center-to-center ─────────────►
```

### Detail Spesifikasi Cetakan:
* **Jumlah Rongga Slot:** 6 slot sejajar.
* **Ukuran Tiap Rongga:** Panjang 21.3 cm × Lebar 6.6 cm × Kedalaman/Tebal 3.6 cm (Standar komersial tempe pasar).
* **Sekat Pemisah Antar Slot:** Plat stainless tebal 1.0 cm.
* **Margin Tepi Kiri & Kanan:** Masing-masing 6.75 cm untuk penempatan klem as poros Ø20mm dan bracket elektromagnet pengunci tutup.
* **Penutup Cetakan (Lid):** 6 lembar plat aluminium 3mm berengsel baja 2 inchi di sisi belakang tiap slot, dengan pelat penangkap magnet di sisi depan.

---

## 3. Desain Rangka Utama (Frame 90 cm)

```
TAMPAK DEPAN RANGKA MESIN (Besi Hollow 40×40mm, Tebal 2.0mm):

┌─────────────────────────────────────────────────────────────┐
│                 [CORONG HOPPER SS304 60cm]                  │ h = 130 cm
│                 \─────────────────────────/                 │
│                 / ○   ○   ○   ○   ○   ○ \  [SOLENOID GATE]  │
├─────────────────────────────────────────────────────────────┤ h = 100 cm
│  [LEAD SCREW]     [PELAT PENEKAN 6-PAD 59cm]   [LEAD SCREW] │
│       │                      ↕                      │       │ h = 85 cm
│   [BEARING 608]    [MOTOR DC GEARBOX 12V]     [BEARING 608] │
├─────────────────────────────────────────────────────────────┤
│  [BRACKET NEMA23]                                           │ h = 55 cm
│       │ (Belt HTD3M)                                        │
│  [PULLEY 60T] ─── [AS POROS Ø20mm + MOLD 6-SLOT] ───────────┤
│  [BEARING UCFL204]                             [BEARING FL] │
├─────────────────────────────────────────────────────────────┤ h = 30 cm
│                 [RAK PENAMPUNG ANCAK BAMBU]                 │
├─────────────────────────────────────────────────────────────┤ h = 15 cm
│               [BOX ENCLOSURE ELEKTRONIK ABS]                │
└─────────────────────────────────────────────────────────────┘
  ◄────────────────────────── 90 cm ─────────────────────────►
```

### Ketinggian Titik-Titik Kritis Rangka:
1. **h = 0 cm (Lantai):** 4 Kaki besi siku/hollow dilengkapi baut karet leveling M10 (anti-getar dan anti-slip).
2. **h = 15 cm:** Dudukan box panel kontrol ABS (200×150×100mm) di sisi samping terlindung dari cipratan kedelai.
3. **h = 30 cm:** Rak penopang ancak bambu (tempat tempe jatuh saat cetakan dibalik 180°). Jarak jatuh tempe ke ancak diatur sangat minim (2–3 cm) agar tempe tidak hancur saat lepas.
4. **h = 55 cm:** Titik pusat poros rotasi cetakan (as Ø20mm ditopang 2 Bearing Flange UCFL 204) dan dudukan bracket NEMA 23 (h=50cm di tiang kiri).
5. **h = 85 cm:** Posisi pelat penekan saat posisi *HOMING/LIFT-OFF* dan dudukan motor DC gearbox 12V.
6. **h = 100 cm:** Posisi bawah pintu geser corong hopper (*sliding gate*).
7. **h = 130 cm:** Rangka paling atas penopang corong hopper kedelai.

---

## 4. Mekanisme Pembalikan Rotari 180° (Flip Mold)

```
DIAGRAM TRANSMISI ROTASI CETAKAN (Tampak Sisi Kiri Frame):

            [Tiang Rangka Kiri]
                     │
    h=50cm  [Motor Stepper NEMA 23]
                     │ (Shaft Ø6.35mm)
            [Pulley 20T HTD3M]
                     │
                     │  ◄── Timing Belt HTD3M (Panjang ~700mm, Lebar 15mm)
                     │
    h=55cm  [Pulley 60T HTD3M] (Bore 20mm)
                     │
            [Bearing Flange UCFL 204]
                     │
            [Poros As Pejal Ø20mm] ════════► Terhubung ke Cetakan 6-Slot SS304
```

### Parameter Kinematika Rotasi:
* **Rasio Reduksi Gigi:** $20\text{T} : 60\text{T} = 1 : 3$.
* **Torsi Efektif As:** $1.9\text{ Nm (motor)} \times 3 = 5.7\text{ Nm}$ (sangat memadai untuk memutar cetakan seberat ~5 kg).
* **Langkah Putar 180°:**
  $$\text{Steps} = \frac{200 \times 8 \times 3}{2} = 2400 \text{ langkah}$$
* **Waktu Rotasi:** Kecepatan diatur 800 step/detik dengan akselerasi 400 step/detik² → durasi putar 180° berkisar **3.5–4.0 detik** (sangat mulus tanpa goncangan).
* **Elektromagnet Pengunci:** 2 unit elektromagnet 12V (masing-masing gaya tarik 10 kg) dipasang di bibir flange depan cetakan untuk mengunci 6 penutup cetakan secara serentak selama rotasi berlangsung.

---

## 5. Mekanisme Pengepresan Vertikal (Dual Lead Screw T8)

```
TAMPAK MEKANISME PRESS:

   [Motor DC Gearbox 12V High Torque]
                 │
   [Shaft Coupler Fleksibel] ──► [Poros Penghubung Horizontal]
        ┌────────┴────────┐
        ▼                 ▼
   [Lead Screw T8]   [Lead Screw T8]   (Panjang 300mm, Pitch 2mm, Kiri-Kanan)
        │                 │
   [Nut Kuningan]    [Nut Kuningan]
        └────────┬────────┘
                 ▼
   [Pelat Gantry Aluminium 5mm (59.0 × 15.0 cm)]
   [6 Pad Penekan Aluminium / Karet Food-Grade]
```

### Parameter Pengepresan:
* **Stroke Gerak Vertikal:** Maksimal 12 cm (dari h=85cm turun ke h=73cm).
* **Sensor Batas (Endstop):**
  - **Limit Switch Atas (GPIO 32):** Posisi istirahat (*home*) saat cetakan berputar atau saat dosing.
  - **Limit Switch Bawah (GPIO 33):** Posisi tekanan penuh. Motor berhenti dan menahan tekanan statis selama 5 detik.
* **Kecepatan Turun:** Sekitar 10–12 mm/detik → waktu penekanan turun sekitar 6–8 detik.

---

## 6. Corong Kedelai (Hopper) & Pintu Dosing

```
DIMENSI CORONG HOPPER SS304:
- Panjang atas    : 60.0 cm
- Lebar atas      : 25.0 cm
- Tinggi corong   : 30.0 cm
- Sudut kemiringan: 60° (mencegah kedelai basah tersangkut di dinding corong)
- Kapasitas isi   : ±10–12 kg kedelai rebus

SISTEM DISTRIBUSI (6 CABANG Y-FORK):
- Pipa stainless Ø38 mm (1.5 inchi)
- 6 lubang outlet dengan jarak pitch 8.5 cm center-to-center
- 1 plat pintu geser aluminium 3mm (panjang 62cm × lebar 4cm)
- Digerakkan oleh 1 Solenoid Push-Pull 12V dengan pegas pengembali (*spring return*)
```

---

## 7. Panduan Pemotongan Bahan untuk Bengkel Las

### Kebutuhan Besi Hollow 40×40×2.0 mm (Total ±12 Meter):
1. **Kaki Vertikal:** 4 batang × 130 cm = 520 cm
2. **Palang Horizontal (Lebar):** 6 batang × 90 cm = 540 cm
3. **Palang Samping (Kedalaman):** 4 batang × 40 cm = 160 cm
   *(Total: 1.220 cm ≈ 12.2 meter atau 2 batang standar 6 meter)*

### Kebutuhan Poros & Plat:
1. **As Baja / SS Pejal Ø20mm:** 1 batang × 65 cm
2. **Plat Aluminium 5mm:** 1 lembar 60 × 15 cm (Gantry press)
3. **Plat Aluminium 3mm:** 1 lembar 70 × 30 cm (Pintu geser & 6 tutup cetakan)
4. **Plat SS304 1.0mm:** 1 lembar 80 × 60 cm (Hopper & Y-Fork)
