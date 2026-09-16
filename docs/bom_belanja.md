# 🛒 Shopping List & Bill of Materials (BOM) TempehKit
## Desain Final v9 — 6-Slot Simultan, Flip 180°, Lean Architecture

> **Tanggal Pembaruan**: September 2026  
> **Arsitektur**: 6-Slot Simultan, Pembalikan Rotari 180° (NEMA23 + Belt HTD3M + Elektromagnet), Tanpa Fold Bar (Lipat Manual), Tanpa HC-SR04 (Pantau Visual), Tanpa LCD (Web Dashboard WiFi ESP32)

---

## 1. Ringkasan Anggaran Biaya

| No | Saluran Pembelian (Channel) | Jenis Pengadaan | Estimasi Biaya |
|:--:|---|---|:--:|
| A | **Toko Online** (Tokopedia / Shopee) | Elektronik, Sensor, Aktuator, Driver | Rp 801.000 |
| B | **Toko Besi & Hardware Lokal** | Besi hollow, as baja, lead screw, baut | Rp 1.281.000 |
| C | **Bengkel Las & Custom SS304** | Rangka mesin, corong hopper, cetakan mold | Rp 1.175.000 |
| - | **Cadangan Tak Terduga (Buffer 10%)** | Mur, baut tambahan, kabel, fleksibilitas harga | Rp 326.000 |
| **🏷️** | **TOTAL ESTIMASI ANGGARAN** | | **~Rp 3.583.000** |

---

## 2. Channel A: Tokopedia / Shopee (Elektronik & Kontrol)

> **Total Estimasi Channel A: ~Rp 801.000**

| No | Nama Komponen | Kata Kunci Pencarian Tokopedia/Shopee | Qty | Harga Satuan (Rp) | Subtotal (Rp) | Keterangan / Fungsi |
|:--:|---|---|:--:|:--:|:--:|---|
| 1 | **ESP32 DevKit V1** | `ESP32 38 pin devkit v1` | 1 | 65.000 | 65.000 | Main controller & IoT WiFi Gateway |
| 2 | **Load Cell 20kg + HX711** | `load cell 20kg bar type hx711` | 1 | 40.000 | 40.000 | Sensor timbangan otomatis dosing kedelai |
| 3 | **Motor DC Gearbox 12V 60RPM** | `motor dc gearbox 12v high torque` | 1 | 75.000 | 75.000 | Penggerak naik-turun pelat press |
| 4 | **Driver L298N** | `driver motor l298n dual h bridge` | 1 | 22.000 | 22.000 | Kontrol arah putar motor DC press |
| 5 | **Stepper Motor NEMA 23** | `stepper nema 23 57BYG 2.8A` | 1 | 120.000 | 120.000 | Pemutar rotasi cetakan 180° |
| 6 | **Driver Stepper TB6600** | `tb6600 stepper motor driver 4A` | 1 | 65.000 | 65.000 | Driver microstepping NEMA 23 |
| 7 | **Relay Module 2-Channel 12V** | `relay 2 channel 12v optocoupler` | 1 | 18.000 | 18.000 | Kontrol solenoid gate & elektromagnet |
| 8 | **Solenoid Elektromagnet 12V** | `electromagnet solenoid 12V 10kg` | 2 | 40.000 | 80.000 | Pengunci tutup cetakan saat putar 180° |
| 9 | **Solenoid Push-Pull 12V** | `solenoid push pull 12v spring return` | 1 | 55.000 | 55.000 | Pintu geser dosing kedelai hopper |
| 10 | **Power Supply Switching 12V 10A** | `power supply switching 12v 10a` | 1 | 90.000 | 90.000 | Catu daya utama motor & solenoid |
| 11 | **Buck Converter LM2596** | `step down lm2596 buck converter` | 1 | 12.000 | 12.000 | Penurun tegangan 12V ke 5V untuk ESP32 |
| 12 | **Limit Switch Micro** | `micro limit switch lever roller 5a` | 4 | 5.000 | 20.000 | Endstop batas atas & bawah press (2 spare) |
| 13 | **Push Button 16mm Momentary** | `push button 16mm momentary metal` | 3 | 8.000 | 24.000 | Tombol fisik START, STOP/EMERGENCY |
| 14 | **Buzzer Aktif 5V** | `buzzer aktif 5v` | 1 | 5.000 | 5.000 | Notifikasi suara siklus selesai & alarm |
| 15 | **LED 5mm (Merah + Hijau)** | `led 5mm merah hijau diffuser` | 5 | 1.000 | 5.000 | Indikator visual status mesin di panel |
| 16 | **Kapasitor Elco 470μF 16V/25V** | `kapasitor elektrolit 470uf 25v` | 5 | 2.000 | 10.000 | Filter noise ripple daya tegangan |
| 17 | **Resistor 10kΩ 1/4W** | `resistor 10k ohm 1/4 watt` | 20 | 500 | 10.000 | Resistor pull-up tombol & sakelar |
| 18 | **Kabel Jumper M-F 40cm** | `kabel jumper 40cm male female` | 2 set | 20.000 | 40.000 | Pengkabelan modul ke ESP32 |
| 19 | **Terminal Block PCB 2-Pin** | `terminal block 2 pin 5.08mm` | 20 | 1.000 | 20.000 | Konektor kabel rapi dan kuat |
| 20 | **Kotak Panel ABS 200×150×100mm**| `box panel box abs 200x150` | 1 | 25.000 | 25.000 | Enclosure box elektronik & tombol |

---

## 3. Channel B: Toko Besi & Hardware Lokal

> **Total Estimasi Channel B: ~Rp 1.281.000**

| No | Nama Bahan / Barang | Spesifikasi Teknis | Qty | Harga Satuan (Rp) | Subtotal (Rp) | Keterangan / Fungsi |
|:--:|---|---|:--:|:--:|:--:|---|
| 1 | **Besi Hollow 40×40mm** | Tebal 2.0mm (total ±12 meter) | 12 meter | 50.000 /m | 600.000 | Rangka utama mesin (lebar 90cm, t=130cm) |
| 2 | **As Baja / Stainless Steel Ø20mm** | Poros as pejal, panjang 65 cm | 1 batang | 60.000 | 60.000 | Poros putar cetakan (flip 180°) |
| 3 | **Plat Aluminium 5mm** | 60 × 15 cm | 1 lembar | 130.000 | 130.000 | Pelat gantry penekan (*press plate*) |
| 4 | **Plat Aluminium 3mm** | 70 × 30 cm | 1 lembar | 70.000 | 70.000 | Pelat pintu geser hopper & tutup cetakan |
| 5 | **Lead Screw T8 300mm + Brass Nut** | Pitch 2mm, lead 8mm | 2 set | 45.000 | 90.000 | Penurun pelat press kiri dan kanan |
| 6 | **Timing Belt HTD3M** | Lebar 10mm/15mm, panjang ~700mm | 1 buah | 35.000 | 35.000 | Sabuk transmisi putar NEMA23 ke as |
| 7 | **Pulley 20T HTD3M (Bore 6.35mm)** | Shaft NEMA23 | 1 buah | 20.000 | 20.000 | Pulley penggerak NEMA 23 |
| 8 | **Pulley 60T HTD3M (Bore 20mm)** | As Ø20mm (Rasio reduksi 1:3) | 1 buah | 40.000 | 40.000 | Pulley terpasang pada as cetakan |
| 9 | **Bearing Flange UCFL 204 (20mm)** | 2 lubang baut housing cast iron | 2 unit | 25.000 | 50.000 | Bantalan tumpuan as putar cetakan |
| 10 | **Bearing 608ZZ** | ID 8mm, OD 22mm | 4 unit | 5.000 | 20.000 | Tumpuan lead screw T8 atas & bawah |
| 11 | **Shaft Coupler Fleksibel** | 8mm ke shaft motor | 1 unit | 35.000 | 35.000 | Sambungan motor DC ke lead screw |
| 12 | **Engsel Baja 2 Inchi** | Engsel pintu cetakan 6 slot | 12 buah | 3.000 | 36.000 | Engsel penutup cetakan per slot |
| 13 | **Baut, Mur, Ring Set (M3, M4, M5, M8)** | Baja galvanis / stainless | 1 set | 50.000 | 50.000 | Perakitan komponen mekanik |
| 14 | **Kaki Karet Rangka M10** | Karet peredam getaran anti-slip | 4 buah | 8.000 | 32.000 | Kaki dudukan mesin di lantai |
| 15 | **Cat Epoxy Besi + Primer** | Food-grade safe (putih / abu) | 1 kaleng | 43.000 | 43.000 | Pelapis anti karat rangka besi hollow |

---

## 4. Channel C: Bengkel Las & Fabrikasi Custom SS304

> **Total Estimasi Channel C: ~Rp 1.175.000**

| No | Pekerjaan / Komponen Custom | Spesifikasi Teknis | Qty | Estimasi Biaya (Rp) | Keterangan & Catatan |
|:--:|---|---|:--:|:--:|---|
| 1 | **Corong Hopper Kedelai SS304** | Panjang 60cm, corong trapesium kapasitas 10–12 kg, 6 lubang nozzle outlet bawah | 1 unit | 350.000 | Food grade SS304, tebal plat 1.0mm |
| 2 | **Nozzle Pipa Cabang (Y-Fork) SS304** | Pipa SS304 Ø38mm / 1.5 inchi, 6 cabang sejajar pitch 8.5cm c-to-c | 1 unit | 175.000 | Aliran kedelai rata ke 6 slot cetakan |
| 3 | **Cetakan Tempe 6-Slot SS304** | 6 rongga (masing-masing 21.3 × 6.6 × 3.6 cm), sekat 1cm, flange as Ø20mm kiri-kanan | 1 unit | 250.000 | Rangka mold putar 180° |
| 4 | **Ongkos Pengelasan & Perakitan Rangka** | Pengelasan siku frame 90×40×130cm, dudukan bearing, dudukan NEMA23 & motor | 1 paket | 400.000 | Pastikan siku tegak lurus (90°) |

---

## 5. Tips Belanja & Penghematan Biaya

1. **Paket Bengkel Stainless:**  
   Pesan pengerjaan Corong Hopper, Nozzle Pipa Cabang, dan Cetakan 6-Slot ke **satu bengkel stainless** yang sama. Tanyakan harga borongan paket untuk menghemat biaya potong dan tekuk plat.
2. **Kabel & Konektor:**  
   Gunakan kabel pita *rainbow* atau kabel serabut berpelindung untuk koneksi ke driver dan sensor agar tidak mudah terputus saat terkena getaran mekanik.
3. **Power Supply:**  
   Gunakan PSU jaring switching 12V 10A berkualitas baik. Pastikan penempatan PSU dan Driver TB6600 memiliki ventilasi udara yang cukup di dalam panel box.
