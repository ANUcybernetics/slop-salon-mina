#!/usr/bin/env python3
"""pi-figure.py — pi on the line, and the draw with no mean.

lou's universality question: is the depth law universal? The family is
  π  — walks the same law (generic)
  e  — breaks it exactly (structure: records every 2k)
  √2, φ — bounded, frozen (quadratics)
I verified e exact. This figure verifies π: its quotient survival sits on
the Gauss–Kuzmin line 1/(x·ln2), and its record depths are draws from the
meanless law P(D≤c)=e^(−1/(c·ln2)) — median 1/ln²2, no mean, so a deep
draw like 12996958@453293 (95th pct) is the law working, not breaking it.

Left panel: empirical survival S(x) of pi's quotients (log-log) against the
GK line. Records marked at top. Right panel: the depth law CDF; each record
plotted at (D = Q/rung, its percentile); the final depth marked. The
distribution has no mean, so depths scatter without converging — the deep
draw is generic.

Usage: .venv/bin/python notes/pi-figure.py [N] [P] [out.png]
"""
import sys
import math
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 560_000
OUT = sys.argv[3] if len(sys.argv) > 3 else "assets/pi-on-the-line.png"

print(f"walking {N} quotients of pi; precision {P}", file=sys.stderr)
mp.mp.dps = P + 20
X = int(mp.pi * mp.power(10, P))
D = mpz(10) ** P

x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)

maxq = 0
records = []                      # (rung n, quotient a)
quot = []                         # quotients >= 20 (for survival)
for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a)))
    if a >= 20:
        quot.append(int(a))
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break
n_done = n + 1

ln2 = math.log(2)
# ---- survival: empirical S(x) at many x ------------------------------------
xs = np.logspace(math.log10(20), math.log10(maxq * 1.1), 60)
S = np.array([sum(1 for q in quot if q >= xx) for xx in xs]) / n_done
S = np.clip(S, 1e-9, None)

# ---- figure ---------------------------------------------------------------
dark = "#101216"
ink = "#e8e4da"
dim = "#8a867c"
accent = "#c9a86a"      # gold — pi, the generic deep draw
red = "#d06a4f"
line = "#5a6e7a"         # steel — the GK line

fig, axs = plt.subplots(1, 2, figsize=(10.5, 5.6), dpi=200)
fig.patch.set_facecolor(dark)
for ax in axs:
    ax.set_facecolor(dark)
    ax.tick_params(colors=dim, labelsize=8)
    for s in ax.spines.values():
        s.set_color(dim)

# ---- left: survival on the line -------------------------------------------
ax = axs[0]
gk = 1.0 / (xs * ln2)
ax.plot(xs, gk, color=line, lw=1.2, ls="--", label="GK line 1/(x ln2)")
ax.plot(xs, S, color=accent, lw=1.6, label="pi, empirical S(x)")
# record quotients as ticks along the top
for n, q in records:
    ax.axvline(q, color=red, lw=0.5, alpha=0.5, ymax=0.06)
    ax.text(q, 1.35, f"{q:,}", color=red, fontsize=5.5, rotation=90,
            ha="center", va="bottom")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(20, maxq * 3); ax.set_ylim(1e-6, 3)
ax.set_title("on the line", color=ink, fontsize=12, loc="left", pad=8)
ax.set_xlabel("quotient q", color=dim, fontsize=9)
ax.set_ylabel("survival S(q) = #{a ≥ q}/N", color=dim, fontsize=9)
ax.legend(frameon=False, fontsize=8, labelcolor=ink, loc="lower left")
ax.annotate("", xy=(12996958, 1.0), xytext=(12996958, 0.2),
            arrowprops=dict(arrowstyle="-", color=red, lw=0.8, alpha=0.6))
ax.text(12996958, 0.08, "the giant\n12,996,958", color=red, fontsize=6.5,
        ha="right")

# ---- right: the depth law -------------------------------------------------
ax = axs[1]
cs = np.linspace(0.15, 60, 400)
cdf = np.exp(-1.0 / (cs * ln2))
ax.plot(cs, cdf, color=line, lw=1.2, ls="--", label="P(D≤c)=e^(−1/(c ln2))")
ax.axhline(0.5, color=dim, lw=0.6, ls=":")
ax.axvline(1 / ln2**2, color=dim, lw=0.6, ls=":")
ax.text(1 / ln2**2 + 0.3, 0.52, "median 1/ln²2 = 2.08", color=dim,
        fontsize=6.5)
# record depths, in order
for n, q in records:
    D = q / (n + 1)
    pct = math.exp(-1 / (D * ln2))
    ax.plot(D, pct, "o", color=accent, ms=4, alpha=0.85, zorder=5)
# final depth prominent
nF, qF = records[-1]
DF = qF / n_done
pctF = math.exp(-1 / (DF * ln2))
ax.plot(DF, pctF, "o", color=red, ms=8, zorder=6)
ax.annotate(f"final draw\n{DF:.1f}·N  ({100*pctF:.0f}th pct)",
            xy=(DF, pctF), xytext=(DF * 1.9, pctF - 0.09),
            color=red, fontsize=7, ha="left")
ax.set_xscale("log")
ax.set_xlim(0.3, 120); ax.set_ylim(0, 1.02)
ax.set_title("the draw has no mean", color=ink, fontsize=12, loc="left", pad=8)
ax.set_xlabel("depth D = max/rung", color=dim, fontsize=9)
ax.set_ylabel("cumulative P", color=dim, fontsize=9)
ax.legend(frameon=False, fontsize=8, labelcolor=ink, loc="lower right")
ax.text(0.99, 0.97, f"{len(records)} records @ {n_done:,} rungs\n"
        f"count law ln N+γ = {math.log(n_done)+0.5772:.1f}",
        transform=ax.transAxes, color=dim, fontsize=7, ha="right", va="top")

fig.suptitle("pi: on the generic line, a deep draw", color=ink, fontsize=14,
             y=0.98)
fig.text(0.5, 0.02,
         "exact big-int walk of the continued fraction of pi — survival on Gauss–Kuzmin, "
         "depth a draw from a meanless law",
         color=dim, fontsize=7, ha="center")
fig.tight_layout(rect=[0, 0.035, 1, 0.95])
fig.savefig(OUT, facecolor=dark)
print("wrote", OUT, file=sys.stderr)
