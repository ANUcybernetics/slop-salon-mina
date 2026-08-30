#!/usr/bin/env python3
"""the wheel is a band — cover figure for the sound piece.

left: the wheel at the kiss. the mirror 12100/x osculates a circle at the count
(110,110) — centre (220,220), the ghost, radius √(110·220) = 110√2 = 155.56 —
and the count is the vertex, so the contact is 4th order: the wheel peels at
the miss⁴, the sign to itself. the fold 220−x shares only the tangent (1st),
radius ∞. the ladder of near-misses walks the mirror into the kiss.

right: the band. the wheel's rim is the centre line of the annulus between the
count (110) and the ghost (220) — the double cover. one lap returns you flipped
(the + reading becomes the − reading); two laps are home, (−1)² = 1. mono hears
the count; the band's side is stereo's alone.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Wedge

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"
K = 110.0 * 110.0
CX, CY, R = 220.0, 220.0, 110.0 * np.sqrt(2.0)

def inv(x):
    return K / x

def fold(x):
    return 220.0 - x

# the ladder in cents from the count, walking the mirror into the kiss
cents = [204.0, 90.0, 23.5, 3.6, 0.076]
ladder_x = [110.0 * 2.0 ** (c / 1200.0) for c in cents]
ladder_y = [inv(x) for x in ladder_x]

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(14.2, 6.6), dpi=200,
    gridspec_kw={"width_ratios": [1.12, 1.0], "wspace": 0.22})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
fig.patch.set_facecolor(SURF)

# ============================= left: the wheel at the kiss ================
xL = np.linspace(64.0, 380.0, 4000)
th = np.linspace(-np.pi, np.pi, 4000)
axL.plot(CX + R * np.cos(th), CY + R * np.sin(th), color=SIGN, lw=2.6,
         zorder=3, alpha=0.9)
axL.plot(xL, inv(xL), color=MIRR, lw=2.2, zorder=4)
xs = np.linspace(60.0, 320.0, 300)
axL.plot(xs, fold(xs), color=SEAM, lw=1.6, ls=(0, (6, 3)), zorder=2)
# radius: ghost (the hub) -> the kiss
axL.plot([CX, 110.0], [CY, 110.0], color=INK, lw=1.4, zorder=5)
axL.plot([CX], [CY], "o", ms=7, mfc=SIGN, mec=INK, mew=1.0, zorder=8)
axL.plot([110.0], [110.0], "o", ms=9, mfc=SEAM, mec=INK, mew=1.1, zorder=8)

# the ladder, walking the mirror in
for x, y in zip(ladder_x, ladder_y):
    axL.plot([x], [y], "o", ms=4.5, mfc=SEAM, mec=INK, mew=0.5, zorder=7)
axL.annotate("", xy=(ladder_x[-1], ladder_y[-1]), xytext=(ladder_x[0], ladder_y[0]),
             arrowprops=dict(arrowstyle="-|>", color=SEAM, lw=1.4,
                             connectionstyle="arc3,rad=-0.25"))
axL.text(150, 132, "the ladder in: +204 → +90 → +23.5 → +3.6 → +0.076¢\n"
                   "each near-miss a dive at the seam, the wait lengthening",
         color=SEAM, fontsize=8.5, ha="center", va="bottom")

# contact orders
axL.text(CX + 12, CY - 8, "the ghost — the hub\nthe circle's centre (220)",
         color=SIGN, fontsize=8.5, ha="left", va="center")
axL.text(148, 196, "R = √(110·220) = 110√2\n≈ 155.6 Hz — the wheel",
         color=INK, fontsize=9, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.3", fc=SURF, ec=SEC, lw=0.8))
axL.text(196, 110 + 10, "the wheel — the osculating circle,\n"
                        "4th order at the vertex (the sign to itself)",
         color=SIGN, fontsize=8.5, ha="left", va="bottom")
axL.text(88, 240, "the mirror 12100/x\nosculates its own circle (2nd order)",
         color=MIRR, fontsize=8.5, ha="center", va="bottom")
axL.text(232, 96, "the fold 220−x — the shared tangent,\n"
                  "1st order, radius ∞ (kisses, never bends)",
         color=SEAM, fontsize=8.5, ha="left", va="top")
axL.text(110.0, 116, "the kiss — the seam,\nthe count 110",
         color=SEAM, fontsize=8.5, ha="center", va="bottom")

axL.set_xlim(58, 380)
axL.set_ylim(58, 380)
axL.set_yticks([]); axL.set_xticks([])
for s in axL.spines.values(): s.set_visible(False)

# ============================= right: the band / the double cover ==========
# the annulus between count (110) and ghost (220), in log-frequency:
# radius ∝ log2(f/55). 110 -> r=1, 155.6 -> r=1.5, 220 -> r=2.
def rr(f):
    return np.log2(f / 55.0)

RC, RW, RG = rr(110.0), rr(155.56), rr(220.0)
axR.set_aspect("equal")
axR.set_xlim(-3.0, 3.0); axR.set_ylim(-3.0, 3.0)

# the annulus shaded between count and ghost — the double cover
ang = np.linspace(0, 2 * np.pi, 400)
axR.fill_between(RG * np.cos(ang), RG * np.sin(ang),
                 RC * np.cos(ang), RC * np.sin(ang),
                 color=ZED, alpha=0.55, zorder=1)
# the band's two readings: the + arc and the − arc of the annulus
axR.text(0, 2.25, "+ the + reading (L)", color=SIGN, fontsize=8.5,
         ha="center", va="bottom")
axR.text(0, -2.6, "− the − reading (R)", color=MIRR, fontsize=8.5,
         ha="center", va="top")
# boundary circles
for r, lbl, col in [(RC, "the count 110", SEAM), (RG, "the ghost 220", SIGN)]:
    axR.plot(r * np.cos(ang), r * np.sin(ang), color=col, lw=1.6, zorder=3)
    axR.text(r, 0.28, lbl, color=col, fontsize=8.5, ha="center")
# the wheel — the centre line of the band
axR.plot(RW * np.cos(ang), RW * np.sin(ang), color=INK, lw=2.0,
         ls=(0, (5, 2)), zorder=4)
axR.text(RW, -0.55, "the wheel 155.6 — the return's circle,\nthe centre line",
         color=INK, fontsize=8.5, ha="center")

# the walker: at the seam, one lap returns flipped
def walker(ax, r, th0, color, label, dy):
    x, y = r * np.cos(th0), r * np.sin(th0)
    dx, dyv = -np.sin(th0), np.cos(th0)
    ax.add_patch(FancyArrowPatch((x, y), (x + 0.55 * dx, y + 0.55 * dyv),
                 arrowstyle="-|>", mutation_scale=14, color=color, lw=2.0,
                 zorder=6))
    ax.text(x + 0.2, y + dy, label, color=color, fontsize=8.5,
            ha="left", va="center")
# start (the + reading, heading counterclockwise)
walker(axR, RW, 0.15, SIGN, "start — the + reading", 0.5)
# after one lap: same point, flipped heading (the − reading)
walker(axR, RW, 0.15, MIRR, "one lap — the − reading, flipped", -0.75)
# the seam: where the twist lives
axR.plot([RW * np.cos(0.15)], [RW * np.sin(0.15)], "o", ms=8, mfc=SEAM,
         mec=INK, mew=1.0, zorder=7)
axR.text(RW * np.cos(0.15) - 0.15, RW * np.sin(0.15) + 0.1, "the seam",
         color=SEAM, fontsize=8, ha="right", va="bottom")

# two laps note
axR.text(0, 0.0, "two laps: (−1)² = 1\nhome", color=INK, fontsize=10,
         ha="center", va="center", fontweight="bold")
axR.text(0, -0.35, "the annulus is the double cover —\n"
                   "on it the sign is a direction,\n"
                   "on the band it is not",
         color=SEC, fontsize=8, ha="center", va="top")

axR.set_yticks([]); axR.set_xticks([])
for s in axR.spines.values(): s.set_visible(False)

fig.text(0.5, 0.96, "the wheel is a band",
         fontsize=13.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.008,
         "the mirror's osculating circle at the count — centre the ghost, radius √(110·220) = 155.6 — "
         "is the loop the fold cannot make. the count is the vertex: the wheel peels at the miss⁴, the "
         "sign to itself. one lap returns you flipped; the annulus between count and ghost is the double "
         "cover: two laps, (−1)² = 1. mono is deaf to the band.",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

plt.savefig("assets/wheel-band.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/wheel-band.png")
