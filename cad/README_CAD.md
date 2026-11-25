# 📐 Panduan Berkas CAD 3D & 2D (.HTML, .DXF, .PNG) — TempehKit v13 (Opsi 2 Final)

Folder ini berisi seluruh berkas **Simulasi CAD 3D Interaktif**, **Blueprint 200 DPI siap cetak**, dan **AutoCAD DXF R2010 (skala 1:1, 0 error)** yang sudah diverifikasi bebas tabrakan (*zero-collision*).

---

## 1. Simulasi CAD 3D Interaktif (Buka Langsung di Browser)

* **[`viewer_3d_v13.html`](viewer_3d_v13.html)** — **Model 3D Final v13 (Opsi 2: Laci Elevator Naik–Turun 75 mm)**
  * 1 file HTML mandiri (bisa langsung dibagikan lewat WhatsApp/Email; cukup tersambung internet untuk memuat `Three.js` dan dibuka di Chrome/Edge).
  * Fitur: putar 360°, zoom preset kamera, timeline interaktif, dan **animasi runtut 7 tahap**:
    1. Timbang di bawah Hopper (Load Cell stasioner) → Geser Rel X (`Ø16`) → Luncur Rel Teleskopik Z (`+280 mm`) → Clamshell tebar rata `200 mm`
    2. Motor Getar 12V (`1,5 dtk`) meratakan 4 sudut & lipat plastik berlubang kiri–kanan
    3. Vibro-Press 6-Slot dengan Bantalan Silikon Food-Grade `5 mm` (cetakan dibaut mati, 100% kaku menahan 1500 N)
    4. Selip Ancak Bambu horizontal ke Rel L-Channel (`0 mm gap`) + kunci 2× Elektromagnet 12V (`16 kgf`)
    5. Flip 180° + Laci masuk & naik `+75 mm` menempel bawah ancak
    6. Magnet OFF → **Laci turun vertikal `-75 mm`** membuka clearance `+45 mm` di bawah cetakan
    7. Tarik Laci keluar (0% gesekan dinding cetakan) → Cetakan kosong kembali `0°`

---

## 2. Daftar Blueprint 2D (PNG 200 DPI) & File AutoCAD DXF R2010

| Berkas | Format | Kegunaan Utama |
|:---|:---:|:---|
| [`v13_desain_elevator_demolding.png`](v13_desain_elevator_demolding.png) | PNG 200 DPI | Penjelasan visual & perbandingan Opsi 1 (Mold Lift) vs **Opsi 2 (Laci Elevator `-75 mm`)** |
| [`v12_solusi_granular_dan_press.png`](v12_solusi_granular_dan_press.png) | PNG 200 DPI | Diagram fisika granular kedelai belah: Kotak Takar Memanjang `58×200`, Vibrator 12V, & Pad Silikon |
| [`v12_mekanisme_rel_dosing.png`](v12_mekanisme_rel_dosing.png) | PNG 200 DPI | Blueprint tampak samping & belakang mekanisme rel luncur dosing X-Z terhubung penuh |
| [`v12_dosing_dan_press.dxf`](v12_dosing_dan_press.dxf) | DXF R2010 | Gambar kerja 1:1 Kotak Takar Clamshell `58×200×70 mm`, Pad 2-Lapis, & Bracket Vibrator 12V |
| [`v11_visualisasi_proses_tempe.png`](v11_visualisasi_proses_tempe.png) | PNG 200 DPI | Storyboard 6 tahap plastik berlubang 1-per-1 & mekanisme Flip 180° anti-jatuh |
| [`v10_cetakan_6slot.dxf`](v10_cetakan_6slot.dxf) / [`.png`](v10_cetakan_6slot.png) | DXF + PNG | Gambar laser-cut 1:1 Cetakan 6-Slot SS304 (`591×240 mm`, rongga `66×213 mm`, pitch eksak `76 mm`) |
| [`v10_pelat_penekan.dxf`](v10_pelat_penekan.dxf) / [`.png`](v10_pelat_penekan.png) | DXF + PNG | Gambar fabrikasi Pelat Gantry Press + 6 Pad `64×210 mm` (pitch `76 mm`) |

---

## 3. Script Generator Parametrik (Python `ezdxf` + `matplotlib`)

* `python cad/generate_v10.py` — generate ulang DXF & blueprint Cetakan 6-Slot & Pelat Press
* `python cad/generate_v11.py` — generate ulang storyboard 6-tahap proses plastik & flip
* `python cad/generate_v12.py` — generate ulang diagram solusi granular, blueprint rel dosing X-Z, & DXF v12
* `python cad/generate_v13.py` — generate ulang blueprint elevator demolding v13

---

## 4. Petunjuk Bawa ke Bengkel Las & Stainless

1. **Bengkel Las Rangka Hollow:** Bawa [`docs/bom_belanja.md`](../docs/bom_belanja.md) (Daftar Potong Besi Hollow), [`v12_mekanisme_rel_dosing.png`](v12_mekanisme_rel_dosing.png), [`v13_desain_elevator_demolding.png`](v13_desain_elevator_demolding.png), serta **komponen fisik** (UCFL 204, NEMA 23, Linear Actuator, Rel Laci) agar posisi lubang baut langsung *real-fit*.
2. **Bengkel Stainless / Laser Cut:** Kirim [`v10_cetakan_6slot.dxf`](v10_cetakan_6slot.dxf) dan [`v12_dosing_dan_press.dxf`](v12_dosing_dan_press.dxf) (bahan SUS304 tebal `1.5 mm` untuk cetakan, `1.0 mm` untuk hopper & kotak takar; pastikan poros cetakan memakai **Stub-Axle luar**, jangan melintang di dalam rongga!).
