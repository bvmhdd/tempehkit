"""
Generator Blueprint v13 — Mekanisme Naik-Turun Cetakan Terbalik (+65 mm Vertical Demolding)
===========================================================================================
Menampilkan secara detail:
  1. Kenapa diperlukan Vertical Demolding (+65 mm):
     Jika laci ditarik saat dinding cetakan terbalik masih turun, dinding cetakan akan
     menabrak & merusak 6 balok tempe!
  2. OPSI 1 (Mold Elevator Naik-Turun +65 mm — Dual Lead Screw T8 Sinkron + Hard-Stop 1500N):
     - Bearing UCFL 204 + NEMA 23 duduk di Sub-Frame Elevator kiri & kanan
     - Digerakkan 2× Lead Screw T8 sinkron (1× NEMA 17 + Timing Belt GT2 bawah)
     - Di posisi bawah (0 mm), Sub-Frame menumpu di Steel Hard-Stop -> 100% gaya press
       1500 N ditahan rangka besi (Lead Screw T8 100% aman!)
     - Setelah Flip 180° & Magnet OFF -> Elevator mengangkat cetakan kosong +65 mm ke atas
       (clearance +35 mm di atas tempe & +69 mm di bawah Press HOME!) -> Laci tarik keluar!
  3. OPSI 2 (Alternatif Hemat — Laci Penyambut Naik-Turun -65 mm):
     - Cetakan dibaut mati ke rangka; hanya Laci Penyambut (~3 kg) yang turun -65 mm
       memakai 1× Mini Linear Actuator 12V 300N (lebih murah & lebih kaku!).

Output:
  - cad/v13_desain_elevator_demolding.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

OUT = os.path.dirname(os.path.abspath(__file__))

C_BG     = "#FFFFFF"
C_DARK   = "#0F172A"
C_SLATE  = "#475569"
C_FRAME  = "#334155"
C_FRAMEF = "#E2E8F0"
C_MOLD   = "#92400E"
C_MOLDF  = "#FDE68A"
C_PRESS  = "#6D28D9"
C_PRESSF = "#DDD6FE"
C_MECH   = "#047857"
C_MECHF  = "#D1FAE5"
C_ELEV   = "#0284C7"
C_ELEVF  = "#E0F2FE"
C_RED    = "#DC2626"
C_REDF   = "#FEE2E2"
C_GOLD   = "#A16207"
C_GOLDF  = "#FEF08A"


def build_v13():
    fig = plt.figure(figsize=(16.4, 10.6), dpi=200, facecolor=C_BG)
    fig.add_artist(Rectangle((0.012, 0.012), 0.976, 0.976, fill=False,
                             edgecolor=C_DARK, linewidth=1.8, transform=fig.transFigure))

    fig.text(0.028, 0.966, "DESAIN v13 — MEKANISME NAIK–TURUN PELEPASAN CETAKAN (+65 mm VERTICAL DEMOLDING)",
             fontsize=13.0, fontweight="bold", color=C_DARK, va="top")
    fig.text(0.028, 0.942, "Memastikan ke-6 Balok Tempe 100% Bebas dari Dinding Cetakan Terbalik Sebelum Laci Penyambut Ditarik Keluar — Perbandingan Opsi 1 (Mold Lift) vs Opsi 2 (Drawer Lift)",
             fontsize=8.4, color=C_SLATE, va="top")
    fig.text(0.972, 0.965, "REV v13.0 • DEMOLDING LIFT", fontsize=9, fontweight="bold", color=C_ELEV,
             ha="right", va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor=C_ELEVF, edgecolor="#38BDF8"))

    # Footer komparasi harga
    fig.add_artist(Rectangle((0.018, 0.018), 0.964, 0.058, facecolor="#F8FAFC",
                             edgecolor=C_DARK, linewidth=0.9, transform=fig.transFigure))
    fig.text(0.030, 0.056, "ESTIMASI TAMBAHAN BIAYA OPSI 1 (Mold Elevator Naik +65 mm — Dual T8 Sinkron + Hard-Stop):  +Rp 480.000 s/d Rp 580.000  (Total Full-Auto: ~Rp 4,9–5,1 jt)",
             fontsize=8.0, fontweight="bold", color=C_ELEV, va="center")
    fig.text(0.030, 0.032, "ESTIMASI TAMBAHAN BIAYA OPSI 2 (Alternatif Hemat: Laci Penyambut Turun -65 mm — 1× Mini Actuator 300N):  +Rp 280.000 s/d Rp 360.000  (Lebih murah Rp 200 rb & rangka 100% kaku!)",
             fontsize=7.8, fontweight="bold", color=C_MECH, va="center")

    # 3 Panel: [1] Sebelum Lift (Terkurung) | [2] Opsi 1: Mold Lift-Up +65 mm (Detail T8 & Hard-Stop) | [3] Opsi 2: Alternatif Laci Turun -65 mm
    panels = [
        [0.030, 0.105, 0.295, 0.800],
        [0.350, 0.105, 0.310, 0.800],
        [0.685, 0.105, 0.285, 0.800],
    ]

    # ═══════════════════════════════════════════════════════════
    # PANEL 1: MASALAH TANPA GERAKAN NAIK-TURUN
    # ═══════════════════════════════════════════════════════════
    ax = fig.add_axes(panels[0])
    ax.set_xlim(0, 180); ax.set_ylim(0, 260)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#FCA5A5"); sp.set_linewidth(1.4)
    ax.add_patch(Rectangle((0, 232), 180, 28, facecolor="#991B1B", edgecolor="none", zorder=10))
    ax.text(8, 250, "1. KENAPA BUTUH LIFT +65 mm?", fontsize=8.4, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(8, 239, "Jika cetakan tidak diangkat, dindingnya menabrak tempe!", fontsize=6.6, color="#FECACA", va="center", zorder=11)

    # Tampak samping: Press HOME atas, Cetakan terbalik membungkus tempe, Laci di bawah
    ax.add_patch(Rectangle((35, 195), 110, 14, ec=C_PRESS, fc=C_PRESSF, lw=1.3, zorder=4))
    ax.text(90, 202, "Press HOME (h=750)", fontsize=6.6, fontweight="bold", color=C_PRESS, ha="center", va="center", zorder=5)

    # Cetakan terbalik (dinding turun ke Y=115 membungkus tempe!)
    ax.add_patch(Rectangle((38, 136), 104, 10, ec=C_MOLD, fc=C_MOLDF, lw=1.5, zorder=5))
    ax.add_patch(Rectangle((38, 106), 9, 30, ec=C_MOLD, fc=C_MOLDF, lw=1.5, zorder=5))
    ax.add_patch(Rectangle((133, 106), 9, 30, ec=C_MOLD, fc=C_MOLDF, lw=1.5, zorder=5))
    # Tempe di dalam dinding cetakan
    ax.add_patch(Rectangle((49, 106), 82, 28, ec=C_ELEV, fc="#FEF3C7", lw=1.4, zorder=4))
    ax.text(90, 120, "TEMPE TERKURUNG\nDI DALAM DINDING\nCETAKAN (36 mm)", fontsize=6.6, fontweight="bold", color="#78350F", ha="center", va="center", zorder=6)
    # Ancak & Laci di bawah
    ax.add_patch(Rectangle((32, 95), 116, 11, ec=C_GOLD, fc=C_GOLDF, lw=1.4, hatch="///", zorder=5))
    ax.add_patch(Rectangle((24, 83), 132, 12, ec=C_MECH, fc=C_MECHF, lw=1.4, zorder=5))
    ax.text(90, 89, "LACI PENYAMBUT (h=520)", fontsize=6.5, fontweight="bold", color=C_MECH, ha="center", va="center", zorder=6)

    # Tanda tabrakan jika laci ditarik ke kiri!
    ax.annotate("", xy=(14, 120), xytext=(45, 120), arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2), zorder=8)
    ax.add_patch(Circle((42, 120), 9, ec=C_RED, fc=C_REDF, lw=1.8, alpha=0.8, zorder=7))
    ax.text(42, 120, "✕", fontsize=11, fontweight="bold", color=C_RED, ha="center", va="center", zorder=9)
    ax.annotate("TABRAKAN!\nDinding cetakan 36 mm\nmenyeret/merusak tempe\njika laci langsung ditarik!",
                xy=(42, 112), xytext=(90, 42), fontsize=6.8, fontweight="bold", color="#991B1B", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc=C_REDF, ec=C_RED),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.3))

    # ═══════════════════════════════════════════════════════════
    # PANEL 2: OPSI 1 — MOLD ELEVATOR NAIK +65 mm (DUAL T8 + HARD-STOP)
    # ═══════════════════════════════════════════════════════════
    ax = fig.add_axes(panels[1])
    ax.set_xlim(0, 220); ax.set_ylim(0, 260)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#38BDF8"); sp.set_linewidth(1.6)
    ax.add_patch(Rectangle((0, 232), 220, 28, facecolor="#0369A1", edgecolor="none", zorder=10))
    ax.text(8, 250, "2. OPSI 1: MOLD ELEVATOR NAIK +65 mm (Tampak Depan)", fontsize=8.1, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(8, 239, "Dual Lead Screw T8 Sinkron + Hard-Stop 1500N (Aman saat Press!)", fontsize=6.6, color="#E0F2FE", va="center", zorder=11)

    # Tiang Rangka Kiri & Kanan
    ax.add_patch(Rectangle((8, 12), 14, 214, ec=C_FRAME, fc=C_FRAMEF, lw=1.3, zorder=2))
    ax.add_patch(Rectangle((198, 12), 14, 214, ec=C_FRAME, fc=C_FRAMEF, lw=1.3, zorder=2))

    # Press HOME di atas (Y=205 -> +69 mm clearance masih lega!)
    ax.add_patch(Rectangle((34, 206), 152, 10, ec=C_PRESS, fc=C_PRESSF, lw=1.3, zorder=4))
    ax.text(110, 211, "PRESS HOME (h=750) — Sisa Ruang +69 mm!", fontsize=6.2, fontweight="bold", color=C_PRESS, ha="center", va="center", zorder=5)

    # 2x LEAD SCREW T8 + GUIDE SHAFT VERTIKAL KIRI (X=30) & KANAN (X=190)
    for lx in [30, 190]:
        ax.add_patch(Rectangle((lx - 3, 40), 6, 155, ec=C_ELEV, fc=C_ELEVF, lw=1.2, hatch="---", zorder=4))
        # Bearing KFL08 atas & bawah
        ax.add_patch(Rectangle((lx - 8, 190), 16, 7, ec=C_FRAME, fc="#94A3B8", lw=1.0, zorder=5))
        ax.add_patch(Rectangle((lx - 8, 40), 16, 7, ec=C_FRAME, fc="#94A3B8", lw=1.0, zorder=5))
        # Pulley GT2 sinkron di bawah
        ax.add_patch(Rectangle((lx - 7, 30), 14, 9, ec=C_MECH, fc=C_MECHF, lw=1.2, zorder=6))
        # STEEL HARD-STOP 1500N di posisi duduk normal (Y=118)
        ax.add_patch(Rectangle((lx - 8, 106), 16, 12, ec=C_RED, fc=C_REDF, lw=1.3, zorder=5))

    # Belt GT2 Sinkron Bawah + 1x NEMA 17 Penggerak Elevator (X=110, Y=26)
    ax.plot([30, 190], [34.5, 34.5], color=C_DARK, lw=2.2, zorder=7)
    ax.add_patch(Rectangle((94, 16), 32, 22, ec=C_RED, fc=C_REDF, lw=1.3, zorder=8))
    ax.text(110, 27, "NEMA 17\nElevator", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=9)

    # SUB-FRAME ELEVATOR + BEARING UCFL 204 TERANGKAT NAIK +65 mm (ke Y=155)!
    ax.add_patch(Rectangle((24, 146), 16, 26, ec=C_ELEV, fc="#BAE6FD", lw=1.5, zorder=6))
    ax.add_patch(Rectangle((180, 146), 16, 26, ec=C_ELEV, fc="#BAE6FD", lw=1.5, zorder=6))
    # Cetakan kosong terbalik SUDAH TERANGKAT NAIK +65 mm!
    ax.add_patch(Rectangle((46, 152), 128, 22, ec=C_MOLD, fc=C_MOLDF, lw=1.6, zorder=6))
    ax.text(110, 163, "CETAKAN TERANGKAT +65 mm\n(Kosong — Lubang Angin Anti-Vakum)", fontsize=6.1, fontweight="bold", color=C_MOLD, ha="center", va="center", zorder=7)
    # Panah naik +65 mm
    ax.annotate("", xy=(38, 178), xytext=(38, 126), arrowprops=dict(arrowstyle="->", color=C_ELEV, lw=2.0), zorder=8)
    ax.annotate("", xy=(182, 178), xytext=(182, 126), arrowprops=dict(arrowstyle="->", color=C_ELEV, lw=2.0), zorder=8)

    # Ruang bebas +35 mm antara cetakan terangkat (152) dan puncak 6 balok tempe (116)!
    ax.annotate("", xy=(110, 151), xytext=(110, 117), arrowprops=dict(arrowstyle="<->", color=C_MECH, lw=1.8), zorder=8)
    ax.text(110, 134, "CLEARANCE +35 mm\nBEBAS TARIK LACI!", fontsize=6.3, fontweight="bold", color=C_MECH,
            ha="center", va="center", bbox=dict(fc="#ECFDF5", ec=C_MECH, pad=1.5), zorder=9)

    # 6 Balok Tempe duduk aman di atas Ancak + Laci Penyambut (Y=82..116)!
    ax.add_patch(Rectangle((44, 82), 132, 9, ec=C_MECH, fc=C_MECHF, lw=1.3, zorder=5))
    ax.add_patch(Rectangle((48, 91), 124, 8, ec=C_GOLD, fc=C_GOLDF, lw=1.3, hatch="///", zorder=5))
    for i in range(6):
        tx = 52 + i * 19.5
        ax.add_patch(Rectangle((tx, 99), 17, 17, ec=C_ELEV, fc="#FEF3C7", lw=1.1, zorder=6))

    ax.annotate("Steel Hard-Stop\n(Tahan Press 1500N!)", xy=(30, 112), xytext=(72, 62),
                fontsize=6.1, fontweight="bold", color=C_RED, ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc=C_REDF, ec=C_RED),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))
    ax.annotate("2× Lead Screw T8\n+ Belt Sinkron Bawah", xy=(190, 52), xytext=(152, 62),
                fontsize=6.1, fontweight="bold", color=C_ELEV, ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc=C_ELEVF, ec=C_ELEV),
                arrowprops=dict(arrowstyle="->", color=C_ELEV, lw=1.0))

    # ═══════════════════════════════════════════════════════════
    # PANEL 3: OPSI 2 (ALTERNATIF HEMAT) — LACI TURUN -65 mm
    # ═══════════════════════════════════════════════════════════
    ax = fig.add_axes(panels[2])
    ax.set_xlim(0, 180); ax.set_ylim(0, 260)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#34D399"); sp.set_linewidth(1.6)
    ax.add_patch(Rectangle((0, 232), 180, 28, facecolor="#047857", edgecolor="none", zorder=10))
    ax.text(8, 250, "3. OPSI 2 (HEMAT): LACI TURUN -65 mm", fontsize=8.1, fontweight="bold", color="#FFFFFF", va="center", zorder=11)
    ax.text(8, 239, "Cetakan dibaut mati (100% kaku 1500N), Laci yg turun!", fontsize=6.6, color="#D1FAE5", va="center", zorder=11)

    # Cetakan dibaut MATI ke rangka utama (Y=164..186) -> 100% kaku!
    ax.add_patch(Rectangle((34, 164), 112, 22, ec=C_MOLD, fc=C_MOLDF, lw=1.6, zorder=5))
    ax.text(90, 175, "CETAKAN TETAP DIAM\n(Dibaut Mati ke Rangka!)", fontsize=6.3, fontweight="bold", color=C_MOLD, ha="center", va="center", zorder=6)

    # Clearance +35 mm terbentuk karena LACI turun -65 mm!
    ax.annotate("", xy=(90, 162), xytext=(90, 128), arrowprops=dict(arrowstyle="<->", color=C_MECH, lw=1.8), zorder=8)
    ax.text(90, 145, "CLEARANCE +35 mm\n(Laci turun -65 mm!)", fontsize=6.3, fontweight="bold", color=C_MECH,
            ha="center", va="center", bbox=dict(fc="#ECFDF5", ec=C_MECH, pad=1.5), zorder=9)

    # Laci + Ancak + 6 Tempe sudah turun ke bawah!
    ax.add_patch(Rectangle((30, 92), 120, 10, ec=C_MECH, fc=C_MECHF, lw=1.4, zorder=5))
    ax.add_patch(Rectangle((35, 102), 110, 8, ec=C_GOLD, fc=C_GOLDF, lw=1.3, hatch="///", zorder=5))
    for i in range(6):
        tx = 39 + i * 17.2
        ax.add_patch(Rectangle((tx, 110), 15, 17, ec=C_ELEV, fc="#FEF3C7", lw=1.1, zorder=6))

    # 1x Mini Linear Actuator 12V 300N + Scissor / 2 Guide Rod (beban cuma 3 kg!)
    ax.add_patch(Rectangle((80, 48), 20, 44, ec=C_RED, fc=C_REDF, lw=1.4, zorder=5))
    ax.text(90, 70, "Mini\nActuator\n300N", fontsize=5.8, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=6)
    for gx in [46, 134]:
        ax.add_patch(Rectangle((gx - 2.5, 48), 5, 62, ec=C_FRAME, fc="#CBD5E1", lw=1.0, zorder=4))
    ax.add_patch(Rectangle((24, 42), 132, 8, ec=C_FRAME, fc=C_FRAMEF, lw=1.3, zorder=5))

    ax.text(90, 22, "KEUNTUNGAN OPSI 2:\n• Beban angkat cuma ~3 kg (bukan 12 kg!)\n• Hemat ±Rp 200 rb & 0 risiko miring saat press!",
            fontsize=6.3, fontweight="bold", color="#065F46", ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#ECFDF5", ec="#34D399"))

    out_path = os.path.join(OUT, "v13_desain_elevator_demolding.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {out_path}")


if __name__ == "__main__":
    build_v13()
