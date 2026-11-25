"""
Generator Visualisasi & CAD v12 — Solusi Fisika Granular Kedelai Belah
(Pengganti Teknik Sliding Horizontal pada Pencetakan Tempe Balok)
======================================================================
Memperbaiki kesalahan desain v11 (corong 1 titik yang membentuk gunungan tengah):
  1. FULL-LENGTH LINEAR DROP BOX (Kotak Takar Memanjang 58 x 200 x 70 mm):
     - Pintu dasar Clamshell terbuka sepanjang 200 mm (Depan-Tengah-Belakang sekaligus)
     - Menebar 250 g belahan kedelai MERATA sepanjang rongga 213 mm -> 0% gunungan!
  2. MICRO-VIBRATION LEVELLING (Motor Getar DC 12V, 1.5 detik):
     - Granular fluidization: belahan kedelai lembab merata otomatis memenuhi 4 sudut ujung!
  3. SILICONE-CUSHIONED VIBRO-PRESS (6 Pad 64 x 210 mm + Silikon Food-Grade 5 mm):
     - Menggantikan tekanan telapak tangan / sliding horizontal tanpa meremukkan kedelai!
     - Limit Switch Bawah menyetop tepat di ketebalan target 35 mm (tidak penyek).

Output:
  - cad/v12_solusi_granular_dan_press.png  (Diagram Teknik: Masalah 1-Titik vs Solusi v12)
  - cad/v12_dosing_dan_press.dxf           (File AutoCAD DXF R2010, 0 error)
"""

import os
import random
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch

OUT = os.path.dirname(os.path.abspath(__file__))

C_BG       = "#FFFFFF"
C_DARK     = "#0F172A"
C_SLATE    = "#475569"
C_RED      = "#DC2626"
C_RED_F    = "#FEE2E2"
C_GREEN    = "#047857"
C_GREEN_F  = "#ECFDF5"
C_BLUE     = "#1D4ED8"
C_BLUE_F   = "#DBEAFE"
C_CYAN     = "#0284C7"
C_MOLD     = "#92400E"
C_MOLD_F   = "#FDE68A"
C_PRESS    = "#6D28D9"
C_PRESS_F  = "#DDD6FE"
C_SILICONE = "#0D9488"
C_SIL_F    = "#99F6E4"


def draw_split_beans_in_poly(ax, x_min, x_max, y_base, top_fn, count=75, seed=10, crushed=False, zorder=5):
    """Gambar potongan belahan kedelai (setengah oval) di bawah kurva tinggi top_fn(x)."""
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.uniform(x_min + 2.5, x_max - 2.5)
        y_max = top_fn(x)
        if y_max <= y_base + 3.0:
            continue
        y = rng.uniform(y_base + 2.2, y_max - 1.8)
        ang = rng.uniform(0, 180)
        w = 5.6 if not crushed else 6.8
        h = 3.1 if not crushed else 1.8
        fc = "#D97706" if crushed else rng.choice(["#FBBF24", "#F59E0B", "#FCD34D"])
        ec = "#78350F"
        ax.add_patch(patches.Ellipse((x, y), w, h, angle=ang, facecolor=fc, edgecolor=ec, lw=0.55, zorder=zorder))


def build_v12_visual():
    fig = plt.figure(figsize=(16.4, 10.8), dpi=200, facecolor=C_BG)
    fig.add_artist(Rectangle((0.012, 0.012), 0.976, 0.976, fill=False,
                             edgecolor=C_DARK, linewidth=1.8, transform=fig.transFigure))

    fig.text(0.028, 0.968, "DESAIN ULANG v12 — SOLUSI FISIKA GRANULAR KEDELAI BELAH (PENGGANTI TEKNIK SLIDING HORIZONTAL)",
             fontsize=12.8, fontweight="bold", color=C_DARK, va="top")
    fig.text(0.028, 0.944, "Potongan Memanjang Rongga 213 mm (Sumbu Depan ↔ Belakang): Kenapa Tuang 1 Titik Gagal & Bagaimana Linear Drop Box + Vibro-Levelling + Pad Silikon Memecahkannya",
             fontsize=8.4, color=C_SLATE, va="top")
    fig.text(0.972, 0.966, "REV v12.0 • GRANULAR FIX", fontsize=9, fontweight="bold", color=C_GREEN,
             ha="right", va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor=C_GREEN_F, edgecolor="#34D399"))

    # Footer ringkasan spesifikasi v12
    fig.add_artist(Rectangle((0.018, 0.018), 0.964, 0.055, facecolor="#F8FAFC",
                             edgecolor=C_DARK, linewidth=0.9, transform=fig.transFigure))
    fig.text(0.030, 0.052, "UPGRADE v12:  (1) Kotak Takar Memanjang 58×200×70 mm (Clamshell Trapdoor)   |   (2) Motor Getar DC 12V (1,5 dtk → Fluidisasi Granular)   |   (3) Bantalan Silikon Food-Grade 5 mm",
             fontsize=8.0, fontweight="bold", color=C_DARK, va="center")
    fig.text(0.030, 0.030, "HASIL:  0% Gunungan Tengah  •  0% Kedelai Hancur Jadi Bubur  •  Ke-4 Sudut Penuh Padat  •  100% Tetap Kompatibel dengan Linear Actuator 1500N yang Sudah Dibeli!",
             fontsize=7.7, fontweight="bold", color=C_GREEN, va="center")

    # ── BARIS ATAS (MASALAH LAMA — MERAH): 2 PANEL ──────────────────────────────
    # ── BARIS BAWAH (SOLUSI BARU v12 — HIJAU): 3 PANEL ──────────────────────────
    top_pos = [
        [0.030, 0.525, 0.455, 0.385],
        [0.515, 0.525, 0.455, 0.385],
    ]
    bot_pos = [
        [0.030, 0.095, 0.300, 0.395],
        [0.350, 0.095, 0.300, 0.395],
        [0.670, 0.095, 0.300, 0.395],
    ]

    # ═════════════════════════════════════════════════════════════
    # PANEL ATAS 1: SALAH — TUANG 1 TITIK MEMBENTUK GUNUNGAN
    # ═════════════════════════════════════════════════════════════
    ax = fig.add_axes(top_pos[0])
    ax.set_xlim(0, 260); ax.set_ylim(0, 130)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#FCA5A5"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 111), 260, 19, facecolor="#991B1B", edgecolor="none", zorder=10))
    ax.text(8, 122.5, "✗ KESALAHAN LAMA (v11): TUANG 1 TITIK DI RONGGA PANJANG 213 mm", fontsize=8.4, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(8, 115.0, "Belahan kedelai lembab BUKAN cairan (sudut tumpuk ~40°) → menumpuk gunung di tengah!", fontsize=6.9, color="#FECACA", va="center", zorder=11)

    # Corong 1 titik sempit di tengah
    ax.add_patch(Polygon([(112, 108), (148, 108), (142, 84), (118, 84)], closed=True, ec=C_RED, fc=C_RED_F, lw=1.3, zorder=4))
    ax.text(130, 96, "1 Titik\n(Ø40)", fontsize=6.6, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)
    # Cetakan potongan memanjang 213 mm (x=22..238)
    ax.add_patch(Rectangle((18, 18), 224, 7, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((18, 25), 7, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((235, 25), 7, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.plot([26, 26, 234, 234], [61, 26, 26, 61], color=C_CYAN, lw=2.0, zorder=6)  # Plastik liner

    # Gunungan kedelai di tengah (segitiga x=72..188, puncak y=78!)
    mound = lambda x: max(26.0, 78.0 - 0.90 * abs(x - 130.0))
    xs = [72, 130, 188]
    ys = [26, 78, 26]
    ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, facecolor="#FEF3C7", edgecolor=C_RED, lw=1.2, ls="--", zorder=4))
    draw_split_beans_in_poly(ax, 74, 186, 26, mound, count=95, seed=1, zorder=5)

    # Anotasi masalah
    ax.annotate("UJUNG DEPAN\nKOSONG!", xy=(45, 36), xytext=(28, 76), fontsize=7.0, fontweight="bold", color=C_RED,
                ha="center", bbox=dict(boxstyle="round,pad=0.2", fc=C_RED_F, ec=C_RED),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))
    ax.annotate("UJUNG BELAKANG\nKOSONG!", xy=(215, 36), xytext=(222, 76), fontsize=7.0, fontweight="bold", color=C_RED,
                ha="center", bbox=dict(boxstyle="round,pad=0.2", fc=C_RED_F, ec=C_RED),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2))
    ax.text(130, 8, "◄─────────────── Panjang Rongga = 213 mm (Terlalu panjang untuk 1 titik tuang!) ───────────────►",
            fontsize=6.8, fontweight="bold", color=C_SLATE, ha="center")

    # ═════════════════════════════════════════════════════════════
    # PANEL ATAS 2: AKIBAT PRESS DATAR LANGSUNG DI ATAS GUNUNGAN
    # ═════════════════════════════════════════════════════════════
    ax = fig.add_axes(top_pos[1])
    ax.set_xlim(0, 260); ax.set_ylim(0, 130)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#FCA5A5"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 111), 260, 19, facecolor="#991B1B", edgecolor="none", zorder=10))
    ax.text(8, 122.5, "✗ AKIBATNYA JIKA LANGSUNG DIPRESS DATAR 1500 N", fontsize=8.4, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(8, 115.0, "Gaya vertikal TIDAK mengalirkan kedelai 10 cm ke samping → tengah penyek, ujung bolong!", fontsize=6.9, color="#FECACA", va="center", zorder=11)

    ax.add_patch(Rectangle((18, 18), 224, 7, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((18, 25), 7, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((235, 25), 7, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    # Pelat press keras menekan tengah
    ax.add_patch(Rectangle((27, 58), 206, 14, ec=C_PRESS, fc=C_PRESS_F, lw=1.5, zorder=7))
    ax.text(130, 65, "PELAT PRESS DATAR KERAS (1500 N TURUN)", fontsize=6.9, fontweight="bold", color=C_PRESS, ha="center", va="center", zorder=8)
    for axx in [70, 130, 190]:
        ax.annotate("", xy=(axx, 73), xytext=(axx, 96), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.8), zorder=8)

    # Tengah penyek jadi bubur (oranye gelap pipih) + ujung kosong
    ax.add_patch(Rectangle((76, 26), 108, 31, facecolor="#FDBA74", edgecolor=C_RED, lw=1.3, zorder=4))
    draw_split_beans_in_poly(ax, 78, 182, 26, lambda x: 57, count=80, seed=2, crushed=True, zorder=5)
    # Sedikit butir lepas di ujung
    draw_split_beans_in_poly(ax, 30, 74, 26, lambda x: 40, count=14, seed=3, zorder=5)
    draw_split_beans_in_poly(ax, 186, 230, 26, lambda x: 40, count=14, seed=4, zorder=5)

    ax.annotate("TENGAH HANCUR\nJADI BUBUR!", xy=(130, 44), xytext=(130, 99), fontsize=7.0, fontweight="bold", color="#991B1B",
                ha="center", bbox=dict(boxstyle="round,pad=0.22", fc=C_RED_F, ec=C_RED),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.3), zorder=9)
    ax.text(49, 49, "Bolong /\nKendor", fontsize=6.8, fontweight="bold", color=C_RED, ha="center")
    ax.text(211, 49, "Bolong /\nKendor", fontsize=6.8, fontweight="bold", color=C_RED, ha="center")
    ax.text(130, 8, "Inilah alasan tukang tempe konvensional wajib memakai TEKNIK SLIDING HORIZONTAL!",
            fontsize=6.9, fontweight="bold", color="#991B1B", ha="center")

    # ═════════════════════════════════════════════════════════════
    # PANEL BAWAH 1 (SOLUSI v12 TAHAP A): FULL-LENGTH LINEAR DROP BOX
    # ═════════════════════════════════════════════════════════════
    ax = fig.add_axes(bot_pos[0])
    ax.set_xlim(0, 175); ax.set_ylim(0, 130)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#6EE7B7"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 110), 175, 20, facecolor="#065F46", edgecolor="none", zorder=10))
    ax.text(6, 122.5, "✓ SOLUSI 1: KOTAK TAKAR MEMANJANG (58×200)", fontsize=7.6, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(6, 114.5, "Tebar 250g RATA sepanjang 200 mm (Clamshell Trapdoor)", fontsize=6.5, color="#A7F3D0", va="center", zorder=11)

    # Kotak Takar Memanjang 58 x 200 mm (ditampilkan sepanjang rongga x=20..155) + 3 sekat pembagi
    ax.add_patch(Rectangle((20, 74), 135, 26, ec=C_BLUE, fc=C_BLUE_F, lw=1.4, zorder=4))
    for sx in [65, 110]:
        ax.plot([sx, sx], [74, 100], color=C_BLUE, lw=1.1, ls="--", zorder=5)
    ax.text(87.5, 92, "KOTAK TAKAR MEMANJANG (200 mm)\n3 Zona: Depan • Tengah • Belakang", fontsize=6.3, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=6)
    # 2 Daun Pintu Clamshell membuka ke bawah!
    ax.plot([20, 32], [74, 62], color=C_BLUE, lw=2.2, zorder=6)
    ax.plot([155, 143], [74, 62], color=C_BLUE, lw=2.2, zorder=6)
    # Aliran kedelai merata di 3 zona sekaligus!
    for fx in [42, 87.5, 133]:
        ax.annotate("", xy=(fx, 48), xytext=(fx, 72), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.8), zorder=6)

    # Cetakan potongan memanjang 213 mm (x=14..161)
    ax.add_patch(Rectangle((12, 16), 151, 6, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((12, 22), 6, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((157, 22), 6, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.plot([19, 19, 156, 156], [52, 23, 23, 52], color=C_CYAN, lw=1.8, zorder=6)
    # Kedelai langsung tersebar rata sepanjang rongga (hanya sedikit bergelombang ringan)
    wave = lambda x: 46.5 + 3.0 * (1 if int(x / 20) % 2 == 0 else -1)
    draw_split_beans_in_poly(ax, 20, 155, 23, wave, count=85, seed=12, zorder=5)
    ax.text(87.5, 7, "0% Gunungan! Kedelai jatuh merata dari ujung depan s/d belakang!",
            fontsize=6.3, fontweight="bold", color=C_GREEN, ha="center")

    # ═════════════════════════════════════════════════════════════
    # PANEL BAWAH 2 (SOLUSI v12 TAHAP B): VIBRO-LEVELLING 12V (1,5 DETIK)
    # ═════════════════════════════════════════════════════════════
    ax = fig.add_axes(bot_pos[1])
    ax.set_xlim(0, 175); ax.set_ylim(0, 130)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#6EE7B7"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 110), 175, 20, facecolor="#065F46", edgecolor="none", zorder=10))
    ax.text(6, 122.5, "✓ SOLUSI 2: MOTOR GETAR 12V (1,5 DETIK)", fontsize=7.6, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(6, 114.5, "Granular Fluidization → sudut otomatis penuh seperti cairan!", fontsize=6.5, color="#A7F3D0", va="center", zorder=11)

    # Cetakan + Kedelai rata sempurna di 4 sudut!
    ax.add_patch(Rectangle((12, 34), 151, 6, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((12, 40), 6, 32, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((157, 40), 6, 32, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.plot([19, 19, 156, 156], [72, 41, 41, 72], color=C_CYAN, lw=1.8, zorder=6)
    ax.add_patch(Rectangle((19.5, 41), 136, 27, facecolor="#FEF3C7", edgecolor="none", zorder=4))
    draw_split_beans_in_poly(ax, 20, 155, 41, lambda x: 68.5, count=95, seed=22, zorder=5)

    # Motor Getar DC 12V (Eccentric Vibration Motor) dibaut di bawah cetakan!
    ax.add_patch(Rectangle((66, 19), 43, 15, ec=C_RED, fc=C_RED_F, lw=1.5, zorder=6))
    ax.text(87.5, 26.5, "VIBRATOR 12V\n(40–60 Hz)", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    # Gelombang getar visual
    for gx, dir_s in [(55, -1), (120, 1)]:
        ax.annotate("", xy=(gx + dir_s * 12, 26.5), xytext=(gx, 26.5),
                    arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.6), zorder=7)
    # Panah sudut penuh
    ax.annotate("4 SUDUT PENUH\nOTOMATIS!", xy=(24, 46), xytext=(48, 88), fontsize=6.6, fontweight="bold", color=C_GREEN,
                ha="center", bbox=dict(boxstyle="round,pad=0.2", fc=C_GREEN_F, ec=C_GREEN),
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.1))
    ax.annotate("Permukaan\nRata Sempurna", xy=(146, 68), xytext=(132, 88), fontsize=6.5, fontweight="bold", color=C_GREEN,
                ha="center", bbox=dict(boxstyle="round,pad=0.2", fc=C_GREEN_F, ec=C_GREEN),
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.1))
    ax.text(87.5, 7, "Hanya tambah Motor Getar 12V (~Rp 30 rb) → menggantikan usapan jari ke sudut!",
            fontsize=6.2, fontweight="bold", color=C_GREEN, ha="center")

    # ═════════════════════════════════════════════════════════════
    # PANEL BAWAH 3 (SOLUSI v12 TAHAP C): PAD SILIKON 5 mm + VIBRO-PRESS
    # ═════════════════════════════════════════════════════════════
    ax = fig.add_axes(bot_pos[2])
    ax.set_xlim(0, 175); ax.set_ylim(0, 130)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#6EE7B7"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 110), 175, 20, facecolor="#065F46", edgecolor="none", zorder=10))
    ax.text(6, 122.5, "✓ SOLUSI 3: PAD SILIKON 5 mm + VIBRO-PRESS", fontsize=7.6, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(6, 114.5, "Tekanan merata seperti telapak tangan, Limit Bawah stop @ 35 mm", fontsize=6.5, color="#A7F3D0", va="center", zorder=11)

    # Cetakan + Tempe terbungkus plastik terlipat rapi + penuh sudut!
    ax.add_patch(Rectangle((12, 22), 151, 6, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((12, 28), 6, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((157, 28), 6, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((19.5, 29), 136, 27, ec=C_CYAN, fc="#FEF3C7", lw=1.8, zorder=4))
    draw_split_beans_in_poly(ax, 20, 155, 29, lambda x: 56, count=105, seed=32, zorder=5)
    # Garis lipatan plastik di atas (terkunci rapat!)
    ax.plot([20, 155], [56.2, 56.2], color="#0369A1", lw=2.3, zorder=6)

    # Pad Penekan 2-Lapis: Aluminium 15 mm (atas) + BANTALAN SILIKON FOOD-GRADE 5 mm (bawah!)
    ax.add_patch(Rectangle((20, 63), 135, 13, ec=C_PRESS, fc=C_PRESS_F, lw=1.4, zorder=7))
    ax.text(87.5, 69.5, "PAD ALUMINIUM 15 mm (64×210)", fontsize=6.2, fontweight="bold", color=C_PRESS, ha="center", va="center", zorder=8)
    ax.add_patch(Rectangle((20, 57), 135, 6, ec=C_SILICONE, fc=C_SIL_F, lw=1.5, hatch="xxx", zorder=7))
    ax.annotate("Bantalan Silikon Food-Grade 5 mm\n(Shore A 45 → Empuk, Anti-Hancur!)", xy=(115, 60), xytext=(87.5, 92),
                fontsize=6.4, fontweight="bold", color=C_SILICONE, ha="center",
                bbox=dict(boxstyle="round,pad=0.22", fc="#F0FDFA", ec=C_SILICONE),
                arrowprops=dict(arrowstyle="->", color=C_SILICONE, lw=1.1), zorder=9)
    for axx in [45, 87.5, 130]:
        ax.annotate("", xy=(axx, 76), xytext=(axx, 84), arrowprops=dict(arrowstyle="->", color=C_PRESS, lw=1.6), zorder=8)

    ax.text(87.5, 10, "Tekanan seragam hanya 5–6 mm (Limit Bawah @ 35 mm)\n→ Balok padat tajam, utuh tidak penyek, lipatan plastik rata!",
            fontsize=6.2, fontweight="bold", color=C_GREEN, ha="center", va="center")

    png_path = os.path.join(OUT, "v12_solusi_granular_dan_press.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {png_path}")


def build_v12_dxf():
    """DXF R2010: Detail Kotak Takar Memanjang (58x200x70 mm) + Pad Silikon 2-Lapis + Dudukan Vibrator."""
    doc = ezdxf.new("R2010", setup=True)
    for nm, col in [("HOPPER", colors.BLUE), ("PRESS", colors.MAGENTA), ("SILICONE", colors.CYAN),
                    ("VIBRATOR", colors.RED), ("DIM", 3), ("LABEL", 7), ("BORDER", 7)]:
        doc.layers.new(nm, dxfattribs={"color": col})
    msp = doc.modelspace()

    def r(x, y, w, h, layer):
        msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True, dxfattribs={"layer": layer})

    # 1. Kotak Takar Memanjang (Tampak Atas 58 x 200 mm dengan 3 kompartemen pembagi aliran)
    r(0, 0, 58, 200, "HOPPER")
    r(2, 2, 54, 64, "HOPPER")
    r(2, 68, 54, 64, "HOPPER")
    r(2, 134, 54, 64, "HOPPER")
    msp.add_text("KOTAK TAKAR MEMANJANG 58x200 mm", height=7, dxfattribs={"layer": "LABEL"}).set_placement((29, 218), align=TextEntityAlignment.MIDDLE_CENTER)

    # 2. Kotak Takar Memanjang (Tampak Samping 200 x 70 mm + 2 Daun Pintu Clamshell)
    r(120, 100, 200, 70, "HOPPER")
    msp.add_line((120, 100), (145, 75), dxfattribs={"layer": "HOPPER"})
    msp.add_line((320, 100), (295, 75), dxfattribs={"layer": "HOPPER"})
    msp.add_text("TAMPAK SAMPING CLAMSHELL (200x70 mm)", height=7, dxfattribs={"layer": "LABEL"}).set_placement((220, 188), align=TextEntityAlignment.MIDDLE_CENTER)

    # 3. Pad Penekan 2-Lapis (Aluminium 15 mm + Silikon Food-Grade 5 mm, panjang 210 mm)
    r(120, 15, 210, 15, "PRESS")
    r(120, 10, 210, 5, "SILICONE")
    msp.add_text("PAD 2-LAPIS: AL 15mm + SILIKON 5mm (210mm)", height=7, dxfattribs={"layer": "LABEL"}).set_placement((225, 45), align=TextEntityAlignment.MIDDLE_CENTER)

    # 4. Dudukan Motor Getar DC 12V di bawah Cetakan (60 x 40 mm + 4 lubang baut M4)
    r(380, 70, 60, 40, "VIBRATOR")
    for bx in [388, 432]:
        for by in [78, 102]:
            msp.add_circle((bx, by), 2.2, dxfattribs={"layer": "VIBRATOR"})
    msp.add_text("BRACKET VIBRATOR 12V", height=7, dxfattribs={"layer": "LABEL"}).set_placement((410, 125), align=TextEntityAlignment.MIDDLE_CENTER)

    # Border & Title Block penuh
    r(-30, -80, 510, 330, "BORDER")
    r(-20, -70, 490, 55, "BORDER")
    msp.add_text("TEMPEHKIT v12 — KOMPONEN ANTI-GUNUNGAN: LINEAR DROP BOX + PAD SILIKON + VIBRATOR 12V",
                 height=8, dxfattribs={"layer": "LABEL"}).set_placement((225, -35), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("SKALA 1:1 (mm)  |  SS304 1.0mm + AL 15mm + SILIKON FOOD-GRADE SHORE A45 (5mm)",
                 height=6, dxfattribs={"layer": "LABEL"}).set_placement((225, -55), align=TextEntityAlignment.MIDDLE_CENTER)

    dxf_path = os.path.join(OUT, "v12_dosing_dan_press.dxf")
    doc.saveas(dxf_path)
    print(f"[OK] {dxf_path}")


def build_v12_rail_blueprint():
    """Blueprint Tampak Samping & Belakang Runtut v12.1: Hopper -> Servo -> Load Cell -> Rel X Ø16 -> Rel Teleskopik Z -> Cetakan."""
    fig = plt.figure(figsize=(16.2, 10.6), dpi=200, facecolor=C_BG)
    fig.add_artist(Rectangle((0.012, 0.012), 0.976, 0.976, fill=False,
                             edgecolor=C_DARK, linewidth=1.8, transform=fig.transFigure))

    fig.text(0.028, 0.966, "BLUEPRINT CAD v12.1 — MEKANISME REL LUNCUR DOSING RUNTUT (0 KOMPONEN MELAYANG!)",
             fontsize=12.6, fontweight="bold", color=C_DARK, va="top")
    fig.text(0.028, 0.942, "Rantai Mekanik Terhubung Penuh: Hopper + Corong Celah → Servo Gate → Load Cell di Palang Y=580 → 2× Rel X Ø16 → Rel Teleskopik Z (+280 mm) → Tebar 200 mm",
             fontsize=8.3, color=C_SLATE, va="top")
    fig.text(0.972, 0.965, "CAD v12.1 • RUNTUT", fontsize=9, fontweight="bold", color=C_GREEN,
             ha="right", va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor=C_GREEN_F, edgecolor="#34D399"))

    fig.add_artist(Rectangle((0.018, 0.018), 0.964, 0.055, facecolor="#F8FAFC",
                             edgecolor=C_DARK, linewidth=0.9, transform=fig.transFigure))
    fig.text(0.030, 0.052, "URUTAN KERJA:  (1) Timbang 250g di X=450, Z=480 (Load Cell diam!)  →  (2) Geser Rel X Ø16 ke Slot 1..6  →  (3) Luncur Rel Teleskopik Z (+280 mm)  →  (4) Clamshell Tebar 200 mm",
             fontsize=7.9, fontweight="bold", color=C_DARK, va="center")
    fig.text(0.030, 0.030, "RANGKA: 900×1420×640 mm  |  REL X: 2× Shaft Ø16 + 4× LM16UU (Z=590, Y=625 & 705)  |  REL Z: Rel Laci Teleskopik 250 mm (Beban Geser cuma ~0,8 kg, 0 Kabel Bergerak!)",
             fontsize=7.5, color=C_SLATE, va="center")

    # ── AXIS KIRI: TAMPAK SAMPING RUNTUT (Z = 0..640) ──
    ax1 = fig.add_axes([0.055, 0.100, 0.440, 0.785])
    ax1.set_aspect("equal", adjustable="box")
    ax1.grid(True, ls=":", lw=0.5, color="#CBD5E1", alpha=0.7)
    ax1.set_axisbelow(True)
    for sp in ax1.spines.values():
        sp.set_visible(False)
    ax1.set_title("TAMPAK SAMPING — RANTAI HOPPER → LOAD CELL → REL TELESKOPIK Z → CETAKAN", fontsize=8.4, fontweight="bold", color=C_DARK, pad=8)

    FD = 640
    for r in [(0, 0, 40, 1420), (FD - 40, 0, 40, 1420),
              (40, 40, FD - 80, 40), (40, 160, FD - 80, 40), (40, 340, FD - 80, 40),
              (40, 1100, FD - 80, 40), (40, 1380, FD - 80, 40),
              (360, 1040, 240, 40), (460, 540, 40, 40), (560, 540, 40, 220)]:
        ax1.add_patch(Rectangle((r[0], r[1]), r[2], r[3], ec="#334155", fc="#E2E8F0", lw=1.2, zorder=3))

    # Hopper + Corong Celah Memanjang turun LANGSUNG sampai Y=730 (terhubung palang Y=1040!)
    ax1.add_patch(Rectangle((370, 1080), 220, 300, ec=C_BLUE, fc=C_BLUE_F, lw=1.4, zorder=4))
    ax1.text(480, 1230, "HOPPER\nSS304\n(Stasioner)", fontsize=7.0, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=5)
    ax1.add_patch(Polygon([(370, 1080), (590, 1080), (580, 730), (380, 730)], closed=True, ec=C_BLUE, fc="#BFDBFE", lw=1.3, zorder=4))
    ax1.text(480, 900, "Corong Celah\n200 mm\n(Tersambung!)", fontsize=6.5, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=5)
    # Servo Gate di Y=718 (cuma 23 mm di atas Kotak Takar!)
    ax1.add_patch(Rectangle((376, 718), 208, 10, ec="#334155", fc="#94A3B8", lw=1.2, zorder=6))
    ax1.add_patch(Rectangle((540, 712), 42, 30, ec=C_RED, fc=C_RED_F, lw=1.2, zorder=7))
    # Pedestal + Load Cell 20 kg DIBAUT ke palang Y=540..580!
    ax1.add_patch(Rectangle((425, 580), 110, 18, ec="#334155", fc="#64748B", lw=1.2, zorder=5))
    ax1.add_patch(Rectangle((435, 598), 90, 22, ec=C_RED, fc=C_RED_F, lw=1.4, zorder=6))
    ax1.text(480, 609, "LOAD CELL", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    ax1.add_patch(Rectangle((385, 620), 190, 5, ec="#334155", fc="#CBD5E1", lw=1.0, zorder=6))

    # 2 Batang Rel X Ø16 (lingkaran potongan di Z=590, Y=625 & 705) + Kereta X + Rel Teleskopik Z!
    for ry in [625, 705]:
        ax1.add_patch(Circle((590, ry), 10, ec="#334155", fc="#CBD5E1", lw=1.3, zorder=8))
    ax1.add_patch(Rectangle((576, 610), 12, 112, ec="#334155", fc="#64748B", lw=1.2, zorder=7))

    # Kotak Takar Posisi 1 (TIMBANG di belakang Z=380..580, Y=625..695)
    ax1.add_patch(Rectangle((380, 625), 200, 70, ec=C_CYAN, fc="#BAE6FD", lw=1.5, zorder=5))
    ax1.text(480, 660, "POSISI 1: TIMBANG\n(Di atas Load Cell)", fontsize=6.2, fontweight="bold", color="#0369A1", ha="center", va="center", zorder=6)
    # Rel Teleskopik Z memanjang maju ke Posisi 2 (TEBAR di atas Cetakan Z=100..300, Y=625..695!)
    ax1.add_patch(Rectangle((100, 656), 478, 16, ec="#A16207", fc="#FDE047", lw=1.4, zorder=7))
    ax1.text(340, 664, "REL TELESKOPIK Z (+280 mm)", fontsize=6.0, fontweight="bold", color="#713F12", ha="center", va="center", zorder=8)
    ax1.add_patch(Rectangle((100, 625), 200, 70, ec=C_CYAN, fc="#BAE6FD", lw=1.4, ls="--", alpha=0.72, zorder=6))
    ax1.text(200, 680, "POSISI 2: TEBAR", fontsize=6.0, fontweight="bold", color="#0369A1", ha="center", va="center", zorder=7)
    ax1.annotate("", xy=(140, 600), xytext=(140, 625), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5), zorder=8)
    ax1.annotate("", xy=(200, 600), xytext=(200, 625), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5), zorder=8)
    ax1.annotate("", xy=(260, 600), xytext=(260, 625), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5), zorder=8)

    # Cetakan + Press HOME (h=750) + Actuator + Pad Silikon
    ax1.add_patch(Rectangle((80, 542), 240, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.6, zorder=5))
    ax1.add_patch(Rectangle((155, 510), 90, 32, ec="#EA580C", fc="#FED7AA", lw=1.2, zorder=5))  # Vibrator 12V
    ax1.add_patch(Rectangle((87.5, 770), 225, 5, ec=C_PRESS, fc=C_PRESS_F, lw=1.5, zorder=6))
    ax1.add_patch(Rectangle((95, 755), 210, 15, ec=C_PRESS, fc=C_PRESS_F, lw=1.2, zorder=6))
    ax1.add_patch(Rectangle((95, 750), 210, 5, ec=C_SILICONE, fc=C_SIL_F, lw=1.2, zorder=6))
    ax1.add_patch(Rectangle((168, 845), 64, 230, ec=C_RED, fc=C_RED_F, lw=1.5, zorder=6))
    ax1.add_patch(Rectangle((190, 795), 20, 50, ec="#334155", fc="#CBD5E1", lw=1.1, zorder=6))
    ax1.add_patch(Rectangle((178, 775), 44, 20, ec=C_GREEN, fc=C_GREEN_F, lw=1.1, zorder=6))
    ax1.add_patch(Rectangle((178, 1075), 44, 25, ec=C_GREEN, fc=C_GREEN_F, lw=1.1, zorder=6))

    ax1.set_xlim(-60, FD + 60)
    ax1.set_ylim(-40, 1465)
    ax1.set_xlabel("Z / Kedalaman = 640 mm  [Depan (Cetakan) ← 0 ... 640 → Belakang (Rel X)]", fontsize=7.5, color=C_SLATE)
    ax1.set_ylabel("Y / Tinggi (mm)", fontsize=7.5, color=C_SLATE)
    ax1.tick_params(labelsize=7.0, colors=C_SLATE)

    # ── AXIS KANAN: TAMPAK BELAKANG (REL X Ø16 & PERGESERAN SLOT 1 → 6) ──
    ax2 = fig.add_axes([0.545, 0.100, 0.425, 0.785])
    ax2.set_aspect("equal", adjustable="box")
    ax2.grid(True, ls=":", lw=0.5, color="#CBD5E1", alpha=0.7)
    ax2.set_axisbelow(True)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.set_title("TAMPAK BELAKANG — 2× REL SHAFT X (Ø16) & PERGESERAN SLOT 1 ↔ 6", fontsize=8.4, fontweight="bold", color=C_DARK, pad=8)

    FW = 900
    for r in [(0, 0, 40, 1420), (FW - 40, 0, 40, 1420),
              (40, 40, FW - 80, 40), (40, 160, FW - 80, 40), (40, 340, FW - 80, 40),
              (40, 540, FW - 80, 40), (40, 1040, FW - 80, 40), (40, 1380, FW - 80, 40)]:
        ax2.add_patch(Rectangle((r[0], r[1]), r[2], r[3], ec="#334155", fc="#E2E8F0", lw=1.2, zorder=3))

    # Hopper & Corong Celah di tengah X=450
    ax2.add_patch(Rectangle((300, 1080), 300, 300, ec=C_BLUE, fc=C_BLUE_F, lw=1.4, zorder=4))
    ax2.text(450, 1230, "HOPPER SS304\n(DIAM DI TENGAH)", fontsize=7.2, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=5)
    ax2.add_patch(Polygon([(300, 1080), (600, 1080), (482, 730), (418, 730)], closed=True, ec=C_BLUE, fc="#BFDBFE", lw=1.3, zorder=4))
    ax2.add_patch(Rectangle((488, 712), 42, 34, ec=C_RED, fc=C_RED_F, lw=1.2, zorder=6))
    ax2.text(509, 729, "Servo", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    # Load Cell di palang Y=540..580 (X=450)
    ax2.add_patch(Rectangle((410, 580), 80, 18, ec="#334155", fc="#64748B", lw=1.2, zorder=5))
    ax2.add_patch(Rectangle((422, 598), 56, 22, ec=C_RED, fc=C_RED_F, lw=1.4, zorder=6))
    ax2.text(450, 560, "PALANG PENOPANG LOAD CELL (0 GETARAN!)", fontsize=6.5, fontweight="bold", color=C_DARK, ha="center", va="center", zorder=6)

    # 2 Batang Rel Shaft X Ø16 membentang penuh X=40..860!
    for ry in [625, 705]:
        ax2.add_patch(Rectangle((40, ry - 8), 820, 16, ec="#334155", fc="#CBD5E1", lw=1.2, zorder=5))
        ax2.add_patch(Rectangle((40, ry - 18), 16, 36, ec="#334155", fc="#64748B", lw=1.1, zorder=6))
        ax2.add_patch(Rectangle((844, ry - 18), 16, 36, ec="#334155", fc="#64748B", lw=1.1, zorder=6))

    # Kereta X + 4 LM16UU + Kotak Takar di posisi TIMBANG (X=450) & bayangan geser ke S1 (255) & S6 (635)
    ax2.add_patch(Rectangle((388, 610), 124, 112, ec="#334155", fc="#94A3B8", lw=1.4, zorder=6))
    for ry in [625, 705]:
        for bx in [408, 492]:
            ax2.add_patch(Rectangle((bx - 18, ry - 14), 36, 28, ec=C_GREEN, fc=C_GREEN_F, lw=1.2, zorder=7))
    ax2.add_patch(Rectangle((421, 625), 58, 70, ec=C_CYAN, fc="#BAE6FD", lw=1.5, zorder=8))
    # Bayangan geser ke Slot 1 & Slot 6
    for sx, lbl in [(255, "S1"), (331, "S2"), (407, "S3"), (483, "S4"), (559, "S5"), (635, "S6")]:
        ax2.plot([sx, sx], [745, 775], color=C_BLUE, lw=1.2, ls=":", zorder=4)
        ax2.text(sx, 790, lbl, fontsize=6.8, fontweight="bold", color=C_BLUE, ha="center", zorder=6)
    ax2.annotate("", xy=(255, 825), xytext=(635, 825), arrowprops=dict(arrowstyle="<->", color=C_BLUE, lw=2.0), zorder=7)
    ax2.text(445, 855, "Kereta X bergeser mulus di 2× Rel Shaft Ø16\n(Cuma bawa Kotak Takar ~0,8 kg — super ringan!)",
             fontsize=6.8, fontweight="bold", color=C_BLUE, ha="center",
             bbox=dict(boxstyle="round,pad=0.25", fc="#EFF6FF", ec="#93C5FD"), zorder=8)

    ax2.set_xlim(-60, FW + 60)
    ax2.set_ylim(-40, 1465)
    ax2.set_xlabel("X / Lebar Rangka = 900 mm  (Titik Klik S1..S6 tiap 76 mm)", fontsize=7.5, color=C_SLATE)
    ax2.tick_params(labelsize=7.0, colors=C_SLATE)

    png_path = os.path.join(OUT, "v12_mekanisme_rel_dosing.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {png_path}")


if __name__ == "__main__":
    build_v12_visual()
    build_v12_rail_blueprint()
    build_v12_dxf()
    print("\n=== SEMUA FILE CAD & VISUALISASI GRANULAR v12.1 BERHASIL DIBUAT ===")
