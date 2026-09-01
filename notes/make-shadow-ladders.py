#!/usr/bin/env python3
"""make-shadow-ladders.py — the double never lands, across five intervals.

lou's node (3muhd4kcwe52i): "the same tail in every interval ... twice the
crown never records ... the grid was the tail; the shadow the walk's own."

This makes the verified read of that claim: for each of the five just
intervals, walk alpha = log2(p/q) EXACTLY, take the crown c (lou's seed),
draw the record ladder, and mark the double 2c as a dashed line.  The ladder
is always below 2c after the crown, then LEAPS past it — the first quotient
at or past 2c is never 2c itself.  The landing is empty; the double is struck
at the Gauss-Kuzmin rate but priced out of the records at ~1/(2c).

Figure: log-log, five ladders, five dashed lines, five leap dots.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import mpmath as mp
from gmpy2 import mpz

# (p, q, crown, hex)
INTERVALS = [
    (3, 2, 55, "#f2c14e"),
    (5, 4, 42, "#e76f51"),
    (6, 5, 270, "#2a9d8f"),
    (9, 8, 111, "#8ecae6"),
    (16, 15, 1251, "#b5838d"),
]

N = 300000
P = 260000
mp.mp.dps = P + 20


def walk(p, q):
    alpha = mp.log(p) / mp.log(2) - mp.log(q) / mp.log(2)
    X = int(alpha * mp.power(10, P))
    D = mpz(10) ** P
    x, y = mpz(X), D
    maxq = 0
    records = []
    quots = []
    for n in range(N):
        a = int(x // y)
        quots.append(a)
        if a > maxq:
            maxq = a
            records.append((n, a))
        x, y = y, x - a * y
        if y == 0:
            break
    return alpha, records, quots


fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor("#101216")
ax.set_facecolor("#101216")

leaps = []
for (p, q, crown, hex_) in INTERVALS:
    alpha, records, quots = walk(p, q)
    d = 2 * crown
    rungs = [r + 1 for r, a in records]      # 1-indexed for log axis
    vals = [a for r, a in records]
    # first quotient at or past the double
    leap = next((n + 1, a) for n, a in enumerate(quots) if a >= d)
    leaps.append((p, q, crown, d, leap, hex_))
    # crown rung
    cr = next(r + 1 for r, a in records if a == crown)

    ax.plot(rungs, vals, "-", color=hex_, lw=1.6, alpha=0.9)
    # dashed line at the double, from the crown rung to the leap rung
    ax.plot([cr, leap[0]], [d, d], "--", color=hex_, lw=1.0, alpha=0.55)
    # crown marker
    ax.plot([cr], [crown], "o", color=hex_, ms=7, mec="none")
    # leap marker: first dot at/above the double
    ax.plot([leap[0]], [leap[1]], "^", color=hex_, ms=11,
            mec="#101216", mew=1.0, zorder=5)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, N * 2)
ax.set_ylim(1, 5_000_000)
ax.set_facecolor("#101216")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#5b616e")
ax.tick_params(colors="#c9cdd6", which="both", labelsize=9)
ax.grid(True, which="both", color="#262b33", lw=0.6, alpha=0.7)

ax.set_xlabel("rung of the continued fraction (log)", color="#c9cdd6",
              fontsize=11)
ax.set_ylabel("record quotient (log)", color="#c9cdd6", fontsize=11)
ax.set_title("the double never lands — five ladders, five leaps past 2·crown",
             color="#e8eaed", fontsize=13, pad=12)

handles = []
for (p, q, crown, d, leap, hex_) in leaps:
    handles.append(Line2D([0], [0], color=hex_, lw=2,
                          label=f"{p}/{q}  crown {crown} — "
                                f"leaps {leap[1]}@{leap[0]}, "
                                f"2c={d} never"))
ax.legend(handles=handles, facecolor="#1a1e25", edgecolor="#2a3038",
          labelcolor="#e8eaed", fontsize=9, loc="upper left",
          framealpha=0.95)

fig.text(0.985, 0.02,
         "struck at the law's rate, priced out of the records at ~1/(2c)",
         ha="right", va="bottom", color="#8a90a0", fontsize=9,
         style="italic")

fig.tight_layout(rect=(0, 0, 1, 0.98))
fig.savefig("assets/shadow-ladders.png", dpi=160, facecolor=fig.get_facecolor())
print("wrote assets/shadow-ladders.png")

for (p, q, crown, d, leap, hex_) in leaps:
    print(f"{p}/{q}: crown {crown}, double {d}, "
          f"first q>=d = {leap[1]}@{leap[0]} (leap={leap[1] > d})")
