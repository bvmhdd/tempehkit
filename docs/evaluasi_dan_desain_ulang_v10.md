# 🔍 Laporan Evaluasi Bug v9 & Desain Ulang Arsitektur v10
### Proyek: TempehKit — Mesin Pencetak Tempe Otomatis 6-Slot berbasis ESP32

> **Tujuan Dokumen:** Mencatat seluruh kesalahan mekanik, CAD, dan firmware yang ditemukan pada revisi **v9**, serta menetapkan spesifikasi **v10 (Zero-Collision & Production-Ready)** sebelum fabrikasi bengkel dan uji integrasi penuh.

---

## 1. Evaluasi Kesalahan Fatal pada Desain v9

### A. 7 Kesalahan Mekanik & CAD (Wajib Diperbaiki Sebelum Las!)

| No | Temuan Kesalahan di v9 | Dampak Jika Tetap Dibuat | Solusi Desain Ulang v10 |
|:-:|:---|:---|:---|
| 1 | **Hopper tepat di atas Linear Actuator & Pelat Press** (`v2_rangka_tampak_depan.png`, `diagram_mekanik_crosssection.png`) | Kedelai jatuh menimpa bodi aktuator & pelat aluminium 59 cm, tidak bisa masuk ke cetakan | **Rangka 2-Zona Kedalaman (`560 mm`):** Depan (`Z=0..340`) khusus Press + Cetakan Flip 180°; Belakang (`Z=340..560`) khusus Hopper + Stasiun Timbang + Talang distribusi 6-cabang berengsel (*Swing-In Chute*) |
| 2 | **Load Cell 20 kg belum terpasang & rawan hancur oleh gaya 1500 N** | Gaya tekan Linear Actuator **1500 N ≈ 153 kgf** (7,5× kapasitas Load Cell 20 kg!) akan langsung mematahkan sensor jika ditaruh di bawah cetakan | Load Cell 20 kg dipasang di **Stasiun Timbang (*Weigh-Box*) Zona Belakang**, 100% terisolasi dari tekanan press 1500 N & getaran motor NEMA 23 |
| 3 | **Cetakan tabrakan dengan Pelat Press & Palang Besi saat Flip 180°** | Cetakan lebar 240 mm berputar pada `h=550 mm` menyapu sampai `h=685 mm`, menabrak pelat press (`h=625 mm`) dan palang rangka di `h=550 mm` | Poros di `h=560 mm` (tanpa palang melintang depan-belakang); sapuan flip aman `h=425..695 mm`; posisi HOME press di `h=720 mm` (clearance `+25 mm`); pakai **Linear Actuator Stroke 200 mm** (`720 → 550 mm`, butuh travel `170 mm`) |
| 4 | **Ukuran Pad Penekan kependekan (`64×140 mm` vs rongga `66×213 mm`)** | Sisa 73 mm ujung depan & belakang tempe tidak tertekan sama sekali | Ukuran 6 pad diperbaiki menjadi **`64 × 210 mm`** di atas pelat gantry aluminium 5 mm ukuran **`700 × 225 mm`** |
| 5 | **Pitch Nozzle (`85 mm`) ≠ Pitch Rongga Cetakan (`76 mm`)** | Di slot ke-6, posisi nozzle meleset `45 mm` keluar dari rongga cetakan (`66 mm + 10 mm sekat = 76 mm`) | Seluruh jarak pitch disamakan eksak: **Pitch Slot = Pitch Pad = Pitch Chute = `76 mm`** |
| 6 | **Pelat Press 590 mm tanpa Linear Guide & Belt HTD3M terlalu panjang (`700 mm`)** | 1 piston tengah mendorong pelat lebar 59 cm tanpa pemandu akan miring/macet (*binding*); belt 700 mm terlalu kendor untuk jarak pusat 128 mm | Tambah **2 batang pemandu vertikal (Linear Shaft Ø12 mm + LM12UU)** kiri-kanan; panjang belt eksak **HTD3M-384 / 390 mm** (untuk jarak pusat motor–poros `128 mm`) |
| 7 | **Bug Gambar CAD v2 (`generate_v2.py`)** | Garis border memotong gambar karena rumus tinggi lupa menjumlahkan offset bawah (`-145`); teks label bertumpuk; piston aktuator mengambang | Script generator baru [`cad/generate_v10.py`](../cad/generate_v10.py) menghasilkan **4 file DXF R2010 + 4 Blueprint PNG 200 DPI** bebas overlap + **Viewer CAD 3D Interaktif** ([`cad/viewer_3d_v10.html`](../cad/viewer_3d_v10.html)) |

> [!WARNING]
> **Catatan Penting Soal Stroke Linear Actuator:**
> * Untuk gerakan press otomatis + flip 180° bebas tabrakan, dibutuhkan travel vertikal minimal **170 mm** (rekomendasi: **Linear Actuator 12V Stroke 200 mm, 1500N**).
> * Jika kamu **sudah terlanjur membeli** Linear Actuator stroke **100 mm**, kamu tidak harus beli baru — cukup gunakan **dudukan pelat press tipe engsel/geser (*flip-up* atau *slide-out*)** atau geser cetakan keluar dari bawah press sebelum dibalik 180°.

---

### B. 6 Bug pada Firmware v9 ([`firmware/mesin_tempe/mesin_tempe.ino`](../firmware/mesin_tempe/mesin_tempe.ino))

| No | Bug di Firmware v9 | Lokasi | Perbaikan di Firmware v10 |
|:-:|:---|:---|:---|
| 1 | **Gagal Compile:** `PIN_TRIG` & `PIN_ECHO` dipakai di `setup()` padahal tidak didefinisikan | `mesin_tempe.ino` L675–676 | Dibungkus `#if USE_HCSR04` lengkap dengan definisi pin default (`18`, `19`) |
| 2 | **Mismatch Gate Hopper:** masih kode Relay (`digitalWrite`), belum mendukung Servo MG996R | `mesin_tempe.ino` L185–186 | Tambah konfigurasi `#define GATE_USE_SERVO 1` (`ESP32Servo` 0°–90°) & fallback Relay (`GATE_USE_SERVO 0`) + `#define RELAY_ACTIVE_LOW 1` |
| 3 | **Salah `pinMode` tombol START/STOP:** memakai `INPUT_PULLUP` di GPIO 34 & 35 (padahal *input-only*, tidak punya pull-up internal) | `mesin_tempe.ino` L680–681 | Diubah ke `INPUT` (sesuai wiring resistor pull-up eksternal 10kΩ yang sudah lulus uji di `04_buttons_and_limitswitches.ino`) |
| 4 | **Tombol `ROTATE_TEST` di Dashboard tidak memutar motor:** `stepper.run()` tidak dipanggil di `loop()` | `mesin_tempe.ino` L574–577, L748 | Memanggil `stepper.run()` secara kontinu di `loop()` + status posisi akurat |
| 5 | **Loop FSM tidak konsisten & `delay()` blocking:** `handleSelesai()` melompat ke `ST_CEK_HOPPER` padahal tanpa sensor ultrasonik; `delay(2000)` bikin Web UI macet | `mesin_tempe.ino` L473, L481, L490 | Selesai siklus kembali aman ke `ST_IDLE`; delay panjang diganti non-blocking `millis()` sambil tetap melayani `server.handleClient()` |
| 6 | **Belum ada interlock limit switch sebelum motor jalan & belum ada kontrol Serial Bench Dry-Run** | `mesin_tempe.ino` | Proteksi limit switch aktif di setiap perintah turun/naik + **Serial Debug Console** (`s`, `x`, `g`, `m`, `r`, `u`, `d`, `o`, `t`, `i`) untuk tes integrasi meja penuh |

---

## 2. Spesifikasi Dimensi Final v10 (Zero-Collision Blueprint)

| Komponen | Dimensi Final v10 | Posisi / Elevasi (`Y` dari dasar hollow) | Catatan Penting |
|:---|:---|:---|:---|
| **Rangka Utama (Hollow 40×40×2mm)** | `900` (L) × `1400` (T) × `560` (D) mm | `Y = 0..1400` (+ kaki karet `-40..0`) | Total hollow ±16,5 meter (3 batang @ 6 m) |
| **Box Panel ABS & PSU 12V 10A** | Panel `240×140×100` & PSU `200×110×50` | `Y = 200..340` (Rak bawah) | Aman dari cipratan kedelai/air |
| **Rak Ancak Bambu** | `650 × 260 × 25 mm` | Permukaan atas `Y = 400 mm` | Clearance `25 mm` di bawah sapuan flip (`425 mm`) |
| **Poros As Rotasi Ø20 mm + UCFL 204** | Panjang `760 mm`, Ø20 mm SS304 | `Y = 560 mm`, `Z = 180 mm` (Zona Depan) | **Bebas palang depan/belakang** di `Y = 560` |
| **Cetakan 6-Slot SS304 (1.5 mm)** | `591 × 240 × 36 mm` (6 slot @ `66×213`, sekat `10`, pitch `76`) | Pusat di `Y = 560`, `Z = 180` | Sapuan flip 180°: `R = 135 mm` (`Y = 425..695`) |
| **Pelat Gantry Press + 6 Pad** | Pelat Al 5 mm `700 × 225 mm`; 6 Pad `64 × 210 × 20 mm` (pitch `76`) | HOME bawah pad: `Y = 720` / PRESS: `Y = 550` | Clearance flip `+25 mm`; dipandu **2× Shaft Ø12 mm + LM12UU** |
| **Linear Actuator 12V 1500N** | **Stroke 200 mm** (tertutup ~325 mm) | Bracket atas di palang `Y = 1070 mm` | Travel pakai `170 mm` (`720 → 550 mm`) |
| **Transmisi NEMA 23 (1:3)** | Pulley `20T` (bore 8 mm) → `60T` (bore 20 mm) | Motor di `Z = 100, Y = 460` (`C = 128 mm`) | **Belt HTD3M-384 / 390 mm** (lebar 15 mm); 180° = `2400 step` |
| **Hopper SS304 + Servo Gate** | `600 × 200 × 320 mm` (Zona Belakang) | `Y = 1080..1400`, `Z = 340..540` | Tidak menghalangi aktuator press |
| **Stasiun Timbang (*Weigh-Box*)** | Wadah `560 × 160 × 140 mm` di atas **Load Cell 20 kg** | `Y = 820..980`, `Z = 350..530` | Bebas gaya tekan 1500 N & bebas getaran motor |
| **Talang 6-Cabang Berengsel** | 6 kanal pitch `76 mm`, sudut miring `~50°` | `Z = 350 → 180`, `Y = 800 → 610` | Ditarik/dilipat mundur ke `Z > 320` sebelum press turun |

---

## 3. Daftar File Hasil Desain Ulang v10

1. **Blueprint CAD 2D v10 (DXF AutoCAD R2010 + PNG 200 DPI):**
   * `cad/v10_rangka_tampak_depan.dxf` & `cad/v10_rangka_tampak_depan.png`
   * `cad/v10_rangka_tampak_samping.dxf` & `cad/v10_rangka_tampak_samping.png`
   * `cad/v10_cetakan_6slot.dxf` & `cad/v10_cetakan_6slot.png`
   * `cad/v10_pelat_penekan.dxf` & `cad/v10_pelat_penekan.png`
2. **Viewer CAD 3D Interaktif (Buka di Browser):**
   * `cad/viewer_3d_v10.html` — putar 360°, zoom, simulasi animasi **Dosing → Press → Flip 180°**, dan cek clearance secara visual!
3. **Firmware & Dashboard v10:**
   * `firmware/mesin_tempe/mesin_tempe.ino` — sudah diperbaiki semua bug compile, Servo/Relay gate, GPIO 34/35, stepper loop, dan Serial Bench Dry-Run.
   * `firmware/mesin_tempe/data/index.html` — sinkron dengan API v10.
