"""
Generator Visualisasi Proses & CAD v11 — TempehKit Hybrid Zero-Drop
===================================================================
Menjawab kebutuhan real-world pencetakan tempe plastik berlubang 1-per-1:
  1. Dosing 1-Nozzle presisi per slot (Hopper + Servo Gate + Load Cell 20 kg)
  2. Taruh plastik berlubang 1-per-1 -> Isi kedelai -> Lipat kiri & kanan
  3. Press Horizontal Simultan 6-Slot (Linear Actuator 1500N + 6 Pad 64x210 mm)
  4. Sandwich Ancak Clamp (Ancak Bambu menempel 0 mm di mulut cetakan,
     dikunci 2x Elektromagnet 12V = 16 kgf -> ANTI JATUH saat diputar 180°)
  5. Laci Penyambut (Sliding Cradle di h=520 mm) didorong masuk di bawah ancak
     saat cetakan terbalik -> Magnet OFF (jatuh cuma 4 mm!) -> Tarik keluar!
  6. Lubang angin (Air Vent Ø3 mm) di dasar cetakan agar tempe tidak vakum/lengket.

Output:
  - cad/v11_visualisasi_proses_tempe.png  (Storyboard Teknis 6-Tahap + Detail Potongan)
  - cad/v11_arsitektur_hibrida.png        (Blueprint 2-Pandangan Mesin v11)
  - cad/v11_arsitektur_hibrida.dxf        (File AutoCAD DXF R2010 bebas error)
"""

import os
import math
import random
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle, Arc

OUT = os.path.dirname(os.path.abspath(__file__))

# Warna konsisten engineering modern (putih bersih, sangat jelas saat dicetak)
C_BG       = "#FFFFFF"
C_DARK     = "#0F172A"
C_SLATE    = "#475569"
C_FRAME    = "#334155"
C_FRAME_F  = "#E2E8F0"
C_MOLD     = "#92400E"
C_MOLD_F   = "#FDE68A"
C_SOY      = "#D97706"
C_SOY_F    = "#F59E0B"
C_PLASTIC  = "#0284C7"
C_PLASTIC_F= "#BAE6FD"
C_PRESS    = "#6D28D9"
C_PRESS_F  = "#DDD6FE"
C_ANCAK    = "#A16207"
C_ANCAK_F  = "#FEF08A"
C_MAGNET   = "#DC2626"
C_MAGNET_F = "#FCA5A5"
C_MECH     = "#047857"
C_MECH_F   = "#A7F3D0"
C_DIM      = "#0369A1"


def draw_beans(ax, x0, y0, w, h, seed=42, count=42, zorder=4):
    """Gambar butiran kacang kedelai secara realistis dalam area (x0, y0, w, h)."""
    rng = random.Random(seed)
    for _ in range(count):
        bx = x0 + 3.2 + rng.random() * max(1.0, w - 6.4)
        by = y0 + 2.6 + rng.random() * max(1.0, h - 5.2)
        ang = rng.uniform(0, 180)
        ell = patches.Ellipse((bx, by), width=5.4, height=3.6, angle=ang,
                              facecolor=rng.choice(["#FBBF24", "#F59E0B", "#EAB308", "#FCD34D"]),
                              edgecolor="#92400E", linewidth=0.55, zorder=zorder)
        ax.add_patch(ell)


def draw_perforations(ax, xs, ys, zorder=8):
    """Titik lubang pernafasan jamur (perforasi) pada lembaran plastik."""
    ax.scatter(xs, ys, s=7, facecolors="#FFFFFF", edgecolors="#0369A1", linewidths=0.7, zorder=zorder)


# ═══════════════════════════════════════════════════════════════════════════════
# GAMBAR 1: STORYBOARD VISUALISASI 6 TAHAP (PLASTIK, KEDELAI, PRESS & FLIP ANTI-JATUH)
# ═══════════════════════════════════════════════════════════════════════════════
def build_process_storyboard():
    fig = plt.figure(figsize=(16.5, 11.2), dpi=200, facecolor=C_BG)

    # Border luar kertas teknik
    fig.add_artist(Rectangle((0.012, 0.012), 0.976, 0.976, fill=False,
                             edgecolor=C_DARK, linewidth=1.8, transform=fig.transFigure))
    fig.text(0.028, 0.968, "VISUALISASI MEKANISME TEMPEHKIT v11 — PLASTIK BERLUBANG 1-PER-1 & SANDWICH FLIP 180° ANTI-JATUH",
             fontsize=13.2, fontweight="bold", color=C_DARK, va="top")
    fig.text(0.028, 0.944, "Menunjukkan posisi detail Plastik Berlubang, Kacang Kedelai, Pemadatan Sudut/Horizontal, Penjepit Ancak Bambu (0 mm Gap), Elektromagnet 16 kgf, & Laci Penyambut",
             fontsize=8.6, color=C_SLATE, va="top")
    fig.text(0.972, 0.966, "REV v11.0 • ZERO-DROP SYSTEM", fontsize=9, fontweight="bold", color="#047857",
             ha="right", va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor="#ECFDF5", edgecolor="#34D399", lw=1.0))

    # Footer legenda warna
    fig.add_artist(Rectangle((0.018, 0.018), 0.964, 0.052, facecolor="#F8FAFC",
                             edgecolor=C_DARK, linewidth=0.9, transform=fig.transFigure))
    legends = [
        ("#BAE6FD", "#0284C7", "Plastik Berlubang"),
        ("#FBBF24", "#92400E", "Kedelai (±250g/slot)"),
        ("#DDD6FE", "#6D28D9", "Press 6-Pad (1500N)"),
        ("#FEF08A", "#A16207", "Ancak Bambu (0 mm)"),
        ("#FCA5A5", "#DC2626", "2× Magnet 12V (16 kgf)"),
        ("#A7F3D0", "#047857", "Laci & Lubang Angin"),
    ]
    for idx_l, (fc, ec, lbl) in enumerate(legends):
        lx = 0.032 + idx_l * 0.160
        fig.add_artist(Rectangle((lx, 0.035), 0.013, 0.018, facecolor=fc, edgecolor=ec, lw=1.1, transform=fig.transFigure))
        fig.text(lx + 0.017, 0.044, lbl, fontsize=7.8, fontweight="bold", color=C_DARK, va="center")

    # 6 Panel Grid (2 baris × 3 kolom)
    positions = [
        [0.030, 0.515, 0.300, 0.395],
        [0.350, 0.515, 0.300, 0.395],
        [0.670, 0.515, 0.300, 0.395],
        [0.030, 0.090, 0.300, 0.395],
        [0.350, 0.090, 0.300, 0.395],
        [0.670, 0.090, 0.300, 0.395],
    ]

    titles = [
        "TAHAP 1: TARUH PLASTIK & TAKAR 1-NOZZLE",
        "TAHAP 2: LIPAT PLASTIK KIRI–KANAN (SLOT 1→6)",
        "TAHAP 3: PRESS SIMULTAN 6-SLOT (1500 N)",
        "TAHAP 4: JEPIT ANCAK BAMBU (GAP 0 mm!)",
        "TAHAP 5: FLIP 180° ANTI-JATUH + LACI MASUK",
        "TAHAP 6: MAGNET OFF & TARIK KELUAR RAPI",
    ]
    subtitles = [
        "1 lembar plastik berlubang dipasang di Slot → Mesin takar pas 250g",
        "Sayap plastik tidak tabrakan karena dikerjakan berurutan 1-per-1",
        "Pad 64×210 mm memadatkan sudut & mengunci lipatan rata horizontal",
        "Ancak ditaruh menempel di mulut cetakan → 2× Elektromagnet KUNCI",
        "Cetakan + Ancak putar 180° bersamaan → Magnet tahan, Laci didorong",
        "Jatuh cuma 4 mm ke Laci! Lipatan plastik di BAWAH tertindih tempe",
    ]

    axes = []
    for i, pos in enumerate(positions):
        ax = fig.add_axes(pos)
        ax.set_facecolor("#FFFFFF")
        ax.set_xlim(0, 160)
        ax.set_ylim(0, 125)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor("#CBD5E1")
            sp.set_linewidth(1.1)
        # Header banner per panel
        ax.add_patch(Rectangle((0, 108), 160, 17, facecolor="#0F172A", edgecolor="none", zorder=10))
        ax.text(5, 118.5, titles[i], fontsize=8.3, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
        ax.text(5, 111.5, subtitles[i], fontsize=6.7, color="#BAE6FD", va="center", zorder=11)
        axes.append(ax)

    # ── PANEL 1: TARUH PLASTIK BERLUBANG + DOSING 1-NOZZLE (Potongan 1 Slot) ──
    ax = axes[0]
    # Nozzle tunggal + Load Cell weigh-cup di atas
    ax.add_patch(Polygon([(58, 104), (102, 104), (90, 82), (70, 82)], closed=True, ec="#1D4ED8", fc="#DBEAFE", lw=1.3, zorder=3))
    ax.text(80, 94, "1-NOZZLE TAKAR\n(HX711: 250 g)", fontsize=6.8, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=5)
    ax.add_patch(Rectangle((94, 83), 26, 9, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.0, zorder=4))
    ax.text(107, 87.5, "Servo", fontsize=6.2, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)

    # Kedelai jatuh dari 1 nozzle ke dalam rongga
    draw_beans(ax, 72, 46, 16, 35, seed=11, count=18, zorder=5)
    ax.annotate("", xy=(80, 50), xytext=(80, 81), arrowprops=dict(arrowstyle="->", color=C_SOY, lw=1.8, ls="--"), zorder=6)

    # Dinding Cetakan 1 Slot (potongan U) + Lubang angin di dasar
    ax.add_patch(Rectangle((40, 14), 80, 7, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((40, 21), 8, 34, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((112, 21), 8, 34, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=3))
    # 2 lubang angin (air vent Ø3 mm) di dasar cetakan
    for vx in [64, 96]:
        ax.add_patch(Rectangle((vx - 1.8, 13.5), 3.6, 8, ec=C_MECH, fc="#FFFFFF", lw=0.9, zorder=6))

    # Lembaran Plastik Berlubang masuk ke rongga + sayap kiri-kanan terjuntai keluar
    plastic_u = [(14, 57), (49, 57), (49, 22), (111, 22), (111, 57), (146, 57)]
    px, py = zip(*plastic_u)
    ax.plot(px, py, color=C_PLASTIC, lw=2.6, zorder=7)
    # Shading transparan plastik
    ax.add_patch(Rectangle((50, 23), 60, 26, facecolor=C_PLASTIC_F, edgecolor="none", alpha=0.25, zorder=3))
    draw_perforations(ax, [24, 34, 42, 60, 80, 100, 118, 128, 138], [57, 57, 57, 22, 22, 22, 57, 57, 57], zorder=8)
    # Kedelai menumpuk di dalam plastik
    draw_beans(ax, 51, 23, 58, 26, seed=12, count=52, zorder=4)

    ax.annotate("Sayap Plastik Berlubang\n(Menjuntai Kiri & Kanan)", xy=(26, 57), xytext=(8, 72),
                fontsize=6.5, fontweight="bold", color=C_PLASTIC,
                arrowprops=dict(arrowstyle="->", color=C_PLASTIC, lw=1.0))
    ax.annotate("Lubang Angin Ø3 mm\n(Anti-Vakum saat lepas)", xy=(64, 14), xytext=(55, 3),
                fontsize=6.3, fontweight="bold", color=C_MECH,
                arrowprops=dict(arrowstyle="->", color=C_MECH, lw=0.9))

    # ── PANEL 2: LIPAT PLASTIK KIRI–KANAN BERURUTAN (SLOT 1 → 6) ──
    ax = axes[1]
    # Gambar 3 slot berdampingan untuk menunjukkan kenapa HARUS 1-per-1!
    slot_xs = [12, 58, 104]
    for idx, sx in enumerate(slot_xs):
        ax.add_patch(Rectangle((sx, 20), 44, 6, ec=C_MOLD, fc=C_MOLD_F, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((sx, 26), 5, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((sx + 39, 26), 5, 30, ec=C_MOLD, fc=C_MOLD_F, lw=1.2, zorder=3))

        if idx == 0:  # Slot 1: SUDAH DILIPAT RAPI
            draw_beans(ax, sx + 6, 27, 32, 27, seed=21, count=36, zorder=4)
            # Plastik tertutup amplop bertumpuk di atas
            ax.plot([sx + 5.5, sx + 5.5, sx + 38.5, sx + 38.5, sx + 12], [55, 27, 27, 55, 55], color=C_PLASTIC, lw=2.2, zorder=7)
            ax.plot([sx + 5.5, sx + 33], [56.8, 56.8], color="#0369A1", lw=2.2, zorder=8)
            ax.text(sx + 22, 66, "SLOT 1\n✓ Terlipat", fontsize=6.8, fontweight="bold", color=C_MECH, ha="center")
        elif idx == 1:  # Slot 2: SEDANG DILIPAT KIRI & KANAN
            draw_beans(ax, sx + 6, 27, 32, 27, seed=22, count=36, zorder=4)
            ax.plot([sx + 5.5, sx + 5.5, sx + 38.5, sx + 38.5], [56, 27, 27, 56], color=C_PLASTIC, lw=2.2, zorder=7)
            # Sayap kiri melipat masuk (melengkung)
            ax.plot([sx + 5.5, sx + 16, sx + 28], [56, 67, 62], color=C_PLASTIC, lw=2.2, ls="--", zorder=8)
            # Sayap kanan melipat masuk (melengkung)
            ax.plot([sx + 38.5, sx + 30, sx + 18], [56, 68, 63], color="#0369A1", lw=2.2, ls="--", zorder=8)
            ax.annotate("", xy=(sx + 26, 61), xytext=(sx + 6, 69),
                        arrowprops=dict(arrowstyle="->", color=C_PLASTIC, lw=1.4, connectionstyle="arc3,rad=-0.3"))
            ax.annotate("", xy=(sx + 18, 62), xytext=(sx + 38, 70),
                        arrowprops=dict(arrowstyle="->", color="#0369A1", lw=1.4, connectionstyle="arc3,rad=0.3"))
            ax.text(sx + 22, 82, "SLOT 2\nLipat Kiri → Kanan\n(Tangan Operator ~2 dtk)", fontsize=6.7, fontweight="bold", color=C_PLASTIC, ha="center")
        else:  # Slot 3: KOSONG SIAP BERIKUTNYA
            ax.text(sx + 22, 41, "Kosong\n(Next)", fontsize=6.8, color="#64748B", ha="center", va="center")
            ax.text(sx + 22, 66, "SLOT 3..6\nMenunggu", fontsize=6.8, fontweight="bold", color="#64748B", ha="center")

    ax.add_patch(FancyBboxPatch((10, 3), 140, 12, boxstyle="round,pad=0.3", fc="#EFF6FF", ec="#93C5FD", lw=0.9))
    ax.text(80, 9, "KENAPA 1-PER-1? Sayap plastik (±4 cm) bebas melipat tanpa menimpa lubang slot sebelahnya!",
            fontsize=6.3, fontweight="bold", color="#1E40AF", ha="center", va="center")

    # ── PANEL 3: PRESS SIMULTAN 6-SLOT (LINEAR ACTUATOR 1500N) ──
    ax = axes[2]
    # Linear Actuator turun + Pelat Gantry + 6 Pad
    ax.add_patch(Rectangle((72, 80), 16, 25, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.3, zorder=4))
    ax.text(80, 93, "1500N", fontsize=6.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)
    ax.add_patch(Rectangle((77, 67), 6, 13, ec="#334155", fc="#CBD5E1", lw=1.1, zorder=4))
    # Pelat gantry lebar 6 slot
    ax.add_patch(Rectangle((12, 62), 136, 5, ec=C_PRESS, fc=C_PRESS_F, lw=1.4, zorder=6))
    # 2 Guide Shaft kiri-kanan
    for gx in [16, 144]:
        ax.add_patch(Rectangle((gx - 1.5, 22), 3, 80, ec="#475569", fc="#CBD5E1", lw=0.9, zorder=3))
        ax.add_patch(Rectangle((gx - 4, 60), 8, 9, ec=C_MECH, fc=C_MECH_F, lw=1.0, zorder=7))

    # Cetakan 6-slot di bawah + 6 pad menekan rata
    ax.add_patch(Rectangle((22, 22), 116, 5, ec=C_MOLD, fc=C_MOLD_F, lw=1.3, zorder=3))
    for i in range(6):
        sx = 24 + i * 19
        ax.add_patch(Rectangle((sx, 27), 2, 24, ec=C_MOLD, fc=C_MOLD_F, lw=0.9, zorder=4))
        # Kedelai padat penuh sudut + terbungkus plastik
        ax.add_patch(Rectangle((sx + 2.5, 27.5), 15.5, 21.5, ec=C_PLASTIC, fc="#FDE68A", lw=1.2, zorder=4))
        draw_beans(ax, sx + 2.5, 27.5, 15.5, 21.5, seed=30 + i, count=14, zorder=5)
        # Pad penekan masuk pas menekan permukaan atas
        ax.add_patch(Rectangle((sx + 3.0, 49.5), 14.5, 12.5, ec=C_PRESS, fc=C_PRESS_F, lw=1.1, zorder=6))
    ax.add_patch(Rectangle((138, 27), 2, 24, ec=C_MOLD, fc=C_MOLD_F, lw=0.9, zorder=4))

    # Panah tekanan merata ke sudut
    for axx in [40, 80, 120]:
        ax.annotate("", xy=(axx, 52), xytext=(axx, 75), arrowprops=dict(arrowstyle="->", color=C_PRESS, lw=1.7), zorder=9)
    ax.text(80, 11, "6 Pad (64×210 mm) menekan 6 slot serentak (tahan 5 dtk)\n→ Kedelai padat hingga sudut + lipatan plastik terkunci rata!",
            fontsize=6.5, fontweight="bold", color=C_PRESS, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.25", fc="#F5F3FF", ec="#C4B5FD"))

    # ── PANEL 4: JEPIT ANCAK BAMBU (SANDWICH CLAMP — GAP 0 mm!) ──
    ax = axes[3]
    # Tampak samping cetakan di poros h=560 mm (Y=45 di panel)
    ax.add_patch(Rectangle((35, 32), 90, 22, ec=C_MOLD, fc=C_MOLD_F, lw=1.5, zorder=3))
    # Tempe terbungkus plastik (lipatan di ATAS!)
    ax.add_patch(Rectangle((40, 35), 80, 18, ec=C_PLASTIC, fc="#FEF3C7", lw=1.4, zorder=4))
    draw_beans(ax, 41, 35, 78, 17, seed=41, count=46, zorder=5)
    # Garis lipatan plastik di atas
    ax.plot([42, 118], [53.2, 53.2], color="#0369A1", lw=2.3, zorder=6)

    # ANCAK BAMBU MENEMPEL RAPAT (GAP 0 mm!) di atas cetakan
    ax.add_patch(Rectangle((30, 54), 100, 11, ec=C_ANCAK, fc=C_ANCAK_F, lw=1.6, hatch="///", zorder=6))
    ax.text(80, 59.5, "ANCAK BAMBU (MENEMPEL 0 mm!)", fontsize=6.8, fontweight="bold", color="#713F12",
            ha="center", va="center", bbox=dict(fc=C_ANCAK_F, ec="none", pad=0.8), zorder=7)

    # Bingkai Penjepit Baja Berengsel (Clamp Frame) menindih ancak & dikunci 2x Elektromagnet!
    ax.add_patch(Rectangle((28, 65), 104, 4.5, ec="#1E293B", fc="#94A3B8", lw=1.3, zorder=7))
    # Engsel belakang (kanan)
    ax.add_patch(Circle((132, 65), 3.8, ec=C_MECH, fc=C_MECH_F, lw=1.3, zorder=8))
    # 2x Elektromagnet 12V di depan (kiri) mengunci bingkai ke badan cetakan!
    ax.add_patch(Rectangle((24, 48), 10, 17, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.5, zorder=8))
    ax.text(14, 56, "MAGNET\n12V ON\n(16 kgf)", fontsize=6.2, fontweight="bold", color=C_MAGNET, ha="center", va="center")

    # Poros As Ø20 mm di tengah cetakan
    ax.add_patch(Circle((80, 43), 5, ec=C_MECH, fc="#FFFFFF", lw=1.6, zorder=9))
    ax.text(80, 86, "PRINSIP SANDWICH CLAMP:\nAncak Bambu dijepit langsung ke mulut cetakan!\nLipatan plastik tertekan rapat → MUSTAHIL terbuka!",
            fontsize=6.7, fontweight="bold", color=C_DARK, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.35", fc="#FEF2F2", ec="#FCA5A5", lw=1.0))
    ax.annotate("Engsel Penjepit", xy=(132, 65), xytext=(116, 75), fontsize=6.3, fontweight="bold", color=C_MECH,
                arrowprops=dict(arrowstyle="->", color=C_MECH, lw=0.9))
    ax.text(80, 14, "Poros As Ø20 mm (NEMA 23) — Press sudah di HOME (atas)", fontsize=6.5, color=C_SLATE, ha="center")

    # ── PANEL 5: FLIP 180° ANTI-JATUH + DORONG LACI PENYAMBUT ──
    ax = axes[4]
    # Lingkaran lintasan putar 180°
    ax.add_patch(Circle((80, 62), 38, ec=C_MAGNET, fc="#FEE2E2", lw=1.1, ls="--", alpha=0.18, zorder=1))
    ax.add_patch(Circle((80, 62), 38, ec=C_MAGNET, fc="none", lw=1.1, ls="--", zorder=2))
    # Panah lengkung rotasi 180°
    ax.annotate("", xy=(42, 64), xytext=(118, 64),
                arrowprops=dict(arrowstyle="->", color=C_MAGNET, lw=1.8, connectionstyle="arc3,rad=-0.65"), zorder=9)
    ax.text(80, 99, "NEMA 23 PUTAR 180° (2400 STEP)\nMAGNET TETAP ON — TEMPE TIDAK JATUH!",
            fontsize=6.7, fontweight="bold", color=C_MAGNET, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec=C_MAGNET, lw=0.8), zorder=10)

    # Posisi TERBALIK 180°: Cetakan di ATAS, Tempe di TENGAH (lipatan kini di BAWAH!), Ancak di BAWAH!
    ax.add_patch(Rectangle((40, 56), 80, 18, ec=C_MOLD, fc=C_MOLD_F, lw=1.4, zorder=4))
    ax.add_patch(Rectangle((44, 52), 72, 16, ec=C_PLASTIC, fc="#FEF3C7", lw=1.3, zorder=5))
    draw_beans(ax, 45, 52, 70, 15, seed=51, count=42, zorder=6)
    ax.plot([46, 114], [52.2, 52.2], color="#0369A1", lw=2.3, zorder=7)  # Lipatan plastik sekarang di BAWAH!
    # Ancak di bawah menempel rapat
    ax.add_patch(Rectangle((36, 42), 88, 10, ec=C_ANCAK, fc=C_ANCAK_F, lw=1.5, hatch="///", zorder=6))
    # Clamp & Magnet masih mengunci
    ax.add_patch(Rectangle((34, 38), 92, 4, ec="#1E293B", fc="#94A3B8", lw=1.2, zorder=7))
    ax.add_patch(Rectangle((120, 38), 9, 18, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.3, zorder=8))
    ax.add_patch(Circle((80, 62), 4.5, ec=C_MECH, fc="#FFFFFF", lw=1.5, zorder=9))

    # LACI PENYAMBUT (Sliding Tray di h=520 mm -> gap cuma 4 mm di bawah ancak!)
    ax.add_patch(Rectangle((20, 24), 102, 10, ec=C_MECH, fc=C_MECH_F, lw=1.5, zorder=6))
    ax.text(71, 29, "LACI PENYAMBUT (REL LACI) → DORONG MASUK", fontsize=6.4, fontweight="bold", color="#065F46", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(118, 16), xytext=(30, 16), arrowprops=dict(arrowstyle="->", color=C_MECH, lw=2.2), zorder=8)
    ax.text(80, 8, "Setelah 180° berhenti: Dorong Laci Penyambut tepat di bawah ancak (selisih cuma 4 mm!)",
            fontsize=6.2, fontweight="bold", color=C_MECH, ha="center", va="center")

    # ── PANEL 6: MAGNET OFF → ANCAK MENDARAT 4 mm → TARIK KELUAR RAPI! ──
    ax = axes[5]
    # Cetakan kosong terangkat / berputar balik 0° di atas (bebas karena lubang angin anti-vakum)
    ax.add_patch(Rectangle((40, 74), 80, 18, ec=C_MOLD, fc=C_MOLD_F, lw=1.3, ls="--", alpha=0.65, zorder=3))
    ax.text(80, 83, "Cetakan Kosong (Balik 0°)\nLubang Angin → Lepas Mulus", fontsize=6.5, fontweight="bold", color=C_MOLD, ha="center", va="center", zorder=4)
    ax.annotate("", xy=(80, 96), xytext=(80, 74), arrowprops=dict(arrowstyle="->", color=C_MOLD, lw=1.5, ls="--"), zorder=5)

    # Laci Penyambut ditarik keluar ke depan membawa Ancak + 6 Balok Tempe RAPI!
    ax.add_patch(Rectangle((12, 22), 124, 9, ec=C_MECH, fc=C_MECH_F, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((18, 31), 112, 9, ec=C_ANCAK, fc=C_ANCAK_F, lw=1.5, hatch="///", zorder=5))
    for i in range(6):
        tx = 22 + i * 17.5
        ax.add_patch(Rectangle((tx, 40.5), 15.5, 19, ec=C_PLASTIC, fc="#FEF3C7", lw=1.3, zorder=6))
        draw_beans(ax, tx, 40.5, 15.5, 19, seed=60 + i, count=14, zorder=7)
        # Garis tebal lipatan plastik berada di BAWAH (tertindih berat tempe!)
        ax.plot([tx + 1, tx + 14.5], [41.2, 41.2], color="#0369A1", lw=2.4, zorder=8)

    ax.annotate("LIPATAN PLASTIK DI BAWAH!\nTertindih berat tempe → Rapi & Rapat", xy=(47, 41), xytext=(80, 64),
                fontsize=6.5, fontweight="bold", color="#0369A1", ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="#F0F9FF", ec="#38BDF8"),
                arrowprops=dict(arrowstyle="->", color="#0369A1", lw=1.2))
    ax.annotate("", xy=(14, 13), xytext=(125, 13), arrowprops=dict(arrowstyle="->", color=C_MECH, lw=2.2), zorder=8)
    ax.text(80, 6, "Tarik Laci ke Depan → Angkat Ancak isi 6 Tempe Siap Fermentasi (0% Tumpah!)",
            fontsize=6.5, fontweight="bold", color="#065F46", ha="center", va="center")

    out_path = os.path.join(OUT, "v11_visualisasi_proses_tempe.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {out_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# GAMBAR 2: BLUEPRINT ARSITEKTUR MESIN v11.1 (DOSING GESER BELAKANG + REL SELIP L-CHANNEL)
# ═══════════════════════════════════════════════════════════════════════════════
def build_v11_cad():
    # --- DXF R2010 (Tampak Depan + Samping Gabungan v11.1 Zero-Collision) ---
    doc = ezdxf.new("R2010", setup=True)
    for nm, col in [("FRAME", colors.CYAN), ("MOLD", colors.YELLOW), ("PRESS", colors.MAGENTA),
                    ("MECHANISM", colors.GREEN), ("ELEC", colors.RED), ("HOPPER", colors.BLUE),
                    ("PLASTIC", 5), ("DIM", 3), ("LABEL", 7), ("BORDER", 7)]:
        doc.layers.new(nm, dxfattribs={"color": col})
    msp = doc.modelspace()

    def drect(x, y, w, h, layer, lt=None):
        a = {"layer": layer}
        if lt:
            a["linetype"] = lt
        msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True, dxfattribs=a)

    # Tampak Depan v11.1 (Rangka terpadu 900 x 1420 mm)
    FW, FH, HW = 900, 1420, 40
    drect(0, 0, HW, FH, "FRAME")
    drect(FW - HW, 0, HW, FH, "FRAME")
    for by in [40, 160, 340, 1100, 1380]:
        drect(HW, by, FW - 2 * HW, HW, "FRAME")
    # Rel Geser Dosing Belakang (Y=810 & Y=1310) + Unit Dosing di atas Slot 1 (X=255)
    drect(HW, 800, FW - 2 * HW, 20, "MECHANISM", "DASHED")
    drect(HW, 1300, FW - 2 * HW, 20, "MECHANISM", "DASHED")
    msp.add_lwpolyline([(175, 1310), (335, 1310), (285, 1070), (225, 1070)], close=True, dxfattribs={"layer": "HOPPER"})
    drect(210, 880, 90, 110, "HOPPER")   # Weigh-Cup 250g
    drect(215, 855, 80, 22, "ELEC")      # Load Cell 20 kg
    drect(228, 615, 54, 240, "HOPPER", "DASHED")  # Corong tuang masuk tepat ke Slot 1!

    # Cetakan 6-slot + Rel Selip L-Channel (X=124..776) + Ancak 0 mm + Press HOME (h=750) + Guide X=95 & 805
    drect(154.5, 542, 591, 36, "MOLD")
    drect(130, 578, 640, 18, "MECHANISM")   # Ancak bambu 0 mm
    drect(120, 574, 20, 28, "ELEC")         # Rel L-Channel kiri
    drect(760, 574, 20, 28, "ELEC")         # Rel L-Channel kanan
    drect(89, 380, 12, 720, "MECHANISM")    # Linear Guide Kiri (X=95 -> LUAR Ancak!)
    drect(799, 380, 12, 720, "MECHANISM")   # Linear Guide Kanan (X=805 -> LUAR Ancak!)
    drect(75, 770, 750, 5, "PRESS")         # Pelat Gantry Press HOME
    for i in range(6):
        drect(223 + i * 76, 750, 64, 20, "PRESS")
    drect(418, 845, 64, 230, "ELEC")        # Linear Actuator Stroke 200mm
    drect(125, 496, 650, 24, "MECHANISM", "DASHED")

    # Tampak Samping v11.1 di offset XO = 1220 (Kedalaman 580 mm)
    XO, FD = 1220, 580
    drect(XO, 0, HW, FH, "FRAME")
    drect(XO + FD - HW, 0, HW, FH, "FRAME")
    for by in [40, 160, 340, 1100, 1380]:
        drect(XO + HW, by, FD - 2 * HW, HW, "FRAME")
    AS_Z = XO + 200
    AS_Y = 560
    msp.add_circle((AS_Z, AS_Y), 135, dxfattribs={"layer": "ELEC", "linetype": "DASHED"})
    drect(AS_Z - 120, AS_Y - 18, 240, 36, "MOLD")
    drect(AS_Z - 124, AS_Y + 18, 248, 18, "MECHANISM")  # Ancak di dalam Rel L-Channel
    drect(AS_Z - 112.5, 770, 225, 5, "PRESS")
    drect(AS_Z - 105, 750, 210, 20, "PRESS")
    drect(AS_Z - 32, 845, 64, 230, "ELEC")
    # Unit Dosing Belakang (Z=460) + Corong Miring masuk tepat ke Z=200 (Cetakan!)
    drect(XO + 400, 880, 120, 110, "HOPPER")
    drect(XO + 410, 855, 100, 22, "ELEC")
    msp.add_lwpolyline([(XO + 420, 855), (AS_Z - 20, 625), (AS_Z + 20, 610), (XO + 455, 835)],
                       close=True, dxfattribs={"layer": "HOPPER", "linetype": "DASHED"})
    drect(XO - 240, 500, 260, 20, "MECHANISM")

    drect(-60, -160, 1960, 1700, "BORDER")
    drect(-40, -140, 1920, 110, "BORDER")
    msp.add_text("TEMPEHKIT v11.1 — DOSING GESER MASUK TIAP SLOT + REL SELIP L-CHANNEL ANTI-TABRAKAN",
                 height=18, dxfattribs={"layer": "LABEL"}).set_placement((920, -70), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("RANGKA TERPADU 900x1420x580mm | GUIDE SHAFT X=95 & 805 (LUAR ANCAK) | PRESS HOME h=750mm | LACI h=520mm",
                 height=11, dxfattribs={"layer": "LABEL"}).set_placement((920, -108), align=TextEntityAlignment.MIDDLE_CENTER)

    dxf_path = os.path.join(OUT, "v11_arsitektur_hibrida.dxf")
    doc.saveas(dxf_path)

    # --- PNG Blueprint 2-Pandangan (v11.1 Fixed) ---
    fig = plt.figure(figsize=(16.2, 10.6), dpi=200, facecolor=C_BG)
    fig.add_artist(Rectangle((0.012, 0.012), 0.976, 0.976, fill=False,
                             edgecolor=C_DARK, linewidth=1.8, transform=fig.transFigure))
    fig.text(0.028, 0.966, "BLUEPRINT CAD v11.1 — DOSING GESER 1-NOZZLE MASUK KE TIAP SLOT & REL SELIP ANCAK ANTI-TABRAKAN",
             fontsize=12.4, fontweight="bold", color=C_DARK, va="top")
    fig.text(0.028, 0.942, "Perbaikan v11.1: (1) Unit Dosing bergeser di rel belakang menuang langsung ke Slot 1→6  (2) Rel Selip L-Channel rendah bebas press  (3) Guide Ø12 di luar ancak",
             fontsize=8.3, color=C_SLATE, va="top")
    fig.text(0.972, 0.965, "CAD v11.1 • ZERO-BUG", fontsize=9, fontweight="bold", color="#047857",
             ha="right", va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor="#ECFDF5", edgecolor="#34D399"))

    fig.add_artist(Rectangle((0.018, 0.018), 0.964, 0.055, facecolor="#F8FAFC",
                             edgecolor=C_DARK, linewidth=0.9, transform=fig.transFigure))
    fig.text(0.030, 0.052, "RANGKA TERPADU: 900 (L) × 1420 (T) × 580 (D) mm   |   GUIDE SHAFT: X=95 & 805 mm (35 mm DI LUAR ANCAK)   |   PRESS HOME: h=750 mm (+55 mm BEBAS FLIP)",
             fontsize=7.9, fontweight="bold", color=C_DARK, va="center")
    fig.text(0.030, 0.030, "DOSING GESER BELAKANG (Z=460): SLOT 1→6 (PITCH 76 mm) + CORONG TUANG BERENGSEL   |   PENGUNCI ANCAK: REL SELIP L-CHANNEL + PALANG MAGNET 16 kgf",
             fontsize=7.5, color=C_SLATE, va="center")

    # Axis Kiri: Tampak Depan (900 x 1420)
    ax1 = fig.add_axes([0.055, 0.100, 0.440, 0.785])
    ax1.set_aspect("equal", adjustable="box")
    ax1.grid(True, ls=":", lw=0.5, color="#CBD5E1", alpha=0.7)
    ax1.set_axisbelow(True)
    for sp in ax1.spines.values():
        sp.set_visible(False)
    ax1.set_title("TAMPAK DEPAN — RANGKA TERPADU + DOSING GESER SLOT 1→6", fontsize=9.0, fontweight="bold", color=C_DARK, pad=8)

    for r in [(0, 0, 40, 1420), (860, 0, 40, 1420),
              (40, 40, 820, 40), (40, 160, 820, 40), (40, 340, 820, 40), (40, 1100, 820, 40), (40, 1380, 820, 40)]:
        ax1.add_patch(Rectangle((r[0], r[1]), r[2], r[3], ec=C_FRAME, fc=C_FRAME_F, lw=1.3, zorder=3))
    for xk in [0, 860]:
        ax1.add_patch(Rectangle((xk + 10, -28), 20, 28, ec=C_FRAME, fc="#94A3B8", lw=1.0, zorder=3))
        ax1.add_patch(Rectangle((xk, -40), 40, 12, ec=C_FRAME, fc="#475569", lw=1.1, zorder=3))

    # Rel Geser Belakang + Unit Dosing di posisi Slot 1 (X=255) dengan panah geser ke Slot 6!
    for ry in [805, 1305]:
        ax1.add_patch(Rectangle((40, ry), 820, 12, ec="#64748B", fc="#E2E8F0", lw=0.9, ls="--", zorder=1))
    ax1.add_patch(Polygon([(180, 1320), (330, 1320), (285, 1080), (225, 1080)], closed=True, ec="#1D4ED8", fc="#DBEAFE", lw=1.3, alpha=0.75, zorder=2))
    ax1.add_patch(Rectangle((210, 880), 90, 115, ec="#1D4ED8", fc="#EFF6FF", lw=1.2, alpha=0.8, zorder=2))
    ax1.add_patch(Rectangle((215, 852), 80, 24, ec=C_MAGNET, fc="#FEE2E2", lw=1.1, zorder=2))
    ax1.add_patch(Rectangle((230, 610), 50, 240, ec="#0284C7", fc="#BAE6FD", lw=1.2, ls="--", alpha=0.6, zorder=4))
    ax1.annotate("", xy=(650, 1220), xytext=(345, 1220), arrowprops=dict(arrowstyle="<->", color="#1D4ED8", lw=2.0), zorder=5)
    ax1.text(500, 1255, "Unit Dosing Geser\nSlot 1 ↔ Slot 6 (Pitch 76 mm)", fontsize=7.0, fontweight="bold", color="#1D4ED8", ha="center", zorder=6)

    # Panel ABS & PSU
    ax1.add_patch(Rectangle((150, 200), 270, 120, ec=C_MAGNET, fc="#FEE2E2", lw=1.2, zorder=4))
    ax1.text(285, 260, "PANEL ABS\nESP32 + TB6600 + L298N", fontsize=6.9, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)
    ax1.add_patch(Rectangle((490, 200), 220, 110, ec=C_MAGNET, fc="#FEE2E2", lw=1.2, zorder=4))
    ax1.text(600, 255, "PSU 12V 10A\n+ LM2596", fontsize=6.9, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)

    # Laci Penyambut h=520
    ax1.add_patch(Rectangle((125, 496), 650, 24, ec=C_MECH, fc=C_MECH_F, lw=1.2, ls="--", alpha=0.55, zorder=4))
    ax1.text(450, 508, "LACI PENYAMBUT (h = 520 mm)", fontsize=6.5, fontweight="bold", color="#065F46", ha="center", va="center", zorder=5)

    # Cetakan + Rel Selip L-Channel + Ancak 0 mm + Guide Shaft di X=95 & 805 (LUAR Ancak!)
    ax1.add_patch(Rectangle((40, 520), 30, 80, ec=C_MECH, fc=C_MECH_F, lw=1.2, zorder=5))
    ax1.add_patch(Rectangle((830, 520), 30, 80, ec=C_MECH, fc=C_MECH_F, lw=1.2, zorder=5))
    ax1.add_patch(Rectangle((70, 550), 760, 20, ec=C_MECH, fc=C_MECH_F, lw=1.0, zorder=4))
    ax1.add_patch(Rectangle((154.5, 542), 591, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.5, zorder=6))
    for i in range(6):
        sx = 222 + i * 76
        ax1.add_patch(Rectangle((sx, 545), 66, 30, ec=C_PLASTIC, fc="#FEF3C7", lw=1.1, zorder=7))
        ax1.text(sx + 33, 560, f"S{i + 1}", fontsize=7.0, fontweight="bold", color="#78350F", ha="center", va="center", zorder=8)
    ax1.add_patch(Rectangle((130, 578), 640, 18, ec=C_ANCAK, fc=C_ANCAK_F, lw=1.4, hatch="///", zorder=7))
    # Rel Selip L-Channel kiri & kanan (tidak menabrak Guide Shaft!)
    ax1.add_patch(Rectangle((120, 574), 16, 28, ec=C_DARK, fc="#94A3B8", lw=1.2, zorder=8))
    ax1.add_patch(Rectangle((764, 574), 16, 28, ec=C_DARK, fc="#94A3B8", lw=1.2, zorder=8))

    # Guide Shaft X=95 & X=805 (35 mm di LUAR Ancak!) + Pelat Press HOME h=750
    for gx in [95, 805]:
        ax1.add_patch(Rectangle((gx - 5, 380), 10, 720, ec="#475569", fc="#CBD5E1", lw=1.1, zorder=5))
        ax1.add_patch(Rectangle((gx - 13, 760), 26, 30, ec=C_MECH, fc=C_MECH_F, lw=1.1, zorder=7))
    ax1.add_patch(Rectangle((75, 770), 750, 5, ec=C_PRESS, fc=C_PRESS_F, lw=1.5, zorder=6))
    for i in range(6):
        ax1.add_patch(Rectangle((223 + i * 76, 750), 64, 20, ec=C_PRESS, fc=C_PRESS_F, lw=1.1, zorder=6))
    ax1.add_patch(Rectangle((418, 845), 64, 230, ec=C_MAGNET, fc="#FEE2E2", lw=1.5, zorder=6))
    ax1.text(450, 960, "ACTUATOR\n1500N\nStroke 200", fontsize=6.9, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    ax1.add_patch(Rectangle((440, 795), 20, 50, ec="#334155", fc="#CBD5E1", lw=1.1, zorder=6))
    ax1.add_patch(Rectangle((428, 775), 44, 20, ec=C_MECH, fc=C_MECH_F, lw=1.1, zorder=6))
    ax1.add_patch(Rectangle((428, 1075), 44, 25, ec=C_MECH, fc=C_MECH_F, lw=1.1, zorder=6))

    ax1.set_xlim(-60, 960)
    ax1.set_ylim(-65, 1475)
    ax1.set_xlabel("X / Lebar Total = 900 mm (Kompak & Simetris)", fontsize=7.8, color=C_SLATE)
    ax1.set_ylabel("Y / Tinggi (mm)", fontsize=7.8, color=C_SLATE)
    ax1.tick_params(labelsize=7.2, colors=C_SLATE)

    # Axis Kanan: Tampak Samping (Pembuktian Corong Masuk Slot + Rel Selip + Laci Penyambut)
    ax2 = fig.add_axes([0.555, 0.100, 0.415, 0.785])
    ax2.set_aspect("equal", adjustable="box")
    ax2.grid(True, ls=":", lw=0.5, color="#CBD5E1", alpha=0.7)
    ax2.set_axisbelow(True)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.set_title("TAMPAK SAMPING — CORONG MASUK SLOT + REL SELIP + LACI", fontsize=9.0, fontweight="bold", color=C_DARK, pad=8)

    FD = 580
    for r in [(0, 0, 40, 1420), (FD - 40, 0, 40, 1420),
              (40, 40, FD - 80, 40), (40, 160, FD - 80, 40), (40, 340, FD - 80, 40),
              (40, 1100, FD - 80, 40), (40, 1380, FD - 80, 40)]:
        ax2.add_patch(Rectangle((r[0], r[1]), r[2], r[3], ec=C_FRAME, fc=C_FRAME_F, lw=1.3, zorder=3))
    for zk in [0, FD - 40]:
        ax2.add_patch(Rectangle((zk + 10, -28), 20, 28, ec=C_FRAME, fc="#94A3B8", lw=1.0, zorder=3))
        ax2.add_patch(Rectangle((zk, -40), 40, 12, ec=C_FRAME, fc="#475569", lw=1.1, zorder=3))

    AS_Z, AS_Y = 200, 560
    ax2.add_patch(Circle((AS_Z, AS_Y), 135, ec=C_MAGNET, fc="#FEE2E2", lw=1.2, ls="--", alpha=0.22, zorder=2))
    ax2.add_patch(Circle((AS_Z, AS_Y), 135, ec=C_MAGNET, fc="none", lw=1.2, ls="--", zorder=5))

    # Cetakan + Ancak (Rel Selip L-Channel profil rendah 24 mm -> 0% tabrak press!)
    ax2.add_patch(Rectangle((AS_Z - 120, AS_Y - 18), 240, 36, ec=C_MOLD, fc=C_MOLD_F, lw=1.6, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 124, AS_Y + 18), 248, 18, ec=C_ANCAK, fc=C_ANCAK_F, lw=1.4, hatch="///", zorder=7))
    ax2.add_patch(Rectangle((AS_Z - 128, AS_Y + 36), 256, 6, ec=C_DARK, fc="#94A3B8", lw=1.2, zorder=8))  # Bibir Rel L-Channel
    ax2.add_patch(Rectangle((AS_Z - 134, AS_Y + 14), 10, 28, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.3, zorder=8)) # Palang Kunci Depan + Magnet
    ax2.add_patch(Circle((AS_Z, AS_Y), 10, ec=C_MECH, fc="#FFFFFF", lw=1.5, zorder=9))

    # NEMA 23 + Belt HTD3M-384
    ax2.add_patch(Rectangle((120 - 28, 460 - 28), 56, 56, ec=C_MAGNET, fc="#FEE2E2", lw=1.3, zorder=6))
    ax2.add_patch(Circle((120, 460), 10, ec=C_MECH, fc=C_MECH_F, lw=1.4, zorder=8))
    ax2.add_patch(Circle((AS_Z, AS_Y), 29, ec=C_MECH, fc="none", lw=1.6, zorder=7))
    ax2.plot([112, 177], [467, 578], color=C_DARK, lw=1.8, zorder=8)
    ax2.plot([128, 223], [453, 542], color=C_DARK, lw=1.8, zorder=8)

    # Press HOME h=750 (+55 mm bebas flip!)
    ax2.add_patch(Rectangle((AS_Z - 112.5, 770), 225, 5, ec=C_PRESS, fc=C_PRESS_F, lw=1.5, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 105, 750), 210, 20, ec=C_PRESS, fc=C_PRESS_F, lw=1.2, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 32, 845), 64, 230, ec=C_MAGNET, fc="#FEE2E2", lw=1.5, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 10, 795), 20, 50, ec="#334155", fc="#CBD5E1", lw=1.1, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 22, 775), 44, 20, ec=C_MECH, fc=C_MECH_F, lw=1.1, zorder=6))
    ax2.add_patch(Rectangle((AS_Z - 22, 1075), 44, 25, ec=C_MECH, fc=C_MECH_F, lw=1.1, zorder=6))

    # UNIT DOSING BELAKANG (Z=460) + CORONG TUANG MIRING MASUK LANGSUNG KE CETAKAN (Z=200)!
    ax2.add_patch(Polygon([(395, 1320), (535, 1320), (495, 1075), (435, 1075)], closed=True, ec="#1D4ED8", fc="#DBEAFE", lw=1.4, zorder=5))
    ax2.text(465, 1200, "HOPPER\n1-NOZZLE", fontsize=6.8, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=6)
    ax2.add_patch(Rectangle((435, 1030), 60, 45, ec="#1D4ED8", fc="#BFDBFE", lw=1.1, zorder=5))
    ax2.add_patch(Rectangle((495, 1034), 34, 34, ec=C_MAGNET, fc=C_MAGNET_F, lw=1.1, zorder=6))
    ax2.add_patch(Rectangle((415, 885), 100, 110, ec="#1D4ED8", fc="#EFF6FF", lw=1.4, zorder=5))
    draw_beans(ax2, 420, 890, 90, 62, seed=88, count=36, zorder=6)
    ax2.add_patch(Rectangle((420, 855), 90, 24, ec=C_MAGNET, fc="#FEE2E2", lw=1.3, zorder=6))
    ax2.text(465, 867, "LOAD CELL", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    # Corong tuang miring masuk ke cetakan Z=200!
    ax2.add_patch(Polygon([(420, 855), (195, 635), (222, 610), (445, 830)], closed=True, ec="#0284C7", fc="#BAE6FD", lw=1.3, ls="--", alpha=0.65, zorder=5))
    ax2.annotate("", xy=(205, 585), xytext=(425, 835), arrowprops=dict(arrowstyle="->", color=C_SOY, lw=2.0), zorder=8)

    # Laci Penyambut di depan (h=520)
    ax2.add_patch(Rectangle((-230, 498), 250, 22, ec=C_MECH, fc=C_MECH_F, lw=1.5, zorder=7))
    ax2.text(-105, 509, "LACI PENYAMBUT", fontsize=6.4, fontweight="bold", color="#065F46", ha="center", va="center", zorder=8)
    ax2.add_patch(Rectangle((AS_Z - 125, 498), 250, 22, ec=C_MECH, fc=C_MECH_F, lw=1.1, ls="--", alpha=0.45, zorder=4))
    ax2.annotate("", xy=(90, 509), xytext=(22, 509), arrowprops=dict(arrowstyle="<->", color=C_MECH, lw=1.8), zorder=9)

    ax2.annotate("HOME Press h=750\n(+55 mm bebas flip!)", xy=(AS_Z - 105, 760), xytext=(-245, 850),
                 fontsize=6.7, fontweight="bold", color=C_PRESS,
                 bbox=dict(boxstyle="round,pad=0.25", fc="#F5F3FF", ec=C_PRESS),
                 arrowprops=dict(arrowstyle="->", color=C_PRESS, lw=1.0))
    ax2.annotate("Corong Tuang Miring\nMasuk LANGSUNG ke Slot!\n(Dilipat mundur saat press)", xy=(315, 725), xytext=(FD + 35, 725),
                 fontsize=6.7, fontweight="bold", color="#0284C7",
                 bbox=dict(boxstyle="round,pad=0.25", fc="#F0F9FF", ec="#0284C7"),
                 arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.1))
    ax2.annotate("Rel Selip L-Channel\n+ Palang Magnet Depan\n(0% tabrak Press!)", xy=(AS_Z - 134, AS_Y + 28), xytext=(-245, 650),
                 fontsize=6.6, fontweight="bold", color=C_MAGNET,
                 bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec=C_MAGNET),
                 arrowprops=dict(arrowstyle="->", color=C_MAGNET, lw=1.0))

    ax2.set_xlim(-275, FD + 265)
    ax2.set_ylim(-65, 1475)
    ax2.set_xlabel("Z / Kedalaman = 580 mm  [Depan ← 0 ... 580 → Belakang]", fontsize=7.6, color=C_SLATE)
    ax2.tick_params(labelsize=7.2, colors=C_SLATE)

    png_path = os.path.join(OUT, "v11_arsitektur_hibrida.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {dxf_path}\n[OK] {png_path}")


if __name__ == "__main__":
    build_process_storyboard()
    build_v11_cad()
    print("\n=== VISUALISASI PROSES & CAD v11 BERHASIL DIBUAT ===")
