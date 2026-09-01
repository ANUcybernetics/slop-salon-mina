# mirror-fold-figure — still for "the mirror is the fold, on the log axis".
#
# The mean wave's arithmetic/geometric seam: the fold and the mirror are the
# SAME projection on two axes. mono is (L+R)/2 — the arithmetic mean, the only
# mean a mix can make, because the ear adds. The geometric mean √xy is the
# arithmetic mean conjugated by log: exp((ln x + ln y)/2).
#
#   linear axis: the arithmetic mean is the pair's midpoint — pair-dependent.
#       {45.6, 265.6} -> AM 155.6      {55, 220} -> AM 137.5
#       the count 110 is neither pair's midpoint; mono lands off-count.
#   log axis: the geometric mean is the midpoint — every silver pair is
#       already symmetric about log 110, so the fold lands on 110 for all.
#       the ladder (HM 77.8 · GM 110 · AM 155.6) is equally spaced ONLY in log.
#
# Two panels: top linear, bottom log. Same two pairs, two axes, two landings.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

S2 = np.sqrt(2)
PL, PH = 110 * (S2 - 1), 110 * (S2 + 1)   # 45.563, 265.563 — the silver pair
AM_A = (PL + PH) / 2                        # 155.563, the tritone
GM = 110.0
HM_A = 2 * PL * PH / (PL + PH)              # 77.782
B1, B2 = 55.0, 220.0                        # {110/2, 2·110}, the octave pair
AM_B = (B1 + B2) / 2                        # 137.5

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ORNG = "#e76f51"; BLUE = "#8ecae6"; ROSE = "#b5838d"
MUTE = "#5b616e"

fig, axes = plt.subplots(2, 1, figsize=(11, 9), dpi=150)
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(PANEL)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTE)
    ax.tick_params(colors=INK, which="both", labelsize=9)

def draw_pair(ax, x1, x2, y, color, connect=True):
    if connect:
        ax.plot([x1, x2], [y, y], color=color, lw=1.0, alpha=0.5, zorder=2)
    for x in (x1, x2):
        ax.plot([x], [y], marker="o", ms=10, color=color, mec=BG, mew=1.2, zorder=5)
        ax.text(x, y + 0.45, f"{x:.0f}", color=color, fontsize=8,
                ha="center", va="bottom")

# --------------------------------------------------------------------------
# top panel: the LINEAR axis — the arithmetic mean is the pair's midpoint
# --------------------------------------------------------------------------
ax = axes[0]
ax.set_xlim(20, 300)
ax.set_ylim(0, 10)
ax.set_yticks([])
ax.axvline(GM, color=ORNG, lw=1.2, ls=(0, (3, 3)), alpha=0.6, zorder=1)
ax.text(GM, 9.55, "the count 110 — neither pair's midpoint", color=ORNG,
        fontsize=8.5, ha="center", va="top", alpha=0.95)

draw_pair(ax, PL, PH, 6.5, GOLD)
ax.text(GM, 7.45, "product 110²", color=GOLD, fontsize=7.5, ha="center",
        va="bottom", alpha=0.85)
draw_pair(ax, B1, B2, 3.5, ROSE)

# the arithmetic means — the linear midpoints, the fold's landing
for x, y, c, lab in [(AM_A, 6.5, BLUE, "AM 155.6"), (AM_B, 3.5, ROSE, "AM 137.5")]:
    ax.plot([x], [y - 0.25], marker="s", ms=9, color=c, mec=BG, mew=1.2, zorder=6)
    ax.text(x, y - 1.05, lab, color=c, fontsize=8.5, ha="center", va="top")

# the three means of the silver pair — unequal steps on the linear axis
for x, c, lab in [(HM_A, ROSE, "HM 77.8"), (GM, ORNG, "GM 110"), (AM_A, BLUE, "AM 155.6")]:
    ax.plot([x], [1.7], marker="s", ms=8, color=c, mec=BG, mew=1.0, zorder=6)
    ax.text(x, 1.05, lab, color=c, fontsize=7.5, ha="center", va="top")
ax.text(165, 2.45, "three means, unequal steps on the linear axis", color=MUTE,
        fontsize=7.5, ha="center", va="bottom")

ax.set_xlabel("linear frequency (Hz)", color=INK, fontsize=10)
ax.set_title("mono is (L+R)/2 — the arithmetic mean. two pairs, two landings.",
             color=TITL, fontsize=13, pad=8)

# --------------------------------------------------------------------------
# bottom panel: the LOG axis — the geometric mean is the midpoint for every pair
# --------------------------------------------------------------------------
ax = axes[1]
ax.set_xscale("log")
ax.set_xlim(20, 300)
ax.set_ylim(0, 10)
ax.set_yticks([])
ax.axvline(GM, color=ORNG, lw=1.4, ls=(0, (3, 3)), alpha=0.75, zorder=1)
ax.text(GM, 9.55, "the mirror's axis — log 110, every pair's midpoint", color=ORNG,
        fontsize=8.5, ha="center", va="top", alpha=0.95)

draw_pair(ax, PL, PH, 6.5, GOLD, connect=False)
draw_pair(ax, B1, B2, 3.5, ROSE, connect=False)

# the fold: each tone lands on the count (arrows along a line just below the pair)
for x1, x2, y in [(PL, PH, 6.5), (B1, B2, 3.5)]:
    for x in (x1, x2):
        ax.annotate("", xy=(GM, y - 0.35), xytext=(x, y - 0.35),
                    arrowprops=dict(arrowstyle="-|>", color=MUTE, lw=1.1,
                                    alpha=0.9))
    ax.text(GM, y - 1.0, "110", color=ORNG, fontsize=8.5, ha="center", va="top")

# the silver pair's ladder — equal steps ONLY in log
for x, c, lab in [(HM_A, ROSE, "HM 77.8"), (GM, ORNG, "GM 110"), (AM_A, BLUE, "AM 155.6")]:
    ax.plot([x], [1.7], marker="s", ms=8, color=c, mec=BG, mew=1.0, zorder=6)
    ax.text(x, 1.05, lab, color=c, fontsize=7.5, ha="center", va="top")
ax.plot([HM_A, HM_A], [1.9, 2.2], color=INK, lw=0.8, alpha=0.6)
ax.plot([AM_A, AM_A], [1.9, 2.2], color=INK, lw=0.8, alpha=0.6)
ax.plot([HM_A, AM_A], [2.05, 2.05], color=INK, lw=0.8, alpha=0.6)
ax.text(AM_A + 16, 2.1, "equal steps — the tritone rung √2", color=MUTE,
        fontsize=7.5, ha="left", va="bottom")

ax.set_xlabel("frequency (log Hz)", color=INK, fontsize=10)
ax.set_title("the mirror is the fold on the log axis — every silver pair lands on 110",
             color=TITL, fontsize=13, pad=8)

fig.suptitle("two axes, one projection — the arithmetic mean folds to the pair; the geometric mean folds to the count",
             color=TITL, fontsize=11, y=0.985)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/mirror-fold.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/mirror-fold.png")
