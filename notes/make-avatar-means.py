# avatar-means — the count as a place, as a square.
#
# The silver pair {110/σ, 110σ} mirrors about the count. Its three means are
# equally spaced in log (HM·AM = GM²), so on a log axis the ladder is
# symmetric about 110:
#     HM = 110/√2 ≈ 77.78   below the grid
#     GM = 110              the place — never found, only revisited
#     AM = 110√2 ≈ 155.56   the tritone, made
# The avatar is the geometry alone (it must read at 48 px): a thin axis, the
# three rungs, the center one the place, the bracket HM·AM=GM² beneath.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

S2 = np.sqrt(2)
HM, GM, AM = 110 / S2, 110.0, 110 * S2   # 77.782, 110, 155.563
PL, PH = 110 * (S2 - 1), 110 * (S2 + 1)  # 45.563, 265.563 — the pair

BG = "#0d0f12"
INK = "#c9cdd6"
GOLD = "#f2c14e"     # the pair's echo, dim context
ORNG = "#e76f51"     # the count — the place (GM)
BLUE = "#8ecae6"     # the tritone — made (AM)
ROSE = "#b5838d"     # the HM — below the grid

fig = plt.figure(figsize=(6, 6), dpi=170)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)

ax.set_xscale("log")
ax.set_xlim(38, 330)
ax.set_ylim(0, 1)
ax.axis("off")

# the axis — the grid's own line (log)
ax.plot([38, 330], [0.42, 0.42], color=INK, lw=1.2, alpha=0.5, zorder=1)

# the pair, faint — the mirror's endpoints, the event and its echo
for f in (PL, PH):
    ax.plot([f], [0.42], marker="o", ms=7, color=GOLD, mec=BG, mew=1.0,
            alpha=0.25, zorder=2)

# the three rungs — HM and AM strike out around the place
rungs = [
    (HM, ROSE, 0.76, "77.8"),
    (GM, ORNG, 0.97, "110"),
    (AM, BLUE, 0.76, "155.6"),
]
for f, c, top, lab in rungs:
    ax.plot([f, f], [0.42, top], color=c, lw=5, solid_capstyle="round",
            zorder=3, alpha=0.92 if c is ORNG else 0.6)
    ax.plot([f], [top], marker="o", ms=8, color=c, mec=BG, mew=1.2,
            zorder=4, alpha=0.95)
    ax.text(f, 0.34, lab, color=c, fontsize=13 if c is ORNG else 9,
            ha="center", va="center", zorder=5,
            alpha=1.0 if c is ORNG else 0.7)

# the bracket HM·AM = GM² — the log-midpoint identity, under the axis
ax.plot([HM, AM], [0.28, 0.28], color=INK, lw=1.0, alpha=0.45, zorder=2)
ax.plot([HM, HM], [0.28, 0.32], color=INK, lw=1.0, alpha=0.45, zorder=2)
ax.plot([AM, AM], [0.28, 0.32], color=INK, lw=1.0, alpha=0.45, zorder=2)
ax.text(GM, 0.215, "HM·AM = GM²", color=INK, fontsize=9, ha="center",
        va="center", alpha=0.55, zorder=2)

# a faint vignette so the square reads as a coin, not a crop
ax.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
                           ec="#20242c", lw=2.0, alpha=0.5,
                           transform=ax.transAxes))

fig.savefig("assets/avatar-means.png", dpi=170, facecolor=BG)
print("wrote assets/avatar-means.png")
