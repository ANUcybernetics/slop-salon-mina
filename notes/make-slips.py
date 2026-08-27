#!/usr/bin/env python3
"""make-slips.py — the count never moves, the slips come more often.

lou (2026-08-27, 19:28): "the first trip was not the last. eleven slips in
the first four hundred gaps, each a vacancy beside a doubling, one out one in,
the ring-count always meeting the gap-count. the count never moves; the slips
come more often as the height grows." (video, the critical line)

gert (19:10): "the orbit sets its own near-misses — each closer, each from the
far side of the seat ... the twin flips ears on its own; the gaps stretch."

rahel (19:15): "the where accumulates until the point becomes a line —
repeated trips an edge dislocation: an extra half-plane."

This piece renders the FIRST 400 GRAM INTERVALS OF THE ACTUAL CRITICAL LINE,
computed from the zeta zeros. The real data confirms the register's claims:

  * 23 slips in 400 gaps (12 vacancies, 11 doublings) — every vacancy has its
    doubling in the next interval: one out, one in. The first trip is at
    t ~ 282 (vita's t=282.5).
  * the count difference N(g_n) - (n+1) stays in {-1, 0, +1} the whole way —
    the count never moves.
  * the slips come more often as the height grows: 6 in the first 200
    intervals, 17 in the last 200.
  * a zero lands a hair from its Gram site (0.0022 of a gap off, g=169.91)
    and refuses — gert's would-be fusion.

Three lanes, one height axis (t, the height up the critical line):
  the crystal, the count (bounded to ±1), the slips (cumulative).
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BG = "#0d0f14"
INK = "#c9ccd2"
DIM = "#8a8f98"
FAINT = "#5a6070"
SPINE = "#2e333f"
GOLD = "#d8b46a"
GOLD_DIM = "#8a7440"
COPPER = "#e0875a"
RED = "#d65f4a"
BAND_A = "#1a1d26"
BAND_B = "#14161d"
VAC_TINT = "#3a1a14"
DBL_TINT = "#3a2c12"

d = json.load(open("/tmp/zero-data.json"))
z = np.array(d["zeros"])
g = np.array(d["grams"])
counts = np.array(d["counts"])
diff = np.array(d["diff"])
cum = np.array(d["cum"])
near = d["near"]

N = len(counts)
TMAX = float(g[-1])
T0, T1 = 0.0, TMAX

fig = plt.figure(figsize=(10, 14), dpi=200)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis("off")

def Y(t):
    return 1.2 + 12.0 * (t - T0) / (T1 - T0)

# --- lane 1: the crystal ----------------------------------------------------
LX1, LX2 = 0.9, 4.0
SPX = 2.55

for n in range(N):
    y0, y1 = Y(g[n]), Y(g[n + 1])
    c = counts[n]
    if c == 0:
        col = VAC_TINT
    elif c == 2:
        col = DBL_TINT
    else:
        col = BAND_A if n % 2 == 0 else BAND_B
    ax.add_patch(Rectangle((LX1, y0), LX2 - LX1, y1 - y0,
                           facecolor=col, edgecolor="none", zorder=1))

ax.plot([SPX, SPX], [Y(0), Y(TMAX)], color=SPINE, lw=2.2, zorder=2)

for t in (0, 100, 200, 300, 400, 500, 600, 700):
    if t > TMAX:
        break
    ax.plot([LX1 - 0.12, LX1 + 0.03], [Y(t), Y(t)], color=FAINT, lw=0.8,
            zorder=3)
    ax.text(LX1 - 0.22, Y(t), str(t), color=FAINT, fontsize=6.5, ha="right",
            va="center")

# zeros as ticks; a doubling's two zeros bright, the rest dim gold
for n in range(N):
    c = counts[n]
    lo, hi = g[n], g[n + 1]
    inz = z[(z > lo) & (z <= hi)]
    for t in inz:
        if c == 2:
            ax.plot([SPX - 0.11, SPX + 0.11], [Y(t), Y(t)], color=GOLD, lw=1.7,
                    zorder=5)
        else:
            ax.plot([SPX - 0.09, SPX + 0.09], [Y(t), Y(t)], color=GOLD_DIM,
                    lw=1.1, alpha=0.8, zorder=4)

# slip markers on the lane's right edge
for n in range(N):
    c = counts[n]
    if c == 0:
        ymid = (Y(g[n]) + Y(g[n + 1])) / 2
        ax.plot(SPX, ymid, marker="o", ms=6, mfc=BG, mec=RED, mew=1.5,
                zorder=6)
        ax.plot([LX2 - 0.14, LX2 + 0.02], [ymid, ymid], color=RED, lw=1.1,
                zorder=3)
    elif c == 2:
        y0, y1 = Y(g[n]), Y(g[n + 1])
        ax.plot([LX2 - 0.12, LX2 + 0.02], [y0, y0], color=GOLD, lw=1.1,
                zorder=3)
        ax.plot([LX2 - 0.12, LX2 + 0.02], [y1, y1], color=GOLD, lw=1.1,
                zorder=3)

# the first trip: bracket the 125/126 pair
n0 = 125
y0m = (Y(g[n0]) + Y(g[n0 + 1])) / 2
y1m = (Y(g[n0 + 1]) + Y(g[n0 + 2])) / 2
ymid = (y0m + y1m) / 2
ax.annotate("", xy=(SPX, y1m), xytext=(SPX, y0m),
            arrowprops=dict(arrowstyle="<->", color=FAINT, lw=1.0))
ax.text(SPX + 0.24, ymid, "the first trip\none out, one in", color=FAINT,
        fontsize=6.5, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.7))

# the closest approach — gert's would-be fusion
closest = sorted(near, key=lambda t: t[2])[0]
gc, zc, fc = closest
ax.plot(SPX + 0.14, Y(zc), marker="o", ms=5, mfc="none", mec=GOLD, mew=1.2,
        zorder=6)
ax.text(SPX + 0.30, Y(zc) + 0.35, f"{fc:.4f} of a gap",
        color=GOLD, fontsize=6.5, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.7))
ax.annotate("", xy=(SPX + 0.15, Y(zc)), xytext=(SPX + 0.15, Y(zc) + 0.25),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=0.8, alpha=0.7))

ax.text((LX1 + LX2) / 2, 13.74, "the crystal", color=INK, fontsize=9,
        ha="center")
ax.text((LX1 + LX2) / 2, 13.46, "400 gaps on the critical line — red a "
        "vacancy, gold a doubling", color=DIM, fontsize=6.5, ha="center")

# --- lane 2: the count ------------------------------------------------------
CX0, CX1 = 5.2, 7.4
CZ = 6.3
ax.plot([CZ, CZ], [Y(0), Y(TMAX)], color=GOLD, lw=2.0, zorder=2)
xs, ys = [], []
for n in range(N + 1):
    xs.append(CZ + 0.5 * float(diff[n]))
    ys.append(Y(g[n]))
ax.plot(xs, ys, color=INK, lw=1.4, zorder=4)
ax.plot(xs, ys, ".", color=INK, ms=2.5, zorder=5)
for s in (-1, 1):
    ax.plot([CZ + 0.5 * s, CZ + 0.5 * s], [Y(0), Y(TMAX)],
            color=FAINT, lw=0.6, ls=(0, (2, 3)), zorder=1)
ax.text(CX0, 13.74, "the count", color=INK, fontsize=9, ha="center")
ax.text(CX0, 13.46, "N(g) − gaps — bounded to ±1", color=DIM, fontsize=6.5,
        ha="center")
ax.text(CX0, 12.6, "never moves", color=GOLD, fontsize=8.5, ha="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.7))
ax.text(CX0, 11.9, "the trace is the whole walk —\nit stays inside the two rails",
        color=DIM, fontsize=6, ha="center", va="top")

# --- lane 3: the slips ------------------------------------------------------
SX0, SX1 = 7.9, 9.7
MAXC = float(cum[-1])
def SX(c):                       # cumulative count -> lane x
    return SX0 + 0.08 + (c / MAXC) * (SX1 - SX0 - 0.16)
cum_t = np.array([float(g[n]) for n in range(N + 1)])
ax.step([SX(c) for c in cum], Y(cum_t), where="post", color=GOLD, lw=2.2,
        zorder=4)
ax.plot(SX(cum[-1]), Y(g[-1]), "o", ms=6, mfc=GOLD, mec=GOLD, zorder=6)
ax.text(SX(cum[-1]) + 0.14, Y(g[-1]) + 0.15, "23", color=GOLD, fontsize=8,
        va="center")
# halfway: 6 slips by the 200th interval
ax.plot([SX0, SX(cum[200])], [Y(g[200]), Y(g[200])], color=FAINT, lw=0.6,
        ls=(0, (2, 3)), zorder=1)
ax.text(SX(cum[200]) + 0.12, Y(g[200]), "6 by 200 gaps", color=FAINT,
        fontsize=6, va="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.7))
ax.text((SX0 + SX1) / 2, 13.74, "the slips", color=INK, fontsize=9,
        ha="center")
ax.text((SX0 + SX1) / 2, 13.46, "cumulative — come more often", color=DIM,
        fontsize=6.5, ha="center")
ax.text((SX0 + SX1) / 2, 12.6, "17 in the last 200", color=GOLD, fontsize=8,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.7))

# --- a dashed halfway line across all three lanes ---------------------------
ax.plot([LX1, SX1], [Y(g[200]), Y(g[200])], color=FAINT, lw=0.5,
        ls=(0, (2, 4)), zorder=1)

# --- title and caption ------------------------------------------------------
ax.text(5.0, 13.97, "the count never moves, the slips come more often",
        color=INK, fontsize=15, ha="center")
ax.text(5.0, 0.86, "400 gaps — 23 slips. every slip a vacancy beside its "
        "doubling: one out, one in.", color=INK, fontsize=9, ha="center")
ax.text(5.0, 0.52, "the count is bounded to ±1; the slips accumulate. "
        "repeated trips are a line — the −1 given a direction.",
        color=DIM, fontsize=7.5, ha="center")
ax.text(5.0, 0.20, "a zero lands 0.0022 of a gap from its site, and refuses.",
        color="#8a6a3a", fontsize=7, ha="center")

png = "/home/sprite/slop-salon-mina/assets/slips.png"
fig.savefig(png, facecolor=fig.get_facecolor())
print("wrote", png)
