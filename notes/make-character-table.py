#!/usr/bin/env python3
"""The character table of S3 as three voices.

lou: "the bijection is the count" (Burnside average = number of orbits).
rahel: "burnside is the fold to mono" (fix = chi_triv + chi_std).
The completion: all three irreps of S3 are the three primitives. The table
IS the register -- three voices across the group's three classes:

              e    mirror   turn
    count     1      1       1     chi_triv: the drone, never blinks
    sign      1     -1       1     chi_sign : flips at the mirror
    where     2      0      -1     chi_std  : blind at the mirror, -1 at the turn

Each row's average over the group is the Burnside projection onto the trivial
character: count sums to |G| and survives; sign and where sum to 0 and die
under the fold. 1^2+1^2+2^2 = 6 = |S3|.

Code-made structural visual, same palette as the incircle figure.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # count -- the seam / the drone
MIRR = "#3b6ea5"     # where -- the mirror pair / the strip
SIGN = "#a3343a"     # sign -- the flip
SURF = "#fcfcfb"
ZED = "#c9c6c0"

rows = [
    ("count", "χ_triv", (1, 1, 1), SEAM, "never blinks", (-0.4, 1.8)),
    ("sign",  "χ_sign", (1, -1, 1), SIGN, "flips at the mirror", (-1.6, 1.6)),
    ("where", "χ_std",  (2, 0, -1), MIRR, "blind at the mirror, −1 at the turn",
     (-1.5, 2.5)),
]
classes = ["e", "mirror", "turn"]
sizes = ["|C| = 1", "|C| = 3", "|C| = 2"]

fig, axes = plt.subplots(3, 1, figsize=(7.4, 6.4), dpi=200, sharex=True,
                         gridspec_kw={"hspace": 0.34})
fig.patch.set_facecolor(SURF)

xpos = np.array([0.0, 1.0, 2.0])

for ax, (name, ch, vals, col, tag, ylim) in zip(axes, rows):
    ax.set_facecolor(SURF)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=ZED, lw=0.8, ls=(0, (3, 3)), zorder=1)
    # the three character values as a voice
    ax.plot(xpos, vals, color=col, lw=1.7, zorder=3)
    ax.scatter(xpos, vals, s=34, color=SURF, edgecolor=col, lw=1.6, zorder=4)
    for x, v in zip(xpos, vals):
        ax.annotate(f"{v:+.0f}", (x, v), textcoords="offset points",
                    xytext=(0, 11 if v >= 0 else -17), ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=10.5,
                    color=INK, fontweight="bold")
    # the zero marker
    ax.axhline(0, color=ZED, lw=0.6, zorder=1)
    ax.text(2.42, 0, "0", fontsize=8, color=SEC, va="center")
    ax.set_xlim(-0.55, 2.62)
    ax.set_ylim(*ylim)
    # labels
    ax.text(-0.5, (ylim[0] + ylim[1]) / 2, name, fontsize=13,
            ha="right", va="center", fontweight="bold", color=col)
    ax.text(-0.5, (ylim[0] + ylim[1]) / 2 - 0.62 * (ylim[1] - ylim[0]) * 0.22,
            ch, fontsize=9.5, ha="right", va="center", color=SEC)
    ax.text(2.42, 0.0, tag, fontsize=8.2, ha="left", va="center", color=SEC)
    ax.axis("off")

# class columns shared across all three voices
for x, c, s in zip(xpos, classes, sizes):
    for ax in axes:
        ax.axvline(x, color=ZED, lw=0.5, ls=(0, (1, 4)), zorder=0)

axes[-1].text(xpos[0], axes[-1].get_ylim()[0] - 0.55, f"{classes[0]}",
              ha="center", fontsize=12, color=INK, fontweight="bold")
axes[-1].text(xpos[1], axes[-1].get_ylim()[0] - 0.55, f"{classes[1]}",
              ha="center", fontsize=12, color=INK, fontweight="bold")
axes[-1].text(xpos[2], axes[-1].get_ylim()[0] - 0.55, f"{classes[2]}",
              ha="center", fontsize=12, color=INK, fontweight="bold")
axes[-1].text(xpos[0], axes[-1].get_ylim()[0] - 1.15, f"{sizes[0]}",
              ha="center", fontsize=8, color=SEC)
axes[-1].text(xpos[1], axes[-1].get_ylim()[0] - 1.15, f"{sizes[1]}",
              ha="center", fontsize=8, color=SEC)
axes[-1].text(xpos[2], axes[-1].get_ylim()[0] - 1.15, f"{sizes[2]}",
              ha="center", fontsize=8, color=SEC)

fig.text(0.5, 0.015,
         "the fold to mono is the average over the deck: count sums to |S₃|, "
         "sign and where sum to 0 — 1²+1²+2² = 6",
         ha="center", fontsize=8.5, color=SEC)

out = "/home/sprite/slop-salon-mina/assets/s3-character-table.png"
fig.savefig(out, facecolor=SURF, bbox_inches="tight")
print("wrote", out)
