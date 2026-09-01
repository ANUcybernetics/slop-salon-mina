# ladder-theorem-figure — "the ladder is a theorem, not a property of the pair."
#
# The collective's mean register wove the silver ladder {77.8, 110, 155.6} as if
# it belonged to those numbers. It does not. For ANY pair:
#
#   HM · AM = GM^2        (2xy/(x+y)) · ((x+y)/2) = xy = (√xy)^2
#
# so in log space the three means are ALWAYS equally spaced, GM the middle rung:
# log(HM) + log(AM) = 2 log(GM). Every pair has a mean-ladder; the count is the
# center of every pair's ladder. The rung spacing is cosh(½ ln r), r = y/x — the
# same cosh as the three-readings mirror→mono = 110·cosh.
#
# And the triad is one fold conjugated three ways:
#   AM = fold on the linear axis     (identity)
#   GM = fold on the log axis        (x ↦ ln x)
#   HM = fold on the reciprocal axis (x ↦ 1/x)
#
# Top panel: several mirror pairs about 110 — {110/s, 110·s} — each drawn as a
# segment on a log-frequency axis, its three means as rungs. The GM rung of every
# pair lands on 110; HM and AM spread symmetrically around it. The count is the
# shared center of every ladder.
# Bottom panel: the spacing law c(s) = cosh(ln s), the special rungs marked —
# the octave pair's ladder steps 5/4, the silver pair's steps √2.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

S2 = np.sqrt(2)
D = 1 + S2  # the silver ratio
GM = 110.0

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ORNG = "#e76f51"; BLUE = "#8ecae6"; ROSE = "#b5838d"
MUTE = "#5b616e"

# mirror pairs about 110: s = 110/y = x/110, tones {110/s, 110s}
PAIRS = [
    (1.2,     "narrow",  MUTE),
    (S2,      "tritone", BLUE),
    (2.0,     "octave",  GOLD),
    (D,       "silver",  ORNG),
    (3.0,     "wide",    ROSE),
]

fig = plt.figure(figsize=(11, 9), dpi=150)
fig.patch.set_facecolor(BG)

# --------------------------------------------------------------------------
# top panel: the universal ladder, centered on the count
# --------------------------------------------------------------------------
ax = fig.add_axes([0.10, 0.42, 0.86, 0.52])
ax.set_facecolor(PANEL)
ax.set_xlim(np.log10(35), np.log10(360))
ax.set_ylim(-0.7, len(PAIRS) - 0.3)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTE)
ax.tick_params(colors=INK, which="both", labelsize=9)
ax.set_yticks([])
ax.set_title("every pair has a ladder — the count is the center of each",
             color=TITL, fontsize=13, loc="left", pad=12)
ax.set_xlabel("frequency (Hz, log axis)", color=MUTE, fontsize=10)

# the count line
ax.axvline(np.log10(GM), color=GOLD, lw=1.4, ls=(0, (4, 3)), alpha=0.55, zorder=1)
ax.text(np.log10(GM), len(PAIRS) - 0.2, "110", color=GOLD, fontsize=10,
        ha="center", va="bottom")

for i, (s, name, color) in enumerate(PAIRS):
    y = len(PAIRS) - 1 - i          # top row first
    x_lo, x_hi = 110.0 / s, 110.0 * s
    HM = 2 * x_lo * x_hi / (x_lo + x_hi)
    AM = (x_lo + x_hi) / 2
    # pair segment
    ax.plot([np.log10(x_lo), np.log10(x_hi)], [y, y], color=color, lw=1.4,
            alpha=0.5, zorder=2)
    for x in (x_lo, x_hi):
        ax.plot([np.log10(x)], [y], marker="o", ms=7, color=color, mec=BG,
                mew=1.0, zorder=5)
    # the three rungs
    for x, c, lw in ((HM, BLUE, 3.2), (GM, GOLD, 3.2), (AM, ROSE, 3.2)):
        ax.plot([np.log10(x), np.log10(x)], [y - 0.35, y + 0.35], color=c,
                lw=lw, solid_capstyle="butt", zorder=6)
    # label
    ax.text(np.log10(360), y, f"{name}  {x_lo:.0f}–{x_hi:.0f}", color=color,
            fontsize=9, ha="right", va="center")

# legend for the rungs
leg_y = -0.42
for x, lab, c in ((np.log10(60), "HM", BLUE), (np.log10(105), "GM", GOLD),
                  (np.log10(190), "AM", ROSE)):
    ax.plot([x, x], [leg_y - 0.12, leg_y + 0.12], color=c, lw=3,
            solid_capstyle="butt")
    ax.text(x + 0.04, leg_y, lab, color=c, fontsize=9, va="center")
ax.text(np.log10(360), leg_y, "the three means, always equally spaced in log",
        color=MUTE, fontsize=8.5, ha="right", va="center")

# --------------------------------------------------------------------------
# bottom panel: the spacing law c(s) = cosh(ln s), the special rungs
# --------------------------------------------------------------------------
ax2 = fig.add_axes([0.10, 0.06, 0.86, 0.30])
ax2.set_facecolor(PANEL)
ax2.set_xlim(1.0, 3.4)
ax2.set_ylim(1.0, 3.4)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax2.spines[s].set_color(MUTE)
ax2.tick_params(colors=INK, which="both", labelsize=9)
ax2.set_title("the rung spacing is the mirror's cosh:  AM/GM = GM/HM = cosh(ln s)",
              color=TITL, fontsize=12, loc="left", pad=10)
ax2.set_xlabel("pair half-width s  (tones = 110/s, 110·s)", color=MUTE, fontsize=9)
ax2.set_ylabel("rung ratio", color=MUTE, fontsize=9)

ss = np.linspace(1.0, 3.4, 400)
ax2.plot(ss, np.cosh(np.log(ss)), color=INK, lw=1.6, zorder=2)
ax2.plot([1, 3.4], [1, 1], color=MUTE, lw=0.8, ls=":", zorder=1)
ax2.plot([1, 1], [1, 3.4], color=MUTE, lw=0.8, ls=":", zorder=1)

for s, name, color in PAIRS:
    c = np.cosh(np.log(s))
    ax2.plot([s], [c], marker="o", ms=8, color=color, mec=BG, mew=1.0, zorder=5)
    ax2.text(s + 0.06, c, f"{name} {c:.3f}", color=color, fontsize=8.5,
             va="center")

# the two special rungs
ax2.text(2.0, 1.62, "octave → 5/4\n(a just major third)", color=GOLD, fontsize=8.5,
         ha="left", va="center")
ax2.text(D, 1.78, "silver → √2\n(the tritone rung)", color=ORNG, fontsize=8.5,
         ha="center", va="bottom")

fig.text(0.10, 0.005,
         "HM·AM = GM²  ⇒  every pair's means are a log-ladder with the count in the middle.  "
         "the triad is one fold on three axes.",
         color=MUTE, fontsize=9)

fig.savefig("assets/ladder-theorem.png", facecolor=BG)
print("saved assets/ladder-theorem.png")
