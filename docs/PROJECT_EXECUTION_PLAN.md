# 🏭 Project Execution Plan — Mesin Pencetak Tempe Tier 2
## End-to-End: Dari Nol sampai Produksi (Desain v9 — 6-Slot Flip 180° Lean)

> **Framework**: Hardware Agile Sprint (5 Sprint × 1 Minggu)  
> **Status Tracking**: GitHub Projects / Trello / Notion  
> **Estimasi Total**: 4–6 Minggu kerja bertahap

---

## FRAMEWORK SPRINT

```
Hardware Agile Sprint Method:
┌──────────────────────────────────────────────────────────┐
│ SPRINT 0: Procurement & Persiapan          (Minggu 0–1)  │
│ SPRINT 1: Mekanik & Frame 90cm             (Minggu 1–2)  │
│ SPRINT 2: Elektronik & Unit Test           (Minggu 2–3)  │
│ SPRINT 3: Firmware & Integrasi FSM v9      (Minggu 3–4)  │
│ SPRINT 4: System Test & Kalibrasi Dosing   (Minggu 4–5)  │
│ SPRINT 5: Uji Coba Produksi Penuh          (Minggu 5–6)  │
└──────────────────────────────────────────────────────────┘
```

---

## SPRINT 0: PROCUREMENT & PERSIAPAN
### Target: Seluruh komponen elektronik, mekanik, dan custom parts dipesan
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 0

#### S0-1: Siapkan Dokumen Acuan Pembelian
- [ ] Buka `docs/bom_belanja.md` sebagai panduan belanja 3-channel.
- [ ] Pastikan spesifikasi teknis dan dimensi sudah dipahami:
  - Lebar cetakan: 59.1 cm (6 slot @ 6.6cm).
  - Rangka utama: Lebar 90 cm, Tinggi 130 cm, Kedalaman 40 cm.

#### S0-2: Order Komponen Elektronik (Tokopedia / Shopee)
- [ ] **Batch 1 (Kontrol Utama & Sensor):**
  - ESP32 DevKit V1 (38-pin) ×1
  - Load Cell 20kg Bar-Type + HX711 ×1
  - Modul Relay 2-Channel 12V Optocoupler ×1
  - Micro Limit Switch Roller Lever ×4
  - Push Button Metal 16mm Momentary ×3
  - Buzzer Aktif 5V ×1 & LED 5mm (Merah, Hijau) ×5
- [ ] **Batch 2 (Aktuator & Driver Tenaga):**
  - Stepper Motor NEMA 23 57BYG (2.8A, 1.9Nm) ×1
  - Driver Stepper TB6600 4A ×1
  - Motor DC Gearbox 12V 60RPM High Torque ×1
  - Driver Motor L298N Dual H-Bridge ×1
  - Solenoid Elektromagnet 12V (Daya Tahan ≥10kg) ×2
  - Solenoid Push-Pull 12V Spring Return (Pintu Corong) ×1
- [ ] **Batch 3 (Catu Daya & Komponen Pasif):**
  - Power Supply Switching 12V 10A (120W) ×1
  - Step-Down Buck Converter LM2596 ×1
  - Box Panel ABS 200×150×100mm ×1
  - Kabel jumper M-F 40cm, Terminal block PCB 2-pin, Kapasitor 470μF, Resistor 10kΩ

#### S0-3: Belanja Material Mekanik (Toko Besi & Hardware Lokal)
- [ ] Besi Hollow 40×40mm tebal 2.0mm (total 12 meter, minta potong sesuai list ukuran)
- [ ] Poros As Pejal Stainless Steel Ø20mm panjang 65cm
- [ ] 2× Bearing Flange UCFL 204 (dudukan as Ø20mm)
- [ ] 2× Lead Screw T8 panjang 300mm + Brass Nut + 4× Bearing 608ZZ
- [ ] Timing Belt HTD3M panjang ~700mm + Pulley 20T (bore 6.35mm) + Pulley 60T (bore 20mm)
- [ ] Plat aluminium 5mm (60×15cm) untuk pelat penekan & plat aluminium 3mm (70×30cm)
- [ ] 12× Engsel baja 2 inchi, baut/mur M3-M8, kaki karet M10, cat epoxy besi

#### S0-4: Pemesanan Custom Parts Stainless Steel 304 (Bengkel Las/Bubut)
- [ ] Hubungi bengkel stainless untuk paket 3 item:
  1. Corong Hopper kedelai SS304 kapasitas 10–12 kg (lebar 60cm, 6 lubang bawah).
  2. Nozzle pipa cabang Y-Fork SS304 (6 cabang pitch 8.5cm c-to-c).
  3. Cetakan tempe 6-slot SS304 (59.1×24×3.6cm) dengan telinga dudukan as Ø20mm.

#### S0-5: Persiapan Lingkungan Firmware
- [ ] Install Arduino IDE & board support ESP32.
- [ ] Install library pendukung: `HX711`, `AccelStepper`, `ArduinoJson`, `Preferences`.

#### ✅ DEFINITION OF DONE — Sprint 0
- [ ] Semua pesanan online telah diproses dan memiliki nomor resi.
- [ ] Besi hollow dan material toko besi siap di bengkel kerja.
- [ ] Bengkel stainless telah menerima sketsa teknik dan estimasi tanggal jadi.
- [ ] Sketch test dasar di Arduino IDE berhasil di-compile tanpa error.

---

## SPRINT 1: MEKANIK & FRAME 90 CM
### Target: Rangka berdiri kokoh, mekanisme press dual lead screw terpasang, as putar flip 180° beroperasi manual
### Durasi: 5–7 hari

---

### 📋 TASK LIST SPRINT 1

#### S1-1: Pemotongan & Pengelasan Frame Utama
- [ ] Potong besi hollow 40×40mm:
  - 4× Kaki vertikal 130 cm
  - 6× Palang horizontal panjang 90 cm
  - 4× Palang samping kedalaman 40 cm
- [ ] Las rangka dasar dengan siku presisi 90° (cek waterpass & penggaris siku).
- [ ] Pasang dudukan kaki karet M10 pada dasar 4 kaki.

#### S1-2: Pemasangan As Putar & Cetakan Rotari 180°
- [ ] Pasang 2 unit Bearing Flange UCFL 204 pada ketinggian h=55 cm di sisi kiri dan kanan rangka.
- [ ] Masukkan poros as pejal Ø20mm (65cm) melintasi bearing flange.
- [ ] Pasang pulley HTD3M 60T pada ujung as kiri luar.
- [ ] Pasang cetakan 6-slot ke as poros dengan klem/baut baja yang kokoh.
- [ ] Pasang 6 penutup cetakan berengsel 2 inchi beserta pelat penangkap elektromagnet.
- [ ] Test putar manual: cetakan harus berputar 360° dengan seimbang, bebas gesekan ke tiang rangka.

#### S1-3: Pemasangan Motor Stepper NEMA 23 & Sabuk HTD3M
- [ ] Pasang bracket NEMA 23 di tiang kiri frame (h=50 cm).
- [ ] Pasang pulley 20T pada shaft NEMA 23 (Ø6.35mm).
- [ ] Pasang Timing Belt HTD3M dan atur kekencangan sabuk (*tensioning*).
- [ ] Pastikan kedua pulley sejajar (*aligned*) tanpa sudut miring.

#### S1-4: Pemasangan Sistem Pengepresan (Dual Lead Screw T8)
- [ ] Pasang 2 unit lead screw T8 vertikal (kiri dan kanan) ditopang bearing 608ZZ atas-bawah.
- [ ] Pasang pelat penekan aluminium 5mm (dengan 6 pad cetak) ke brass nut T8.
- [ ] Sambungkan motor DC gearbox 12V ke poros penggerak lead screw.
- [ ] Pasang Limit Switch Atas (h=85cm) dan Limit Switch Bawah (h=55cm).
- [ ] Test putar manual: pelat press bergerak naik-turun tegak lurus tanpa macet.

#### S1-5: Pemasangan Corong Hopper & Nozzle Y-Fork
- [ ] Pasang corong hopper SS304 pada rangka paling atas (h=100–130cm).
- [ ] Pasang pintu geser aluminium 3mm dengan solenoid push-pull 12V.
- [ ] Pasang pipa nozzle 6-cabang tepat sejajar di atas masing-masing slot cetakan (pitch 8.5cm).

#### S1-6: Finishing Frame
- [ ] Amplas dan bersihkan kotoran bekas las.
- [ ] Beri cat primer anti karat dan topcoat epoxy food-safe.

#### ✅ DEFINITION OF DONE — Sprint 1
- [ ] Frame berdiri stabil, tidak goyang, dan cat telah kering sempurna.
- [ ] Cetakan rotari 6-slot terpasang pada as Ø20mm dan dapat diputar halus manual.
- [ ] Pelat penekan dapat bergerak naik-turun di sepanjang dual lead screw.
- [ ] Pintu geser hopper membuka dan menutup rapat tanpa tersendat.

---

## SPRINT 2: ELEKTRONIK & UNIT TEST
### Target: Pengujian individual masing-masing modul sensor, aktuator, dan driver
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 2

#### S2-1: Wiring Power Supply & Catu Daya
- [ ] Sambungkan PSU 12V 10A ke jala-jala PLN 220V dengan sakelar pengaman & sekring.
- [ ] Sambungkan input Buck Converter LM2596 ke output 12V PSU.
- [ ] Putar trimpot LM2596 dan ukur tegangan output menggunakan multimeter hingga **tepat 5.05V**.
- [ ] Sambungkan 5V ke pin VIN ESP32 dan hubungkan seluruh GND sistem (*common ground*).

#### S2-2: Unit Test Load Cell 20kg + HX711 (Dosing Timbangan)
- [ ] Sambungkan HX711: DOUT→GPIO 4, SCK→GPIO 5, VCC→5V, GND.
- [ ] Kalibrasi timbangan menggunakan beban referensi (misal 500g dan 1000g).
- [ ] **Kriteria Lulus:** Pembacaan stabil dengan toleransi < ±5 gram. Simpan faktor kalibrasi ke firmware.

#### S2-3: Unit Test NEMA 23 + Driver TB6600 (Rotasi Flip 180°)
- [ ] Konfigurasi DIP Switch TB6600: Microstep = 8 (1600 pulse/rev), Arus = 2.8A.
- [ ] Sambungkan TB6600: STEP→GPIO 12, DIR→GPIO 14, Power→12V.
- [ ] Jalankan kode uji pergerakan 2400 langkah:
  - Motor memutar cetakan dari 0° ke 180° secara halus (akselerasi/deselerasi AccelStepper).
  - Tahan 2 detik, lalu putar balik 2400 langkah ke 0°.
- [ ] **Kriteria Lulus:** Sudut putar tepat 180° (diukur dengan busur/waterpass) tanpa loncat langkah.

#### S2-4: Unit Test Solenoid Elektromagnet & Relay 12V
- [ ] Sambungkan pin kontrol relay ke GPIO 13.
- [ ] Sambungkan terminal kontak relay ke kedua elektromagnet 12V secara paralel.
- [ ] Aktifkan relay: magnet harus menempel sangat kuat pada pelat tutup cetakan (daya tahan gabungan ≥20 kg).
- [ ] Matikan relay: tutup cetakan seketika terlepas bebas.

#### S2-5: Unit Test Motor DC Press + Driver L298N
- [ ] Sambungkan L298N: IN1→GPIO 25, IN2→GPIO 26, VCC→12V.
- [ ] Uji arah putar turun dan naik pelat penekan.
- [ ] Verifikasi proteksi otomatis: motor berhenti seketika saat Limit Switch Bawah (GPIO 33) atau Atas (GPIO 32) tertekan.

#### S2-6: Unit Test Solenoid Gate Hopper
- [ ] Sambungkan relay gate ke GPIO 27.
- [ ] Picu relay ON: solenoid push-pull membuka pintu geser.
- [ ] Picu relay OFF: pegas pengembali (*spring return*) menutup pintu geser dengan rapat.

#### S2-7: Unit Test Tombol START/STOP, LED & Buzzer
- [ ] Uji pembacaan tombol START (GPIO 34) dan STOP (GPIO 35) dengan fungsi debounce.
- [ ] Uji LED Hijau (GPIO 2), LED Merah (GPIO 15), dan Buzzer (GPIO 23).

#### ✅ DEFINITION OF DONE — Sprint 2
- [ ] Seluruh unit test hardware berhasil 100% pada protoboard/kabel panel.
- [ ] Tidak ada tegangan drop atau panas berlebih pada driver TB6600 dan L298N.

---

## SPRINT 3: FIRMWARE & INTEGRASI FSM v9
### Target: State machine otomatis 9-tahap terintegrasi penuh dengan Web Dashboard WiFi
### Durasi: 5–7 hari

---

### 📋 TASK LIST SPRINT 3

#### S3-1: Konfigurasi Pinout & Parameter FSM v9
- [ ] Sesuaikan pin mapping pada `mesin_tempe.ino` (hilangkan deklarasi LCD & HC-SR04).
- [ ] Konfigurasi konstanta gerak:
  - `SLOT_COUNT = 6`
  - `STEPS_180DEG = 2400`
  - `WAKTU_TAHAN_DEFAULT = 5000` (ms)

#### S3-2: Integrasi Finite State Machine 9-Tahap
- [ ] Implementasikan alur:
  `HOMING` → `IDLE` → `DOSING` → `PRESSING` → `LIFT_OFF` → `LOCK_LID` → `ROTATE_MOLD` → `UNLOCK_LID` → `RETURN_MOLD` → `SELESAI`.
- [ ] Pastikan fungsi STOP darurat dapat memotong seluruh state dan mengembalikan mesin ke status aman.

#### S3-3: Integrasi Web Server & REST API
- [ ] Endpoint `/api/status`: mengembalikan JSON status state terkini, berat real-time, counter produksi harian & total.
- [ ] Endpoint `/api/control`: menerima perintah START, STOP, Tare Timbangan, Toggle Magnet, dan Test Rotasi.
- [ ] Endpoint `/api/config`: menerima update target berat per slot dan durasi press.

#### S3-4: Dry Run Integrasi Mekanik
- [ ] Jalankan siklus penuh tanpa kedelai (hanya dengan plastik kosong).
- [ ] Pantau kelancaran gerakan mekanik dari web dashboard smartphone.

#### ✅ DEFINITION OF DONE — Sprint 3
- [ ] Siklus otomatis berjalan mulus dari awal hingga akhir tanpa intervensi kode manual.
- [ ] Dashboard web dapat diakses lancar via WiFi lokal dan memperbarui data secara real-time.

---

## SPRINT 4: SYSTEM TEST & KALIBRASI DOSING
### Target: Pengujian dengan kedelai sungguhan dan kalibrasi berat per slot
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 4

#### S4-1: Kalibrasi Aliran Corong Kedelai
- [ ] Isi corong dengan 5 kg kedelai.
- [ ] Uji pembukaan gate: amati apakah kedelai terbagi rata ke 6 cabang nozzle pipa Y-Fork.
- [ ] Jika aliran tidak rata, sesuaikan sudut kemiringan corong atau pasang sekat pemandu internal.

#### S4-2: Kalibrasi Setpoint Berat Timbangan (Dosing Offset)
- [ ] Set target berat: 900 gram (6 slot × 150 gram).
- [ ] Ukur waktu tunda (*cutoff delay*) dari penutupan solenoid hingga butiran terakhir jatuh (*in-flight compensation*).
- [ ] Lakukan 10 kali siklus penimbangan berturut-turut: target deviasi total < ±15 gram.

#### S4-3: Uji Pengepresan & Pembalikan Rotari
- [ ] Masukkan plastik dan kedelai ke 6 slot.
- [ ] Jalankan siklus press (5 detik tahan) → amati kepadatan balok tempe.
- [ ] Jalankan pembalikan 180°: pastikan elektromagnet menahan tutup dengan kokoh.
- [ ] Verifikasi pelepasan: tempe harus terlepas sempurna ke atas alas ancak bambu.

#### ✅ DEFINITION OF DONE — Sprint 4
- [ ] 6 balok tempe terbentuk rapi dan padat dengan variasi berat antar slot < 5%.
- [ ] Tidak ada tumpahan kedelai di luar area cetakan selama proses flip 180°.

---

## SPRINT 5: UJI COBA PRODUKSI PENUH
### Target: Mesin siap digunakan untuk produksi harian berkelanjutan
### Durasi: 3–5 hari

---

### 📋 TASK LIST SPRINT 5

#### S5-1: Uji Ketahanan Operasional (Endurance Run)
- [ ] Jalankan produksi berturut-turut selama 50 batch (total 300 balok tempe).
- [ ] Catat cycle time rata-rata per batch (target: < 75 detik).
- [ ] Cek suhu driver TB6600, L298N, dan motor penggerak.

#### S5-2: SOP Operator & Pelabelan Panel
- [ ] Tempel label petunjuk tombol START, STOP, dan lampu indikator pada panel ABS.
- [ ] Buat ringkasan SOP 1 lembar: cara koneksi WiFi, cara kalibrasi tare, dan prosedur pembersihan harian (*washdown*).

#### ✅ DEFINITION OF DONE — Sprint 5
- [ ] Mesin lolos uji 50 batch tanpa kegagalan mekanik atau error sistem.
- [ ] Mesin siap diserahterimakan untuk operasional pabrik tempe.
