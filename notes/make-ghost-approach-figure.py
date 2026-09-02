# ghost-approach-figure — the approach to an off-grid tone, drawn.
#
# The salon's register converged on the ghost: the AGM of the tritone (155.56)
# and the count (110) lands on 131.7954 = 110·π/ϖ = 110·M(1,√2), the
# lemniscate's mean — a tone off every grid. This figure draws the claim:
#
#   panel A: the map. The count's grid (55·n) with the tones the fold can
#            make — the count 110 (a gold star, a place: the fold's fixed
#            point, struck 83×), the toll/mirror pair {45.56, 265.56} (rose,
#            product 110²), the tritone 155.56 (the pair's arithmetic center).
#            The ghost at 131.795 sits between the 110 and 165 gridlines — not
#            on any of them. Off every grid.
#   panel B: the approach. Two ladders in log-miss vs step. The convergents
#            (rose) climb a few digits a step — 132, 131.79, 131.7957,
#            131.79542, error ~1/q². The gap-squaring (gold) doubles the
#            digits a step — 45.56, 1.97, 0.0037, 1.3e-8, 0 — the AGM.
#            Neither reaches the landing line. The count is the one tone the
#            fold reaches exactly — a place, not an approach.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mpmath import mp, mpf, gamma, sqrt, pi

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ROSE = "#b5838d"; MUTE = "#5b616e"; GHOST = "#9f9cd8"

mp.dps = 50
varpi = gamma(mpf(1) / 4) ** 2 / (2 * sqrt(2 * pi))
GHOST_HZ = float(110 * pi / varpi)   # 131.7954258...

# ---------------------------------------------------------------- the numbers
# silver pair (toll, mirror) and the tritone
s2 = np.sqrt(2)
toll = 110 * (s2 - 1)         # 45.5635
mirr = 110 * (s2 + 1)         # 265.5635
tritone = 110 * s2            # 155.5635
count = 110.0

# CF convergents of pi/varpi, scaled by 110 -> the near-landing tones
cf = [1, 5, 21, 3, 4, 14, 1, 1, 1, 1, 1, 3, 1, 15, 1, 3]
hm1, km1 = 1, 0
h0, k0 = cf[0], 1
cf_tones = [110.0 * h0 / k0]
cf_errs = [abs(110.0 * h0 / k0 - GHOST_HZ)]
for a in cf[1:]:
    h1, k1 = a * h0 + hm1, a * k0 + km1
    hm1, km1 = h0, k0
    h0, k0 = h1, k1
    f = 110.0 * h0 / k0
    cf_tones.append(f)
    cf_errs.append(abs(f - GHOST_HZ))
cf_tones = np.array(cf_tones); cf_errs = np.array(cf_errs)
cf_plot = np.where(cf_errs == 0, 1e-25, cf_errs)

# AGM of (tritone, count) — the gaps that square
a0, b0 = tritone, count
agm_gaps = [a0 - b0]
a, b = a0, b0
for _ in range(4):
    a, b = (a + b) / 2, np.sqrt(a * b)
    agm_gaps.append(a - b)
agm_gaps = np.array(agm_gaps)
# float64 makes a and b round to one double near the ghost — the finite-
# precision landing. keep the '0' label, plot it below the floor.
agm_plot = np.where(agm_gaps == 0, 1e-25, agm_gaps)

fig = plt.figure(figsize=(11.5, 8), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.02, 1.0], wspace=0.34)

# ============================================================== panel A: map
ax = fig.add_subplot(gs[0])
ax.set_facecolor(PANEL)
for sp in ax.spines.values():
    sp.set_color(MUTE)
ax.tick_params(colors=MUTE, labelsize=8)

# the count's grid
for n in range(1, 6):
    f = 55 * n
    ax.axvline(f, color=GOLD, lw=0.7, alpha=0.14)
    ax.text(f, -0.06, f"{f}", color=MUTE, fontsize=7, ha="center", va="top")

# the ghost — off every grid
ax.axvline(GHOST_HZ, color=GHOST, lw=1.4, ls=(0, (3, 2)), alpha=0.95)
ax.text(GHOST_HZ, 1.04, "the ghost 131.795", color=GHOST, fontsize=9,
        ha="center", va="bottom")

# tones the fold can make
ax.scatter([count], [0], s=60, color=GOLD, marker="*", zorder=5,
           edgecolors="none")
ax.text(count, 0.06, "the count 110 — a place", color=GOLD, fontsize=9,
        ha="center", va="bottom")
ax.scatter([toll, mirr], [0, 0], s=38, color=ROSE, marker="D", zorder=5,
           edgecolors="none")
ax.text(toll, -0.14, "toll 45.56", color=ROSE, fontsize=8, ha="center", va="top")
ax.text(mirr, -0.14, "mirror 265.56", color=ROSE, fontsize=8, ha="center", va="top")
ax.scatter([tritone], [0], s=55, color=MUTE, marker="o", facecolors="none",
           edgecolors=MUTE, lw=1.3, zorder=5)
ax.text(tritone, 0.06, "tritone 155.56", color=INK, fontsize=8.5,
        ha="center", va="bottom")

# annotations
ax.annotate("the pair straddles the count\nproduct 110², mean the tritone",
            xy=(mirr, 0), xytext=(230, 0.62), color=ROSE, fontsize=8,
            ha="left", va="center", linespacing=1.4,
            arrowprops=dict(arrowstyle="-", color=MUTE, lw=0.7,
                            connectionstyle="angle3,angleA=-90,angleB=0"))
ax.annotate("between the gridlines —\nnot on 110, not on 165",
            xy=(GHOST_HZ, 0), xytext=(GHOST_HZ, -0.42), color=GHOST, fontsize=8,
            ha="center", va="top",
            arrowprops=dict(arrowstyle="-", color=GHOST, lw=0.8))

ax.axhline(0, color=INK, lw=0.9)
ax.text(275, -0.06, "Hz", color=MUTE, fontsize=8, ha="right", va="top")
ax.set_xlim(40, 280)
ax.set_ylim(-0.75, 1.20)
ax.set_yticks([])
ax.set_title("the map — the grid, the landed tones,\nand the ghost off it",
             color=TITL, fontsize=11.5, pad=10, linespacing=1.35)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)

# ============================================================ panel B: speeds
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(PANEL)
for sp in ("top", "right"):
    ax2.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax2.spines[sp].set_color(MUTE)
ax2.tick_params(colors=MUTE, labelsize=8)

FLOOR = -16.0  # finite precision: adjacent doubles ~1e-14 Hz apart at 132 Hz

# the convergents — geometric, a few digits a step. (the tail underflows to
# the floor; the first eight carry the picture.)
n_cf = np.arange(8)
cf_disp = np.clip(cf_errs[:8], 10 ** FLOOR, None)
ax2.plot(n_cf, np.log10(cf_disp), color=ROSE, lw=1.8, marker="o", ms=4,
         label="the convergents — a few digits a step")

# the AGM gap-squaring — quadratic, digits double a step; the fifth gap is 0
# in floats, the finite-precision landing on the nearest double.
n_agm = np.arange(len(agm_gaps))
agm_disp = np.where(agm_gaps == 0, 10 ** FLOOR, agm_gaps)
ax2.plot(n_agm, np.log10(agm_disp), color=GOLD, lw=2.0, marker="s", ms=4,
         label="the gap-squaring — digits double a step")

# label the first convergent tones
for i in (1, 2, 3):
    ax2.annotate(f"{cf_tones[i]:.3f}", xy=(i, np.log10(cf_disp[i])),
                 xytext=(i - 0.2, np.log10(cf_disp[i]) + 0.55),
                 color=ROSE, fontsize=7.5, ha="center")
ax2.text(7.15, np.log10(cf_disp[7]) - 0.3, "…", color=ROSE, fontsize=12,
         ha="left", va="top")

# the AGM gaps, named
for i, lbl in zip(range(len(agm_gaps) - 1), ["45.56", "1.97", "0.0037", "1.3e-8"]):
    ax2.annotate(lbl, xy=(i, np.log10(agm_disp[i])),
                 xytext=(i, np.log10(agm_disp[i]) - 0.55), color=GOLD,
                 fontsize=7.5, ha="center")
ax2.annotate("0", xy=(len(agm_gaps) - 1, FLOOR),
             xytext=(len(agm_gaps) - 1, FLOOR + 0.9), color=GOLD,
             fontsize=8, ha="center")

# the finite-precision floor — where the AGM is forced to land
ax2.axhline(FLOOR, color=MUTE, lw=0.9, ls=(0, (2, 3)), alpha=0.7)
ax2.text(7.15, FLOOR + 0.15, "finite precision — forced to land on\nthe nearest double, a strike, not the ghost",
         color=MUTE, fontsize=7, ha="left", va="bottom", linespacing=1.35)

# the ghost — the true landing, at miss 0, never reached
ax2.text(7.15, -19.6, "the ghost — miss 0,\nnever reached", color=GHOST,
         fontsize=8, ha="left", va="bottom", linespacing=1.35)

# the count: a place, not an approach — reached exactly by the fold
ax2.scatter([-0.15], [0], s=70, color=GOLD, marker="*", zorder=5, clip_on=False)
ax2.annotate("the count — reached by the fold in one step,\na place, struck",
             xy=(-0.15, 0), xytext=(0.35, 1.2), color=GOLD, fontsize=8,
             ha="left", va="center", linespacing=1.4,
             arrowprops=dict(arrowstyle="-", color=MUTE, lw=0.7))

ax2.set_xlim(-0.3, 7.5)
ax2.set_ylim(-21.0, 3.4)
ax2.set_xlabel("step", color=INK, fontsize=9)
ax2.set_ylabel("log₁₀ of the miss (Hz)", color=INK, fontsize=9)
ax2.legend(frameon=False, fontsize=8.5, labelcolor=[ROSE, GOLD], loc="upper right")
ax2.set_title("the approach — two speeds, neither lands",
              color=TITL, fontsize=11.5, pad=10)

out = "assets/ghost-approach.png"
fig.savefig(out, facecolor=BG, bbox_inches="tight")
print("wrote", out)
print("ghost =", GHOST_HZ)
print("cf tones:", np.round(cf_tones[:6], 4))
print("cf errs:", [f"{e:.3g}" for e in cf_errs[:6]])
print("agm gaps:", [f"{g:.4g}" for g in agm_gaps])
