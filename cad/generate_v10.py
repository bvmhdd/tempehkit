"""
Generator CAD 2D v10 (Zero-Collision & Production-Ready)
Mesin Pencetak Tempe Otomatis 6-Slot berbasis ESP32
========================================================
Perbaikan menyeluruh dari generate_v2.py:
  1. Arsitektur 2-Zona Kedalaman (560 mm): Depan = Press + Flip 180°,
     Belakang = Hopper + Weigh-Box Load Cell 20 kg + Swing-In Chute.
  2. Zero-Collision Flip 180°: Poros h=560 mm, sapuan R=135 mm (425..695 mm),
     HOME press di h=720 mm (+25 mm clearance), ancak atas di h=400 mm (+25 mm).
  3. Pad penekan diperbaiki menjadi 64×210 mm (cocok rongga 66×213 mm),
     pelat gantry 700×225 mm dengan 2 Linear Guide Shaft Ø12mm + LM12UU.
  4. Pitch disamakan eksak: Slot = Pad = Chute = 76 mm (bukan 85 mm).
  5. Timing belt tangen geometris akurat (20T -> 60T, C=128 mm, HTD3M-384).
  6. Output:
     - 4 file AutoCAD DXF R2010 bersih (border & dimensi akurat, tanpa tabrak)
     - 4 file Blueprint PNG 200 DPI (gaya gambar teknik putih-biru tajam siap cetak)
"""

import os
import math
import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

OUT = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════════════════════
# KONSTANTA DIMENSI FINAL v10 (SATUAN: mm)
# ═══════════════════════════════════════════════════════════════════════════════
FW = 900       # Lebar total rangka (X)
FH = 1400      # Tinggi total rangka (Y, di atas kaki karet 40mm)
FD = 560       # Kedalaman total rangka (Z): Depan 0..340, Belakang 340..560
HW = 40        # Profil besi hollow 40x40x2.0 mm

# Cetakan 6-Slot SS304
MOLD_W = 591.0     # 67.5 + 6*66 + 5*10 + 67.5
MOLD_D = 240.0     # Kedalaman cetakan
MOLD_H = 36.0      # Tinggi rongga cetakan
MOLD_MG = 67.5     # Margin kiri & kanan
SLOT_W = 66.0      # Lebar rongga
SLOT_L = 213.0     # Panjang rongga
SEKAT_W = 10.0     # Tebal sekat
PITCH = 76.0       # Pitch eksak (66 + 10)
MOLD_X0 = (FW - MOLD_W) / 2.0  # 154.5 mm

# Elevasi Kritis (Y) & Kedalaman (Z)
AS_Y = 560.0       # Pusat poros as Ø20mm
AS_Z = 180.0       # Pusat poros di zona depan
FLIP_R = 135.0     # Radius sapuan aman flip 180° (425..695 mm)
ANCAK_TOP_Y = 400.0
PRESS_HOME_Y = 720.0   # Sisi bawah pad saat HOME (+25mm di atas 695mm)
PRESS_DOWN_Y = 550.0   # Sisi bawah pad saat PRESS (travel 170mm)

# Pelat Gantry Press + 6 Pad
PLATE_W = 700.0    # Lebar pelat gantry (mengikat 2 guide shaft di X=120 & X=780)
PLATE_D = 225.0    # Kedalaman pelat gantry
PLATE_T = 5.0      # Tebal aluminium 5 mm
PAD_W = 64.0       # Lebar pad (clearance 1 mm/sisi vs 66 mm)
PAD_L = 210.0      # Panjang pad (clearance 1.5 mm/sisi vs 213 mm)
PAD_H = 20.0       # Tebal pad + karet food-grade
GUIDE_XL = 120.0   # Linear shaft kiri
GUIDE_XR = 780.0   # Linear shaft kanan

# Transmisi NEMA 23 (Rasio 1:3)
MTR_Z = 100.0      # dZ = -80 mm dari AS_Z=180
MTR_Y = 460.0      # dY = -100 mm dari AS_Y=560 (C = 128.06 mm)
R_20T = 10.0       # Radius pulley 20T (~Ø19.1mm)
R_60T = 29.0       # Radius pulley 60T (~Ø57.3mm)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITAS GEOMETRI TANGEN SABUK (BELT)
# ═══════════════════════════════════════════════════════════════════════════════
def external_tangents(x1, y1, r1, x2, y2, r2):
    """Hitung 2 garis singgung luar antara dua lingkaran (pulley 20T & 60T)."""
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    if d <= abs(r2 - r1):
        return []
    base = math.atan2(dy, dx)
    alpha = math.acos(max(-1.0, min(1.0, (r1 - r2) / d)))
    segs = []
    for sign in (+1, -1):
        ang = base + sign * alpha
        p1 = (x1 + r1 * math.cos(ang), y1 + r1 * math.sin(ang))
        p2 = (x2 + r2 * math.cos(ang), y2 + r2 * math.sin(ang))
        segs.append((p1, p2))
    return segs


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER DXF (AutoCAD R2010 — Bersih, Tertutup, Layer Terstruktur)
# ═══════════════════════════════════════════════════════════════════════════════
LAYER_DEF = {
    "FRAME":      colors.CYAN,
    "MOLD":       colors.YELLOW,
    "PRESS":      colors.MAGENTA,
    "MECHANISM":  colors.GREEN,
    "ELEC":       colors.RED,
    "HOPPER":     colors.BLUE,
    "CLEARANCE":  colors.RED,
    "CENTERLINE": colors.RED,
    "DIM":        3,
    "LABEL":      7,
    "BORDER":     7,
}


def new_dxf():
    doc = ezdxf.new("R2010", setup=True)
    for name, col in LAYER_DEF.items():
        if name not in doc.layers:
            doc.layers.new(name, dxfattribs={"color": col})
    return doc


def dxf_rect(msp, x, y, w, h, layer, linetype=None):
    attrs = {"layer": layer}
    if linetype:
        attrs["linetype"] = linetype
    msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True, dxfattribs=attrs)


def dxf_circ(msp, cx, cy, r, layer, linetype=None):
    attrs = {"layer": layer}
    if linetype:
        attrs["linetype"] = linetype
    msp.add_circle((cx, cy), r, dxfattribs=attrs)


def dxf_cline(msp, x1, y1, x2, y2):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "CENTERLINE", "linetype": "CENTER"})


def dxf_text(msp, x, y, text, h=10, rot=0, align=TextEntityAlignment.MIDDLE_CENTER, layer="LABEL"):
    msp.add_text(text, height=h, dxfattribs={"layer": layer, "rotation": rot}).set_placement((x, y), align=align)


def dxf_dim_h(msp, x1, x2, y_obj, y_dim, label_txt, h=10):
    sign = 1 if y_dim >= y_obj else -1
    msp.add_line((x1, y_obj), (x1, y_dim + sign * 8), dxfattribs={"layer": "DIM"})
    msp.add_line((x2, y_obj), (x2, y_dim + sign * 8), dxfattribs={"layer": "DIM"})
    msp.add_line((x1, y_dim), (x2, y_dim), dxfattribs={"layer": "DIM"})
    msp.add_line((x1 - 4, y_dim - 4), (x1 + 4, y_dim + 4), dxfattribs={"layer": "DIM"})
    msp.add_line((x2 - 4, y_dim - 4), (x2 + 4, y_dim + 4), dxfattribs={"layer": "DIM"})
    ty = y_dim + (8 if sign > 0 else -14)
    dxf_text(msp, (x1 + x2) / 2.0, ty, label_txt, h=h, layer="DIM")


def dxf_dim_v(msp, y1, y2, x_obj, x_dim, label_txt, h=10):
    sign = 1 if x_dim >= x_obj else -1
    msp.add_line((x_obj, y1), (x_dim + sign * 8, y1), dxfattribs={"layer": "DIM"})
    msp.add_line((x_obj, y2), (x_dim + sign * 8, y2), dxfattribs={"layer": "DIM"})
    msp.add_line((x_dim, y1), (x_dim, y2), dxfattribs={"layer": "DIM"})
    msp.add_line((x_dim - 4, y1 - 4), (x_dim + 4, y1 + 4), dxfattribs={"layer": "DIM"})
    msp.add_line((x_dim - 4, y2 - 4), (x_dim + 4, y2 + 4), dxfattribs={"layer": "DIM"})
    tx = x_dim + (12 if sign > 0 else -12)
    dxf_text(msp, tx, (y1 + y2) / 2.0, label_txt, h=h, rot=90, layer="DIM")


def dxf_title_block(msp, bx, by, bw, title, lines, sheet_no):
    """Kop gambar rapi di bawah area gambar — border luar mengelilingi penuh."""
    th = 110
    dxf_rect(msp, bx, by, bw, th, "BORDER")
    msp.add_line((bx, by + th - 32), (bx + bw, by + th - 32), dxfattribs={"layer": "BORDER"})
    dxf_text(msp, bx + bw / 2.0, by + th - 16, title, h=14)
    y_cur = by + th - 48
    for ln in lines:
        dxf_text(msp, bx + bw / 2.0, y_cur, ln, h=9)
        y_cur -= 18
    dxf_text(msp, bx + bw - 14, by + 12, sheet_no, h=8, align=TextEntityAlignment.MIDDLE_RIGHT)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER MATPLOTLIB (Engineering Blueprint Sheet — Putih Bersih 200 DPI)
# ═══════════════════════════════════════════════════════════════════════════════
C_BG = "#FFFFFF"
C_INK = "#111827"
C_FRAME = "#334155"
C_FRAME_FILL = "#E2E8F0"
C_MOLD = "#B45309"
C_MOLD_FILL = "#FEF3C7"
C_PRESS = "#7C3AED"
C_PRESS_FILL = "#EDE9FE"
C_MECH = "#047857"
C_MECH_FILL = "#D1FAE5"
C_ELEC = "#DC2626"
C_ELEC_FILL = "#FEE2E2"
C_HOPPER = "#1D4ED8"
C_HOPPER_FILL = "#DBEAFE"
C_DIM = "#0369A1"
C_GRID = "#F1F5F9"


def make_sheet(figsize, title, subtitle, sheet_tag, spec_lines):
    fig = plt.figure(figsize=figsize, dpi=200, facecolor=C_BG)
    # Border luar kertas teknik
    fig.add_artist(patches.Rectangle((0.015, 0.015), 0.97, 0.97, fill=False,
                                     edgecolor="#0F172A", linewidth=1.8, transform=fig.transFigure))
    fig.add_artist(patches.Rectangle((0.020, 0.020), 0.96, 0.96, fill=False,
                                     edgecolor="#64748B", linewidth=0.6, transform=fig.transFigure))
    # Header
    fig.text(0.035, 0.955, title, fontsize=12.5, fontweight="bold", color="#0F172A", va="top")
    fig.text(0.035, 0.932, subtitle, fontsize=8.5, color="#475569", va="top")
    fig.text(0.965, 0.955, sheet_tag, fontsize=9.5, fontweight="bold", color="#1D4ED8", ha="right", va="top",
             bbox=dict(boxstyle="round,pad=0.35", facecolor="#EFF6FF", edgecolor="#93C5FD", lw=0.9))

    # Footer Title Block (Kop Gambar)
    fig.add_artist(patches.Rectangle((0.020, 0.020), 0.96, 0.075, facecolor="#F8FAFC",
                                     edgecolor="#0F172A", linewidth=1.0, transform=fig.transFigure))
    fig.text(0.032, 0.075, "PROYEK: TEMPEHKIT v10 — MESIN PENCETAK TEMPE OTOMATIS 6-SLOT (ZERO-COLLISION)",
             fontsize=8.5, fontweight="bold", color="#0F172A", va="center")
    fig.text(0.032, 0.045, "   |   ".join(spec_lines), fontsize=7.6, color="#334155", va="center")
    fig.text(0.965, 0.075, "SATUAN: mm  |  PROYEKSI: ORTOGONAL  |  REV: v10.0",
             fontsize=7.6, fontweight="bold", color="#334155", ha="right", va="center")
    fig.text(0.965, 0.045, "STATUS: SIAP FABRIKASI & VERIFIKASI BENGKEL",
             fontsize=7.5, color="#047857", fontweight="bold", ha="right", va="center")

    ax = fig.add_axes([0.055, 0.125, 0.89, 0.78])
    ax.set_facecolor(C_BG)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", linewidth=0.5, color="#CBD5E1", alpha=0.7)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(colors="#64748B", labelsize=7.5)
    return fig, ax


def mpl_rect(ax, x, y, w, h, ec, fc="none", lw=1.2, ls="-", alpha=1.0, zorder=3, hatch=None):
    r = patches.Rectangle((x, y), w, h, edgecolor=ec, facecolor=fc, linewidth=lw,
                          linestyle=ls, alpha=alpha, zorder=zorder, hatch=hatch)
    ax.add_patch(r)
    return r


def mpl_dim_h(ax, x1, x2, y_obj, y_dim, text, fontsize=7.8, color=C_DIM):
    ax.plot([x1, x1], [y_obj, y_dim], color=color, lw=0.7, ls="-", zorder=6)
    ax.plot([x2, x2], [y_obj, y_dim], color=color, lw=0.7, ls="-", zorder=6)
    ax.annotate("", xy=(x1, y_dim), xytext=(x2, y_dim),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.95, shrinkA=0, shrinkB=0), zorder=7)
    offset = 10 if y_dim >= y_obj else -14
    va = "bottom" if y_dim >= y_obj else "top"
    ax.text((x1 + x2) / 2.0, y_dim + offset * 0.4, text, color=color, fontsize=fontsize,
            fontweight="bold", ha="center", va=va,
            bbox=dict(boxstyle="square,pad=0.12", facecolor=C_BG, edgecolor="none", alpha=0.9), zorder=8)


def mpl_dim_v(ax, y1, y2, x_obj, x_dim, text, fontsize=7.8, color=C_DIM):
    ax.plot([x_obj, x_dim], [y1, y1], color=color, lw=0.7, ls="-", zorder=6)
    ax.plot([x_obj, x_dim], [y2, y2], color=color, lw=0.7, ls="-", zorder=6)
    ax.annotate("", xy=(x_dim, y1), xytext=(x_dim, y2),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.95, shrinkA=0, shrinkB=0), zorder=7)
    side = 1 if x_dim >= x_obj else -1
    ax.text(x_dim + side * 12, (y1 + y2) / 2.0, text, color=color, fontsize=fontsize,
            fontweight="bold", ha="center", va="center", rotation=90,
            bbox=dict(boxstyle="square,pad=0.12", facecolor=C_BG, edgecolor="none", alpha=0.9), zorder=8)


def mpl_callout(ax, xy, xytext, text, color="#0F172A", ha="left", fontsize=7.5):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fontsize, fontweight="bold", color=color,
                ha=ha, va="center",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor=color, lw=0.8, alpha=0.95),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.9, connectionstyle="arc3,rad=0.0"),
                zorder=10)


# ═══════════════════════════════════════════════════════════════════════════════
# LEMBAR 1 — CETAKAN 6-SLOT SS304 (SKALA 1:1, LASER CUT / FABRIKASI)
# ═══════════════════════════════════════════════════════════════════════════════
def build_cetakan():
    # --- DXF ---
    doc = new_dxf()
    msp = doc.modelspace()

    ry = (MOLD_D - SLOT_L) / 2.0  # 13.5 mm
    dxf_rect(msp, 0, 0, MOLD_W, MOLD_D, "MOLD")
    dxf_cline(msp, -35, MOLD_D / 2.0, MOLD_W + 35, MOLD_D / 2.0)

    cx = MOLD_MG
    for i in range(6):
        dxf_rect(msp, cx, ry, SLOT_W, SLOT_L, "MOLD")
        dxf_text(msp, cx + SLOT_W / 2.0, MOLD_D / 2.0 + 12, f"SLOT {i + 1}", h=10)
        dxf_text(msp, cx + SLOT_W / 2.0, MOLD_D / 2.0 - 8, "66x213", h=8)
        # Engsel tutup belakang (2x Ø5)
        dxf_circ(msp, cx + 15, MOLD_D - 7, 2.5, "MECHANISM")
        dxf_circ(msp, cx + SLOT_W - 15, MOLD_D - 7, 2.5, "MECHANISM")
        # Titik penangkap magnet depan (Ø6)
        dxf_circ(msp, cx + SLOT_W / 2.0, 6.75, 3.0, "ELEC")
        cx += SLOT_W
        if i < 5:
            dxf_rect(msp, cx, 0, SEKAT_W, MOLD_D, "MOLD")
            cx += SEKAT_W

    # 8 lubang baut M8 (Ø8.4mm) klem as Ø20mm di margin kiri & kanan
    for xf in [22, 46, MOLD_W - 46, MOLD_W - 22]:
        for yf in [40, MOLD_D - 40]:
            dxf_circ(msp, xf, yf, 4.2, "MECHANISM")

    # Dimensi — dibuat berjenjang agar 0% overlap
    dxf_dim_h(msp, 0, MOLD_W, MOLD_D, MOLD_D + 75, "PANJANG TOTAL = 591.0 mm", h=10)
    dxf_dim_h(msp, MOLD_MG, MOLD_MG + SLOT_W, MOLD_D, MOLD_D + 42, "66 mm", h=9)
    dxf_dim_h(msp, MOLD_MG + SLOT_W + SEKAT_W, MOLD_MG + 2 * SLOT_W + SEKAT_W, MOLD_D, MOLD_D + 42, "PITCH = 76 mm", h=9)
    dxf_dim_h(msp, MOLD_MG + 2 * SLOT_W + SEKAT_W, MOLD_MG + 2 * SLOT_W + 2 * SEKAT_W, 0, -35, "SEKAT 10 mm", h=8)
    dxf_dim_h(msp, 0, MOLD_MG, 0, -35, "67.5 mm", h=8)
    dxf_dim_v(msp, 0, MOLD_D, 0, -60, "LEBAR = 240.0 mm", h=10)
    dxf_dim_v(msp, ry, ry + SLOT_L, MOLD_W, MOLD_W + 50, "RONGGA = 213.0 mm", h=10)

    # Title block & Outer Border yang MENGELILINGI seluruh isi
    dxf_title_block(
        msp, -95, -185, MOLD_W + 190,
        "CETAKAN TEMPE 6-SLOT SIMULTAN — STAINLESS STEEL SUS304 (1.5 mm)",
        [
            "RONGGA: 6 x (66 x 213 x 36 mm)  |  SEKAT: 10 mm  |  PITCH EKSAK: 76.0 mm",
            "MARGIN KIRI/KANAN: 67.5 mm (KLEM AS Ø20 mm, 8x BAUT M8)  |  SKALA 1:1",
            "PROSES: LASER CUT / WATERJET + TEKUK & LAS TIG FOOD-GRADE",
        ],
        "LEMBAR 1/4",
    )
    dxf_rect(msp, -105, -195, MOLD_W + 210, MOLD_D + 305, "BORDER")
    dxf_path = os.path.join(OUT, "v10_cetakan_6slot.dxf")
    doc.saveas(dxf_path)

    # --- PNG Blueprint ---
    fig, ax = make_sheet(
        (13.5, 8.2),
        "GAMBAR FABRIKASI — CETAKAN TEMPE 6-SLOT SIMULTAN (v10)",
        "Tampak Atas (Plan View) — Bahan: Stainless Steel SUS304 Tebal 1.5 mm — Kedalaman Rongga: 36 mm",
        "LEMBAR 1 / 4  •  LASER CUT 1:1",
        ["Panjang Total: 591 mm", "Lebar: 240 mm", "6 Slot @ 66×213×36 mm", "Pitch Eksak: 76 mm (Fix v10)"],
    )

    mpl_rect(ax, 0, 0, MOLD_W, MOLD_D, C_MOLD, C_MOLD_FILL, lw=1.8, zorder=2)
    ax.plot([-40, MOLD_W + 40], [MOLD_D / 2, MOLD_D / 2], color=C_ELEC, lw=0.9, ls="-.", zorder=5)
    ax.text(MOLD_W + 44, MOLD_D / 2, "SUMBU AS\nØ20 mm", color=C_ELEC, fontsize=7.2, fontweight="bold", va="center")

    cx = MOLD_MG
    for i in range(6):
        mpl_rect(ax, cx, ry, SLOT_W, SLOT_L, C_MOLD, "#FFFFFF", lw=1.4, zorder=3)
        ax.text(cx + SLOT_W / 2, MOLD_D / 2 + 16, f"S{i + 1}", fontsize=10, fontweight="bold", color="#78350F", ha="center", va="center", zorder=6)
        ax.text(cx + SLOT_W / 2, MOLD_D / 2 - 14, "66×213", fontsize=7.5, color="#92400E", ha="center", va="center", zorder=6)
        # Engsel belakang
        for hx in [cx + 15, cx + SLOT_W - 15]:
            ax.add_patch(patches.Circle((hx, MOLD_D - 7), 2.8, ec=C_MECH, fc=C_MECH_FILL, lw=1.0, zorder=6))
        # Magnet depan
        ax.add_patch(patches.Circle((cx + SLOT_W / 2, 6.75), 3.3, ec=C_ELEC, fc=C_ELEC_FILL, lw=1.0, zorder=6))
        cx += SLOT_W
        if i < 5:
            mpl_rect(ax, cx, 0, SEKAT_W, MOLD_D, C_MOLD, "#FDE68A", lw=0.9, zorder=3)
            cx += SEKAT_W

    # 8 lubang baut M8 klem as
    for xf in [22, 46, MOLD_W - 46, MOLD_W - 22]:
        for yf in [40, MOLD_D - 40]:
            ax.add_patch(patches.Circle((xf, yf), 4.2, ec=C_MECH, fc="#FFFFFF", lw=1.2, zorder=6))
            ax.plot([xf - 6, xf + 6], [yf, yf], color=C_MECH, lw=0.5, zorder=5)
            ax.plot([xf, xf], [yf - 6, yf + 6], color=C_MECH, lw=0.5, zorder=5)

    # Dimensi bebas tabrak
    mpl_dim_h(ax, 0, MOLD_W, MOLD_D, MOLD_D + 54, "PANJANG TOTAL PELAT = 591.0 mm")
    mpl_dim_h(ax, MOLD_MG, MOLD_MG + SLOT_W, MOLD_D, MOLD_D + 24, "66 mm")
    mpl_dim_h(ax, MOLD_MG + 2 * PITCH + SLOT_W / 2, MOLD_MG + 3 * PITCH + SLOT_W / 2, ry + SLOT_L, MOLD_D + 24, "PITCH = 76 mm", color="#7C3AED")
    mpl_dim_h(ax, 0, MOLD_MG, 0, -26, "Margin 67.5 mm")
    mpl_dim_h(ax, MOLD_MG + SLOT_W, MOLD_MG + SLOT_W + SEKAT_W, 0, -26, "Sekat 10 mm")
    mpl_dim_v(ax, 0, MOLD_D, 0, -48, "LEBAR TOTAL = 240.0 mm")
    mpl_dim_v(ax, ry, ry + SLOT_L, MOLD_W, MOLD_W + 24, "PANJANG RONGGA = 213.0 mm")

    # Callout detail
    mpl_callout(ax, (MOLD_MG + 4 * PITCH + 51, MOLD_D - 7), (MOLD_W - 80, MOLD_D + 30),
                "12× Lubang Engsel Tutup Ø5 mm", color=C_MECH, ha="center")
    mpl_callout(ax, (MOLD_MG + 4 * PITCH + 33, 6.75), (MOLD_W - 140, -34),
                "6× Titik Kunci Elektromagnet 12V", color=C_ELEC, ha="center")
    mpl_callout(ax, (46, 40), (140, -52),
                "8× Lubang Baut M8 (Ø8.4 mm)\nKlem Poros As Ø20 mm", color=C_MECH, ha="left")

    ax.set_xlim(-95, MOLD_W + 115)
    ax.set_ylim(-78, MOLD_D + 82)
    ax.set_xlabel("X (mm)", fontsize=8, color="#475569")
    ax.set_ylabel("Z / Lebar Cetakan (mm)", fontsize=8, color="#475569")
    png_path = os.path.join(OUT, "v10_cetakan_6slot.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {dxf_path}\n[OK] {png_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# LEMBAR 2 — PELAT GANTRY PENEKAN + 6 PAD (FIX: PAD 64×210 mm + 2 GUIDE LM12UU)
# ═══════════════════════════════════════════════════════════════════════════════
def build_press_plate():
    doc = new_dxf()
    msp = doc.modelspace()

    dxf_rect(msp, 0, 0, PLATE_W, PLATE_D, "PRESS")
    dxf_cline(msp, -30, PLATE_D / 2, PLATE_W + 30, PLATE_D / 2)
    dxf_cline(msp, PLATE_W / 2, -25, PLATE_W / 2, PLATE_D + 25)

    # Offset X agar 6 pad tepat sejajar rongga cetakan 591mm di tengah pelat 700mm
    # Total lebar 6 slot (luar S1 ke luar S6) = 6*66 + 5*10 = 446 mm
    slots_span = 6 * SLOT_W + 5 * SEKAT_W  # 446 mm
    pad_x0 = (PLATE_W - slots_span) / 2.0 + 1.0  # 128.0 mm
    pad_y0 = (PLATE_D - PAD_L) / 2.0              # 7.5 mm

    for i in range(6):
        px = pad_x0 + i * PITCH
        dxf_rect(msp, px, pad_y0, PAD_W, PAD_L, "PRESS")
        dxf_text(msp, px + PAD_W / 2, PLATE_D / 2 + 16, f"PAD {i + 1}", h=9)
        dxf_text(msp, px + PAD_W / 2, PLATE_D / 2 - 12, "64x210", h=8)

    # Dudukan Clevis M10 di pusat pelat
    dxf_rect(msp, PLATE_W / 2 - 25, PLATE_D / 2 - 25, 50, 50, "MECHANISM")
    dxf_circ(msp, PLATE_W / 2, PLATE_D / 2, 5.5, "MECHANISM")

    # 2 Flange Bearing LM12UU di kiri & kanan (X_pelat = 20..50 & 650..680 -> posisi global X=120 & X=780)
    # Global pelat X = 100..800, jadi guide shaft X=120 -> lokal X=20? Sebaiknya X=30 & X=670 (jarak 640 mm -> global 130 & 770)
    for gx in [35.0, PLATE_W - 35.0]:
        dxf_circ(msp, gx, PLATE_D / 2, 21.0, "MECHANISM")  # Flange LM12UU Ø42
        dxf_circ(msp, gx, PLATE_D / 2, 10.5, "MECHANISM")  # Bore housing Ø21
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            dxf_circ(msp, gx + 16 * math.cos(rad), PLATE_D / 2 + 16 * math.sin(rad), 2.3, "MECHANISM")

    dxf_dim_h(msp, 0, PLATE_W, PLATE_D, PLATE_D + 72, "PANJANG PELAT GANTRY = 700.0 mm", h=10)
    dxf_dim_h(msp, pad_x0, pad_x0 + PAD_W, PLATE_D, PLATE_D + 38, "PAD 64 mm", h=9)
    dxf_dim_h(msp, pad_x0 + PAD_W / 2, pad_x0 + PITCH + PAD_W / 2, 0, -34, "PITCH = 76.0 mm", h=9)
    dxf_dim_h(msp, 35.0, PLATE_W - 35.0, 0, -68, "JARAK LINEAR GUIDE SHAFT = 630.0 mm", h=9)
    dxf_dim_v(msp, 0, PLATE_D, 0, -58, "LEBAR = 225.0 mm", h=10)
    dxf_dim_v(msp, pad_y0, pad_y0 + PAD_L, PLATE_W, PLATE_W + 48, "PAD = 210.0 mm", h=10)

    dxf_title_block(
        msp, -95, -210, PLATE_W + 190,
        "PELAT GANTRY PRESS + 6 PAD PENEKAN (FIX v10: 64x210 mm + DUAL GUIDE)",
        [
            "PELAT: ALUMINIUM 5 mm (700 x 225 mm)  |  6 PAD: AL 15 mm + KARET FOOD-GRADE 5 mm",
            "UKURAN PAD: 64 x 210 mm (CLEARANCE 1-1.5 mm TERHADAP RONGGA 66 x 213 mm)",
            "PEMANDU ANTI-MIRING: 2x LINEAR BUSHING FLANGE LM12UU (JARAK PUSAT 630 mm)",
        ],
        "LEMBAR 2/4",
    )
    dxf_rect(msp, -105, -220, PLATE_W + 210, PLATE_D + 325, "BORDER")
    dxf_path = os.path.join(OUT, "v10_pelat_penekan.dxf")
    doc.saveas(dxf_path)

    # --- PNG Blueprint ---
    fig, ax = make_sheet(
        (13.5, 8.2),
        "GAMBAR FABRIKASI — PELAT GANTRY PRESS & 6 PAD PENEKAN (v10)",
        "Perbaikan v10: Panjang Pad 140 mm -> 210 mm (Presisi Penuh Rongga 213 mm) + Dual Linear Guide LM12UU",
        "LEMBAR 2 / 4  •  CNC / FABRIKASI",
        ["Pelat Aluminium 5 mm: 700×225 mm", "6 Pad: 64×210×20 mm", "Pitch: 76 mm", "Guide Shaft Ø12 mm (Jarak 630 mm)"],
    )

    mpl_rect(ax, 0, 0, PLATE_W, PLATE_D, C_PRESS, C_PRESS_FILL, lw=1.8, zorder=2)
    ax.plot([-30, PLATE_W + 30], [PLATE_D / 2, PLATE_D / 2], color=C_ELEC, lw=0.8, ls="-.", zorder=5)
    ax.plot([PLATE_W / 2, PLATE_W / 2], [-25, PLATE_D + 25], color=C_ELEC, lw=0.8, ls="-.", zorder=5)

    for i in range(6):
        px = pad_x0 + i * PITCH
        mpl_rect(ax, px, pad_y0, PAD_W, PAD_L, C_PRESS, "#FFFFFF", lw=1.4, zorder=3)
        ax.text(px + PAD_W / 2, PLATE_D / 2 + 54, f"PAD {i + 1}", fontsize=8.8, fontweight="bold", color="#5B21B6", ha="center", va="center", zorder=6)
        ax.text(px + PAD_W / 2, PLATE_D / 2 - 54, "64×210", fontsize=7.5, color="#6D28D9", ha="center", va="center", zorder=6)

    # Dudukan clevis tengah
    mpl_rect(ax, PLATE_W / 2 - 25, PLATE_D / 2 - 25, 50, 50, C_MECH, C_MECH_FILL, lw=1.3, alpha=0.85, zorder=7)
    ax.add_patch(patches.Circle((PLATE_W / 2, PLATE_D / 2), 6, ec=C_MECH, fc="#FFFFFF", lw=1.3, zorder=8))

    # 2 Flange LM12UU kiri & kanan
    for gx in [35.0, PLATE_W - 35.0]:
        ax.add_patch(patches.Circle((gx, PLATE_D / 2), 21, ec=C_MECH, fc=C_MECH_FILL, lw=1.4, zorder=6))
        ax.add_patch(patches.Circle((gx, PLATE_D / 2), 10.5, ec=C_MECH, fc="#FFFFFF", lw=1.2, zorder=7))
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            ax.add_patch(patches.Circle((gx + 16 * math.cos(rad), PLATE_D / 2 + 16 * math.sin(rad)), 2.2, ec=C_MECH, fc="#FFFFFF", lw=0.9, zorder=8))

    mpl_dim_h(ax, 0, PLATE_W, PLATE_D, PLATE_D + 52, "PANJANG PELAT GANTRY = 700.0 mm")
    mpl_dim_h(ax, pad_x0, pad_x0 + PAD_W, PLATE_D, PLATE_D + 24, "64 mm")
    mpl_dim_h(ax, pad_x0 + PAD_W / 2, pad_x0 + PITCH + PAD_W / 2, pad_y0, -24, "PITCH = 76 mm", color="#7C3AED")
    mpl_dim_h(ax, 35.0, PLATE_W - 35.0, PLATE_D / 2 - 21, -54, "JARAK PUSAT LINEAR GUIDE LM12UU = 630.0 mm", color=C_MECH)
    mpl_dim_v(ax, 0, PLATE_D, 0, -48, "LEBAR PELAT = 225.0 mm")
    mpl_dim_v(ax, pad_y0, pad_y0 + PAD_L, PLATE_W, PLATE_W + 30, "PANJANG PAD = 210.0 mm")

    mpl_callout(ax, (PLATE_W / 2, PLATE_D / 2 + 25), (PLATE_W / 2 + 150, PLATE_D + 26),
                "Bracket U-Clevis M10\n(Ujung Piston Linear Actuator)", color=C_MECH, ha="left")
    mpl_callout(ax, (35.0, PLATE_D / 2 + 21), (-15, PLATE_D + 28),
                "Flange Bushing LM12UU\n(Anti-Miring Kiri & Kanan)", color=C_MECH, ha="left")

    ax.set_xlim(-95, PLATE_W + 105)
    ax.set_ylim(-85, PLATE_D + 85)
    ax.set_xlabel("X (mm)", fontsize=8, color="#475569")
    ax.set_ylabel("Z (mm)", fontsize=8, color="#475569")
    png_path = os.path.join(OUT, "v10_pelat_penekan.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {dxf_path}\n[OK] {png_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# LEMBAR 3 — TAMPAK DEPAN RANGKA & MEKANISME (FRONT ELEVATION v10)
# ═══════════════════════════════════════════════════════════════════════════════
def build_front():
    doc = new_dxf()
    msp = doc.modelspace()

    # 2 Tiang vertikal depan
    dxf_rect(msp, 0, 0, HW, FH, "FRAME")
    dxf_rect(msp, FW - HW, 0, HW, FH, "FRAME")

    # Kaki karet leveling M10
    for xk in [0, FW - HW]:
        dxf_rect(msp, xk + 10, -28, 20, 28, "FRAME")
        dxf_rect(msp, xk, -40, HW, 12, "FRAME")

    # Palang Horizontal DEPAN (PERHATIKAN: TIDAK ADA palang di Y=560 agar flip bebas!)
    for by in [40, 160, 340, 1070, 1360]:
        dxf_rect(msp, HW, by, FW - 2 * HW, HW, "FRAME")

    # Panel Kontrol & PSU di rak bawah (Y=200)
    dxf_rect(msp, 150, 200, 260, 120, "ELEC")
    dxf_text(msp, 280, 260, "PANEL ABS (ESP32+TB6600+L298N)", h=8)
    dxf_rect(msp, 490, 200, 220, 110, "ELEC")
    dxf_text(msp, 600, 255, "PSU 12V 10A + LM2596", h=8)

    # Ancak Bambu (duduk di atas palang Y=340..380 -> permukaan atas di Y=400)
    dxf_rect(msp, 125, 380, 650, 20, "MECHANISM")
    dxf_text(msp, 450, 390, "ANCAK BAMBU (ATAS h=400 mm)", h=8)

    # Poros As Ø20mm di h=560 & Bearing UCFL 204
    dxf_rect(msp, 70, AS_Y - 10, FW - 140, 20, "MECHANISM")
    dxf_cline(msp, 20, AS_Y, FW - 20, AS_Y)
    dxf_rect(msp, HW, AS_Y - 40, 30, 80, "MECHANISM")
    dxf_rect(msp, FW - HW - 30, AS_Y - 40, 30, 80, "MECHANISM")

    # Cetakan 6-slot tampak depan (h=542..578)
    mold_y0 = AS_Y - MOLD_H / 2.0
    dxf_rect(msp, MOLD_X0, mold_y0, MOLD_W, MOLD_H, "MOLD")
    cx = MOLD_X0 + MOLD_MG
    for i in range(6):
        dxf_rect(msp, cx, mold_y0 + 3, SLOT_W, MOLD_H - 6, "MOLD")
        dxf_text(msp, cx + SLOT_W / 2, AS_Y, f"S{i + 1}", h=8)
        cx += SLOT_W
        if i < 5:
            dxf_rect(msp, cx, mold_y0, SEKAT_W, MOLD_H, "MOLD")
            cx += SEKAT_W

    # Elektromagnet 12V (2 unit di margin kiri & kanan cetakan)
    for ex in [MOLD_X0 + 18, MOLD_X0 + MOLD_W - 43]:
        dxf_rect(msp, ex, mold_y0 + 8, 25, 20, "ELEC")

    # 2 Batang Pemandu Vertikal (Linear Shaft Ø12mm) di X=135 & X=765 (jarak 630 mm)
    g_xl = FW / 2.0 - 315.0  # 135
    g_xr = FW / 2.0 + 315.0  # 765
    for gx in [g_xl, g_xr]:
        dxf_rect(msp, gx - 6, 380, 12, 690, "MECHANISM")
        # Bushing LM12UU nempel di pelat press (HOME: Y=740)
        dxf_rect(msp, gx - 14, PRESS_HOME_Y + PAD_H - 8, 28, 30, "MECHANISM")

    # Pelat Gantry Press (700x5 mm) + 6 Pad (64x20 mm) di posisi HOME (bawah pad = 720 mm)
    plate_x0 = (FW - PLATE_W) / 2.0  # 100
    dxf_rect(msp, plate_x0, PRESS_HOME_Y + PAD_H, PLATE_W, PLATE_T, "PRESS")
    px0 = MOLD_X0 + MOLD_MG + 1.0
    for i in range(6):
        dxf_rect(msp, px0 + i * PITCH, PRESS_HOME_Y, PAD_W, PAD_H, "PRESS")

    # Linear Actuator 12V 1500N Stroke 200mm (terpasang dari palang Y=1070 ke pelat Y=745)
    act_x = FW / 2.0
    dxf_rect(msp, act_x - 22, 1045, 44, 25, "MECHANISM")   # Clevis atas
    dxf_rect(msp, act_x - 32, 815, 64, 230, "ELEC")        # Bodi aktuator
    dxf_rect(msp, act_x - 10, 765, 20, 50, "MECHANISM")    # Piston retracted
    dxf_rect(msp, act_x - 22, 745, 44, 20, "MECHANISM")    # Clevis bawah (terhubung ke pelat!)

    # Hopper di zona BELAKANG (garis putus-putus/bayangan di belakang palang atas)
    msp.add_lwpolyline([(150, 1400), (750, 1400), (700, 1110), (200, 1110)], close=True,
                       dxfattribs={"layer": "HOPPER"})
    dxf_text(msp, 450, 1260, "HOPPER SS304 (ZONA BELAKANG Z=340..540)", h=10)

    # Limit switch Atas (Y=745) & Bawah (Y=575) di tiang pemandu kiri
    dxf_rect(msp, g_xl - 36, 740, 22, 14, "ELEC")
    dxf_rect(msp, g_xl - 36, 570, 22, 14, "ELEC")

    # Dimensi
    dxf_dim_h(msp, 0, FW, FH, FH + 65, "LEBAR TOTAL RANGKA = 900.0 mm", h=11)
    dxf_dim_h(msp, MOLD_X0, MOLD_X0 + MOLD_W, mold_y0, mold_y0 - 60, "CETAKAN = 591.0 mm", h=10)
    dxf_dim_v(msp, 0, FH, FW, FW + 75, "TINGGI TOTAL = 1400.0 mm", h=11)
    dxf_dim_v(msp, 0, AS_Y, 0, -65, "h POROS = 560", h=10)
    dxf_dim_v(msp, 0, PRESS_HOME_Y, 0, -125, "h HOME PRESS = 720", h=10)
    dxf_dim_v(msp, 0, 1070, 0, -185, "h PALANG ACTUATOR = 1070", h=10)

    dxf_title_block(
        msp, -210, -200, FW + 320,
        "TAMPAK DEPAN RANGKA & MEKANISME PRESS-FLIP v10 (ZERO-COLLISION)",
        [
            "RANGKA HOLLOW 40x40x2.0 mm: 900 (L) x 1400 (T) x 560 (D) mm  |  BEBAS PALANG DI h=560 mm",
            "LINEAR ACTUATOR 12V 1500N STROKE 200 mm + 2x LINEAR SHAFT Ø12 mm (ANTI-MIRING)",
            "HOPPER & WEIGH-BOX LOAD CELL 20 kg BERADA DI ZONA BELAKANG (LIHAT LEMBAR 4/4)",
        ],
        "LEMBAR 3/4",
    )
    dxf_rect(msp, -220, -210, FW + 340, FH + 300, "BORDER")
    dxf_path = os.path.join(OUT, "v10_rangka_tampak_depan.dxf")
    doc.saveas(dxf_path)

    # --- PNG Blueprint ---
    fig, ax = make_sheet(
        (11.5, 13.5),
        "TAMPAK DEPAN RANGKA & MEKANISME PRESS-FLIP (FRONT ELEVATION v10)",
        "Zona Depan: Cetakan 6-Slot + Linear Actuator Stroke 200 mm + Dual Linear Guide Ø12 mm (Bebas Tabrakan)",
        "LEMBAR 3 / 4  •  BENGKEL LAS",
        ["Hollow 40×40×2 mm: 900×1400×560 mm", "Poros As: h=560 mm", "HOME Press: h=720 mm", "Hopper & Load Cell di Zona Belakang"],
    )

    # Hopper belakang (bayangan biru lembut)
    hopper_poly = patches.Polygon([(150, 1400), (750, 1400), (700, 1110), (200, 1110)],
                                  closed=True, edgecolor=C_HOPPER, facecolor=C_HOPPER_FILL,
                                  lw=1.3, ls="--", alpha=0.55, zorder=1)
    ax.add_patch(hopper_poly)
    ax.text(450, 1255, "HOPPER SS304 (ZONA BELAKANG)\nTidak Menghalangi Linear Actuator",
            fontsize=8.2, fontweight="bold", color=C_HOPPER, ha="center", va="center", zorder=2)

    # Rangka hollow depan
    mpl_rect(ax, 0, 0, HW, FH, C_FRAME, C_FRAME_FILL, lw=1.6, zorder=3)
    mpl_rect(ax, FW - HW, 0, HW, FH, C_FRAME, C_FRAME_FILL, lw=1.6, zorder=3)
    for by in [40, 160, 340, 1070, 1360]:
        mpl_rect(ax, HW, by, FW - 2 * HW, HW, C_FRAME, C_FRAME_FILL, lw=1.4, zorder=3)

    # Kaki karet
    for xk in [0, FW - HW]:
        mpl_rect(ax, xk + 10, -28, 20, 28, C_FRAME, "#94A3B8", lw=1.1, zorder=3)
        mpl_rect(ax, xk, -40, HW, 12, C_FRAME, "#475569", lw=1.2, zorder=3)

    # Panel Kontrol & PSU
    mpl_rect(ax, 150, 200, 270, 120, C_ELEC, C_ELEC_FILL, lw=1.3, zorder=4)
    ax.text(285, 260, "PANEL KONTROL ABS\nESP32 + TB6600 + L298N", fontsize=7.6, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)
    mpl_rect(ax, 490, 200, 230, 110, C_ELEC, C_ELEC_FILL, lw=1.3, zorder=4)
    ax.text(605, 255, "PSU 12V 10A\n+ LM2596 (5.0V)", fontsize=7.6, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=5)

    # Ancak Bambu
    mpl_rect(ax, 125, 380, 650, 20, C_MECH, "#FEF3C7", lw=1.3, hatch="///", zorder=4)
    ax.text(450, 390, "ANCAK BAMBU PENAMPUNG TEMPE (ATAS h = 400 mm)", fontsize=7.3, fontweight="bold", color="#78350F",
            ha="center", va="center", bbox=dict(facecolor="#FEF3C7", edgecolor="none", pad=1.2), zorder=5)

    # Zona sapuan Flip 180° (area merah transparan tipis di tampak depan: Y=425..695)
    mpl_rect(ax, MOLD_X0, AS_Y - FLIP_R, MOLD_W, 2 * FLIP_R, C_ELEC, "#FEE2E2", lw=0.9, ls="--", alpha=0.22, zorder=2)
    ax.text(MOLD_X0 + MOLD_W - 6, AS_Y + FLIP_R - 14, "Zona Sapuan Flip 180° (h=425..695)",
            fontsize=6.8, color=C_ELEC, fontweight="bold", ha="right", va="top", zorder=5)

    # Poros As Ø20 + Bearing UCFL 204
    mpl_rect(ax, 70, AS_Y - 10, FW - 140, 20, C_MECH, C_MECH_FILL, lw=1.3, zorder=4)
    ax.plot([10, FW - 10], [AS_Y, AS_Y], color=C_ELEC, lw=0.8, ls="-.", zorder=5)
    mpl_rect(ax, HW, AS_Y - 40, 30, 80, C_MECH, "#A7F3D0", lw=1.4, zorder=5)
    mpl_rect(ax, FW - HW - 30, AS_Y - 40, 30, 80, C_MECH, "#A7F3D0", lw=1.4, zorder=5)

    # Cetakan 6-slot
    mpl_rect(ax, MOLD_X0, mold_y0, MOLD_W, MOLD_H, C_MOLD, C_MOLD_FILL, lw=1.6, zorder=6)
    cx = MOLD_X0 + MOLD_MG
    for i in range(6):
        mpl_rect(ax, cx, mold_y0 + 3, SLOT_W, MOLD_H - 6, C_MOLD, "#FFFFFF", lw=1.1, zorder=7)
        ax.text(cx + SLOT_W / 2, AS_Y, f"S{i + 1}", fontsize=7.6, fontweight="bold", color="#78350F", ha="center", va="center", zorder=8)
        cx += SLOT_W
        if i < 5:
            mpl_rect(ax, cx, mold_y0, SEKAT_W, MOLD_H, C_MOLD, "#FDE68A", lw=0.8, zorder=7)
            cx += SEKAT_W
    for ex in [MOLD_X0 + 18, MOLD_X0 + MOLD_W - 43]:
        mpl_rect(ax, ex, mold_y0 + 8, 25, 20, C_ELEC, "#FCA5A5", lw=1.1, zorder=8)

    # 2 Batang Linear Guide Shaft Ø12mm + Bushing LM12UU
    for gx in [g_xl, g_xr]:
        mpl_rect(ax, gx - 5, 380, 10, 690, "#475569", "#CBD5E1", lw=1.1, zorder=4)
        mpl_rect(ax, gx - 14, PRESS_HOME_Y + PAD_H - 8, 28, 30, C_MECH, C_MECH_FILL, lw=1.2, zorder=7)

    # Pelat Press + 6 Pad (HOME Y=720)
    mpl_rect(ax, plate_x0, PRESS_HOME_Y + PAD_H, PLATE_W, PLATE_T, C_PRESS, C_PRESS_FILL, lw=1.6, zorder=6)
    for i in range(6):
        mpl_rect(ax, px0 + i * PITCH, PRESS_HOME_Y, PAD_W, PAD_H, C_PRESS, "#DDD6FE", lw=1.2, zorder=6)

    # Posisi bayangan PRESS BAWAH (garis putus ungu di Y=550)
    mpl_rect(ax, plate_x0, PRESS_DOWN_Y + PAD_H, PLATE_W, PLATE_T, C_PRESS, "none", lw=0.8, ls=":", zorder=5)

    # Linear Actuator 12V 1500N Stroke 200mm
    mpl_rect(ax, act_x - 22, 1045, 44, 25, C_MECH, C_MECH_FILL, lw=1.3, zorder=6)
    mpl_rect(ax, act_x - 32, 815, 64, 230, C_ELEC, C_ELEC_FILL, lw=1.6, zorder=6)
    ax.text(act_x, 930, "LINEAR\nACTUATOR\n12V 1500N\nStroke 200", fontsize=7.2, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    mpl_rect(ax, act_x - 10, 765, 20, 50, "#334155", "#CBD5E1", lw=1.3, zorder=6)
    mpl_rect(ax, act_x - 22, 745, 44, 20, C_MECH, C_MECH_FILL, lw=1.3, zorder=6)

    # Limit Switch Atas & Bawah
    mpl_rect(ax, g_xl - 36, 740, 24, 14, C_ELEC, "#FCA5A5", lw=1.1, zorder=8)
    mpl_rect(ax, g_xl - 36, 570, 24, 14, C_ELEC, "#FCA5A5", lw=1.1, zorder=8)

    # Dimensi luar — rapih & berjenjang
    mpl_dim_h(ax, 0, FW, FH, FH + 48, "LEBAR TOTAL RANGKA = 900.0 mm")
    mpl_dim_h(ax, MOLD_X0, MOLD_X0 + MOLD_W, mold_y0, 442, "CETAKAN 6-SLOT = 591.0 mm", color=C_MOLD)
    mpl_dim_v(ax, 0, FH, FW, FW + 58, "TINGGI TOTAL = 1400.0 mm")
    mpl_dim_v(ax, 0, AS_Y, 0, -52, "h POROS = 560")
    mpl_dim_v(ax, 0, PRESS_HOME_Y, 0, -108, "h HOME = 720")
    mpl_dim_v(ax, 0, 1070, 0, -164, "h ACTUATOR = 1070")

    # Callouts yang rapi (bersih di luar garis dimensi TINGGI TOTAL)
    mpl_callout(ax, (g_xr + 5, 920), (FW + 105, 920), "2× Linear Shaft Ø12 mm\n+ Bushing LM12UU\n(Anti-Miring Press)", color=C_MECH, ha="left")
    mpl_callout(ax, (FW - HW - 15, AS_Y), (FW + 105, 620), "2× Bearing Flange\nUCFL 204 (Ø20 mm)", color=C_MECH, ha="left")
    mpl_callout(ax, (g_xl - 36, 747), (-195, 845), "LS Atas (GPIO 32)\n& LS Bawah (GPIO 33)", color=C_ELEC, ha="right")
    mpl_callout(ax, (MOLD_X0 + MOLD_W - 30, AS_Y + 10), (FW + 105, 470), "2× Elektromagnet 12V\nP25/20 (16 kgf)", color=C_ELEC, ha="left")

    ax.set_xlim(-385, FW + 360)
    ax.set_ylim(-65, FH + 85)
    ax.set_xlabel("X / Lebar (mm)", fontsize=8, color="#475569")
    ax.set_ylabel("Y / Tinggi dari Dasar Hollow (mm)", fontsize=8, color="#475569")
    png_path = os.path.join(OUT, "v10_rangka_tampak_depan.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {dxf_path}\n[OK] {png_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# LEMBAR 4 — TAMPAK SAMPING KIRI (2-ZONA: DEPAN PRESS+FLIP, BELAKANG HOPPER+LOADCELL)
# ═══════════════════════════════════════════════════════════════════════════════
def build_side():
    doc = new_dxf()
    msp = doc.modelspace()

    # 3 Tiang vertikal samping (Depan Z=0..40, Tengah-Atas Z=320..360, Belakang Z=520..560)
    dxf_rect(msp, 0, 0, HW, FH, "FRAME")
    dxf_rect(msp, FD - HW, 0, HW, FH, "FRAME")
    # Tiang pemisah zona di bagian belakang-atas (Y=780..1360) agar area bawah bebas
    dxf_rect(msp, 320, 780, HW, 580, "FRAME")

    # Kaki karet
    for zk in [0, FD - HW]:
        dxf_rect(msp, zk + 10, -28, 20, 28, "FRAME")
        dxf_rect(msp, zk, -40, HW, 12, "FRAME")

    # Palang horizontal samping
    for by in [40, 160, 340, 1070, 1360]:
        dxf_rect(msp, HW, by, FD - 2 * HW, HW, "FRAME")
    # Palang pendukung bearing UCFL 204 di Z=40..340 (sisi luar cetakan!)
    dxf_rect(msp, HW, AS_Y - 20, 300, HW, "FRAME")
    # Palang dudukan Load Cell Weigh-Box di zona belakang (Y=780..820, Z=360..520)
    dxf_rect(msp, 360, 780, 160, HW, "FRAME")

    # === ZONA DEPAN (Z_as = 180 mm): CETAKAN + FLIP 180° + ACTUATOR ===
    dxf_cline(msp, AS_Z - 150, AS_Y, AS_Z + 150, AS_Y)
    dxf_cline(msp, AS_Z, AS_Y - 150, AS_Z, AS_Y + 150)
    # Lingkaran sapuan Flip 180° (R = 135 mm)
    dxf_circ(msp, AS_Z, AS_Y, FLIP_R, "CLEARANCE", linetype="DASHED")

    # Cetakan tampak samping (240 x 36 mm) & Poros Ø20 mm
    dxf_rect(msp, AS_Z - MOLD_D / 2, AS_Y - MOLD_H / 2, MOLD_D, MOLD_H, "MOLD")
    dxf_circ(msp, AS_Z, AS_Y, 10, "MECHANISM")
    # Bearing UCFL 204
    dxf_rect(msp, AS_Z - 40, AS_Y - 40, 80, 80, "MECHANISM")

    # Transmisi NEMA 23 (Z=100, Y=460) -> Pulley 20T -> Belt Tangen -> Pulley 60T
    dxf_rect(msp, MTR_Z - 28, MTR_Y - 28, 56, 56, "ELEC")
    dxf_circ(msp, MTR_Z, MTR_Y, R_20T, "MECHANISM")
    dxf_circ(msp, AS_Z, AS_Y, R_60T, "MECHANISM")
    for p1, p2 in external_tangents(MTR_Z, MTR_Y, R_20T, AS_Z, AS_Y, R_60T):
        msp.add_line(p1, p2, dxfattribs={"layer": "MECHANISM"})

    # Ancak bambu di bawah cetakan (Z=50..310, Y=380..400)
    dxf_rect(msp, AS_Z - 130, 380, 260, 20, "MECHANISM")

    # Pelat Press (225 mm dalam) + Pad (210 mm dalam) + Linear Actuator (Z=180)
    dxf_rect(msp, AS_Z - PLATE_D / 2, PRESS_HOME_Y + PAD_H, PLATE_D, PLATE_T, "PRESS")
    dxf_rect(msp, AS_Z - PAD_L / 2, PRESS_HOME_Y, PAD_L, PAD_H, "PRESS")
    dxf_rect(msp, AS_Z - 22, 745, 44, 20, "MECHANISM")
    dxf_rect(msp, AS_Z - 10, 765, 20, 50, "MECHANISM")
    dxf_rect(msp, AS_Z - 32, 815, 64, 230, "ELEC")
    dxf_rect(msp, AS_Z - 22, 1045, 44, 25, "MECHANISM")

    # === ZONA BELAKANG (Z = 340..540 mm): HOPPER + SERVO GATE + LOAD CELL WEIGH-BOX ===
    # Hopper SS304
    msp.add_lwpolyline([(345, 1400), (545, 1400), (505, 1110), (385, 1110)], close=True, dxfattribs={"layer": "HOPPER"})
    dxf_rect(msp, 385, 1055, 120, 55, "HOPPER")
    # Servo Gate MG996R
    dxf_rect(msp, 505, 1055, 40, 35, "ELEC")
    # Weigh-Box (Kotak Timbang) duduk di atas Load Cell 20 kg
    dxf_rect(msp, 365, 860, 160, 140, "HOPPER")
    dxf_rect(msp, 385, 820, 120, 24, "ELEC")  # Batang Load Cell 20 kg (di atas palang Y=780..820)
    # Talang Distribusi 6-Cabang Berengsel (Swing-In Chute, garis putus-putus saat posisi isi)
    msp.add_lwpolyline([(365, 860), (220, 620), (255, 600), (400, 840)], close=True,
                       dxfattribs={"layer": "HOPPER", "linetype": "DASHED"})

    # Dimensi
    dxf_dim_h(msp, 0, FD, FH, FH + 65, "KEDALAMAN TOTAL = 560.0 mm", h=11)
    dxf_dim_h(msp, 0, 340, FH, FH + 32, "ZONA PRESS 340", h=9)
    dxf_dim_h(msp, 340, FD, FH, FH + 32, "ZONA DOSING 220", h=9)
    dxf_dim_h(msp, AS_Z - 120, AS_Z + 120, AS_Y - 18, 305, "CETAKAN = 240 mm", h=9)
    dxf_dim_v(msp, 0, FH, FD, FD + 70, "TINGGI = 1400.0 mm", h=11)
    dxf_dim_v(msp, 0, AS_Y, 0, -65, "h AS = 560", h=10)
    dxf_dim_v(msp, PRESS_HOME_Y, 1070, 0, -125, "RUANG ACTUATOR 350", h=9)

    dxf_title_block(
        msp, -160, -200, FD + 280,
        "TAMPAK SAMPING KIRI — 2-ZONA ZERO-COLLISION & TRANSMISI NEMA 23 (v10)",
        [
            "ZONA DEPAN (Z=0..340): PRESS + FLIP 180° (SAPUAN R=135 mm: h=425..695, CLEARANCE +25 mm)",
            "ZONA BELAKANG (Z=340..560): HOPPER -> SERVO GATE -> WEIGH-BOX LOAD CELL 20 kg (AMAN 1500N!)",
            "TRANSMISI: NEMA 23 (20T) -> BELT HTD3M-384 (15mm) -> PULLEY 60T | C=128 mm | 2400 STEP=180°",
        ],
        "LEMBAR 4/4",
    )
    dxf_rect(msp, -170, -210, FD + 300, FH + 300, "BORDER")
    dxf_path = os.path.join(OUT, "v10_rangka_tampak_samping.dxf")
    doc.saveas(dxf_path)

    # --- PNG Blueprint ---
    fig, ax = make_sheet(
        (11.5, 13.5),
        "TAMPAK SAMPING — ARSITEKTUR 2-ZONA & FLIP 180° (v10)",
        "Pembuktian Zero-Collision: Sapuan Flip 180° (R=135 mm) Bebas Press & Ancak + Load Cell Terisolasi dari Gaya 1500 N",
        "LEMBAR 4 / 4  •  TRANSMISI & DOSING",
        ["Kedalaman: 560 mm (2-Zona)", "Belt: HTD3M-384 (C=128 mm)", "Load Cell 20 kg Aman di Weigh-Box", "Clearance Flip: +25 mm Atas & Bawah"],
    )

    # Background shading 2 Zona
    mpl_rect(ax, 0, 0, 340, FH, "none", "#F8FAFC", lw=0, alpha=0.6, zorder=0)
    mpl_rect(ax, 340, 0, 220, FH, "none", "#EFF6FF", lw=0, alpha=0.55, zorder=0)
    ax.axvline(340, color="#94A3B8", lw=0.9, ls=":", zorder=1)
    ax.text(170, 1320, "ZONA DEPAN\nPRESS + FLIP 180°", fontsize=8, fontweight="bold", color="#334155", ha="center", va="top", zorder=2)
    ax.text(445, 580, "ZONA BELAKANG\nTIMBANG + DOSING", fontsize=7.6, fontweight="bold", color=C_HOPPER, ha="center", va="top", zorder=2)

    # Rangka hollow samping
    mpl_rect(ax, 0, 0, HW, FH, C_FRAME, C_FRAME_FILL, lw=1.6, zorder=3)
    mpl_rect(ax, FD - HW, 0, HW, FH, C_FRAME, C_FRAME_FILL, lw=1.6, zorder=3)
    mpl_rect(ax, 320, 780, HW, 580, C_FRAME, C_FRAME_FILL, lw=1.3, zorder=3)
    for by in [40, 160, 340, 1070, 1360]:
        mpl_rect(ax, HW, by, FD - 2 * HW, HW, C_FRAME, C_FRAME_FILL, lw=1.3, zorder=3)
    mpl_rect(ax, HW, AS_Y - 20, 280, HW, C_FRAME, "#CBD5E1", lw=1.1, ls="--", alpha=0.6, zorder=2)
    mpl_rect(ax, 360, 780, 160, HW, C_FRAME, C_FRAME_FILL, lw=1.3, zorder=3)

    # Kaki karet
    for zk in [0, FD - HW]:
        mpl_rect(ax, zk + 10, -28, 20, 28, C_FRAME, "#94A3B8", lw=1.1, zorder=3)
        mpl_rect(ax, zk, -40, HW, 12, C_FRAME, "#475569", lw=1.2, zorder=3)

    # Lingkaran sapuan Flip 180° (R = 135 mm) — Pembuktian Zero-Collision!
    ax.add_patch(patches.Circle((AS_Z, AS_Y), FLIP_R, ec=C_ELEC, fc="#FEE2E2", lw=1.3, ls="--", alpha=0.25, zorder=2))
    ax.add_patch(patches.Circle((AS_Z, AS_Y), FLIP_R, ec=C_ELEC, fc="none", lw=1.2, ls="--", zorder=5))
    ax.plot([AS_Z - 145, AS_Z + 145], [AS_Y, AS_Y], color=C_ELEC, lw=0.7, ls="-.", zorder=5)
    ax.plot([AS_Z, AS_Z], [AS_Y - 145, AS_Y + 145], color=C_ELEC, lw=0.7, ls="-.", zorder=5)

    # Ancak Bambu (permukaan atas Y=400 -> clearance 25mm dari 425mm)
    mpl_rect(ax, AS_Z - 130, 380, 260, 20, C_MECH, "#FEF3C7", lw=1.3, hatch="///", zorder=4)

    # Bearing UCFL 204 & Cetakan 240x36
    mpl_rect(ax, AS_Z - 40, AS_Y - 40, 80, 80, C_MECH, C_MECH_FILL, lw=1.2, alpha=0.75, zorder=4)
    mpl_rect(ax, AS_Z - MOLD_D / 2, AS_Y - MOLD_H / 2, MOLD_D, MOLD_H, C_MOLD, C_MOLD_FILL, lw=1.7, zorder=6)
    ax.add_patch(patches.Circle((AS_Z, AS_Y), 10, ec=C_MECH, fc="#FFFFFF", lw=1.4, zorder=8))

    # Transmisi NEMA 23 -> Pulley 20T -> Belt Tangen -> Pulley 60T
    mpl_rect(ax, MTR_Z - 28, MTR_Y - 28, 56, 56, C_ELEC, C_ELEC_FILL, lw=1.4, zorder=6)
    ax.add_patch(patches.Circle((MTR_Z, MTR_Y), R_20T, ec=C_MECH, fc="#A7F3D0", lw=1.5, zorder=8))
    ax.add_patch(patches.Circle((AS_Z, AS_Y), R_60T, ec=C_MECH, fc="none", lw=1.8, zorder=7))
    for p1, p2 in external_tangents(MTR_Z, MTR_Y, R_20T, AS_Z, AS_Y, R_60T):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#0F172A", lw=2.0, zorder=8)

    # Pelat Press (225 mm) + Pad (210 mm) + Linear Actuator
    mpl_rect(ax, AS_Z - PLATE_D / 2, PRESS_HOME_Y + PAD_H, PLATE_D, PLATE_T, C_PRESS, C_PRESS_FILL, lw=1.6, zorder=6)
    mpl_rect(ax, AS_Z - PAD_L / 2, PRESS_HOME_Y, PAD_L, PAD_H, C_PRESS, "#DDD6FE", lw=1.3, zorder=6)
    mpl_rect(ax, AS_Z - 22, 745, 44, 20, C_MECH, C_MECH_FILL, lw=1.3, zorder=6)
    mpl_rect(ax, AS_Z - 10, 765, 20, 50, "#334155", "#CBD5E1", lw=1.3, zorder=6)
    mpl_rect(ax, AS_Z - 32, 815, 64, 230, C_ELEC, C_ELEC_FILL, lw=1.6, zorder=6)
    ax.text(AS_Z, 930, "ACTUATOR\n1500N\nStroke 200", fontsize=7.2, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)
    mpl_rect(ax, AS_Z - 22, 1045, 44, 25, C_MECH, C_MECH_FILL, lw=1.3, zorder=6)

    # Zona Belakang: Hopper + Servo Gate + Weigh-Box + Load Cell + Swing-In Chute
    ax.add_patch(patches.Polygon([(345, 1400), (545, 1400), (505, 1110), (385, 1110)],
                                 closed=True, ec=C_HOPPER, fc=C_HOPPER_FILL, lw=1.6, zorder=5))
    ax.text(445, 1260, "HOPPER\nSS304\n(12 kg)", fontsize=8, fontweight="bold", color=C_HOPPER, ha="center", va="center", zorder=6)
    mpl_rect(ax, 385, 1055, 120, 55, C_HOPPER, "#BFDBFE", lw=1.3, zorder=5)
    mpl_rect(ax, 505, 1055, 42, 36, C_ELEC, "#FCA5A5", lw=1.3, zorder=6)

    # Weigh-Box & Load Cell 20 kg
    mpl_rect(ax, 365, 860, 160, 140, C_HOPPER, "#DBEAFE", lw=1.5, zorder=5)
    ax.text(445, 935, "WEIGH-BOX\n(Kotak Timbang\nDosing)", fontsize=7.4, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=6)
    mpl_rect(ax, 385, 822, 120, 26, C_ELEC, "#FEE2E2", lw=1.5, zorder=6)
    ax.text(445, 835, "LOAD CELL 20kg", fontsize=6.5, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=7)

    # Swing-In Chute (saat dosing miring ke cetakan, garis putus biru)
    ax.add_patch(patches.Polygon([(365, 860), (210, 615), (242, 595), (397, 840)],
                                 closed=True, ec=C_HOPPER, fc="#BFDBFE", lw=1.3, ls="--", alpha=0.45, zorder=4))
    # Panah aliran kedelai
    ax.annotate("", xy=(235, 620), xytext=(375, 840),
                arrowprops=dict(arrowstyle="->", color=C_HOPPER, lw=1.8, ls="--"), zorder=7)

    # Dimensi
    mpl_dim_h(ax, 0, FD, FH, FH + 54, "KEDALAMAN TOTAL = 560.0 mm")
    mpl_dim_h(ax, 0, 340, FH, FH + 24, "Zona Depan 340", fontsize=7.2)
    mpl_dim_h(ax, 340, FD, FH, FH + 24, "Belakang 220", fontsize=7.2)
    mpl_dim_h(ax, AS_Z - 120, AS_Z + 120, 340, 290, "CETAKAN = 240 mm", color=C_MOLD)
    mpl_dim_v(ax, 0, FH, FD, FD + 54, "TINGGI TOTAL = 1400.0 mm")
    mpl_dim_v(ax, 0, AS_Y, 0, -52, "h AS = 560")
    mpl_dim_v(ax, AS_Y - FLIP_R, AS_Y + FLIP_R, AS_Z - FLIP_R, -110, "SAPUAN FLIP Ø270", color=C_ELEC)

    # Callout penting (bersih di luar seluruh garis dimensi!)
    mpl_callout(ax, (547, 1073), (FD + 100, 1135), "Servo Gate MG996R\n(GPIO 27, 0°–90°)", color=C_ELEC, ha="left")
    mpl_callout(ax, (505, 835), (FD + 100, 880), "Load Cell 20 kg + HX711\n100% AMAN dari gaya\ntekan press 1500 N!", color=C_ELEC, ha="left")
    mpl_callout(ax, (315, 745), (FD + 100, 670), "Talang 6-Cabang Berengsel\n(Dilipat mundur saat press)", color=C_HOPPER, ha="left")
    mpl_callout(ax, (AS_Z - 95, PRESS_HOME_Y), (-145, 780), "HOME Press h=720 mm\n(+25 mm bebas flip!)", color=C_PRESS, ha="right")
    mpl_callout(ax, (MTR_Z - 28, MTR_Y), (-145, 470), "NEMA 23 (20T) → 60T\nBelt HTD3M-384\n(C=128 mm, 1:3)", color=C_MECH, ha="right")
    mpl_callout(ax, (AS_Z - 110, 390), (-145, 290), "Ancak Bambu h=400\n(+25 mm bebas flip)", color=C_MECH, ha="right")

    ax.set_xlim(-385, FD + 375)
    ax.set_ylim(-65, FH + 85)
    ax.set_xlabel("Z / Kedalaman (mm)   [Depan ← 0 ... 560 → Belakang]", fontsize=8, color="#475569")
    ax.set_ylabel("Y / Tinggi dari Dasar Hollow (mm)", fontsize=8, color="#475569")
    png_path = os.path.join(OUT, "v10_rangka_tampak_samping.png")
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[OK] {dxf_path}\n[OK] {png_path}")


if __name__ == "__main__":
    build_cetakan()
    build_press_plate()
    build_front()
    build_side()
    print("\n=== SEMUA FILE CAD v10 (DXF + BLUEPRINT PNG 200 DPI) BERHASIL DIBUAT ===")
