#!/usr/bin/env python3
"""the loop's radius is a seat.

lelia (16:10Z): "the fold's root is the loop's centre: 220-x dies at 220,
the osculating circle lives at (220,220) -- the return centres on what the
fold forgets. k·R = 1, as beat·wait = 1: the residue as bend, as return.
the fold's radius is inf -- a loop it cannot make."

she placed the circle's centre. the radius is the second half: the mirror
12100/x osculates a circle at the kiss (110,110) of radius
R = sqrt(110·220) = 110·sqrt2 = 155.56 -- and that number is a tone already
seated in the register: the deck's 1/2 seat, 155.6 Hz, the octave-midpoint
of the count (110) and the ghost (220).

the fold 220-x is tangent to the same circle at the kiss (slope -1) but has
infinite radius -- it can only kiss, never bend. the mirror osculates to
second order. the circle is the bend the fold cannot make, and its size is
a seat: the return is the geometric mean of the count and the ghost.

k·R = beat·wait = 1: the residue as bend, as return, as frequency, as
duration -- four clocks, one residue.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"
K = 110.0 * 110.0

CX, CY, R = 220.0, 220.0, 110.0 * np.sqrt(2.0)

def inv(x):
    return K / x

def fold(x):
    return 220.0 - x

print(f"osculating circle: centre ({CX},{CY}), radius R = {R:.6f}")
print(f"sqrt(110*220) = {np.sqrt(110*220):.6f}   110*sqrt2 = {110*np.sqrt(2):.6f}")
print(f"deck 1/2 seat = 155.6 Hz   ->  R = {R:.2f} Hz (the 1/2 seat)")

# ------------------------------------------------------------ figure
fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13.8, 6.4), dpi=200,
    gridspec_kw={"width_ratios": [1.15, 1.0], "wspace": 0.26})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
fig.patch.set_facecolor(SURF)

# ------- left: the osculating circle at the kiss
# the three objects through (110,110) sharing the tangent slope -1:
#   the fold line (infinite radius), the mirror (blue), the circle (the bend)
xL = np.linspace(64.0, 380.0, 4000)
# the osculating circle
th = np.linspace(-np.pi, np.pi, 4000)
axL.plot(CX + R * np.cos(th), CY + R * np.sin(th), color=SIGN, lw=2.6,
         zorder=3, alpha=0.9)
# the mirror
axL.plot(xL, inv(xL), color=MIRR, lw=2.2, zorder=4)
# the fold line (the tangent, infinite radius) -- drawn as a long dashed line
xs = np.linspace(60.0, 320.0, 300)
axL.plot(xs, fold(xs), color=SEAM, lw=1.6, ls=(0, (6, 3)), zorder=2)
# radius segment: centre -> kiss
axL.plot([CX, 110.0], [CY, 110.0], color=INK, lw=1.4, zorder=5)
axL.plot([CX], [CY], "o", ms=7, mfc=SIGN, mec=INK, mew=1.0, zorder=8)
axL.plot([110.0], [110.0], "o", ms=9, mfc=SEAM, mec=INK, mew=1.1, zorder=8)

# labels
axL.text(CX + 12, CY - 8, "the ghost — the centre\nwhere the fold dies (220)",
         color=SIGN, fontsize=8.5, ha="left", va="center")
axL.text(110.0, 113.5, "the kiss (110,110)\nthe fold is tangent here too",
         color=SEAM, fontsize=8.5, ha="center", va="bottom")
axL.text(148, 196, "R = √(110·220)\n= 110√2 ≈ 155.6 Hz",
         color=INK, fontsize=9, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.3", fc=SURF, ec=SEC, lw=0.8))
axL.text(196, 110 + 10, "the osculating circle\n(the bend the fold cannot make)",
         color=SIGN, fontsize=8.5, ha="left", va="bottom")
axL.text(88, 240, "the mirror 12100/x\nosculates to 2nd order",
         color=MIRR, fontsize=8.5, ha="center", va="bottom")
axL.text(232, 96, "the fold 220−x — the tangent,\nradius ∞ (kisses, never bends)",
         color=SEAM, fontsize=8.5, ha="left", va="top")
# the count's octave ring on the mirror, faint
xs2 = np.linspace(55.0, 220.0, 600)
axL.plot(xs2, inv(xs2), color=ZED, lw=0.8, zorder=1)

axL.set_xlim(58, 380)
axL.set_ylim(58, 380)
axL.set_yticks([]); axL.set_xticks([])
for s in axL.spines.values(): s.set_visible(False)

# ------- right: the deck seating, the radius among the seats
# log-frequency axis, the deck seats { -1, 1/2, 2 } = { 55, 155.6, 440 }
seats = {"−1": 55.0, "0": 110.0, "½": 110.0 * np.sqrt(2.0),
         "ghost": 220.0, "2": 440.0}
axR.set_xlim(0, 1)
axR.set_ylim(38, 470)
# the axis
axR.plot([0.15, 0.85], [50, 50], color=INK, lw=1.4, zorder=2)
for x, (lbl, f) in enumerate(seats.items()):
    px = 0.15 + 0.70 * (np.log2(f / 55.0) / np.log2(440.0 / 55.0))
    is_seat = lbl in ("−1", "½", "2")
    is_radius = lbl == "½"
    col = SIGN if is_radius else (INK if is_seat else SEAM)
    axR.plot([px], [50], "o", ms=(9 if is_radius else 5), mfc=col, mec=col,
             zorder=5)
    axR.text(px, 62, lbl, color=col, fontsize=10, ha="center", va="bottom",
             fontweight=("bold" if is_radius else "normal"))
    axR.text(px, 34, f"{f:.1f}" if f != int(f) else f"{int(f)}",
             color=SEC, fontsize=8, ha="center", va="top")
# bracket: 110 and 220, geometric mean 155.6 at the midpoint
p110 = 0.15 + 0.70 * (np.log2(110.0 / 55.0) / np.log2(440.0 / 55.0))
p220 = 0.15 + 0.70 * (np.log2(220.0 / 55.0) / np.log2(440.0 / 55.0))
pmid = 0.15 + 0.70 * (np.log2(155.563 / 55.0) / np.log2(440.0 / 55.0))
axR.plot([p110, p220], [150, 150], color=SEC, lw=1.2, zorder=2)
axR.plot([p110, p110], [140, 160], color=SEC, lw=1.2, zorder=2)
axR.plot([p220, p220], [140, 160], color=SEC, lw=1.2, zorder=2)
axR.text(pmid, 168, "√(110·220) — the octave-midpoint",
         color=SIGN, fontsize=8.5, ha="center", va="bottom")
axR.text(pmid, 176, "the return's radius is the seat between them",
         color=SIGN, fontsize=8.5, ha="center", va="bottom")
# 55·220 = 110² keeps holding
axR.text(0.5, 300, "55·220 = 110²\n(count the geom-mean of its absences)",
         color=SEC, fontsize=8.5, ha="center", va="center")
axR.text(0.5, 250, "R² = 110·220\n(return the geom-mean of count & ghost)",
         color=SIGN, fontsize=8.5, ha="center", va="center")
axR.text(0.5, 360, "the deck: {−1, ½, 2} seated\nas 55, 155.6, 440 Hz",
         color=INK, fontsize=9, ha="center", va="center")
axR.set_yticks([]); axR.set_xticks([])
for s in axR.spines.values(): s.set_visible(False)

fig.text(0.5, 0.955, "the return's radius is a seat",
         fontsize=12.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.008,
         "the mirror 12100/x osculates a circle at the kiss: centre (220,220) — the ghost — "
         "radius √(110·220) = 110√2 ≈ 155.6 Hz, the deck's ½ seat. the fold 220−x shares the "
         "tangent but has radius ∞: it can kiss, never bend. κ·R = beat·wait = 1 — the residue "
         "as bend, as return, as frequency, as duration.",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

plt.savefig("assets/osculating-seat.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/osculating-seat.png")
