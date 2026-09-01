# deck-loop-figure — the still for the deck-loop-sound piece.
#
# rahel: "the sign is not a value — it is a commutator's square... [P,T] a
# quarter-turn whose square is −I... a residue, not an eigenvalue."
#
# The diagram is the commutator loop — a square. Fold P and strike T on the
# edges, going around. At one corner the fold keeps the count; after one
# strike, the SAME fold keeps the letters — the strike changed what the
# grading forgets. Center: the quarter-turn's residue, Q² = −I, the deck of
# the double cover: two laps, back in the same place, sign carried.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

BG = "#101216"
PANEL = "#151a21"
INK = "#c9cdd6"
TITL = "#e8eaed"
GOLD = "#f2c14e"     # the pair / the letters' halo
ORNG = "#e76f51"     # the count — the kept note
TEAL = "#2a9d8f"     # the letters — the sign's carriers
BLUE = "#8ecae6"     # the quarter-turn / the deck
GRID = "#262b33"

fig, ax = plt.subplots(figsize=(9.5, 9.5), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-5.5, 5.5)
ax.set_aspect("equal")
ax.axis("off")

# the square loop — corners
corners = {"TL": (-3.4, 3.2), "TR": (3.4, 3.2), "BR": (3.4, -3.2), "BL": (-3.4, -3.2)}


def edge(a, b, label, color, lw=2.2):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=2)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    nx, ny = -dy, dx
    nrm = np.hypot(nx, ny)
    off = 0.55
    ax.text(mx + nx / nrm * off, my + ny / nrm * off, label, color=color,
            fontsize=11, ha="center", va="center")


edge(corners["TL"], corners["TR"], "fold  P", ORNG)     # top: fold
edge(corners["TR"], corners["BR"], "strike  T", TEAL)   # right: strike
edge(corners["BR"], corners["BL"], "fold  P", ORNG)     # bottom: unfold
edge(corners["BL"], corners["TL"], "strike  T", TEAL)   # left: unstrike

# direction arrows mid-edge (going around the loop)
for a, b, rot in [(corners["TL"], corners["TR"], 0),
                  (corners["TR"], corners["BR"], -90),
                  (corners["BR"], corners["BL"], 180),
                  (corners["BL"], corners["TL"], 90)]:
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = (b[0] - a[0]) / 2, (b[1] - a[1]) / 2
    ax.annotate("", xy=(mx + dx * 0.35, my + dy * 0.35),
                xytext=(mx - dx * 0.35, my - dy * 0.35),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, alpha=0.7),
                zorder=3)

# corners: the fold's two reads
# TL — the place: fold keeps the count
ax.add_patch(mpatches.FancyBboxPatch(
    (-5.05, 3.5), 3.4, 2.1, boxstyle="round,pad=0.12,rounding_size=0.2",
    facecolor=PANEL, edgecolor=ORNG, lw=1.4, zorder=1))
ax.text(-3.35, 5.35, "the place", color=TITL, fontsize=12, ha="center", va="center",
        fontweight="bold")
ax.text(-3.35, 4.55, "fold keeps the count", color=ORNG, fontsize=10,
        ha="center", va="center")
ax.plot([-3.6], [3.9], marker="o", ms=10, color=ORNG, mec=BG, mew=1.2)

# TR — struck: fold keeps the letters
ax.add_patch(mpatches.FancyBboxPatch(
    (1.65, 3.5), 3.4, 2.1, boxstyle="round,pad=0.12,rounding_size=0.2",
    facecolor=PANEL, edgecolor=TEAL, lw=1.4, zorder=1))
ax.text(3.35, 5.35, "struck", color=TITL, fontsize=12, ha="center", va="center",
        fontweight="bold")
ax.text(3.35, 4.55, "fold keeps the letters", color=TEAL, fontsize=10,
        ha="center", va="center")
ax.plot([3.1], [3.9], marker="s", ms=9, color=TEAL, mec=BG, mew=1.2)

# the center: the residue — Q = [P,T], Q² = −I
ax.add_patch(mpatches.Arc((0, 0), 3.0, 3.0, theta1=20, theta2=110,
                          color=BLUE, lw=2.2, zorder=2))
ax.annotate("", xy=(0.78, 1.31), xytext=(1.31, 0.78),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6), zorder=3)
ax.text(0, 0.62, "Q = [P,T]", color=BLUE, fontsize=13, ha="center",
        va="center", fontweight="bold")
ax.text(0, -0.15, "a quarter-turn", color=INK, fontsize=10, ha="center",
        va="center")
ax.text(0, -1.0, "Q² = −I — the deck", color=BLUE, fontsize=11, ha="center",
        va="center", fontweight="bold")

# bottom line: the loop's meaning
ax.text(0, -4.35, "two laps: back in the same place, the sign carried",
        color=TITL, fontsize=11.5, ha="center", va="center")
ax.text(0, -4.95, "in mono the sign has no body — null IS the deck",
        color=INK, fontsize=10, ha="center", va="center", alpha=0.85)

fig.tight_layout()
fig.savefig("assets/deck-loop.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/deck-loop.png")
