# 🫘 TempehKit &mdash; Mesin Pencetak Tempe Otomatis berbasis IoT

[![Platform](https://img.shields.io/badge/Platform-ESP32%20DevKit%20V1-blue.svg)](https://www.espressif.com/)
[![Firmware](https://img.shields.io/badge/Firmware-Arduino%20C%2B%2B-00979D.svg)](https://www.arduino.cc/)
[![IoT Dashboard](https://img.shields.io/badge/UI-SPIFFS%20Web%20Dashboard-orange.svg)]()
[![Hardware Status](https://img.shields.io/badge/Status-Ready%20for%20Fabrication-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**TempehKit** adalah solusi otomasi pencetakan tempe 6-slot simultan berbasis Internet of Things (IoT) yang dirancang untuk mentransformasi proses produksi di pabrik tempe UKM / keluarga. Sistem ini mengintegrasikan mikrokontroler **ESP32**, penekanan bermotor *Lead Screw*, penimbangan presisi *Load Cell HX711*, pemantauan level bahan *Ultrasonic HC-SR04*, dan kendali jarak jauh melalui *Web Dashboard Wi-Fi*.

---

## 💡 Inovasi Utama: *Lift-Off Mold Frame* (Tanpa Dibalik)

Pada metode konvensional, operator harus mengangkat cetakan kayu/besi seberat 5–8 kg dan **membalik cetakan secara manual** ratusan kali sehari ke atas ancak bambu. Metode ini menguras tenaga fisik, lambat, serta berisiko tinggi merusak struktur tempe dan memicu cedera pergelangan/pinggang.

**TempehKit memecahkan masalah ini dengan mekanisme Lift-Off:**
1. Papan ancak bambu diletakkan di dasar meja mesin.
2. Plastik lembaran perforasi disisipkan pada tiap slot.
3. Frame cetakan 6-slot diturunkan merapat menindih alas.
4. Kedelai dimasukkan dari corong atas dan dipress simultan dengan motor lead screw.
5. Dinding cetakan diangkat vertikal ke atas (*lift-off*), meninggalkan tempe yang telah terbungkus rapi di atas ancak bambu tanpa perlu pernah dibalik!
6. **Beban fisik operator berkurang > 70%** dengan throughput meningkat signifikan (**144–180 tempe/jam**).

---

## 📸 Visualisasi Desain & Skematik

| Render 3D Konsep Mesin | Skematik Pengkabelan ESP32 |
| :---: | :---: |
| ![Konsep 3D Mesin](assets/mesin_tempe_design.jpg) | ![Wiring Diagram ESP32](assets/wiring_diagram_esp32.jpg) |
| *Desain rangka besi, hopper atas, kolom lead screw, dan panel box* | *Pengkabelan ESP32 ke sensor, driver L298N, LCD, relay, dan limit switch* |

---

## ⚙️ Spesifikasi Teknis Mesin

| Parameter | Spesifikasi Desain |
| :--- | :--- |
| **Kapasitas Cetak** | 6 Slot tempe paralel per siklus (&plusmn;144–180 tempe/jam) |
| **Dimensi Slot Tempe** | Panjang 21.3 cm &times; Lebar 6.6 cm &times; Tebal 3.6 cm |
| **Dimensi Luar Frame** | Panjang 50.5 cm &times; Lebar 24.0 cm (Jarak antar slot 1.0 cm) |
| **Dimensi Alas / Ancak** | Papan bambu 50.5 cm &times; Lebar 7.0 cm |
| **Bahan Pembungkus** | Plastik lembaran berpori 12 &times; 35 cm |
| **Aktuator Penekan** | Motor DC 12V High-Torque (&ge;15 kg.cm) + Lead Screw Stainless M10 |
| **Sensor Berat** | Load Cell 10kg Bar-Type + 24-bit ADC Converter HX711 |
| **Sensor Stok Corong** | Ultrasonic HC-SR04 (Rentang baca 2–400 cm) |
| **Layar & Kontrol Lokal** | LCD Karakter 16&times;2 I2C + Tombol START/STOP + LED Status + Buzzer |
| **Konektivitas IoT** | Wi-Fi 2.4 GHz &bull; HTTP Web Server &bull; Responsive Mobile Dashboard |
| **Catu Daya** | Adaptor AC-DC 12V 5A + Step-Down LM2596 (5.0V teregulasi) |
| **Total Estimasi Biaya** | &plusmn; Rp 1.250.000 (Komponen Elektronik &plusmn;505rb + Mekanik/Las &plusmn;740rb) |

---

## 📁 Struktur Direktori Repositori

```
tempehkit/
├── assets/                          # Dokumentasi visual & gambar teknis
│   ├── cetakan_referensi.jpg        # Foto cetakan kayu & ancak bambu asli pabrik
│   ├── mesin_tempe_design.jpg       # Render 3D visual konsep mesin
│   └── wiring_diagram_esp32.jpg     # Skematik diagram pengkabelan lengkap
├── docs/                            # Dokumentasi teknis & manufaktur
│   ├── Project_Brief_Mesin_Pencetak_Tempe.pdf  # PDF Resmi Blueprint (7 Halaman)
│   ├── project_brief.html           # File sumber print A4 responsive
│   ├── panduan_uji_hardware.md      # Panduan bench-test mandiri sebelum las
│   ├── dimensi_mekanik.md           # Gambar kerja dimensi untuk bengkel las
│   ├── desain_cetakan_final.md      # Spesifikasi detail sistem lift-off
│   ├── dokumentasi_lengkap.md       # Rangkuman arsitektur mekatronika
│   └── implementation_plan.md       # Rencana aksi & jadwal kerja
├── firmware/                        # Source code ESP32 & Web Dashboard
│   ├── mesin_tempe/                 # Kode firmware produksi utama
│   │   ├── mesin_tempe.ino          # Program kontrol FSM ESP32
│   │   └── data/                    # Aset web dashboard SPIFFS
│   │       ├── index.html           # UI antarmuka dashboard
│   │       ├── style.css            # Desain CSS modern dark-mode
│   │       └── app.js               # Logika update data AJAX/WebSocket
│   └── tests/                       # Suite pengujian modular hardware (Bench-test)
│       ├── 01_i2c_scanner_lcd/      # Pemindaian alamat I2C & uji LCD 16x2
│       ├── 02_hx711_loadcell_calibration/ # Kalibrasi timbangan gramasi nyata
│       ├── 03_hcsr04_ultrasonic/    # Uji deteksi stok kedelai hopper
│       ├── 04_buttons_and_limitswitches/ # Uji tombol panel & limit switch
│       ├── 05_motor_l298n_leadscrew/# Uji putaran motor & cut-off safety
│       ├── 06_buzzer_relay_gate/    # Uji alarm buzzer & selenoid/relay gate
│       └── 07_bench_system_mock_test/ # Uji simulasi kering 1 siklus penuh di meja
├── scripts/                         # Skrip otomasi & utilitas
│   └── build_brief_pdf.py           # Skrip kompilasi HTML ke PDF via Edge headless
├── .gitignore                       # Filter file sampah compiler & OS
└── README.md                        # Dokumentasi utama repositori
```

---

## 🚀 Panduan Memulai (Quick Start)

### 1. Uji Coba Hardware Sebelum Rangka Dilas (Bench-Testing)
Sangat disarankan menguji setiap modul elektronik satu per satu di atas breadboard sebelum rangka mesin dilas mati.
* Buka dokumen: [`docs/panduan_uji_hardware.md`](docs/panduan_uji_hardware.md)
* Jalankan sketch uji coba dari folder [`firmware/tests/`](firmware/tests/) menggunakan Arduino IDE.
* Pastikan seluruh ceklis kelayakan hardware berstatus **LULUS**.

### 2. Fabrikasi Mekanik Rangka & Cetakan
* Bawa dokumen [`docs/dimensi_mekanik.md`](docs/dimensi_mekanik.md) dan print-out PDF blueprint ke bengkel las.
* Pastikan ruang bebas gerak lead screw vertikal lancar dan bracket motor NEMA17 terpasang untuk opsi upgrade masa depan.

### 3. Upload Firmware Utama & Web Dashboard
1. Buka Arduino IDE, pastikan package board **esp32 by Espressif** telah terpasang.
2. Install library:
   * `HX711` (oleh bogde)
   * `LiquidCrystal_I2C`
   * `ArduinoJson` (v6.x)
3. Buka [`firmware/mesin_tempe/mesin_tempe.ino`](firmware/mesin_tempe/mesin_tempe.ino), sesuaikan SSID & Password Wi-Fi pabrik:
   ```cpp
   const char* WIFI_SSID     = "WIFI_PABRIK_ANDA";
   const char* WIFI_PASSWORD = "PASSWORD_WIFI_ANDA";
   ```
4. Upload sketch ke ESP32 DevKit V1.
5. Upload Web UI ke flash internal ESP32: Klik menu **Tools &rarr; ESP32 Sketch Data Upload** (mengunggah folder `data/` ke SPIFFS).
6. Buka Serial Monitor (115200 baud) untuk melihat IP Address yang didapatkan ESP32.
7. Buka browser di smartphone/laptop, ketik alamat IP tersebut untuk mengakses Web Dashboard.

---

## 📑 Dokumen Blueprint Resmi
* 📕 **[Download / Buka PDF Resmi Blueprint (7 Halaman A4)](docs/Project_Brief_Mesin_Pencetak_Tempe.pdf)**
  * *Halaman 1: Cover Blueprint Eksekutif*
  * *Halaman 2: Konsep Inovasi Lift-Off & 6 Langkah Siklus Kerja*
  * *Halaman 3: Galeri 3D Render, Skematik Wiring & Pinout GPIO*
  * *Halaman 4: Bill of Materials (BOM) & Rincian Anggaran Lengkap*
  * *Halaman 5: Timeline Gantt Chart 6 Minggu & Critical Path*
  * *Halaman 6: Action Items Detail Fase 1 s/d Fase 4*
  * *Halaman 7: SOP Harian Operator (Kakak), Matriks Risiko & Mitigasi*

---

## 👨‍💻 Kontributor & Pengembang
* **Muhammad Muhibin** ([@bvmhdd](https://github.com/bvmhdd)) &bull; *Lead Developer & Mechatronics Designer*
* Inisiatif Modernisasi & Otomasi Pabrik Tempe Keluarga (September 2026)

---
*Lisensi: Bebas digunakan dan dikembangkan untuk kepentingan UKM pangan Indonesia (MIT License).*
