# 🔬 Panduan Pengujian Hardware Meja (Benchtop Test Guide) v9.0
### Proyek: Mesin Pencetak Tempe Otomatis berbasis ESP32 (Arsitektur Final v9)
**Status Dokumen:** PANDUAN KERJA MEJA &bull; Revisi 2.0 (Linear Actuator + NEMA 23 + TB6600 + Servo Gate)

---

## 🎯 Mengapa Uji Coba Meja (Bench Testing) Sangat Krusial?

Sebelum rangka besi dilas dan komponen dipasang permanen, lakukan pengujian mandiri setiap modul di atas meja kerja:
1. **Verifikasi Barang:** Memastikan komponen e-commerce (ESP32, Driver TB6600, Linear Actuator, NEMA 23, Load Cell, Servo, Solenoid) normal sebelum batas garansi toko berakhir.
2. **Kesesuaian Arah & Batas Gerak:** Mengonfirmasi arah dorong Linear Actuator dan putaran NEMA 23 agar tidak terbalik saat dipasang pada mekanik.
3. **Validasi Safety Cut-Off:** Memastikan Limit Switch langsung menghentikan aktuator seketika saat tersentuh.
4. **Kalibrasi Timbangan:** Mendapatkan nilai faktor kalibrasi HX711 nyata menggunakan beban referensi (air mineral/gula pasir).

---

## ⚡ 3 Aturan Emas Keselamatan Elektronik (Golden Rules)

> [!CAUTION]
> **1. SETEL TEGANGAN STEP-DOWN LM2596 SEBELUM COLOK ESP32!**
> Putar trimpot kecil LM2596 sambil diukur multimeter hingga tegangan output stabil tepat di **5.0V**. Jangan pernah menyambungkan LM2596 ke pin 5V/VIN ESP32 sebelum terukur 5.0V, karena lonjakan tegangan 12V akan langsung membakar chip ESP32!
>
> **2. ATURAN COMMON GROUND (GND BERSAMA):**
> Seluruh jalur GND (Negatif PSU 12V, GND LM2596, GND L298N, GND TB6600, GND Servo, dan GND ESP32) **WAJIB DIHUBUNGKAN MENJADI SATU KESATUAN JALUR (COMMON GND)**. Jika tidak, sinyal kontrol akan floating / motor bergerak liar.
>
> **3. RESISTOR PULL-UP TOMBOL START & STOP (GPIO 34 & 35):**
> Pin GPIO 34 dan 35 pada ESP32 adalah *input-only* tanpa pull-up internal. Wajib pasang resistor 10kΩ eksternal dari pin tersebut ke 3.3V ESP32.

---

## 📌 Peta Pinout ESP32 v9 (Acuan Pengujian)

| Komponen | Pin ESP32 | Mode | Keterangan |
|---|:---:|:---:|---|
| **Load Cell HX711 (DOUT)** | GPIO 4 | Input | Jalur Data timbangan |
| **Load Cell HX711 (SCK)** | GPIO 5 | Output | Jalur Clock timbangan |
| **Linear Actuator (IN1)** | GPIO 25 | Output | Kendali L298N: Dorong Turun (Press) |
| **Linear Actuator (IN2)** | GPIO 26 | Output | Kendali L298N: Tarik Naik (Homing) |
| **Servo Gate Hopper** | GPIO 27 | Output (PWM) | Kendali Sudut Pintu Geser Hopper (0° - 90°) |
| **Relay Elektromagnet** | GPIO 13 | Output | Pengunci Tutup Cetakan (Aktif HIGH) |
| **NEMA 23 (STEP)** | GPIO 12 | Output | Pulsa Langkah TB6600 (PUL-) |
| **NEMA 23 (DIR)** | GPIO 14 | Output | Arah Putar TB6600 (DIR-) |
| **Limit Switch Atas** | GPIO 32 | Input Pull-Up | Batas Homing Press (Aktif LOW) |
| **Limit Switch Bawah** | GPIO 33 | Input Pull-Up | Batas Kedalaman Press (Aktif LOW) |
| **Tombol START** | GPIO 34 | Input (Ext Pull-Up 10k) | Pemicu Siklus Otomatis |
| **Tombol STOP** | GPIO 35 | Input (Ext Pull-Up 10k) | Pemicu Berhenti Darurat |
| **LED Hijau (OK/RUN)** | GPIO 2 | Output | Indikator Berjalan |
| **LED Merah (ALARM)** | GPIO 15 | Output | Indikator Bahaya/Berhenti |
| **Buzzer Aktif 5V** | GPIO 23 | Output | Notifikasi Suara Beep |

---

## 🧪 7 Tahapan Pengujian Mandiri Satu per Satu

---

### 🟢 Uji 1: Penyetelan Power Supply 12V 10A & Step-Down LM2596
* **Alat:** PSU 12V 10A, LM2596, Multimeter Digital, Obeng Minus kecil.
* **Langkah:**
  1. Hubungkan input LM2596 (`IN+` dan `IN-`) ke terminal `+12V` dan `COM/GND` pada PSU 12V.
  2. Colokkan kabel steker PSU ke listrik PLN 220V.
  3. Tempelkan probe multimeter (mode DC Volt) pada terminal output LM2596 (`OUT+` dan `OUT-`).
  4. Putar potensiometer obeng kecil berlawanan arah jarum jam secara perlahan hingga voltmeter membaca **tepat 5.00V – 5.10V**.
  5. Matikan PSU. Output 5V ini aman digunakan untuk memberi daya ESP32 (pin VIN), Modul Relay, HX711, dan Servo.

---

### 🟢 Uji 2: ESP32 + Tombol Fisik + LED + Buzzer
* **Tujuan:** Memverifikasi ESP32 dapat membaca input tombol dan menyalakan indikator visual/suara.
* **Rangkaian:**
  * Tombol START: Kaki 1 ke `GPIO 34` & Resistor 10kΩ ke `3.3V`, Kaki 2 ke `GND`.
  * Tombol STOP: Kaki 1 ke `GPIO 35` & Resistor 10kΩ ke `3.3V`, Kaki 2 ke `GND`.
  * LED Hijau: Anoda ke `GPIO 2` seri resistor 220Ω, Katoda ke `GND`.
  * LED Merah: Anoda ke `GPIO 15` seri resistor 220Ω, Katoda ke `GND`.
  * Buzzer: Positif ke `GPIO 23`, Negatif ke `GND`.
* **Program Pengujian:** [`firmware/tests/04_buttons_and_limitswitches/04_buttons_and_limitswitches.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/04_buttons_and_limitswitches/04_buttons_and_limitswitches.ino)
* **Kriteria Sukses:**
  * Tekan START: LED Hijau menyala, Buzzer berbunyi bip pendek, Serial Monitor mencetak: `[EVENT] START DITEKAN`.
  * Tekan STOP: LED Merah menyala, Buzzer berbunyi bip panjang, Serial Monitor mencetak: `[EVENT] STOP DITEKAN`.

---

### 🟢 Uji 3: Sensor Berat Load Cell 20kg + Modul HX711
* **Tujuan:** Menguji akurasi timbangan dan mencari faktor kalibrasi gram.
* **Rangkaian:**
  * Kabel Load Cell: Merah (`E+`), Hitam (`E-`), Putih (`A-`), Hijau (`A+`) ke modul HX711.
  * Modul HX711 ke ESP32: `VCC` ke 5V, `GND` ke GND, `DT` ke `GPIO 4`, `SCK` ke `GPIO 5`.
* **Program Pengujian:** [`firmware/tests/02_hx711_loadcell_calibration/02_hx711_loadcell_calibration.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/02_hx711_loadcell_calibration/02_hx711_loadcell_calibration.ino)
* **Langkah:**
  1. Upload program, buka Serial Monitor (115200 baud).
  2. Saat sensor kosong, pembacaan harus stabil di sekitar 0.00 gram.
  3. Letakkan benda yang diketahui beratnya (misal: botol air 500g atau 1000g).
  4. Ketik `c` di Serial Monitor, ketik berat benda (misal: `500`), lalu tekan Enter.
  5. Program akan menghitung nilai faktor kalibrasi (misal: `420.5`). **Catat angka ini!**

---

### 🟢 Uji 4: Servo Pintu Dosing Kedelai (Hopper Gate)
* **Tujuan:** Memastikan servo bergerak mulus membuka dan menutup pintu corong tanpa getaran berlebih.
* **Rangkaian:**
  * Kabel Cokelat/Hitam (GND) &rarr; Common GND
  * Kabel Merah (VCC) &rarr; Output 5V LM2596 *(Jangan ambil dari pin 3.3V ESP32!)*
  * Kabel Oranye/Kuning (Signal) &rarr; ESP32 `GPIO 27`
* **Skrip Uji Cepat (ESP32Servo):**
  * Posisi 0°: Pintu corong tertutup rapat.
  * Posisi 90°: Pintu corong terbuka penuh mengalirkan kedelai ke cetakan.
* **Kriteria Sukses:** Servo merespons perintah buka (90°) saat dosing dimulai, dan langsung menutup rapat (0°) saat berat target tercapai.

---

### 🟢 Uji 5: Linear Actuator 12V (1500N) + Driver L298N + Limit Switch
* **Tujuan:** Menguji dorongan turun, tarikan naik, dan proteksi pemutus otomatis (*Safety Interlock*).
* **Rangkaian:**
  * Terminal L298N: `12V` ke PSU +12V, `GND` ke Common GND.
  * Logic Pins: `IN1` ke `GPIO 25`, `IN2` ke `GPIO 26`.
  * Output Motor: `OUT1` & `OUT2` ke 2 kabel Linear Actuator 12V.
  * Limit Switch Atas: Satu pin ke `GPIO 32`, pin lainnya ke `GND`.
  * Limit Switch Bawah: Satu pin ke `GPIO 33`, pin lainnya ke `GND`.
* **Program Pengujian:** [`firmware/tests/05_motor_l298n_leadscrew/05_motor_l298n_leadscrew.ino`](file:///c:/Users/muhib/OneDrive/Dokumen/IOT%20Tempe/firmware/tests/05_motor_l298n_leadscrew/05_motor_l298n_leadscrew.ino)
* **Langkah Safety Check:**
  1. Ketik `d` (down) di Serial Monitor &rarr; Silinder piston aktuator memanjang keluar (menekan).
  2. Tekan tuas Limit Switch Bawah dengan tangan &rarr; **Aktuator harus langsung BERHENTI SEKETIKA!**
  3. Ketik `u` (up) di Serial Monitor &rarr; Silinder piston memendek masuk (menarik ke atas).
  4. Tekan tuas Limit Switch Atas dengan tangan &rarr; **Aktuator harus langsung BERHENTI SEKETIKA!**

---

### 🟢 Uji 6: Stepper NEMA 23 (2.8A) + Driver TB6600 (Rotasi Flip 180°)
* **Tujuan:** Memverifikasi kehalusan putaran 180° dan torsi penahan motor tanpa getaran berlebih.
* **Setting DIP Switch TB6600:**
  * **Microstep (1/8 Microstepping):** S1=OFF, S2=OFF, S3=ON (1600 pulse/rev).
  * **Current Limit (2.8A - 3.0A):** S4=OFF, S5=ON, S6=ON.
* **Rangkaian TB6600:**
  * `VCC` & `GND` &rarr; Hubungkan ke PSU +12V dan COM GND.
  * `A+`, `A-`, `B+`, `B-` &rarr; 4 kabel NEMA 23 (Merah-Hijau / Kuning-Biru sesuai datasheet).
  * Sinyal Kontrol (Metode Common Cathode):
    * `PUL-` & `DIR-` &rarr; Sambung ke Common GND ESP32.
    * `PUL+` &rarr; ESP32 `GPIO 12` (Pulsa Langkah STEP).
    * `DIR+` &rarr; ESP32 `GPIO 14` (Arah Putar DIR).
    * `ENA+` / `ENA-` &rarr; Kosongkan (default enable).
* **Kriteria Sukses:**
  * Motor berputar mulus sejauh 2400 step (memutar poros as 180° dengan reduksi pulley 1:3).
  * Motor menahan posisi dengan kokoh tanpa panas berlebih.

---

### 🟢 Uji 7: Solenoid Elektromagnet 12V (P25/20) + Relay
* **Tujuan:** Menguji daya lekat cengkeraman elektromagnet penahan tutup cetakan.
* **Rangkaian:**
  * Modul Relay: `VCC` ke 5V, `GND` ke GND, `IN` ke `GPIO 13`.
  * Jalur Daya Magnet: Hubungkan `+12V` PSU ke terminal `COM` Relay. Dari terminal `NO` (Normally Open) Relay masuk ke kabel positif kedua Elektromagnet (dipasang paralel). Kabel negatif elektromagnet langsung ke GND 12V.
* **Langkah:**
  1. Trigger GPIO 13 ke level `HIGH`.
  2. Relay berbunyi *klik*, lampu indikator relay menyala.
  3. Dekatkan pelat besi/tutup cetakan ke permukaan elektromagnet.
  4. Cengkeraman magnet harus sangat kuat (daya tahan gabungan 16 kg). Saat GPIO 13 `LOW`, magnet langsung melepaskan pelat seketika.

---

## 📋 Lembar Ceklis Kelayakan Pra-Perakitan (Bench Sign-Off)

| Komponen Hardware | Kriteria Lolos Pengujian | Status |
|---|---|:---:|
| **PSU 12V + LM2596** | Output 5.0V stabil, tidak ada drop tegangan | [ &nbsp; ] LULUS |
| **ESP32 DevKit V1** | Terdeteksi di Arduino IDE, tombol & LED responsif | [ &nbsp; ] LULUS |
| **Load Cell 20kg + HX711** | Pembacaan berat linier, faktor kalibrasi didapat | [ &nbsp; ] LULUS |
| **Servo Gate 180°** | Gerak 0° - 90° mulus, tidak berdengung saat diam | [ &nbsp; ] LULUS |
| **Linear Actuator + L298N** | Mampu maju/mundur, auto-stop limit switch 100% pakem | [ &nbsp; ] LULUS |
| **NEMA 23 + TB6600** | Putaran microstep halus, torsi putar 180° mantap | [ &nbsp; ] LULUS |
| **Solenoid Elektromagnet** | Mengunci pelat besi dengan daya cengkeram kuat | [ &nbsp; ] LULUS |
