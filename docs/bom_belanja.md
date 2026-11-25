# 🛒 Shopping List & Daftar Potong Final — TempehKit v13 (Opsi 2 Final)
## 6-Slot • Kotak Takar Memanjang 200 mm • Pad Silikon • Flip 180° • Laci Elevator 75 mm

> **Arsitektur Final v13 (Opsi 2):** Cetakan + Bearing + NEMA 23 **dibaut mati** ke rangka utama (100% kaku menahan Press 1500 N). Pelepasan tempe vertikal (*demolding*) menggunakan **Laci Penyambut Naik–Turun 75 mm** (1× Mini Linear Actuator 12V 300N + 2× Guide Rod Ø10 mm).
> **Acuan Visual 3D:** [`cad/viewer_3d_v13.html`](../cad/viewer_3d_v13.html)

---

## 1. Ringkasan Estimasi Biaya Lanjutan (Di Luar Komponen yang Sudah Diuji)

| Kategori | Full Otomatis (Rel X & Z Bermotor) | Semi-Otomatis (Rel X & Z Geser Tangan) |
|:---|---:|---:|
| **A. Tambahan Elektronik & Penggerak** *(termasuk Mini Actuator Laci)* | Rp 910.000 | Rp 380.000 |
| **B. Material Besi, Rel, Shaft & Silikon** | Rp 1.945.000 | Rp 1.945.000 |
| **C. Jasa Bengkel Las & Fabrikasi SS304** | Rp 1.500.000 | Rp 1.500.000 |
| **D. Buffer Tak Terduga (~10% + Ongkir)** | Rp 400.000 | Rp 350.000 |
| **ESTIMASI TOTAL LANJUTAN** | **~Rp 4.755.000** *(Rp 4,4–5,0 jt)* | **~Rp 4.175.000** *(Rp 3,8–4,3 jt)* |

> **Catatan Linear Actuator Press:** Jika Linear Actuator yang sudah kamu punya adalah **stroke 10 cm** dan ingin ganti ke **stroke 20 cm (1500 N)** agar clearance flip `+55 mm` tanpa modifikasi engsel, tambahkan ~Rp 350–450 rb.

---

## 2. Channel A: Tambahan Elektronik & Penggerak (Tokopedia / Shopee)

> Komponen utama yang **SUDAH DIUJI LULUS** (tidak perlu beli lagi): ESP32 DevKit V1, PSU 12V 10A, LM2596, HX711 + Load Cell 20 kg, NEMA 23 + TB6600, Linear Actuator + L298N, 1× Servo MG996R, 2× Elektromagnet P25/20 + Relay, Limit Switch Press, LED, Buzzer.

| No | Komponen | Qty | Estimasi (Rp) | Mode | Keterangan |
|:-:|:---|:---:|---:|:---:|---|
| 1 | **Mini Linear Actuator 12V Stroke 100 mm (300N, 15 mm/s)** | 1 | 185.000 | Wajib (Opsi 2) | Penggerak **Laci Elevator Naik–Turun 75 mm** |
| 2 | **Modul Relay 2-Channel 12V / L298N Mini** | 1 | 25.000 | Wajib (Opsi 2) | Driver naik-turun Mini Linear Actuator Laci |
| 3 | **Motor Getar DC 12V (*Vibration Motor*) + MOSFET/Relay** | 1 | 45.000 | Wajib | *Vibro-Levelling* 1,5 dtk meratakan 4 sudut |
| 4 | **Box Panel ABS 200×150×100 mm + Push Button + Kabel** | 1 pkt | 115.000 | Wajib | Panel kontrol & kabel rapi (+ drag chain jika full-auto) |
| 5 | **Limit Switch Laci Atas & Bawah** | 2 | 10.000 | Wajib (Opsi 2) | Batas atas (`Y=520`) & batas bawah (`Y=445`) |
| 6 | **Stepper NEMA 17 + Driver A4988/TMC2208 + Belt GT2** | 2 set | 345.000 | *Full-Auto* | Penggerak otomatis Rel X (Slot 1→6) & Rel Teleskopik Z |
| 7 | **Servo MG996R Metal Gear** *(tambahan)* | 2 | 110.000 | *Full-Auto* | 1× Pintu Weigh-Cup + 1× Pintu Clamshell |
| 8 | **Modul PCA9685 (16-Ch PWM) + Buck XL4015 5A** | 1 set | 60.000 | *Full-Auto* | Hemat pin ESP32 & catu stabil 3 Servo |
| 9 | **Limit Switch Home X & Home Z** | 2 | 15.000 | *Full-Auto* | Sensor titik nol (*homing*) Rel X & Z |

*(Subtotal A: **Rp 910.000** Full-Auto / **Rp 380.000** Semi-Auto)*

---

## 3. Channel B: Material Mekanik, Rel & Hardware (Toko Besi & Online)

| No | Material / Barang | Spesifikasi | Qty | Estimasi (Rp) |
|:-:|:---|:---|:---:|---:|
| 1 | **Besi Hollow 40×40×2.0 mm** | Total ±18 meter (lihat daftar potong di bawah) | 3 btg (6m) | 600.000 |
| 2 | **Rel Laci *Double Track* Stainless 30 cm** | Full Extension, **Non Soft-Close** (Rel Z Kotak Takar) | 1 pasang | 70.000 |
| 3 | **Rel Laci *Double Track* Stainless 35–40 cm** | Full Extension, **Non Soft-Close** (Laci Penyambut) | 1 pasang | 85.000 |
| 4 | **Linear Shaft Ø12 mm (56 cm) + LM12UU Flange + SK12** | Pemandu anti-miring Pelat Press (`X=95 & 805, Z=265`) | 1 set | 170.000 |
| 5 | **Linear Shaft Ø16 mm (85 cm) + LM16UU ×4 + SK16 ×4** | Rel Geser Sumbu-X belakang (`Z=602`) | 1 set | 260.000 |
| 6 | **Linear Shaft Ø10 mm (20 cm) ×2 + LM10UU ×2** | Pemandu vertikal **Laci Elevator** (`X=56 & 844`) | 1 set | 65.000 |
| 7 | **As Pejal SS Ø20 mm (35 cm) + 2× Bearing UCFL 204** | **Stub-Axle** kiri & kanan cetakan (rongga bersih!) | 1 set | 140.000 |
| 8 | **Pulley HTD3M 20T (Bore 8mm) + 60T (Bore 20mm) + Belt 384mm** | Transmisi reduksi 1:3 NEMA 23 | 1 set | 110.000 |
| 9 | **Plat Aluminium 5 mm (`75×23 cm`) + 6 Pad Al 15 mm** | Pelat gantry press & badan 6 pad `64×210 mm` | 1 paket | 210.000 |
| 10 | **Lembaran Silikon Food-Grade 5 mm (Shore A 45)** | Bantalan empuk anti-bubur di bawah 6 pad | 1 lembar | 95.000 |
| 11 | **Baut/Mur SS M3–M10, 4× Kaki Karet M10, Cat Epoxy** | Perakitan & pelapis anti karat food-safe | 1 paket | 140.000 |
| | **Subtotal B** | | | **Rp 1.945.000** |

---

## 4. Channel C: Jasa Bengkel Las & Fabrikasi Custom SS304

| No | Pekerjaan Bengkel | Estimasi (Rp) | Catatan Penting |
|:-:|:---|---:|:---|
| 1 | **Potong & Las Rangka Hollow `900×1420×640 mm` + Sub-Frame Lift Laci + Bracket NEMA 23 & Pedestal Load Cell** | 600.000 | Pastikan siku 90° & tinggi poros kiri-kanan (`h=560`) rata waterpass |
| 2 | **Cetakan 6-Slot SS304 (1,5 mm) + Lubang Angin Ø3 mm + Rel Selip L-Channel + Palang Magnet** | 400.000 | `591×240×36 mm`, pitch `76 mm`, pakai Stub-Axle luar (jangan tembus rongga!) |
| 3 | **Hopper Trapesium SS304 + Corong Celah 200 mm + Kotak Takar Clamshell (`58×200×70 mm`) + Pelat Laci** | 500.000 | Borongan 1 bengkel stainless |
| | **Subtotal C** | **Rp 1.500.000** | |

---

## 5. Daftar Ukuran Potong Besi Hollow 40×40×2.0 mm (Bawa ke Bengkel Las!)

| Bagian Rangka | Ukuran Potong | Jumlah | Total Panjang |
|:---|:---:|:---:|---:|
| **Tiang Vertikal Utama** (4 sudut) | `142 cm` | 4 batang | 568 cm |
| **Palang Lebar Depan & Belakang** (`Y = 40, 160, 340, 1100, 1380`) | `82 cm` | 10 batang | 820 cm |
| **Palang Lebar Tengah** (`Actuator`, `Guide Z=265`, `2× Hopper`, `Load Cell`, `Mini Actuator Laci`) | `82 cm` | 6 batang | 492 cm |
| **Palang Samping Full-Depth** (`Y = 40, 160, 340, 540, 1100, 1380`, kiri & kanan) | `56 cm` | 12 batang | 672 cm |
| **Tiang Penguat Samping Tengah** (`Z = 320`, `Y = 380..540`) | `16 cm` | 2 batang | 32 cm |
| **TOTAL KEBUTUHAN BESI HOLLOW** *(+ waste potong ~5%)* | | | **~25,8 m (≈ 4–5 btg @ 6 m)** |

> [!NOTE]
> *Koreksi ukuran potong:* Karena palang samping `56 cm` dibuat *full-depth* (12 batang) dan ada 6 palang tengah tambahan untuk kekakuan 1500 N, kebutuhan besi hollow totalnya menjadi **~26 meter (5 batang @ 6 m ≈ Rp 950 rb–1 jt, atau bisa pakai hollow 40×40×1.6 mm untuk palang sekunder agar tetap hemat di kisaran Rp 700–800 rb)**.
