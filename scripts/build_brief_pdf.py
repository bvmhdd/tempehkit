import base64
import os
import subprocess
import time

def get_b64(rel_path):
    full_path = os.path.join(os.path.dirname(__file__), rel_path)
    with open(full_path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

img_cetakan = get_b64('../assets/cetakan_referensi.jpg')
img_mesin = get_b64('../assets/mesin_tempe_design.jpg')
img_wiring = get_b64('../assets/wiring_diagram_esp32.jpg')

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Execution Brief — Mesin Pencetak Tempe Otomatis</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: A4 portrait;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #e2e8f0;
    color: #1e293b;
    font-size: 8.5pt;
    line-height: 1.45;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page {{
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 14mm 16mm 10mm 16mm;
    margin: 0 auto 15px auto;
    background: #ffffff;
    position: relative;
    overflow: hidden;
    page-break-after: always;
    page-break-inside: avoid;
    display: flex;
    flex-direction: column;
  }}

  @media print {{
    body {{
      background: transparent;
    }}
    .page {{
      margin: 0;
      width: 210mm;
      height: 297mm;
      page-break-after: always;
      page-break-inside: avoid;
    }}
    .page:last-child {{
      page-break-after: avoid;
    }}
  }}

  /* Page Header */
  .p-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 2px solid #0f172a;
    margin-bottom: 12px;
  }}
  .p-header-left {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .p-header-num {{
    background: #0f172a;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
  }}
  .p-header-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
  }}
  .p-header-tag {{
    font-size: 7.5pt;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  /* Page Footer */
  .p-footer {{
    margin-top: auto;
    padding-top: 6px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7pt;
    color: #94a3b8;
  }}
  .p-footer strong {{
    color: #475569;
  }}

  /* Typography */
  h1, h2, h3, h4 {{
    color: #0f172a;
    font-weight: 700;
  }}
  .section-title {{
    font-size: 8.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0369a1;
    margin: 8px 0 6px 0;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .section-title::before {{
    content: '';
    display: inline-block;
    width: 4px;
    height: 11px;
    background: #0284c7;
    border-radius: 2px;
  }}

  /* Cover Page Styling */
  .page-cover {{
    padding: 0;
    background: linear-gradient(135deg, #091219 0%, #0f1e2b 50%, #162c3d 100%);
    color: white;
    position: relative;
  }}
  .cover-decor-1 {{
    position: absolute;
    top: -80px;
    right: -80px;
    width: 380px;
    height: 380px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(56, 189, 248, 0) 70%);
  }}
  .cover-decor-2 {{
    position: absolute;
    bottom: -100px;
    left: -100px;
    width: 420px;
    height: 420px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(34, 197, 94, 0.12) 0%, rgba(34, 197, 94, 0) 70%);
  }}
  .cover-content {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24mm 20mm 18mm 20mm;
  }}
  .cover-badge-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .cover-badge {{
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}
  .cover-date {{
    font-size: 8.5pt;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
  }}
  .cover-main {{
    margin: auto 0;
  }}
  .cover-tag {{
    font-size: 9pt;
    font-weight: 700;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
  }}
  .cover-title {{
    font-size: 32pt;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -1.2px;
    margin-bottom: 12px;
    color: #ffffff;
  }}
  .cover-desc {{
    font-size: 11pt;
    font-weight: 400;
    color: #cbd5e1;
    max-width: 580px;
    line-height: 1.6;
    margin-bottom: 28px;
  }}
  .cover-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 24px;
  }}
  .c-box {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px 14px;
  }}
  .c-box-label {{
    font-size: 7pt;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
  }}
  .c-box-val {{
    font-size: 14pt;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
  }}
  .c-box-sub {{
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 2px;
  }}
  .cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8pt;
    color: #94a3b8;
  }}

  /* Content Cards & Boxes */
  .card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 8px;
  }}
  .card-highlight {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
  }}
  .card-info {{
    background: #f0f9ff;
    border: 1px solid #bae6fd;
  }}

  /* Tables */
  table.compact-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.5pt;
    margin-bottom: 8px;
  }}
  table.compact-table th {{
    background: #0f172a;
    color: #ffffff;
    text-align: left;
    padding: 5px 7px;
    font-weight: 600;
    font-size: 7.2pt;
    letter-spacing: 0.3px;
  }}
  table.compact-table th:first-child {{ border-radius: 4px 0 0 0; }}
  table.compact-table th:last-child {{ border-radius: 0 4px 0 0; }}
  table.compact-table td {{
    padding: 4.5px 7px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: middle;
  }}
  table.compact-table tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  /* Badges */
  .badge {{
    display: inline-block;
    padding: 1.5px 6px;
    border-radius: 4px;
    font-size: 6.8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .badge-red {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }}
  .badge-yellow {{ background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }}
  .badge-green {{ background: #dcfce7; color: #15803d; border: 1px solid #86efac; }}
  .badge-blue {{ background: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }}

  /* Visual Step Workflow */
  .workflow-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    margin: 6px 0 10px 0;
  }}
  .wf-step {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    position: relative;
  }}
  .wf-num {{
    position: absolute;
    top: 6px;
    right: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    font-weight: 800;
    color: #0284c7;
  }}
  .wf-title {{
    font-size: 8pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 3px;
    padding-right: 20px;
  }}
  .wf-desc {{
    font-size: 7.2pt;
    color: #64748b;
    line-height: 1.35;
  }}

  /* Gantt Chart */
  .gantt-wrap {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 10px;
    margin-bottom: 10px;
  }}
  .gantt-row {{
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    font-size: 7.5pt;
  }}
  .gantt-label {{
    width: 135px;
    font-weight: 600;
    color: #1e293b;
    flex-shrink: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .gantt-timeline {{
    flex: 1;
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 3px;
    align-items: center;
    height: 16px;
  }}
  .g-col-head {{
    text-align: center;
    font-size: 6.8pt;
    font-weight: 700;
    color: #64748b;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
  }}
  .g-bar {{
    height: 12px;
    border-radius: 3px;
    background: linear-gradient(90deg, #0284c7, #38bdf8);
  }}
  .g-bar-mech {{
    background: linear-gradient(90deg, #d97706, #fbbf24);
  }}
  .g-bar-elec {{
    background: linear-gradient(90deg, #0284c7, #38bdf8);
  }}
  .g-bar-soft {{
    background: linear-gradient(90deg, #7c3aed, #a855f7);
  }}
  .g-bar-test {{
    background: linear-gradient(90deg, #16a34a, #4ade80);
  }}

  /* Phase Detail Cards */
  .phase-box {{
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 8px;
    background: #ffffff;
  }}
  .phase-top {{
    background: #0f172a;
    color: #ffffff;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .phase-top-title {{
    font-size: 8.5pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .phase-badge {{
    font-size: 7pt;
    font-weight: 700;
    background: rgba(56, 189, 248, 0.2);
    color: #38bdf8;
    padding: 2px 8px;
    border-radius: 10px;
    border: 1px solid rgba(56, 189, 248, 0.3);
  }}
  .phase-body {{
    padding: 8px 10px;
  }}
  .p-item {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 7.6pt;
    color: #334155;
    margin-bottom: 3px;
  }}
  .p-check {{
    width: 11px;
    height: 11px;
    border: 1.5px solid #94a3b8;
    border-radius: 2px;
    flex-shrink: 0;
    margin-top: 1.5px;
  }}

  /* Budget summary cards */
  .budget-cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 8px;
  }}
  .b-card {{
    border-radius: 6px;
    padding: 8px 10px;
    text-align: center;
  }}
  .b-card-blue {{ background: #f0f9ff; border: 1px solid #bae6fd; }}
  .b-card-amber {{ background: #fffbeb; border: 1px solid #fde68a; }}
  .b-card-green {{ background: #f0fdf4; border: 1px solid #bbf7d0; }}
  .b-card-label {{ font-size: 6.8pt; font-weight: 700; text-transform: uppercase; color: #64748b; }}
  .b-card-val {{ font-size: 13pt; font-weight: 800; line-height: 1.2; margin: 2px 0; }}
  .b-card-sub {{ font-size: 6.8pt; color: #64748b; }}

  /* Checklist box */
  .chk-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }}
  .chk-col {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 10px;
  }}
  .chk-head {{
    font-size: 7.8pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .chk-item {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 7.3pt;
    color: #334155;
    margin-bottom: 3.5px;
  }}
  .chk-box {{
    width: 11px;
    height: 11px;
    border: 1.5px solid #64748b;
    border-radius: 2px;
    flex-shrink: 0;
    margin-top: 1.5px;
  }}

  /* Risk box */
  .risk-card {{
    background: #fff1f2;
    border-left: 3px solid #e11d48;
    border-radius: 0 5px 5px 0;
    padding: 5px 8px;
    margin-bottom: 5px;
  }}
  .risk-title {{
    font-size: 7.5pt;
    font-weight: 700;
    color: #be123c;
  }}
  .risk-desc {{
    font-size: 7.1pt;
    color: #475569;
    margin-top: 1px;
  }}
</style>
</head>
<body>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 1: COVER PAGE                                   ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page page-cover">
  <div class="cover-decor-1"></div>
  <div class="cover-decor-2"></div>
  <div class="cover-content">
    <div class="cover-badge-row">
      <span class="cover-badge">IoT &bull; Otomasi Pabrik Pangan UKM</span>
      <span class="cover-date">Doc Ref: PB-TEMPE-2026-V1</span>
    </div>

    <div class="cover-main">
      <div class="cover-tag">Project Execution Brief &amp; Blueprint</div>
      <h1 class="cover-title">Mesin Pencetak<br>Tempe Semi-Otomatis</h1>
      <p class="cover-desc">
        Sistem otomasi pencetakan tempe 6-slot simultan berbasis ESP32, mekanisme <em>Lift-Off Mold Frame</em> (tanpa balik), kontrol presisi beban dosis, penekanan bermotor, dan monitoring real-time via Web Dashboard Wi-Fi.
      </p>

      <div class="cover-grid">
        <div class="c-box">
          <div class="c-box-label">Durasi Proyek</div>
          <div class="c-box-val">6 Minggu</div>
          <div class="c-box-sub">Fabrikasi mekanik &amp; IoT paralel</div>
        </div>
        <div class="c-box">
          <div class="c-box-label">Total Anggaran</div>
          <div class="c-box-val">&plusmn; Rp 1,25 Juta</div>
          <div class="c-box-sub">Elektronik + Mekanik + Jasa Las</div>
        </div>
        <div class="c-box">
          <div class="c-box-label">Target Kapasitas</div>
          <div class="c-box-val">144&ndash;180</div>
          <div class="c-box-sub">Tempe per jam (24&ndash;30 papan)</div>
        </div>
        <div class="c-box">
          <div class="c-box-label">Mikrokontroler</div>
          <div class="c-box-val">ESP32 38-Pin</div>
          <div class="c-box-sub">Web Server + SPIFFS UI</div>
        </div>
        <div class="c-box">
          <div class="c-box-label">Dimensi Cetakan</div>
          <div class="c-box-val">6 Slot Simultan</div>
          <div class="c-box-sub">Slot: 21.3 &times; 6.6 &times; 3.6 cm</div>
        </div>
        <div class="c-box">
          <div class="c-box-label">Bahan Kemasan</div>
          <div class="c-box-val">12 &times; 35 cm</div>
          <div class="c-box-sub">Plastik perforasi + Ancak bambu</div>
        </div>
      </div>
    </div>

    <div class="cover-footer">
      <div>Pabrik Tempe Keluarga &nbsp;|&nbsp; <strong>Divisi Otomasi &amp; Modernisasi Alat</strong></div>
      <div>Status: <strong>FINAL &bull; SIAP EKSEKUSI</strong> (September 2026)</div>
    </div>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 2: RINGKASAN & MEKANISME KERJA                  ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">01</span>
      <span class="p-header-title">Ringkasan Eksekutif &amp; Mekanisme Inovasi Alat</span>
    </div>
    <span class="p-header-tag">Overview &bull; Konsep</span>
  </div>

  <div class="section-title">Latar Belakang &amp; Solusi Inovasi</div>
  <div class="card card-info" style="margin-bottom:8px;">
    <p style="font-size:7.8pt;color:#0369a1;line-height:1.45;">
      <strong>Permasalahan:</strong> Proses cetak manual di pabrik tempe membutuhkan tenaga fisik konstan, khususnya saat mengisi, memadatkan, dan <strong>membalik cetakan tempe yang berat</strong> ke atas ancak bambu. Metode balik manual rawan merusak bentuk tempe, membuat kelelahan tinggi pada operator (kakak), dan throughput lambat (&plusmn;30-40 tempe/jam).<br>
      <strong>Solusi Terobosan (Lift-Off Frame):</strong> Alih-alih membuat mekanisme putar/balik mekanik yang rumit, mahal, dan rawan rusak, alat ini menggunakan sistem <strong>Frame Angkat (Lift-Off)</strong>. Papan ancak bambu diletakkan langsung di bagian paling dasar, frame cetakan 6-slot diturunkan menindih plastik &amp; ancak, kedelai dimasukkan dari atas, dipress bersamaan, lalu frame diangkat ke atas. Tempe yang sudah terbungkus rapi tetap tertinggal di atas ancak tanpa pernah dibalik!
    </p>
  </div>

  <div class="section-title">Alur 6 Langkah Siklus Kerja Otomatis</div>
  <div class="workflow-grid">
    <div class="wf-step">
      <span class="wf-num">1</span>
      <div class="wf-title">Persiapan Dasar</div>
      <div class="wf-desc">Operator meletakkan papan ancak bambu di meja platform, lalu meletakkan lembaran plastik 12&times;35 cm di atas tiap slot.</div>
    </div>
    <div class="wf-step">
      <span class="wf-num">2</span>
      <div class="wf-title">Lock Frame Cetakan</div>
      <div class="wf-desc">Frame cetakan 6-slot (tinggi 3.6 cm) dikunci merapat di atas ancak. Plastik secara alami membentuk wadah cetakan.</div>
    </div>
    <div class="wf-step">
      <span class="wf-num">3</span>
      <div class="wf-title">Pengisian &amp; Dosing</div>
      <div class="wf-desc">Kedelai beragi dimasukkan ke 6 slot. Sensor berat Load Cell HX711 memverifikasi batas gramasi target dengan toleransi presisi.</div>
    </div>
    <div class="wf-step">
      <span class="wf-num">4</span>
      <div class="wf-title">Press Simultan Otomatis</div>
      <div class="wf-desc">Operator menekan START. Motor DC Lead Screw M10 bergerak turun, menekan 6 tempe sekaligus dengan bantalan peredam karet 3mm.</div>
    </div>
    <div class="wf-step">
      <span class="wf-num">5</span>
      <div class="wf-title">Mekanisme Lift-Off</div>
      <div class="wf-desc">Press plate menahan tempe sejenak, lalu dinding frame cetakan naik ke atas (lift-off). Tempe lolos mulus dari dinding mold.</div>
    </div>
    <div class="wf-step">
      <span class="wf-num">6</span>
      <div class="wf-title">Ambil &amp; Ulangi</div>
      <div class="wf-desc">Press plate kembali ke posisi awal (homing). Operator langsung menarik papan ancak berisi 6 tempe siap fermentasi. Siklus: &plusmn;60-90 detik!</div>
    </div>
  </div>

  <div class="section-title">Spesifikasi Parameter Kunci Mesin</div>
  <table class="compact-table">
    <thead>
      <tr>
        <th style="width:28%;">Parameter Mesin</th>
        <th style="width:36%;">Dimensi &amp; Nilai Desain</th>
        <th style="width:36%;">Manfaat &amp; Catatan Fabrikasi</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Kapasitas Slot</strong></td>
        <td>6 Slot tempe paralel dalam 1 papan</td>
        <td>Mencetak 6 tempe per satu kali siklus penekanan</td>
      </tr>
      <tr>
        <td><strong>Ukuran Slot Tempe</strong></td>
        <td>Panjang 21.3 cm &times; Lebar 6.6 cm &times; Tebal 3.6 cm</td>
        <td>Sesuai ukuran standar pasar tempe keluarga</td>
      </tr>
      <tr>
        <td><strong>Dimensi Luar Frame</strong></td>
        <td>Panjang 50.5 cm &times; Lebar 24.0 cm</td>
        <td>Jarak antar slot 1.0 cm, dinding luar kokoh</td>
      </tr>
      <tr>
        <td><strong>Spesifikasi Ancak</strong></td>
        <td>Alas bambu: Panjang 50.5 cm &times; Lebar 7.0 cm / papan</td>
        <td>1 ancak memuat 1 baris cetakan 6 tempe</td>
      </tr>
      <tr>
        <td><strong>Plastik Pembungkus</strong></td>
        <td>Lembaran 12 &times; 35 cm berpori (perforasi jarum)</td>
        <td>Mudah disisipkan di frame sebelum kedelai masuk</td>
      </tr>
      <tr>
        <td><strong>Penggerak Penekan</strong></td>
        <td>Motor DC 12V High-Torque + Lead Screw M10 pitch 1.5</td>
        <td>Gaya tekan mekanik &plusmn;30-40 kg merata di 6 slot</td>
      </tr>
      <tr>
        <td><strong>Kesiapan Upgrade V2</strong></td>
        <td>Pre-weld mounting bracket NEMA17 &amp; Slider Rail</td>
        <td>Bisa ditambah motor geser otomatis tanpa rombak total</td>
      </tr>
    </tbody>
  </table>

  <div class="card card-highlight">
    <div style="font-size:7.8pt;font-weight:700;color:#15803d;margin-bottom:2px;">Efisiensi Kerja &amp; Ergonomi:</div>
    <div style="font-size:7.3pt;color:#334155;line-height:1.4;">
      Dengan sistem Lift-Off ini, beban fisik operator berkurang <strong>lebih dari 70%</strong> karena operator tidak perlu lagi mengangkat cetakan kayu/besi seberat 5-8 kg lalu membalikkannya secara manual ratusan kali sehari. Risiko cedera pergelangan tangan dan pinggang hilang sepenuhnya.
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>2</strong> dari 7</span>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 3: VISUALISASI DESAIN & WIRING DIAGRAM          ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">02</span>
      <span class="p-header-title">Visualisasi Desain 3D &amp; Skematik Wiring Diagram</span>
    </div>
    <span class="p-header-tag">Engineering &bull; Schematics</span>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:8px;">
    <!-- Kolom Kiri: Visual Mekanik -->
    <div>
      <div class="section-title">Konsep 3D Render Mesin Tempe</div>
      <div style="border:1px solid #cbd5e1;border-radius:6px;overflow:hidden;background:#0f172a;text-align:center;">
        <img src="{img_mesin}" style="width:100%;height:155px;object-fit:cover;display:block;">
      </div>
      <div style="font-size:6.8pt;color:#64748b;margin:4px 0 8px 0;line-height:1.35;">
        <strong>Gbr 1:</strong> Konsep 3D mesin tempe lengkap dengan Hopper penampung atas, motor penekan lead-screw vertikal, rel geser platform, dan panel kontrol display.
      </div>

      <div class="section-title">Cetakan Asli &amp; Ancak Bambu Pabrik</div>
      <div style="border:1px solid #cbd5e1;border-radius:6px;overflow:hidden;background:#0f172a;text-align:center;">
        <img src="{img_cetakan}" style="width:100%;height:105px;object-fit:cover;display:block;">
      </div>
      <div style="font-size:6.8pt;color:#64748b;margin:4px 0 0 0;line-height:1.35;">
        <strong>Gbr 2:</strong> Referensi dimensi fisik cetakan kayu 50.5&times;24 cm dan ancak bambu 50.5&times;7 cm yang dijadikan dasar ukuran frame baja baru.
      </div>
    </div>

    <!-- Kolom Kanan: Wiring Diagram -->
    <div>
      <div class="section-title">Skematik Pengkabelan ESP32 (Wiring)</div>
      <div style="border:1px solid #cbd5e1;border-radius:6px;overflow:hidden;background:#0f172a;text-align:center;">
        <img src="{img_wiring}" style="width:100%;height:155px;object-fit:cover;display:block;">
      </div>
      <div style="font-size:6.8pt;color:#64748b;margin:4px 0 8px 0;line-height:1.35;">
        <strong>Gbr 3:</strong> Wiring diagram ESP32 38-Pin terhubung ke Driver L298N, Load Cell HX711, Ultrasonic HC-SR04, LCD 16&times;2 I2C, tombol panel, dan relay.
      </div>

      <div class="section-title">Ringkasan Pinout Hardware ESP32</div>
      <table class="compact-table" style="font-size:7.1pt;margin-bottom:0;">
        <thead>
          <tr>
            <th>Modul / Sensor</th>
            <th>Pin ESP32</th>
            <th>Level Tegangan</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>HX711 (Load Cell)</strong></td>
            <td>DT: GPIO 16 | SCK: GPIO 4</td>
            <td>VCC: 5V (Step-Down)</td>
          </tr>
          <tr>
            <td><strong>HC-SR04 (Ultrasonic)</strong></td>
            <td>TRIG: GPIO 5 | ECHO: GPIO 18</td>
            <td>5V (Divider ke 3.3V)</td>
          </tr>
          <tr>
            <td><strong>LCD 16&times;2 I2C</strong></td>
            <td>SDA: GPIO 21 | SCL: GPIO 22</td>
            <td>VCC: 5V</td>
          </tr>
          <tr>
            <td><strong>L298N Motor Driver</strong></td>
            <td>ENA: 25 | IN1: 26 | IN2: 27</td>
            <td>Logika 3.3V / Power 12V</td>
          </tr>
          <tr>
            <td><strong>Limit Switch Atas/Bwh</strong></td>
            <td>LIMIT_TOP: 32 | LIMIT_BOT: 33</td>
            <td>Pull-up internal 3.3V</td>
          </tr>
          <tr>
            <td><strong>Tombol START / STOP</strong></td>
            <td>BTN_START: 13 | BTN_STOP: 14</td>
            <td>Pull-up internal 3.3V</td>
          </tr>
          <tr>
            <td><strong>Buzzer &amp; Status LED</strong></td>
            <td>BUZZER: 19 | LED_OK: 2 | LED_ERR: 15</td>
            <td>Resistor pembatas 220&Omega;</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card card-highlight" style="margin-top:2px;">
    <div style="font-size:7.5pt;font-weight:700;color:#15803d;margin-bottom:1px;">Prinsip Keselamatan Elektrikal:</div>
    <div style="font-size:7.1pt;color:#334155;line-height:1.4;">
      Semua kabel motor DC 12V dipisahkan jalurnya dari kabel sinyal sensor (HX711 &amp; I2C) untuk mencegah noise elektromagnetik. Modul Step-Down LM2596 wajib disetel tepat ke 5.0V sebelum disambungkan ke ESP32 dan modul sensor.
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>3</strong> dari 7</span>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 4: BILL OF MATERIALS & BUDGET                   ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">03</span>
      <span class="p-header-title">Bill of Materials (BOM) &amp; Rincian Anggaran</span>
    </div>
    <span class="p-header-tag">Procurement &bull; Costing</span>
  </div>

  <div class="section-title">Daftar Komponen Elektronik &amp; Otomasi</div>
  <table class="compact-table">
    <thead>
      <tr>
        <th style="width:5%;">#</th>
        <th style="width:28%;">Nama Komponen</th>
        <th style="width:35%;">Spesifikasi &amp; Tipe Rekomendasi</th>
        <th style="width:8%;">Qty</th>
        <th style="width:14%;">Harga Est.</th>
        <th style="width:10%;">Prioritas</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>ESP32 DevKit V1</td><td>38-Pin Microcontroller, WiFi+BT, USB-C/Micro</td><td>1 pcs</td><td>Rp 55.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>2</td><td>Load Cell 10kg + HX711</td><td>Bar type sensor timbangan + 24-bit ADC module</td><td>1 set</td><td>Rp 45.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>3</td><td>Ultrasonic HC-SR04</td><td>Sensor pantul jarak level kedelai di hopper</td><td>1 pcs</td><td>Rp 15.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>4</td><td>LCD 16&times;2 + I2C Module</td><td>Display karakter lokal dengan modul backpack PCF8574</td><td>1 set</td><td>Rp 30.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>5</td><td>Motor DC 12V + Gearbox</td><td>High Torque &ge; 15 kg.cm, putaran 60-100 RPM</td><td>1 pcs</td><td>Rp 110.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>6</td><td>Driver L298N Dual H-Bridge</td><td>Kapasitas arus 2A per channel dengan heatsink</td><td>1 pcs</td><td>Rp 20.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>7</td><td>Lead Screw M10 &plusmn; Nut</td><td>Stainless steel panjang 20-25 cm, pitch 1.5-2.0mm</td><td>1 set</td><td>Rp 50.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>8</td><td>Micro Limit Switch NO/NC</td><td>Roller lever type untuk sensor posisi atas &amp; bawah</td><td>4 pcs</td><td>Rp 20.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>9</td><td>Power Supply Adaptor 12V</td><td>12 Volt DC, arus &ge; 5 Ampere teregulasi stabil</td><td>1 pcs</td><td>Rp 80.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>10</td><td>Step-Down LM2596</td><td>Regulator DC-DC 12V ke 5V 3A (efisiensi tinggi)</td><td>1 pcs</td><td>Rp 15.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>11</td><td>Push Button &amp; Emergency</td><td>Tombol panel 22mm Hijau (Start) + Merah (E-Stop)</td><td>2 pcs</td><td>Rp 25.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>12</td><td>Relay Module 2 Channel</td><td>Isolasi optocoupler 5V coil, beban 10A 250VAC</td><td>1 pcs</td><td>Rp 15.000</td><td><span class="badge badge-yellow">Cadangan</span></td></tr>
      <tr><td>13</td><td>Buzzer &amp; Indicator LED</td><td>Buzzer aktif 5V + LED panel 5mm merah &amp; hijau</td><td>1 paket</td><td>Rp 10.000</td><td><span class="badge badge-red">Wajib</span></td></tr>
      <tr><td>14</td><td>Box Panel &amp; Terminal</td><td>Box ABS 20&times;15&times;9 cm + terminal blok kabel &amp; protoboard</td><td>1 paket</td><td>Rp 50.000</td><td><span class="badge badge-blue">Kerapian</span></td></tr>
      <tr style="background:#e0f2fe;font-weight:700;">
        <td colspan="4" style="text-align:right;">Subtotal Pengadaan Elektronik:</td>
        <td style="color:#0369a1;">&plusmn; Rp 505.000</td>
        <td></td>
      </tr>
    </tbody>
  </table>

  <div class="section-title">Daftar Kebutuhan Mekanik &amp; Fabrikasi Las</div>
  <table class="compact-table">
    <thead>
      <tr>
        <th style="width:5%;">#</th>
        <th style="width:33%;">Material / Jasa</th>
        <th style="width:38%;">Ukuran &amp; Spesifikasi Teknis</th>
        <th style="width:24%;">Estimasi Biaya</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>Besi Siku 40&times;40&times;4mm</td><td>Panjang 6 meter &mdash; Rangka meja utama dan pilar vertikal</td><td>Rp 85.000</td></tr>
      <tr><td>2</td><td>Besi Hollow 40&times;40&times;3mm</td><td>Panjang 2 meter &mdash; Penguat kolom penekan press</td><td>Rp 45.000</td></tr>
      <tr><td>3</td><td>Plat Besi Tebal 5mm</td><td>Ukuran 60&times;40 cm &mdash; Dudukan timbangan &amp; press plate</td><td>Rp 85.000</td></tr>
      <tr><td>4</td><td>Plat Besi Tebal 3mm (Food Safe)</td><td>Bahan frame cetakan 6-slot baru (tinggi 3.6 cm)</td><td>Rp 55.000</td></tr>
      <tr><td>5</td><td>Karet Bantalan Pad 3mm</td><td>Ukuran 45&times;22 cm &mdash; Menempel bawah press plate (higienis)</td><td>Rp 30.000</td></tr>
      <tr><td>6</td><td>Baut, Mur &amp; Leveling Pad</td><td>Baut M6/M8/M10 + 4 kaki karet leveling meja</td><td>Rp 45.000</td></tr>
      <tr><td>7</td><td>Cat Besi Anti-Karat &amp; Thinner</td><td>Primer anti karat + cat finish warna abu/hitam</td><td>Rp 40.000</td></tr>
      <tr><td>8</td><td><strong>Ongkos Tukang Las Bengkel</strong></td><td>Pemotongan, perakitan presisi, pengelasan struktur &amp; frame</td><td>Rp 350.000 &ndash; 400.000</td></tr>
      <tr style="background:#fef3c7;font-weight:700;">
        <td colspan="3" style="text-align:right;">Subtotal Fabrikasi Mekanik:</td>
        <td style="color:#b45309;">&plusmn; Rp 690.000 &ndash; 740.000</td>
      </tr>
    </tbody>
  </table>

  <div class="section-title">Ringkasan Total Anggaran Proyek</div>
  <div class="budget-cards">
    <div class="b-card b-card-blue">
      <div class="b-card-label">Biaya Elektronik</div>
      <div class="b-card-val" style="color:#0369a1;">Rp 505.000</div>
      <div class="b-card-sub">Sensor, kontroler, motor, adaptor</div>
    </div>
    <div class="b-card b-card-amber">
      <div class="b-card-label">Biaya Mekanik &amp; Las</div>
      <div class="b-card-val" style="color:#b45309;">Rp 740.000</div>
      <div class="b-card-sub">Baja, plat mold, jasa tukang las</div>
    </div>
    <div class="b-card b-card-green">
      <div class="b-card-label">Total Anggaran (Max)</div>
      <div class="b-card-val" style="color:#15803d;">Rp 1.245.000</div>
      <div class="b-card-sub">Jauh di bawah plafon Rp 2.000.000 &check;</div>
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>4</strong> dari 7</span>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 5: STRATEGI WAKTU & GANTT CHART                 ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">04</span>
      <span class="p-header-title">Strategi Waktu &amp; Timeline Gantt Chart 6 Minggu</span>
    </div>
    <span class="p-header-tag">Schedule &bull; Critical Path</span>
  </div>

  <div class="section-title">Timeline Gantt Chart Pelaksanaan Proyek</div>
  <div class="gantt-wrap">
    <div class="gantt-row" style="margin-bottom:8px;">
      <div class="gantt-label" style="font-weight:700;color:#0f172a;">Tahapan Aktivitas</div>
      <div class="gantt-timeline">
        <div class="g-col-head">Mgg 1</div>
        <div class="g-col-head">Mgg 2</div>
        <div class="g-col-head">Mgg 3</div>
        <div class="g-col-head">Mgg 4</div>
        <div class="g-col-head">Mgg 5</div>
        <div class="g-col-head">Mgg 6</div>
        <div class="g-col-head">Mgg 7</div>
        <div class="g-col-head">Mgg 8</div>
      </div>
    </div>

    <div class="gantt-row">
      <div class="gantt-label">1. Persiapan &amp; Order Online</div>
      <div class="gantt-timeline">
        <div class="g-bar g-bar-elec" style="grid-column:1/2;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">2. Fabrikasi Bengkel Las</div>
      <div class="gantt-timeline">
        <div class="g-bar g-bar-mech" style="grid-column:1/3;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">3. Wiring Panel &amp; Sensor</div>
      <div class="gantt-timeline">
        <div></div>
        <div class="g-bar g-bar-elec" style="grid-column:2/4;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">4. Firmware &amp; Dashboard IoT</div>
      <div class="gantt-timeline">
        <div></div><div></div>
        <div class="g-bar g-bar-soft" style="grid-column:3/5;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">5. Assembly &amp; Dry-Run</div>
      <div class="gantt-timeline">
        <div></div><div></div><div></div><div></div>
        <div class="g-bar g-bar-test" style="grid-column:5/6;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">6. Trial Kedelai &amp; Tuning</div>
      <div class="gantt-timeline">
        <div></div><div></div><div></div><div></div><div></div>
        <div class="g-bar g-bar-test" style="grid-column:6/7;"></div>
      </div>
    </div>
    <div class="gantt-row">
      <div class="gantt-label">7. Deployment &amp; Training</div>
      <div class="gantt-timeline">
        <div></div><div></div><div></div><div></div><div></div><div></div>
        <div class="g-bar" style="grid-column:7/8;background:#0f172a;"></div>
      </div>
    </div>
  </div>

  <div class="section-title">Milestone Kunci &amp; Bukti Keberhasilan (Deliverables)</div>
  <table class="compact-table">
    <thead>
      <tr>
        <th style="width:12%;">Periode</th>
        <th style="width:25%;">Milestone Sasaran</th>
        <th style="width:48%;">Hasil / Output Fisik yang Wajib Terpenuhi</th>
        <th style="width:15%;">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Minggu 1</strong></td>
        <td>Pengadaan &amp; SPK Bengkel</td>
        <td>Order online komponen selesai; gambar kerja dimensi diserahkan ke tukang las</td>
        <td><span class="badge badge-blue">Tahap 1</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 2</strong></td>
        <td>Rangka Mekanik Selesai</td>
        <td>Frame baja 50.5&times;24cm selesai dilas, cat anti karat rapi, lead screw terpasang</td>
        <td><span class="badge badge-blue">Tahap 2</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 3</strong></td>
        <td>Uji Sensor di Meja Kerja</td>
        <td>Load cell terkalibrasi gram asli, SR04 akurat, limit switch teruji cut-off motor</td>
        <td><span class="badge badge-yellow">Tahap 3</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 4</strong></td>
        <td>Sistem IoT Beroperasi</td>
        <td>ESP32 tersambung WiFi lokal, Dashboard HP terbuka, tombol start/stop responsif</td>
        <td><span class="badge badge-yellow">Tahap 4</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 5</strong></td>
        <td>Dry-Run 20 Siklus Penuh</td>
        <td>Mesin bergerak 20 siklus tanpa kedelai tanpa macet, limit switch presisi</td>
        <td><span class="badge badge-yellow">Tahap 5</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 6</strong></td>
        <td>Trial Produksi Nyata</td>
        <td>Pencetakan tempe dengan kedelai beragi; ketebalan 3.6 cm seragam, bentuk rapi</td>
        <td><span class="badge badge-green">Tahap 6</span></td>
      </tr>
      <tr>
        <td><strong>Minggu 7&ndash;8</strong></td>
        <td>Serah Terima ke Kakak</td>
        <td>Operator (kakak) lancar mengoperasikan mesin mandiri &plusmn;120 tempe/jam</td>
        <td><span class="badge badge-green">Goal Akhir</span></td>
      </tr>
    </tbody>
  </table>

  <div class="section-title">Strategi Jalur Kritis (Critical Path Optimization)</div>
  <div class="card card-highlight">
    <div style="font-size:7.6pt;font-weight:700;color:#15803d;margin-bottom:2px;">Kunci Agar Jadwal Tidak Molor:</div>
    <div style="font-size:7.2pt;color:#334155;line-height:1.4;">
      <strong>1. Paralelisasi Minggu 1:</strong> Jangan tunggu barang elektronik datang baru ke tukang las. Hubungi tukang las pada hari pertama proyek berjalan agar waktu tunggu pengerjaan rangka (5-7 hari) berbarengan dengan pengiriman barang Shopee/Tokopedia.<br>
      <strong>2. Pengujian Sub-Sistem:</strong> Selalu uji komponen satu per satu di breadboard sebelum dirakit ke rangka fisik mesin. Hal ini menghindari pusing mencari sumber masalah saat mesin sudah terpasang.
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>5</strong> dari 7</span>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 6: TAHAP PELAKSANAAN DETAIL (1 - 4)             ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">05</span>
      <span class="p-header-title">Tahap Pelaksanaan Detail: Fase 1 s/d Fase 4</span>
    </div>
    <span class="p-header-tag">Implementation Steps &bull; Part 1</span>
  </div>

  <!-- Fase 1 -->
  <div class="phase-box">
    <div class="phase-top">
      <div class="phase-top-title"><span>1.</span> Fase Persiapan, Pengukuran Awal &amp; Pengadaan</div>
      <span class="phase-badge">Minggu 1</span>
    </div>
    <div class="phase-body">
      <div class="p-item"><div class="p-check"></div><strong>Timbang Berat Kedelai per Slot:</strong> Ambil 1 takaran kedelai yang biasa dibungkus manual, timbang di timbangan dapur, catat gramasinya (misal: 120 gram) untuk diinput ke program ESP32.</div>
      <div class="p-item"><div class="p-check"></div><strong>Serahkan Dokumen Mekanik ke Tukang Las:</strong> Bawa print-out <code>docs/dimensi_mekanik.md</code> ke bengkel las, jelaskan sistem lift-off frame dan minta estimasi selesai 5-7 hari.</div>
      <div class="p-item"><div class="p-check"></div><strong>Order Komponen Elektronik Online:</strong> Beli paket ESP32, Load cell HX711, SR04, Motor DC, L298N, Lead Screw M10, adaptor 12V 5A di e-commerce.</div>
      <div class="p-item"><div class="p-check"></div><strong>Setup Software:</strong> Download Arduino IDE, tambahkan Board ESP32 (Espressif), serta pasang library <code>HX711</code>, <code>LiquidCrystal_I2C</code>, dan <code>ArduinoJson</code>.</div>
    </div>
  </div>

  <!-- Fase 2 -->
  <div class="phase-box">
    <div class="phase-top" style="background:#1e293b;">
      <div class="phase-top-title"><span>2.</span> Fase Fabrikasi Mekanik Rangka &amp; Cetakan Baru</div>
      <span class="phase-badge" style="color:#fbbf24;background:rgba(251,191,36,0.15);border-color:rgba(251,191,36,0.3);">Minggu 1 &ndash; 2</span>
    </div>
    <div class="phase-body">
      <div class="p-item"><div class="p-check"></div><strong>Fabrikasi Rangka Utama:</strong> Pengelasan meja besi siku 40&times;40 mm ukuran 90&times;70&times;45 cm dengan 4 pilar penguat.</div>
      <div class="p-item"><div class="p-check"></div><strong>Pembuatan Frame Cetakan 6-Slot:</strong> Rangkai sekat plat 3mm presisi 21.3 &times; 6.6 cm, tinggi 3.6 cm, jarak antar slot 1 cm.</div>
      <div class="p-item"><div class="p-check"></div><strong>Pembuatan Press Plate:</strong> Potong plat 5mm ukuran 44 &times; 21 cm, tempelkan karet peredam makanan 3mm di sisi bawah untuk distribusi tekan rata.</div>
      <div class="p-item"><div class="p-check"></div><strong>Pre-Weld Bracket NEMA17:</strong> Titik las lubang baut motor stepper di ujung meja (investasi awal untuk upgrade V2 geser otomatis nanti).</div>
      <div class="p-item"><div class="p-check"></div><strong>Pengecatan &amp; Finishing:</strong> Lakukan amplas karat lalu semprot cat primer anti-karat agar higienis dan awet terkena uap kedelai.</div>
    </div>
  </div>

  <!-- Fase 3 -->
  <div class="phase-box">
    <div class="phase-top">
      <div class="phase-top-title"><span>3.</span> Fase Perakitan Panel Elektronik &amp; Kalibrasi Sensor</div>
      <span class="phase-badge">Minggu 2 &ndash; 3</span>
    </div>
    <div class="phase-body">
      <div class="p-item"><div class="p-check"></div><strong>Bench Test &amp; Wiring:</strong> Rakit ESP32, driver L298N, dan modul sensor di protoboard sesuai skematik wiring diagram.</div>
      <div class="p-item"><div class="p-check"></div><strong>Kalibrasi Load Cell HX711:</strong> Jalankan program kalibrasi, letakkan beban standar (misal gula 1 kg), catat faktor kalibrasi ke firmware.</div>
      <div class="p-item"><div class="p-check"></div><strong>Uji Ultrasonic &amp; Limit Switch:</strong> Verifikasi pembacaan jarak hopper di Serial Monitor dan pastikan switch langsung mematikan motor saat tersentuh.</div>
      <div class="p-item"><div class="p-check"></div><strong>Perakitan Box Panel:</strong> Masukkan rangkaian ke box ABS, pasang tombol START/STOP di pintu panel, dan bungkus kabel dengan selang spiral.</div>
    </div>
  </div>

  <!-- Fase 4 -->
  <div class="phase-box">
    <div class="phase-top" style="background:#1e293b;">
      <div class="phase-top-title"><span>4.</span> Fase Upload Firmware ESP32 &amp; Konfigurasi Dashboard</div>
      <span class="phase-badge" style="color:#a855f7;background:rgba(168,85,247,0.15);border-color:rgba(168,85,247,0.3);">Minggu 3 &ndash; 4</span>
    </div>
    <div class="phase-body">
      <div class="p-item"><div class="p-check"></div><strong>Konfigurasi Jaringan WiFi:</strong> Masukkan Nama SSID dan Password WiFi pabrik ke dalam file firmware <code>mesin_tempe.ino</code>.</div>
      <div class="p-item"><div class="p-check"></div><strong>Flash Firmware &amp; Web UI:</strong> Upload kode program via Arduino IDE, lalu lakukan <em>ESP32 Sketch Data Upload</em> untuk memasukkan web UI ke SPIFFS.</div>
      <div class="p-item"><div class="p-check"></div><strong>Uji Akses Browser HP:</strong> Sambungkan HP ke WiFi pabrik, ketik alamat IP ESP32 di browser, verifikasi tampilan dashboard interaktif terbuka lancar.</div>
      <div class="p-item"><div class="p-check"></div><strong>Uji Tombol Virtual:</strong> Coba tekan tombol START, STOP, dan Tare Timbangan dari browser untuk memastikan responsivitas WebSocket/AJAX.</div>
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>6</strong> dari 7</span>
  </div>
</div>

<!-- ╔══════════════════════════════════════════════════════╗
     ║ PAGE 7: TAHAP 5-6, SOP OPERATOR & RISIKO            ║
     ╚══════════════════════════════════════════════════════╝ -->
<div class="page">
  <div class="p-header">
    <div class="p-header-left">
      <span class="p-header-num">06</span>
      <span class="p-header-title">Integrasi Mekatronika, SOP Harian &amp; Mitigasi Risiko</span>
    </div>
    <span class="p-header-tag">Deployment &bull; SOP &bull; Risk</span>
  </div>

  <!-- Fase 5 & 6 Grid -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
    <div class="phase-box" style="margin-bottom:0;">
      <div class="phase-top" style="background:#14532d;">
        <div class="phase-top-title"><span>5.</span> Integrasi &amp; Trial Produksi</div>
        <span class="phase-badge" style="color:#4ade80;background:rgba(74,222,128,0.15);border-color:rgba(74,222,128,0.3);">Mgg 5&ndash;6</span>
      </div>
      <div class="phase-body" style="padding:6px 8px;">
        <div class="p-item"><div class="p-check"></div>Dry-run 20 siklus tanpa kedelai untuk uji ketahanan mekanik &amp; limit switch.</div>
        <div class="p-item"><div class="p-check"></div>Uji coba pencetakan dengan kedelai basah 2-3 kg.</div>
        <div class="p-item"><div class="p-check"></div>Fine-tuning durasi press (3-5 detik) dan ketebalan hasil tempe (&plusmn;3.6 cm).</div>
      </div>
    </div>

    <div class="phase-box" style="margin-bottom:0;">
      <div class="phase-top" style="background:#701a75;">
        <div class="phase-top-title"><span>6.</span> Deployment &amp; Training</div>
        <span class="phase-badge" style="color:#f472b6;background:rgba(244,114,182,0.15);border-color:rgba(244,114,182,0.3);">Mgg 6&ndash;8</span>
      </div>
      <div class="phase-body" style="padding:6px 8px;">
        <div class="p-item"><div class="p-check"></div>Pemasangan unit mesin permanen di line produksi tempe.</div>
        <div class="p-item"><div class="p-check"></div>Pelatihan kakak (operator): pengoperasian dasar, stop darurat, dan pembersihan.</div>
        <div class="p-item"><div class="p-check"></div>Simpan bookmark Dashboard di layar utama HP kakak.</div>
      </div>
    </div>
  </div>

  <!-- SOP Operator Checklist -->
  <div class="section-title">Standard Operating Procedure (SOP) Harian Operator</div>
  <div class="chk-grid" style="margin-bottom:8px;">
    <div class="chk-col">
      <div class="chk-head" style="color:#0369a1;">&bull; Prosedur Sebelum Mulai Kerja (Pagi)</div>
      <div class="chk-item"><div class="chk-box"></div>Nyalakan saklar power &amp; pastikan LCD menyala "READY".</div>
      <div class="chk-item"><div class="chk-box"></div>Cek kebersihan platform penekan dan frame dari kotoran sisa.</div>
      <div class="chk-item"><div class="chk-box"></div>Isi hopper atas dengan kedelai beragi siap cetak.</div>
      <div class="chk-item"><div class="chk-box"></div>Siapkan stok plastik perforasi 12&times;35 cm dan papan ancak.</div>
      <div class="chk-item"><div class="chk-box"></div>Lakukan Tare (Nol-kan timbangan) via Dashboard HP.</div>
    </div>
    <div class="chk-col">
      <div class="chk-head" style="color:#15803d;">&bull; Prosedur Setelah Selesai Produksi (Sore)</div>
      <div class="chk-item"><div class="chk-box"></div>Tekan STOP, pastikan press plate parkir di posisi atas (homing).</div>
      <div class="chk-item"><div class="chk-box"></div>Matikan sumber listrik utama adaptor 12V.</div>
      <div class="chk-item"><div class="chk-box"></div>Lap bersih sisa minyak kedelai menggunakan kain lembab bersih.</div>
      <div class="chk-item"><div class="chk-box"></div>Catat total counter produksi harian yang tertera di dashboard.</div>
      <div class="chk-item"><div class="chk-box"></div>Beri pelumas silikon/grease pada ulir lead screw 1x seminggu.</div>
    </div>
  </div>

  <!-- Analisis Risiko & Mitigasi -->
  <div class="section-title">Matriks Risiko Teknis &amp; Tindakan Pencegahan</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;">
    <div class="risk-card">
      <div class="risk-title">&bull; Motor DC Kurang Torsi / Tertahan Saat Press</div>
      <div class="risk-desc"><strong>Mitigasi:</strong> Gunakan gearbox rasio 1:50 atau ganti ke Linear Actuator 12V 750N (tersedia pasaran Rp 220rb). Lead screw wajib diberi grease pelumas.</div>
    </div>
    <div class="risk-card">
      <div class="risk-title">&bull; Sinyal WiFi Pabrik Terputus / Drop</div>
      <div class="risk-desc"><strong>Mitigasi:</strong> Mesin beroperasi 100% mandiri via LCD &amp; tombol fisik. Koneksi WiFi hanya untuk monitoring &mdash; hilangnya sinyal tidak menghentikan mesin.</div>
    </div>
    <div class="risk-card">
      <div class="risk-title">&bull; Hasil Las Rangka Kurang Siku / Macet</div>
      <div class="risk-desc"><strong>Mitigasi:</strong> Sediakan toleransi celah 2mm pada frame cetakan. Lakukan uji coba geser lead screw secara manual di bengkel sebelum rangka dibawa pulang.</div>
    </div>
    <div class="risk-card">
      <div class="risk-title">&bull; Bacaan Berat Load Cell Bergeser (Drift)</div>
      <div class="risk-desc"><strong>Mitigasi:</strong> Pasang tombol Tare fisik dan software. Lakukan kalibrasi ulang cepat setiap awal pekan menggunakan botol air mineral 1 liter (1000g).</div>
    </div>
  </div>

  <div class="card card-highlight" style="margin-bottom:0;">
    <div style="font-size:7.5pt;font-weight:700;color:#15803d;margin-bottom:1px;">Indikator Kesuksesan Proyek (Key Results):</div>
    <div style="font-size:7.1pt;color:#334155;line-height:1.4;">
      &bull; Kapasitas produksi tempe mencapai <strong>&ge; 144 tempe/jam</strong> secara konsisten.<br>
      &bull; Beban fisik operator berkurang drastis tanpa perlu mengangkat/membalik cetakan.<br>
      &bull; Keseluruhan realisasi belanja tetap berada dalam batas anggaran <strong>&le; Rp 1,5 Juta</strong>.
    </div>
  </div>

  <div class="p-footer">
    <span>Mesin Pencetak Tempe Semi-Otomatis berbasis IoT &bull; Project Brief v1.0</span>
    <span>Halaman <strong>7</strong> dari 7 &bull; DOKUMEN SIAP CETAK</span>
  </div>
</div>

</body>
</html>
"""

html_out_path = os.path.abspath('docs/project_brief.html')
with open(html_out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated HTML at: {html_out_path} (Size: {os.path.getsize(html_out_path)} bytes)")

pdf_out_path = os.path.abspath('docs/Project_Brief_Mesin_Pencetak_Tempe.pdf')
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print("Running Edge headless to print to PDF...")
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out_path}",
    html_out_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
time.sleep(2)

if os.path.exists(pdf_out_path):
    print(f"SUCCESS! PDF created at: {pdf_out_path} (Size: {os.path.getsize(pdf_out_path)} bytes)")
else:
    print("FAILED to create PDF:", res.stderr)
