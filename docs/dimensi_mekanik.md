# 📐 Spesifikasi Dimensi Mekanik Final — TempehKit v13 (Opsi 2)
## 6-Slot • Tebar Rata 200 mm • Pad Silikon • Flip 180° • Laci Elevator 75 mm

> **Status Dokumen:** FINAL v13 (Opsi 2 — Zero-Collision & Verified 3D)
> **Acuan Visual:** [`cad/viewer_3d_v13.html`](../cad/viewer_3d_v13.html) & [`cad/v12_mekanisme_rel_dosing.png`](../cad/v12_mekanisme_rel_dosing.png)

---

## 1. Rangkuman Dimensi Utama (Satuan mm)

| Elemen Mesin | Lebar (X) | Tinggi (Y) | Kedalaman (Z) | Material & Catatan |
|:---|:---:|:---:|:---:|:---|
| **Rangka Utama (Frame)** | `900 mm` | `1420 mm` | `640 mm` | Besi Hollow `40×40×2.0 mm` (+ kaki karet `40 mm`) |
| **Cetakan 6-Slot (SS304)** | `591 mm` | `36 mm` | `240 mm` | 6 rongga @ `66×213 mm`, sekat `10 mm`, **pitch eksak `76 mm`** |
| **Poros Rotasi (Stub-Axle)** | `2× 145 mm` | `Ø 20 mm` | — | **Stub-Axle kiri & kanan** + flange luar + spine bawah (rongga 100% bersih!) |
| **Pelat Gantry Press + 6 Pad** | `750 mm` | `5 + 20 mm` | `225 mm` | Pelat Al `5 mm` + 6 Pad (`64×210 mm`: Al `15 mm` + **Silikon Food-Grade `5 mm`**) |
| **2× Linear Guide Press** | `X = 95 & 805` | `545 mm` | `Z = 265` | Shaft `Ø12 mm` + LM12UU + SK12 (`Y = 555..1100`, bebas poros as & bebas laci!) |
| **Hopper Trapesium + Corong** | `300 → 64 mm` | `650 mm` | `210 → 200 mm` | SS304 `1.0 mm`, duduk di palang `Y=1100`, mulut celah `Y=730` + Servo Gate `Y=718` |
| **Kotak Takar Memanjang** | `58 mm` | `70 mm` | `200 mm` | SS304 `1.0 mm`, 3 kompartemen, pintu Clamshell (`Y = 625..695`) |
| **Rel Geser X & Rel Z Dosing** | `820 mm` (X) | `Y = 625 & 705` | `+280 mm` (Z) | 2× Shaft `Ø16 mm` + 4× LM16UU (`Z=602`) + Rel Laci Double Track `30 cm` |
| **Laci Elevator Penyambut** | `772 mm` | `Y = 445↔520` | `270 mm` | Rel Laci Double Track `35–40 cm` + **Mini Actuator 12V 300N** + 2× Guide `Ø10 mm` |
| **Ancak Bambu Penampung** | `640 mm` | `18 mm` | `248 mm` | Diselipkan horizontal ke **Rel Selip L-Channel** di mulut cetakan (`0 mm gap`) |

---

## 2. Geometri Cetakan 6-Slot & Pad Penekan (Pitch Eksak 76 mm)

* **Lebar Total Cetakan:** `67.5` (margin kiri) `+ 6 × 66` (rongga) `+ 5 × 10` (sekat) `+ 67.5` (margin kanan) `= 591.0 mm`.
* **Koordinat Pusat 6 Slot (dari sisi kiri rangka `X = 0`):**
  * `S1 = 255 mm`, `S2 = 331 mm`, `S3 = 407 mm`, `S4 = 483 mm`, `S5 = 559 mm`, `S6 = 635 mm` (jarak eksak **`76.0 mm`**).
* **Lubang Angin (*Air Vent*):** 2–3 lubang `Ø3 mm` di dasar setiap rongga agar tidak vakum/lengket saat tempe dilepas ke ancak.
* **Rel Selip Ancak (*L-Channel*):** Terpasang di tepi kiri & kanan cetakan (tinggi profil hanya `24 mm`, di dalam lebar `660 mm`), dilengkapi stopper belakang dan palang pengunci depan bermagnet (`2× Elektromagnet P25/20 = 16 kgf`).
* **Motor Getar DC 12V (*Vibro-Levelling*):** Dibaut tepat di tengah bawah tulang penguat cetakan (`Y = 521 mm`).

---

## 3. Elevasi Kritis & Bukti Clearance Zero-Collision

| Ketinggian (`Y` dari dasar hollow) | Komponen / Zona | Keterangan Clearance |
|---:|:---|:---|
| `-40 .. 0 mm` | 4× Kaki Karet Leveling M10 | Anti-getar & rata lantai |
| `160 .. 204 mm` | Rak Bawah (Panel ABS kiri, PSU kanan, Dudukan Mini Actuator tengah) | Terlindung dari air & kedelai |
| `445 mm` | **Laci Elevator posisi BAWAH** (`Y_atas = 445`) | Puncak tempe `Y = 497` → **clearance `+45 mm`** di bawah dinding cetakan (`Y = 542`)! |
| `520 mm` | **Laci Elevator posisi ATAS** (`+75 mm` naik) | Menempel rapat di bawah Ancak saat terbalik 180° (`Y = 524`, **gap cuma 4 mm!**) |
| `560 mm` | **Poros Rotasi Flip 180°** (`Z = 200`, dibaut mati ke palang samping) | Sapuan Flip `R = 135 mm` (`Y = 425..695`, `Z = 65..335`) — **bebas palang depan!** |
| `625 .. 695 mm` | **Lintasan Kotak Takar Memanjang (`58×200×70 mm`)** | `+47 mm` di atas cetakan (`578`), `-55 mm` di bawah Press HOME (`750`) |
| `750 mm` | **Press HOME (sisi bawah Pad Silikon)** | **`+55 mm` bebas di atas sapuan Flip `695 mm`**! |
| `550 mm` | **Press BAWAH (Limit Switch Bawah)** | Travel `200 mm` (**Linear Actuator Stroke 200 mm**), ketebalan akhir balok `~35 mm` |
| `1100 mm` | Palang Atas Actuator, Guide Shaft (`Z=265`), & Penopang Hopper (`Z=360 & 560`) | Panjang tertutup actuator pin-to-pin `325 mm` (`775 → 1100`) pas eksak |

---

## 4. Transmisi Rotasi Flip 180° (NEMA 23)

* **Motor:** NEMA 23 `23HS5628` (Shaft `Ø8 mm`, 2.8A) terpasang pada **Bracket Baja L-Shape** di sisi kiri rangka (`Y = 464, Z = 122`).
* **Reduksi:** Pulley `20T` (Bore `8 mm`) → Pulley `60T` (Bore `20 mm`), rasio **`1 : 3`**.
* **Jarak antar pusat poros (`C`):** $\sqrt{78^2 + 96^2} \approx 123.7\text{ mm}$ → **Timing Belt HTD3M-384 / HTD3M-390 (lebar 15 mm)**.
* **Pulsa 180° (1/8 Microstep di TB6600):** `200 × 8 × 3 / 2 = 2400 steps`.
