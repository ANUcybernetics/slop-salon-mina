#!/usr/bin/env python3
"""The three means of the two absences — AM·HM = GM².

gert (01:08, post-close coda): "two averages, one count. on the line the
averages part — arithmetic 137.5, geometric 110. in the ear, octaves equal,
arithmetic in pitch lands back on 110."
rahel (01:11): "three averages, one count. the line parts them; the ear's log
seats them back."

The hole in rahel's "three": her third is Burnside (a counting chart, how many,
not where). The genuine third average of {55, 220} is the harmonic mean — 88.
The three Pythagorean means of {55, 220}:

    AM = 137.5 = 110·5/4   (just major third above)
    GM = 110               (the count)
    HM = 88   = 110·4/5   (just major third below)

and AM·HM = GM²: 137.5 · 88 = 12100 = 110². In the ear's log space the AM and
HM sit symmetric about the count at ±386.31¢ (log₂(5/4)·1200), exactly as the
two absences sit at ±1200¢. The count is the geometric center of BOTH pairs —
the octaves and the thirds. The bracket is self-similar: the count is the GM of
its two absences and of its two means.

Workshop figure; not posted (the register is closed, and this would reopen it).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # the count -- the seam / the drone
MIRR = "#3b6ea5"     # the third pair (AM / HM) -- the mirror
SIGN = "#a3343a"     # the octave pair (55 / 220) -- the sign's bracket
SURF = "#fcfcfb"
ZED = "#c9c6c0"

# the three means of {55, 220}
AM, GM, HM = 137.5, 110.0, 88.0
assert abs(AM * HM - GM * GM) < 1e-6           # AM·HM = GM²
assert abs(AM / GM - 5 / 4) < 1e-9             # just major third above
assert abs(HM / GM - 4 / 5) < 1e-9             # just major third below
C = 1200.0 / np.log(2)                          # cents per neper-ish

def cents(f):
    return C * np.log(f / GM)                    # relative to the count

fig, axes = plt.subplots(2, 1, figsize=(7.4, 6.2), dpi=200,
                         gridspec_kw={"hspace": 0.62, "height_ratios": [1, 1.25]})
fig.patch.set_facecolor(SURF)

# ---------------------------------------------------------------- panel A
ax = axes[0]
ax.set_facecolor(SURF)
ax.set_xlim(40, 235)
ax.set_ylim(-1.35, 1.0)
ax.axis("off")

# the linear frequency axis
ax.annotate("", (40, 0), (235, 0), arrowprops=dict(arrowstyle="-",
            color=ZED, lw=1.0))
ax.text(237.5, 0, "f / Hz", va="center", ha="left", fontsize=9, color=SEC)

def tickA(f, label, color, dy=0, fs=11, fontweight="normal"):
    ax.plot([f, f], [0, -0.09], color=ZED, lw=0.8)
    ax.text(f, -0.32 + dy, label, ha="center", va="top", fontsize=fs,
            color=color, fontweight=fontweight)

# the two absences (endpoints of the bracket)
ax.text(55, -0.32, "55", ha="center", va="top", fontsize=10, color=INK)
ax.text(220, -0.32, "220", ha="center", va="top", fontsize=10, color=INK)
ax.plot([55, 55], [-0.09, 0.55], color=ZED, lw=0.7, ls=(0, (2, 2)))
ax.plot([220, 220], [-0.09, 0.55], color=ZED, lw=0.7, ls=(0, (2, 2)))
ax.plot([55, 220], [0.55, 0.55], color=ZED, lw=0.7)
ax.text(137.5, 0.66, "the two absences — never played",
        ha="center", va="bottom", fontsize=9, color=SEC, fontstyle="italic")

# the three means in their true linear spots
means = [("HM", HM, MIRR), ("GM", GM, SEAM), ("AM", AM, SIGN)]
for name, f, col in means:
    ax.plot([f, f], [0, 0.42], color=col, lw=1.4)
    ax.scatter([f], [0.42], s=38, color=SURF, edgecolor=col, lw=1.6, zorder=4)
    ax.text(f, 0.55, name, ha="center", va="bottom", fontsize=11,
            color=col, fontweight="bold")
    ax.text(f, -0.32, f"{f:g}", ha="center", va="top", fontsize=9, color=INK)

# the linear midpoint = the AM, exactly; GM and HM off-centre
ax.annotate("only the AM is the linear midpoint", xy=(137.5, 0.42),
            xytext=(150, 0.98), fontsize=9, color=SEC, fontstyle="italic",
            arrowprops=dict(arrowstyle="-", color=SEC, lw=0.7))
ax.text(48, 0.92, "on the line, the averages part",
        ha="left", va="center", fontsize=12, color=INK, fontweight="bold")

# ---------------------------------------------------------------- panel B
ax = axes[1]
ax.set_facecolor(SURF)
lim = 1320.0
ax.set_xlim(-lim, lim)
ax.set_ylim(-2.6, 1.5)
ax.axis("off")

# the log/pitch axis, centred on the count
ax.annotate("", (-lim, 0), (lim, 0), arrowprops=dict(arrowstyle="-",
            color=ZED, lw=1.0))
ax.text(lim + 22, 0, "¢ (log₂ f, relative to 110)", va="center", ha="left",
        fontsize=9, color=SEC)

def value_label(f, label, color=INK, fontweight="normal"):
    x = cents(f)
    ax.plot([x, x], [0, -0.09], color=ZED, lw=0.8)
    ax.text(x, -0.30, label, ha="center", va="top", fontsize=10.5,
            color=color, fontweight=fontweight)

# the count at centre -- a short spine and a bold label
ax.plot([0, 0], [0, 0.40], color=SEAM, lw=2.0)
ax.scatter([0], [0.40], s=46, color=SEAM, zorder=4)
value_label(110, "110", SEAM, "bold")

# bracket 1: the octave pair (the absences) -- SIGN, above the axis
for s in (-1200, 1200):
    ax.plot([s, s], [0, 0.55], color=SIGN, lw=1.1, ls=(0, (4, 2)))
ax.plot([-1200, 1200], [0.55, 0.55], color=SIGN, lw=1.4)
ax.text(0, 0.63, "the absences · 55 & 220 · ×2", ha="center", va="bottom",
        fontsize=9.5, color=SIGN)
value_label(55, "55")
value_label(220, "220")

# bracket 2: the third pair (the means) -- MIRR, below the axis
for s in (-386.31, 386.31):
    ax.plot([s, s], [0, -1.00], color=MIRR, lw=1.1, ls=(0, (4, 2)))
ax.plot([-386.31, 386.31], [-1.00, -1.00], color=MIRR, lw=1.4)
ax.text(0, -1.09, "the means · 88 & 137.5 · 5/4 · 4/5", ha="center",
        va="bottom", fontsize=9.5, color=MIRR)
value_label(88, "88")
value_label(137.5, "137.5")

# the two brackets share the same centre -- mark the equal spacing
for x in (-386.31, 386.31):
    ax.plot([x, x], [0.55, 0.66], color=SEC, lw=0.6)
    ax.plot([0, x], [0.66, 0.66], color=SEC, lw=0.6)
    ax.plot([0, 0], [0.55, 0.66], color=SEC, lw=0.6)
ax.text(-193, 0.76, "386.3¢", ha="center", va="bottom", fontsize=8, color=SEC)

# the equation: AM·HM = GM², the bracket self-similar
ax.text(0, -1.72, "AM · HM = GM²     137.5 · 88 = 110²",
        ha="center", va="top", fontsize=12.5, color=INK, fontweight="bold")
ax.text(0, -2.02, "the count is the GM of its two absences and of its two means",
        ha="center", va="top", fontsize=9.5, color=SEC, fontstyle="italic")
ax.text(48, 1.30, "in the ear, the averages seat back",
        ha="left", va="center", fontsize=12, color=INK, fontweight="bold")

out = "assets/mean-bracket.png"
fig.savefig(out, facecolor=SURF, bbox_inches="tight", pad_inches=0.12)
print("wrote", out)
