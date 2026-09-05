# 🔬 Panduan Pengujian Hardware & Elektronik Sebelum Las
### Proyek: Mesin Pencetak Tempe Otomatis berbasis ESP32
**Status Dokumen:** PANDUAN KERJA MEJA (BENCHTOP TEST GUIDE) &bull; Revisi 1.0

---

## 🎯 Mengapa Harus Uji Coba Sebelum Rangka Dilas?

Melakukan uji coba mandiri terhadap setiap modul elektronik di atas meja kerja (*Bench Testing*) sebelum proses pengelasan rangka besi adalah langkah terbaik dalam rekayasa mekatronika:

1. **Jaminan Komponen Normal:** Memastikan semua barang belanjaan dari e-commerce (Shopee/Tokopedia) berfungsi normal sebelum masa komplain/garansi toko habis.
2. **Kesesuaian Torsi Motor:** Memverifikasi arah putar dan kekuatan torsi motor DC 12V sebelum dudukan bracket dilas mati ke tiang mesin.
3. **Mencegah Kerusakan Fatal:** Menguji fungsi *safety interlock* (limit switch pemutus otomatis) di atas meja sehingga saat dipasang di mesin nyata, motor tidak akan menabrak rangka atau meremukkan komponen.
4. **Pola Pikir Lebih Rileks:** Memahami logika kerja sistem dari layar Serial Monitor secara santai di meja tanpa debu bengkel las.

---

## 🧰 Alat & Bahan yang Disiapkan di Meja Kerja

| No | Peralatan / Bahan | Fungsi & Catatan |
| :---: | :--- | :--- |
| 1 | **Breadboard (Project Board)** | Tempat merangkai komponen tanpa perlu disolder terlebih dahulu |
| 2 | **Kabel Jumper** (M-M, M-F, F-F) | Min. 20 pcs untuk menghubungkan kaki modul |
| 3 | **Kabel Data USB ke ESP32** | Menghubungkan ESP32 ke laptop/komputer untuk upload program |
| 4 | **Adaptor Power Supply 12V 5A** | Sumber daya utama untuk motor DC 12V dan driver L298N |
| 5 | **Step-Down LM2596** | Menurunkan 12V dari adaptor menjadi tepat 5.0V untuk ESP32 & sensor |
| 6 | **Multimeter Digital** | Wajib untuk mengukur tegangan output step-down sebelum dicolok ke ESP32 |
| 7 | **Resistor 10k&Omega; (2 pcs)** | Resistor Pull-Up eksternal untuk tombol START (GPIO 34) & STOP (GPIO 35) |
| 8 | **Resistor 220&Omega; (2 pcs)** | Pembatas arus untuk LED status Hijau & Merah |
| 9 | **Benda Uji Kalibrasi** | Botol air mineral 500 ml (500 gram) atau 1 liter (1000 gram) / gula pasir |

---

## ⚡ Peringatan Keselamatan Penting (Golden Rules)

> [!CAUTION]
> **1. SETEL STEP-DOWN SEBELUM COLOK KE ESP32:**
> Putar trimpot kecil pada modul LM2596 sambil diukur dengan multimeter sampai layar multimeter menunjukkan **tepat 5.0V**. Jangan pernah menyambungkan LM2596 ke ESP32 sebelum tegangan terukur stabil di 5.0V!
>
> **2. ATURAN COMMON GROUND (GND BERSAMA):**
> GND dari Adaptor 12V, GND dari modul LM2596, GND dari Driver L298N, dan GND dari ESP32 **WAJIB DIHUBUNGKAN MENJADI SATU KESATUAN JALUR (COMMON GND)**. Jika tidak terhubung bersama, logika kontrol motor tidak akan bekerja!
>
> **3. KHUSUS GPIO 34 & 35 (PIN INPUT ONLY):**
> Pin GPIO 34 dan GPIO 35 pada ESP32 tidak memiliki resistor pull-up internal. Oleh karena itu, pasanglah resistor 10k&Omega; eksternal dari pin tersebut ke pin 3.3V ESP32.

---

## 📋 7 Tahap Pengujian Modular Bertahap

Semua file kode uji coba sudah disediakan di dalam folder:  
📍 [`firmware/tests/`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/)

```
firmware/tests/
├── 01_i2c_scanner_lcd/
│   └── 01_i2c_scanner_lcd.ino
├── 02_hx711_loadcell_calibration/
│   └── 02_hx711_loadcell_calibration.ino
├── 03_hcsr04_ultrasonic/
│   └── 03_hcsr04_ultrasonic.ino
├── 04_buttons_and_limitswitches/
│   └── 04_buttons_and_limitswitches.ino
├── 05_motor_l298n_leadscrew/
│   └── 05_motor_l298n_leadscrew.ino
├── 06_buzzer_relay_gate/
│   └── 06_buzzer_relay_gate.ino
└── 07_bench_system_mock_test/
    └── 07_bench_system_mock_test.ino
```

---

### 🟢 Tahap 1: Uji Layar LCD 16×2 + I2C Adapter
* **Program:** [`01_i2c_scanner_lcd.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/01_i2c_scanner_lcd/01_i2c_scanner_lcd.ino)
* **Wiring:**
  * LCD `GND` &rarr; ESP32 `GND`
  * LCD `VCC` &rarr; ESP32 `VIN` (5V)
  * LCD `SDA` &rarr; ESP32 `GPIO 21`
  * LCD `SCL` &rarr; ESP32 `GPIO 22`
* **Langkah:**
  1. Buka Arduino IDE, buka file sketch Tahap 1, pilih board **ESP32 Dev Module**, lalu Upload.
  2. Buka **Serial Monitor** (kecepatan baud rate: **115200**).
  3. Perhatikan alamat yang terdeteksi (umumnya `0x27` atau `0x3F`).
  4. Layar LCD akan menyala dan menampilkan teks: `"TEST LCD I2C OK!"`.
* **Troubleshooting:**
  * *Lampu LCD menyala biru/hijau tapi tidak ada tulisan?* Ambil obeng minus kecil, putar potensiometer biru di belakang modul I2C untuk mengatur kontras huruf!

---

### 🟢 Tahap 2: Uji Sensor Berat Load Cell 10kg + HX711
* **Program:** [`02_hx711_loadcell_calibration.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/02_hx711_loadcell_calibration/02_hx711_loadcell_calibration.ino)
* **Wiring Modul HX711 ke ESP32:**
  * HX711 `VCC` &rarr; 5V
  * HX711 `GND` &rarr; GND
  * HX711 `DT`  &rarr; ESP32 `GPIO 4`
  * HX711 `SCK` &rarr; ESP32 `GPIO 5`
* **Wiring Kabel Bar Sensor ke Modul HX711:**
  * Merah &rarr; `E+`
  * Hitam &rarr; `E-`
  * Putih &rarr; `A-`
  * Hijau &rarr; `A+`
* **Langkah Kalibrasi Interaktif:**
  1. Upload program dan buka Serial Monitor (115200 baud).
  2. Sensor akan melakukan *Tare* otomatis (nol-kan nilai saat kosong).
  3. Letakkan benda yang diketahui beratnya di atas bar load cell (misal: botol air 500 gram atau gula pasir 1000 gram).
  4. Ketik huruf `c` di Serial Monitor, lalu masukkan angka berat benda (misal: `500`), tekan Enter.
  5. Program akan otomatis menghitung nilai faktor kalibrasi (misal: `418.5`).
  6. **Catat angka ini!** Nilai ini akan dimasukkan ke baris `#define LOADCELL_FAKTOR` di firmware utama.

---

### 🟢 Tahap 3: Uji Sensor Jarak Ultrasonic HC-SR04 (Hopper Kedelai)
* **Program:** [`03_hcsr04_ultrasonic.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/03_hcsr04_ultrasonic/03_hcsr04_ultrasonic.ino)
* **Wiring:**
  * HC-SR04 `VCC`  &rarr; 5V
  * HC-SR04 `GND`  &rarr; GND
  * HC-SR04 `TRIG` &rarr; ESP32 `GPIO 18`
  * HC-SR04 `ECHO` &rarr; ESP32 `GPIO 19`
* **Langkah:**
  1. Upload program dan buka Serial Monitor.
  2. Gerakkan tangan atau buku mendekat (5 cm) dan menjauh (25 cm) di depan kedua mata sensor.
  3. Serial Monitor akan menampilkan jarak nyata dan estimasi persentase kapasitas hopper.
  4. Jika jarak > 20 cm, status berubah menjadi `[ALARM: KEDELAI HAMPIR HABIS!]`.

---

### 🟢 Tahap 4: Uji Tombol Fisik & Limit Switch
* **Program:** [`04_buttons_and_limitswitches.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/04_buttons_and_limitswitches/04_buttons_and_limitswitches.ino)
* **Wiring:**
  * Tombol START &rarr; Pin `GPIO 34` (dengan resistor pull-up 10k&Omega; ke 3.3V, kaki lainnya ke GND)
  * Tombol STOP  &rarr; Pin `GPIO 35` (dengan resistor pull-up 10k&Omega; ke 3.3V, kaki lainnya ke GND)
  * Limit Switch ATAS  &rarr; Pin `GPIO 32` & GND
  * Limit Switch BAWAH &rarr; Pin `GPIO 33` & GND
  * LED Hijau (OK)     &rarr; Pin `GPIO 2` seri resistor 220&Omega; ke GND
  * LED Merah (Alarm)  &rarr; Pin `GPIO 15` seri resistor 220&Omega; ke GND
* **Langkah:**
  1. Tekan tombol START &rarr; LED Hijau menyala & Serial Monitor mencetak `[EVENT] START DITEKAN`.
  2. Tekan tombol STOP &rarr; LED Merah menyala & Serial Monitor mencetak `[EVENT] STOP DITEKAN`.
  3. Tekan tuas roller limit switch atas/bawah &rarr; Serial Monitor langsung memberi notifikasi deteksi posisi home/maksimal.

---

### 🟢 Tahap 5: Uji Motor DC 12V + Driver L298N & Cut-Off Otomatis
* **Program:** [`05_motor_l298n_leadscrew.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/05_motor_l298n_leadscrew/05_motor_l298n_leadscrew.ino)
* **Wiring:**
  * Terminal `12V` L298N &rarr; Positif Adaptor (+12V DC)
  * Terminal `GND` L298N &rarr; Negatif Adaptor & GND ESP32 *(Wajib Common GND!)*
  * Pin `IN1` L298N &rarr; ESP32 `GPIO 25`
  * Pin `IN2` L298N &rarr; ESP32 `GPIO 26`
  * Terminal `OUT1` & `OUT2` &rarr; 2 Kabel Motor DC 12V
  * Pasang Limit Switch Atas (GPIO 32) dan Bawah (GPIO 33)
* **Langkah Pengujian Safety:**
  1. Nyalakan adaptor 12V.
  2. Ketik huruf `d` di Serial Monitor &rarr; Motor berputar searah jarum jam (turun/press).
  3. Tekan tuas Limit Switch Bawah dengan jari &rarr; **Motor harus langsung MATI SEKETIKA (Safety Cut-Off)!**
  4. Ketik huruf `u` di Serial Monitor &rarr; Motor berputar berlawanan arah (naik/homing).
  5. Tekan tuas Limit Switch Atas dengan jari &rarr; **Motor harus langsung MATI SEKETIKA!**
  6. Ketik huruf `s` kapan saja &rarr; Motor berhenti seketika.

---

### 🟢 Tahap 6: Uji Buzzer & Relay Gate Hopper
* **Program:** [`06_buzzer_relay_gate.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/06_buzzer_relay_gate/06_buzzer_relay_gate.ino)
* **Wiring:**
  * Buzzer &rarr; `GPIO 23` & GND
  * Modul Relay `IN` &rarr; ESP32 `GPIO 27`, `VCC` &rarr; 5V, `GND` &rarr; GND
* **Langkah:**
  1. Ketik `1` &rarr; Buzzer berbunyi 2x *beep-beep* (tanda siklus normal).
  2. Ketik `2` &rarr; Buzzer berbunyi panjang 1 detik (tanda alarm).
  3. Ketik `r` &rarr; Relay berbunyi *klik*, lampu LED indikator relay menyala (kontak tertutup/gate buka), ketik `r` lagi untuk menutup.

---

### 🟢 Tahap 7: Uji Simulasi Terintegrasi Meja (Dry-Run Benchtop)
* **Program:** [`07_bench_system_mock_test.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/07_bench_system_mock_test/07_bench_system_mock_test.ino)
* **Tujuan:** Menjalankan **1 siklus kerja mesin tempe 100% lengkap** di atas meja breadboard!
* **Alur Simulasi:**
  1. Layar LCD menampilkan `"MESIN TEMPE READY | TEKAN START >>"`.
  2. Operator menekan tombol fisik START (GPIO 34).
  3. Buzzer berbunyi 1x, LCD menampilkan `"1. MENGISI KEDELAI"`, relay gate hopper aktif selama 1.5 detik.
  4. LCD berubah menjadi `"2. PRESS TURUN"`, motor DC berputar turun.
  5. Operator menekan Limit Switch Bawah (GPIO 33) dengan tangan.
  6. Motor langsung berhenti, LCD menampilkan `"3. TAHAN TEKANAN | Pemadatan 3s..."`.
  7. Setelah 3 detik, motor otomatis berputar balik (naik), LCD menampilkan `"4. LIFT-OFF FRAME"`.
  8. Operator menekan Limit Switch Atas (GPIO 32) dengan tangan.
  9. Motor berhenti sempurna, buzzer berbunyi 2x *beep-beep*, LCD menampilkan `"SIKLUS SUKSES! | HASIL: 1 PAPAN"`.
  10. Counter produksi otomatis bertambah +1 dan sistem kembali ke status READY!

---

## 📋 Tabel Lembar Ceklis Kelayakan Hardware (Sign-Off Sheet)

Beri tanda centang (&check;) setelah masing-masing pengujian berhasil:

| Modul Hardware | Kriteria Lolos Uji | Hasil Uji | Tgl Cek |
| :--- | :--- | :---: | :---: |
| **ESP32 Microcontroller** | Terdeteksi di Arduino IDE, blink/serial monitor lancar | [ &nbsp; ] LULUS | __/__ |
| **Layar LCD 16×2 I2C** | Alamat I2C terdeteksi, huruf kontras dan terbaca jelas | [ &nbsp; ] LULUS | __/__ |
| **Load Cell 10kg + HX711** | Tare berhasil, pembacaan botol 500g/1000g akurat | [ &nbsp; ] LULUS | __/__ |
| **Ultrasonic HC-SR04** | Jarak terukur stabil 5–25 cm, alarm jarak aktif | [ &nbsp; ] LULUS | __/__ |
| **Tombol START & STOP** | Respon debouncing baik, LED status menyala sinkron | [ &nbsp; ] LULUS | __/__ |
| **Limit Switch Atas/Bawah** | Deteksi sentuh presisi, memicu status HOME / MAX | [ &nbsp; ] LULUS | __/__ |
| **Driver L298N & Motor DC** | Putaran turun & naik kuat, cut-off limit switch 100% pakem | [ &nbsp; ] LULUS | __/__ |
| **Buzzer & Relay Gate** | Beep terdengar jelas, relay kontak *klik* membuka/menutup | [ &nbsp; ] LULUS | __/__ |
| **Dry-Run Integrasi Meja** | 1 siklus penuh berjalan mulus dari start sampai counter naik | [ &nbsp; ] LULUS | __/__ |

> [!TIP]
> **Keputusan Maju ke Bengkel Las:**
> Jika seluruh checklist di atas sudah berstatus **LULUS**, Anda bisa 100% percaya diri membawa desain rangka ke tukang las karena seluruh "otak" dan "saraf" elektrikal mesin sudah terbukti bekerja sempurna!
