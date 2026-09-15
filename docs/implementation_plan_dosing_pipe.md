# Implementasi Pipa Dosing, Gate Buka-Tutup & Anti-Tumpah Saat Press
## Implementation Plan v1 — Sistem Pipa Hopper + Sliding Gate + Containment Press

> **Tanggal**: 15 September 2026  
> **Status**: DRAFT v1 — Siap untuk Review & Fabrikasi  
> **Referensi Desain Pengguna**: Ujung pipa bercabang dua (seperti portafilter mesin kopi) + gate hopper bisa lepas dari pipa bawah  
> **Konteks**: Addendum dari `implementation_plan_final.md` (v8, 5-Slot Serentak)

---

## BAGIAN 1: SISTEM PIPA HOPPER (DOSING PIPE ASSEMBLY)

### 1.1 Konsep Utama

Mengadopsi konsep **portafilter mesin espresso**: pipa tunggal bercabang dua di ujungnya. Kedelai tersebar merata ke sepanjang slot mold (bukan menumpuk di satu titik tengah).

```
HOPPER
  |
  | (pipa lurus SS316L Ø35mm)
  |
  +-- [GATE SLIDING] -- titik pemisah buka/tutup
  |
  | (pipa bawah, FIXED ke frame)
  |
 / \  <- Y-FORK NOZZLE (seperti portafilter kopi)
/   \
[<-S1->] <- kedelai tersebar ke 2 titik di sepanjang slot 21.3cm
```

**Kenapa Y-Fork?**
- Slot panjang 21.3cm, lebar 6.6cm — kalau 1 titik jatuh tengah, kedelai menumpuk di tengah
- Y-fork membagi aliran ke 2 titik (±5cm dari masing-masing ujung) — distribusi merata
- Proven di: portafilter espresso dual spout, multi-head granule dispenser industri, feed cattle trough

---

### 1.2 Spesifikasi Pipa Dosing

```
Pipa Vertikal (Hopper -> Gate -> Mold):
  Material  : SS316L food-grade
  Diameter  : Ø35mm (dalam) / Ø38mm (luar) — 1.5mm dinding
  Panjang   : ±400mm (dari gate ke ujung nozzle)
  Jumlah    : 5 pipa (satu per slot)
  Jarak sumbu: 85mm center-to-center (mengikuti jarak antar slot mold)
  Finishing : Dilas ke manifold plate bawah gate (food-grade weld)

Y-Fork Nozzle (ujung bawah tiap pipa):
  Material       : SS316L, dibentuk dari pipa Ø35mm yang dilas bifurkasi
  Sudut fork     : 35-40° dari sumbu vertikal (agar aliran lancar, tidak macet)
  Panjang cabang : 80mm per cabang
  Jarak antar ujung fork: ±100mm (slot 21.3cm / 2 titik)
  Ujung nozzle   : dipotong miring 45° (cut bevel) — aliran lebih lebar, tidak menumpuk

POSISI Y-FORK TERHADAP SLOT (tampak atas):
+--------------------------------+
|         SLOT (21.3cm)          |
|   v fork A       fork B v      |
|  [~4cm dari depan] [~4cm dari belakang]
+--------------------------------+
-> Kedelai jatuh di 2 titik = distribusi merata
```

---

### 1.3 Manifold Plate (Plat Penghubung Pipa-Pipa)

```
MANIFOLD PLATE SS316L:
  Dimensi : 52cm x 6cm x 4mm tebal
  5 lubang Ø35mm dengan jarak 85mm c-to-c
  Fungsi  : Menyatukan 5 pipa menjadi 1 unit yang bisa diangkat/dilepas
  Dipasang TETAP ke frame mesin dengan 4 baut M8
  Gate sliding bergerak DI ATAS manifold plate

KEUNTUNGAN MANIFOLD:
  - Bisa dilepas sebagai 1 unit untuk dibersihkan
  - Pipa + nozzle bisa di-sanitize dengan merendam di larutan NaOH
  - Tidak perlu bongkar seluruh mesin
```

---

## BAGIAN 2: GATE BUKA-TUTUP (SLIDING GATE SYSTEM)

### 2.1 Konsep Desain Gate

Sesuai sketsa pengguna: **gate berupa plat yang menutup antara hopper dan pipa** (bisa tutup tanpa nyambung ke pipa di bawah). Gate berada di **antara hopper bottom dan manifold plate top**.

```
POTONGAN SAMPING - MEKANISME GATE:

HOPPER (SS304)
\_________/
     |||||          <- 5 outlet hopper
-----+++++---------  <- GATE PLATE (geser horizontal ±30mm)
     |||||          <- 5 inlet manifold plate
================    <- MANIFOLD PLATE (FIXED)
  /\  /\  /\       <- Y-fork nozzle

GATE TERTUTUP:
     ooooo          <- 5 lubang gate TIDAK sejajar dengan outlet hopper
-----XXXXX---------  <- plat solid menutupi outlet -> tidak ada flow

GATE TERBUKA:
     ooooo          <- 5 lubang gate SEJAJAR dengan outlet hopper
-----ooooo---------  <- kedelai mengalir bebas ke pipa di bawah
```

**Konsep "bisa tutup tidak nyambung ke pipa di bawah":**
- Gate bisa menutup SEMPURNA tanpa terpasang mekanis ke pipa bawah
- Solusi: antara gate plate dan manifold plate diberi **seal strip silikon Ø2mm** mengitari tiap lubang
- Saat gate tutup → silikon menekan → zero leakage
- Saat gate buka → geser bebas, silikon tidak menghambat

---

### 2.2 Spesifikasi Gate Plate

```
GATE PLATE SS316L:
  Dimensi     : 55cm x 5cm x 3mm tebal
  5 lubang    : Ø35mm, spasi 85mm c-to-c (SAMA PERSIS dengan manifold)
  Travel geser: ±30mm (satu arah saja)
    - Posisi TUTUP: lubang gate offset 30mm dari lubang manifold
    - Posisi BUKA : lubang gate tepat sejajar lubang manifold
  Material rel: 2 batang SS304 Ø8mm (kiri dan kanan gate plate)
  Stopper     : 2 baut M5 sebagai hard stop posisi BUKA dan TUTUP

SEAL ANTI-BOCOR:
  Silikon strip food-grade (PTFE-coated silicone) mengelilingi tiap lubang manifold
  Dipasang di permukaan atas manifold, gate sliding di atasnya
  Ketebalan seal: 1.5mm — cukup untuk seal tanpa hambat gerak gate
  Ganti seal    : lepas manifold, silikon tempel — sangat mudah
```

---

### 2.3 Aktuator Gate

**Rekomendasi: Solenoid 12V Push-Pull (lebih baik dari servo)**

| Aspek | Servo MG996R | Solenoid 12V Push-Pull |
|---|---|---|
| Harga | Rp 35K | Rp 45–65K |
| Kecepatan tutup | ~200ms | ~50ms (lebih cepat) |
| Fail-safe (mati listrik) | **Tidak** (posisi terakhir) | **Ya** (spring menutup) |
| Keandalan | Perlu kalibrasi periodik | Sangat tinggi (>1jt siklus) |
| **Rekomendasi** | Boleh | **Lebih direkomendasikan** |

**Kenapa solenoid lebih baik?** → `spring return = fail-safe`: mati listrik = otomatis tutup → kedelai tidak tumpah.

### 2.4 Siklus Kerja Gate

```
[START] -> [Gate TERBUKA] -> [Kedelai mengalir via Y-fork]
       -> [Load cell baca berat total]
       -> [Berat >= target - offset 10g?] -> [Gate TERTUTUP]
       -> [Tunggu 500ms - sisa pipa jatuh]
       -> [Fold bar aktif] -> [Press plate turun]
```

---

## BAGIAN 3: ANTI-TUMPAH SAAT PRESS (CONTAINMENT SYSTEM)

### 3.1 Analisis Masalah

Saat press plate menekan kedelai, tekanan mendorong ke segala arah:
1. **Kedelai tumpah ke luar slot** melalui celah atas (sebelum plastik terlipat sempurna)
2. **Plastik terdorong ke samping** dan keluar dari slot
3. **Kedelai masuk ke sela antar-slot** dan menempel di dinding pemisah

### 3.2 Solusi: Raised Collar + Guided Press Plate

```
DESAIN CETAKAN DENGAN RAISED COLLAR:

SEBELUM:              SETELAH (DIREKOMENDASIKAN):

[press plate]           [press plate] <- chamfer 45° di tepi
      v                       v v
+-----------+          +--+-------+--+  <- collar 5cm di atas isi
|  kedelai  |          |  | kedelai|  |
|           |          |  |        |  |
+-----------+          +--+--------+--+
v kedelai bisa         v press plate masuk KE DALAM collar
  keluar atas            kedelai terkurung, tidak bisa keluar

SPESIFIKASI COLLAR:
  Material  : SS304, sambungan las ke dinding slot
  Tinggi collar di atas isi: 5cm
  Total tinggi slot + collar : 3.6cm (isi) + 5cm (collar) = 8.6cm
  Press plate bergerak di DALAM collar (clearance 1.5mm per sisi)
```

### 3.3 Press Pad — Dimensi Disesuaikan

```
DIMENSI TIAP PAD PRESS (masuk ke dalam collar slot):
  Lebar  : 6.0cm (slot 6.6cm - clearance 3mm per sisi x 2)
  Panjang: 20.5cm (slot 21.3cm - clearance 4mm total)
  Tinggi : 3cm
  Material: Aluminium 6061 T6
  Tepi chamfer: 45° x 5mm di semua sudut bawah -> mudah masuk collar
  Gasket: silikon strip food-grade di tepi bawah tiap pad

GANTRY BAR PRESS (penghubung 5 pad):
  Material: Besi hollow kotak 40x40mm tebal 2mm
  Panjang : 55cm
  Sambungan ke lead screw: 2 titik simetris (kiri dan kanan)
```

### 3.4 Urutan Press yang Aman (Anti-Tumpah)

```
STEP 1: Kedelai diisi via pipa (gate tutup setelah berat tercapai)
STEP 2: Fold bar DEPAN terangkat 90° -> plastik sisi depan naik
STEP 3: Fold bar BELAKANG terangkat 90° -> plastik sisi belakang naik
        ** Setelah kedua bar naik -> plastik menutupi atas kedelai
           Kedelai terkurung oleh plastik + collar -> TIDAK BISA TUMPAH **
STEP 4: Press plate TURUN -> masuk ke dalam collar -> tekan plastik + kedelai
STEP 5: Motor STOP -> buzzer bunyi 3x -> operator angkat cetakan
STEP 6: Press naik -> fold bars turun -> siap siklus berikutnya
```

---

## BAGIAN 4: BILL OF MATERIALS — TAMBAHAN

### 4.1 Komponen Sistem Pipa

| No | Komponen | Spesifikasi | Qty | Harga | Total |
|----|----------|-------------|-----|-------|-------|
| 1 | Pipa SS316L | Ø38mm × 400mm | 5 pcs | Rp 25K | Rp 125K |
| 2 | Y-Fork Nozzle | SS316L, custom las | 5 pcs | Rp 30K | Rp 150K |
| 3 | Manifold Plate | SS316L 55×6×0.4cm | 1 pcs | Rp 75K | Rp 75K |
| 4 | Gate Plate | SS316L 55×5×0.3cm | 1 pcs | Rp 55K | Rp 55K |
| 5 | Rel Gate | SS304 rod Ø8mm × 60cm | 2 pcs | Rp 15K | Rp 30K |
| 6 | Seal strip silikon | Food-grade PTFE, Ø2mm | 1.5m | Rp 20K/m | Rp 30K |
| 7 | Solenoid 12V | Travel 20mm, spring return | 1 pcs | Rp 55K | Rp 55K |
| 8 | MOSFET/Relay module | Untuk switch solenoid | 1 pcs | Rp 12K | Rp 12K |
| | | | | **SUBTOTAL** | **Rp 532K** |

### 4.2 Komponen Anti-Tumpah Press

| No | Komponen | Spesifikasi | Qty | Harga | Total |
|----|----------|-------------|-----|-------|-------|
| 9 | Raised Collar SS304 | Strip las ke slot, tinggi 5cm | 10 strip | Rp 20K | Rp 200K |
| 10 | Press Pad Aluminium | 6061 T6, 6×20.5×3cm | 5 pcs | Rp 40K | Rp 200K |
| 11 | Gantry Press Bar | Besi hollow 40×40mm, 55cm | 1 pcs | Rp 45K | Rp 45K |
| 12 | Baut M6 + mur SS | Pad ke gantry | 10 set | Rp 3K | Rp 30K |
| 13 | Gasket silikon pad | Strip 5mm per pad | 5 pad | Rp 10K | Rp 50K |
| | | | | **SUBTOTAL** | **Rp 525K** |

**TOTAL UPGRADE PIPA + ANTI-TUMPAH: ≈ Rp 1.057.000**

---

## BAGIAN 5: PROSES FABRIKASI

```
TAHAP A: Pipa & Nozzle (1-2 hari bengkel stainless)
  A1. Potong 5 pipa SS316L Ø38mm masing-masing 400mm
  A2. Las Y-fork di ujung bawah (TIG welding, sudut 35-40°)
  A3. Bevel cut ujung nozzle 45°
  A4. Buat manifold plate: bor 5 lubang Ø35mm spasi 85mm
  A5. Las 5 pipa ke manifold plate (tegak, lurus)
  A6. Polish semua permukaan dalam pipa (halus, tidak ada kasar)

TAHAP B: Gate (0.5 hari)
  B1. Potong gate plate SS316L 55×5cm, bor 5 lubang Ø35mm
  B2. Pasang rel SS304 Ø8mm di kiri dan kanan gate
  B3. Uji geser gate manual: mulus ±30mm
  B4. Pasang seal silikon di permukaan atas manifold
  B5. Pasang solenoid + linkage ke pin gate
  B6. Uji buka-tutup 12V: cek kebocoran saat tutup

TAHAP C: Raised Collar + Press Pad (1 hari)
  C1. Las strip SS304 tinggi 5cm di sekeliling tiap slot mold
  C2. Cek dimensi dalam collar: 6.6cm × 21.3cm (clearance 3mm total)
  C3. Buat 5 press pad aluminium 6061: 6.0×20.5×3cm
  C4. Chamfer semua tepi bawah 45°×5mm
  C5. Pasang gasket silikon di tepi bawah tiap pad
  C6. Baut pad ke gantry bar (posisi tepat di atas tiap slot)
  C7. Uji pad masuk ke collar: mulus tanpa kocak berlebih

TAHAP D: Integrasi & Uji (0.5 hari)
  D1. Pasang manifold+pipa ke frame (4 baut M8)
  D2. Pasang hopper di atas gate
  D3. Uji aliran dengan beras kecil (simulasi kedelai)
  D4. Cek distribusi: timbang per slot setelah 10 siklus
  D5. Kalibrasi solenoid timing di firmware ESP32
```

---

## BAGIAN 6: FIRMWARE ESP32 — TAMBAHAN LOGIC

```cpp
// Pin solenoid gate (via MOSFET/relay)
#define GATE_PIN  26  // GPIO26 -> MOSFET -> solenoid 12V

void openGate() {
  digitalWrite(GATE_PIN, HIGH);  // Solenoid ON -> gate terbuka
  Serial.println("[GATE] OPEN");
}

void closeGate() {
  digitalWrite(GATE_PIN, LOW);   // Solenoid OFF -> spring menutup
  delay(500);                    // Tunggu 500ms sisa kedelai di pipa jatuh
  Serial.println("[GATE] CLOSED");
}

void dosingCycle(float targetGramsPerSlot) {
  float targetTotal = targetGramsPerSlot * 5;
  
  openGate();
  
  while (true) {
    float current = readLoadCell();
    if (current >= targetTotal - 10.0) {  // Offset 10g (sisa di pipa)
      closeGate();
      break;
    }
    delay(50);
  }
}

void fullCycle() {
  dosingCycle(200.0);   // Target 200g per slot
  foldBarsUp();         // Lipat plastik
  delay(1500);
  pressDown();          // Tekan
  waitPressComplete();
  buzzerBeep(3);        // Selesai
  pressUp();
  foldBarsDown();
}
```

---

## BAGIAN 7: CHECKLIST VALIDASI

### Gate & Pipa
- [ ] Gate bergerak mulus di relnya (tidak macet)
- [ ] Seal silikon tidak bocor saat gate tutup (uji 500g beras, tunggu 1 menit)
- [ ] Solenoid merespon sinyal 12V (<100ms)
- [ ] Spring return berfungsi (gate tutup sendiri saat solenoid OFF)
- [ ] Y-fork mendistribusikan ke 2 titik per slot (cek visual)
- [ ] Distribusi antar slot merata (toleransi ±15% per slot)
- [ ] Manifold bisa dilepas/dipasang dalam <5 menit untuk sanitasi

### Anti-Tumpah Press
- [ ] Press pad masuk ke collar slot tanpa tersangkut
- [ ] Tidak ada kedelai yang keluar dari slot saat press (5 siklus)
- [ ] Gasket silikon tetap seal saat press di posisi bawah
- [ ] Gantry bar press tidak melengkung saat tekan penuh

---

## RINGKASAN UPGRADE

| Masalah | Solusi | Biaya |
|---------|--------|-------|
| Kedelai menumpuk di tengah slot | Y-Fork Nozzle (portafilter-style) | Rp 150K |
| Gate bocor / tetes saat tutup | Seal silikon PTFE di manifold | Rp 30K |
| Servo gate bisa gagal | Solenoid 12V dengan spring return (fail-safe) | Rp 55K |
| Kedelai tumpah saat press | Raised Collar 5cm + Press Pad Guided | Rp 400K |
| **TOTAL UPGRADE** | | **≈ Rp 685K–1.1jt** |

> Dokumen ini adalah addendum dari `implementation_plan_final.md` dan harus dibaca bersamaan.
