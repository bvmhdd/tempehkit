# 🚀 Project Execution Plan — TempehKit v13 (Opsi 2 Final)
## Hardware Agile Roadmap (Sprint 0–5)

> **Status Terkini:** **Sprint 2 (Bench Test 7 Modul Elektronik) 100% LULUS!**
> Desain mekanik & CAD 3D telah difinalisasi ke **v13 (Opsi 2: Laci Elevator 75 mm)** dan siap masuk tahap pengadaan lanjutan & fabrikasi rangka.

---

## Ringkasan Progres Sprint

| Sprint | Fokus Pekerjaan | Status |
|:---|:---|:---:|
| **Sprint 0** | Desain Final v13, CAD 3D & Daftar Belanja Awal | ✅ **SELESAI** *(CAD v13 + Elektronik Inti Lengkap)* |
| **Sprint 2** | Unit Test Meja (*Bench Testing* 7 Modul Elektronik) | ✅ **LULUS 100%** |
| **Sprint 1** | Pengadaan Mekanik/Rel + Fabrikasi Rangka & SS304 | ⏳ **TAHAP BERIKUTNYA** |
| **Sprint 3** | Integrasi Full Firmware + Web Dashboard + Laci Elevator | ⏳ **SIAP DIUJI MEJA** |
| **Sprint 4** | Uji Coba & Kalibrasi dengan Kedelai Asli + Plastik Berlubang | ⬜ Menunggu Rangka |
| **Sprint 5** | Endurance Run 50 Batch & SOP Produksi UKM | ⬜ Menunggu Sprint 4 |

---

## SPRINT 2 — BENCH TEST ELEKTRONIK (✅ LULUS 100%)
- [x] PSU 12V 10A + Step-Down LM2596 (`5.0V` stabil)
- [x] ESP32 DevKit V1 + Tombol START/STOP + LED + Buzzer
- [x] Load Cell 20 kg + Modul HX711 (kalibrasi berhasil)
- [x] Servo Gate Hopper MG996R (`0°–90°`)
- [x] Linear Actuator 12V + Driver L298N + Limit Switch Atas & Bawah
- [x] Stepper NEMA 23 (`23HS5628`) + Driver TB6600 (`2400 step = 180°`)
- [x] 2× Solenoid Elektromagnet P25/20 + Modul Relay

---

## SPRINT 1 (NEXT) — PENGADAAN LANJUTAN & FABRIKASI RANGKA v13
Acuan: [`docs/bom_belanja.md`](bom_belanja.md), [`docs/dimensi_mekanik.md`](dimensi_mekanik.md), & [`cad/viewer_3d_v13.html`](../cad/viewer_3d_v13.html)

### 1. Pengadaan Komponen Tambahan (Opsi 2)
- [ ] Order **Mini Linear Actuator 12V Stroke 100 mm (300N)** + Relay 2-Ch (Laci Elevator)
- [ ] Order **Motor Getar DC 12V** + MOSFET/Relay (*Vibro-Levelling*)
- [ ] Order **Rel Laci Double Track Stainless** (`30 cm` ×1 psg, `35–40 cm` ×1 psg, *Non Soft-Close*)
- [ ] Order **Linear Shaft** (`Ø12 mm` press, `Ø16 mm` rel X, `Ø10 mm` laci) + Bushing & Support
- [ ] Order **Lembaran Silikon Food-Grade 5 mm** (Shore A 45) & **Belt HTD3M-384 + Pulley 20T (Bore 8mm) / 60T**
- [ ] *(Jika pilih Full-Auto)* Order 2× NEMA 17 + Driver + Belt GT2 + 2× Servo + PCA9685 + XL4015 5A

### 2. Fabrikasi Bengkel Las & Stainless SS304
- [ ] Potong & las rangka hollow `40×40×2.0 mm` (`900 × 1420 × 640 mm`) sesuai daftar potong di `bom_belanja.md`
- [ ] Pasang rak bawah (Panel ABS & PSU + dudukan tengah Mini Actuator 300N)
- [ ] Pasang Bearing UCFL 204 (`h=560`), Bracket NEMA 23, dan Sub-Frame Laci Elevator (`Y=445↔520`)
- [ ] Fabrikasi Cetakan 6-Slot SS304 (`591×240×36 mm`, Stub-Axle luar, lubang angin Ø3 mm, Rel Selip L-Channel)
- [ ] Fabrikasi Hopper Trapesium + Corong Celah `200 mm` + Kotak Takar Clamshell `58×200×70 mm`
- [ ] Finishing cat primer + epoxy food-safe

---

## SPRINT 3 — INTEGRASI FIRMWARE & WEB DASHBOARD
- [ ] Update `WIFI_SSID`, `WIFI_PASSWORD`, dan `LOADCELL_FAKTOR` di `firmware/mesin_tempe/mesin_tempe.ino`
- [ ] Upload `firmware/mesin_tempe/data/index.html` ke SPIFFS ESP32
- [ ] Uji 1 siklus penuh (*Full Bench Dry-Run*) via Serial Console (`?`) & Web Dashboard HP
- [ ] Tambahkan kontrol pin **Motor Getar 12V** dan **Mini Actuator Laci Elevator (Naik/Turun 75 mm)** ke FSM

---

## SPRINT 4 & 5 — KALIBRASI KEDELAI ASLI & UJI PRODUKSI
- [ ] Kalibrasi takaran `250 g/slot` di Load Cell Stasioner (deviasi `< ±5 g`)
- [ ] Uji tebar rata 200 mm + durasi getar (`1–2 dtk`) + ketebalan tekan Limit Switch Bawah (`35 mm`)
- [ ] Uji lipat plastik berlubang 1-per-1 + Press Pad Silikon + Flip 180° + Laci Elevator Turun `-75 mm`
- [ ] Uji ketahanan (*endurance run*) 50 batch (300 tempe) tanpa macet atau tumpah
