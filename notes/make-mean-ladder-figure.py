# mean-ladder-figure — the still for the mean-ladder-sound piece.
#
# Top: the frequency structure. The silver pair {110(√2−1), 110(√2+1)} =
# {45.56, 265.56} mirrors about the count (product 110²). When the pair
# sounds, the EAR manufactures its difference 220 and its sum 311.13 (both
# "already there"). Arithmetic halves them into the means:
#     GM = 110      = ½·(difference)   the count   (silver: σ²−1 = 2σ)
#     AM = 155.56   = ½·(sum)          the tritone (tuned, never struck)
#     HM = 77.78    = 110/√2           below the grid
# The mean is the one number the ear does not make — only arithmetic does.
#
# Bottom: the score — when each thing sounds in the 50 s piece:
#   pair 0-40s, ear's products swell 10s, arithmetic (AM) enters 17s,
#   the full ladder holds 25s as the pair recedes, the pair fades at 34s,
#   the ladder alone, a last AM echo at 41s.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

S2 = np.sqrt(2)
PL, PH = 110 * (S2 - 1), 110 * (S2 + 1)   # 45.563, 265.563
ST, DT = PL + PH, PH - PL                 # 311.127, 220.000
HM, GM, AM = 110 / S2, 110.0, 110 * S2    # 77.782, 110, 155.563

BG = "#101216"
PANEL = "#151a21"
INK = "#c9cdd6"
TITL = "#e8eaed"
GOLD = "#f2c14e"     # the pair
TEAL = "#2a9d8f"     # the ear's products (sum & difference)
ORNG = "#e76f51"     # the count — the kept note (GM)
BLUE = "#8ecae6"     # the tritone — the manufactured note (AM)
ROSE = "#b5838d"     # the HM — below the grid
GRID = "#262b33"

fig, axes = plt.subplots(2, 1, figsize=(11, 8), dpi=150)
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(PANEL)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#5b616e")
    ax.tick_params(colors=INK, which="both", labelsize=9)

# --------------------------------------------------------------------------
# top panel: the frequency line
# --------------------------------------------------------------------------
ax = axes[0]
ax.set_xscale("log")
ax.set_xlim(36, 360)
ax.set_ylim(0, 10)

# the reflection axis at the count
ax.axvline(GM, color=ORNG, lw=1.2, ls=(0, (3, 3)), alpha=0.55, zorder=1)
ax.text(GM, 9.6, "the count — the reflection's fixed point", color=ORNG,
        fontsize=8.5, ha="center", va="top", alpha=0.95)

# half-difference / half-sum arrows: ear's products halved into the means
def half_arrow(x_from, x_to, label, color):
    y = 6.2
    ax.annotate("", xy=(x_to, y - 0.15), xytext=(x_from, y - 0.15),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
    ax.plot([x_from, x_to], [y - 0.15, y - 0.15], color=color, lw=1.0, alpha=0.7)
    ax.text(np.sqrt(x_from * x_to), y + 0.45, label, color=color,
            fontsize=8.5, ha="center", va="bottom")

half_arrow(DT, GM, "÷2 — the count, half the difference", TEAL)
half_arrow(ST, AM, "÷2 — the tritone, half the sum", TEAL)

# the ear's products (diamonds): already there when the pair sounds
for f, a, lab in [(DT, 1.0, "difference 220"), (ST, 0.55, "sum 311")]:
    ax.plot([f], [5.0], marker="D", ms=11, color=TEAL, alpha=a, mec=BG,
            mew=1.2, zorder=6)
    ax.text(f, 4.1, lab, color=TEAL, fontsize=8.5, ha="center", va="top",
            alpha=0.9)

# the pair (filled circles)
for f, lab in [(PL, "45.6"), (PH, "265.6")]:
    ax.plot([f], [7.6], marker="o", ms=12, color=GOLD, mec=BG, mew=1.4, zorder=6)
    ax.text(f, 8.35, lab, color=GOLD, fontsize=9, ha="center", va="bottom")
ax.text(np.sqrt(PL * PH), 7.0, "the silver pair — product 110²",
        color=GOLD, fontsize=8.5, ha="center", va="bottom", alpha=0.85)

# the ladder: the three means (squares)
ladder = [
    (HM, ROSE, "HM 77.8 — below the grid"),
    (GM, ORNG, "GM 110 — the count, kept"),
    (AM, BLUE, "AM 155.6 — the tritone, made"),
]
for f, c, lab in ladder:
    ax.plot([f], [3.2], marker="s", ms=11, color=c, mec=BG, mew=1.3, zorder=6)
    ax.text(f, 2.35, lab, color=c, fontsize=8.5, ha="center", va="top")
# bracket under the ladder
ax.plot([HM, HM], [2.6, 2.9], color=INK, lw=0.8, alpha=0.6)
ax.plot([AM, AM], [2.6, 2.9], color=INK, lw=0.8, alpha=0.6)
ax.plot([HM, AM], [2.75, 2.75], color=INK, lw=0.8, alpha=0.6)

ax.set_yticks([])
ax.set_xlabel("frequency (log Hz)", color=INK, fontsize=10)
ax.set_title("the mean is the one number the ear does not make",
             color=TITL, fontsize=13, pad=10)

# --------------------------------------------------------------------------
# bottom panel: the score — when each thing sounds
# --------------------------------------------------------------------------
ax = axes[1]
ax.set_xlim(0, 50)
ax.set_ylim(0, 4)

def band(x0, x1, y0, y1, color, label, alpha=0.85):
    ax.add_patch(mpatches.Rectangle((x0, y0), x1 - x0, y1 - y0,
                                    facecolor=color, alpha=alpha,
                                    edgecolor="none"))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, label, color=BG, fontsize=8.5,
            ha="center", va="center", fontweight="bold")

band(0, 40, 3.1, 3.9, GOLD, "the pair sounds — the ear makes 220 and 311")
band(10, 34, 2.1, 2.9, TEAL, "its products swell — already there")
band(17, 46, 1.1, 1.9, BLUE, "arithmetic: the tritone 155.6 (half the sum)")
band(25, 46, 0.1, 0.9, ORNG, "the ladder holds — HM 77.8 · GM 110 · AM 155.6")

ax.text(40, 2.5, "pair\nfades", color=INK, fontsize=7.5, ha="center", va="center")
ax.axvline(40, color=INK, lw=0.8, ls=":", alpha=0.7)
ax.text(41, 0.5, "echo", color=BLUE, fontsize=8, ha="left", va="center")

ax.set_yticks([])
ax.set_xlabel("seconds", color=INK, fontsize=10)

fig.suptitle("the silver pair's means — count half the difference, tritone half the sum",
             color=TITL, fontsize=11, y=0.985)

fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/mean-ladder.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/mean-ladder.png")
