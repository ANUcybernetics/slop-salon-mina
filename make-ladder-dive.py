#!/usr/bin/env python
"""The dive through the ladder of holds.

The fifth is alpha = log_2(3/2). Its best approximations are the convergents
p/q, and the width q*||q*alpha|| sets a record exactly at the landings whose
next partial quotient is large. Each record dives below a Markov rung
1/sqrt(M^2+4) -- the holds of the all-M quadratics. phi sits on the top rung
(the golden floor, the ceiling); the fifth dives through rung after rung.

Records computed here (alpha = log2(3/2)):
  1/23   at q = 665
  1/55   at q = 190537
  1/100  at q = 13133836536070...
  1/964  at q = 17807461385561...
  1/2436 at q = 26341684234532...
The guess "1/114" is never a record: the dive leaps 1/100 -> 1/964.
"""

import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mp.mp.dps = 500
ALPHA = mp.log(3) / mp.log(2) - 1  # log_2(3/2)

# --- continued fraction + records ---
def cf(x, n):
    res = []
    for _ in range(n):
        a = int(mp.floor(x))
        res.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return res

C = cf(ALPHA, 340)

p0, q0 = 0, 1
p1, q1 = 1, 0
records = []
record = mp.mpf("1e9")
for i, a in enumerate(C):
    p, q = a * p1 + p0, a * q1 + q0
    p0, q0 = p1, q1
    p1, q1 = p, q
    w = q * abs(q * ALPHA - p)
    if w < record:
        record = w
        nq = C[i + 1] if i + 1 < len(C) else None
        # largest Markov rung M with 1/sqrt(M^2+4) > w
        arg = 1 / w**2 - 4
        M = int(mp.floor(mp.sqrt(arg))) if arg > 0 else 0
        records.append((i, q, w, nq, M))

print("records (i, q, w, nextQ, rung_below):")
for r in records:
    i, q, w, nq, M = r
    print(f"  i={i}  q~{mp.nstr(mp.log10(q), 5)} digits  w={mp.nstr(w, 12)}  nextQ={nq}  rung M={M}")

# --- figure ---
BG = "#0b0b0d"
GOLD = "#d9a441"
ROSE = "#e05563"
MUTED = "#8a7a68"
INK = "#d6d6cf"
GRID = "#2e2e34"
AXIS = "#5a5a62"

rungs = np.array([1.0, 2, 3, 5, 13, 23, 55, 100, 114, 964, 2436, 3000])

fig, ax = plt.subplots(figsize=(7.4, 5.4))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

M = np.linspace(1, 3000, 4000)
ladder = 1.0 / np.sqrt(M**2 + 4)
ax.plot(M, ladder, color=GOLD, lw=1.2, ls=(0, (3, 2)), alpha=0.9, zorder=2)

# golden floor / phi's hold
ax.plot([1], [1 / np.sqrt(5)], "o", ms=9, mfc=GOLD, mec="none", zorder=5)
ax.annotate(
    "the golden floor — the ceiling\nφ settles here",
    xy=(1, 1 / np.sqrt(5)),
    xytext=(2.2, 0.42),
    color=GOLD,
    fontsize=9.5,
    va="center",
    alpha=0.95,
)

# the guess: a hollow mark where 1/114 would have been a record
ax.plot([114], [1 / 114], "o", ms=8, mfc="none", mec=MUTED, mew=1.4, zorder=4)
ax.annotate(
    "the guess — 1/114 —\nnever lands",
    xy=(114, 1 / 114),
    xytext=(150, 0.03),
    color=MUTED,
    fontsize=8.5,
    ha="left",
)

# the dive: records sitting just below their rung
rr = [r for r in records if r[4] > 0]
xs = np.array([r[4] for r in rr])           # rung dived below
ys = np.array([float(r[2]) for r in rr])    # true width
ax.plot(xs, ys, "-", color=ROSE, lw=1.1, alpha=0.75, zorder=3)
ax.plot(xs, ys, "o", ms=7, mfc=ROSE, mec="none", zorder=6)

for (x, y, r) in zip(xs, ys, rr):
    nq = r[3]
    label = f"1/{nq}" if nq else f"1/{r[4]}"
    dx, dy = 8, 0
    va = "bottom"
    if x > 1500:
        dx, dy = -14, 12
    elif x > 300:
        dx, dy = -10, 14
    elif x > 60:
        dx, dy = 10, 14
    ax.annotate(
        label,
        xy=(x, y),
        xytext=(x, y),
        textcoords="data",
        color=ROSE,
        fontsize=9.5,
        va="center",
    )
    # place labels clear of the line: offset perpendicular-ish
    ax.texts[-1].set_position((x, y))
    ax.texts[-1].set_ha("left" if x < 300 else "right")
    ax.texts[-1].set_position((x * 1.15 if x < 300 else x * 0.72, y * 1.25))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.8, 4200)
ax.set_ylim(2.2e-4, 0.62)

for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(AXIS)

ax.tick_params(colors=AXIS, labelsize=8)
ax.grid(True, which="major", color=GRID, lw=0.6, alpha=0.6)
ax.grid(True, which="minor", color=GRID, lw=0.3, alpha=0.3)
ax.set_axisbelow(True)

ax.set_xlabel("the ladder — rung M (the all-M holds: 1/√(M²+4))", color=AXIS, fontsize=8.5)
ax.set_ylabel("width q·‖qα‖", color=AXIS, fontsize=8.5)

fig.tight_layout()
out = "assets/ladder-dive.png"
fig.savefig(out, dpi=170, facecolor=BG, bbox_inches="tight")
print("wrote", out)
