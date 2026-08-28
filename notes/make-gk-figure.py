#!/usr/bin/env python3
"""make-gk-figure.py — the source, verified.

Two-panel figure:
  Left:  empirical survival S(x) = #{q>=x}/N of log2(3/2)'s quotients
         (exact big-int walk to N=1M rungs) against the Gauss-Kuzmin line
         1/(x·ln2). The records are red points — the deepest sits where the
         empirical tail crosses 1/N. Top-tail scatter is Poisson noise.
  Right: the depth law as the running max of that same tail: D = M_N/N at
         fixed rungs against P(D<=c)=e^(-1/(c·ln2)), median 1/(ln2)^2=2.081.
         Current hold 1138268@1M: D=1.138, the 28th pct (gert's "1.14·N").

Output: assets/gk-source.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gmpy2 import mpz
import mpmath as mp

N = 1_000_000
P = 1_100_000
ln2 = math.log(2)

# ---- exact walk, keep every quotient (small list of python ints) ----------
mp.mp.dps = P + 20
alpha = mp.log(3) / mp.log(2) - 1
X = int((alpha * mp.power(10, P)))
D = mpz(10) ** P
x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)

maxq = 0
records = []                       # (rung, quotient)
qs = np.empty(N, dtype=np.int64)   # quotients; a few exceed int64? max ~1.1e6 < 2^63
for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a)))
    qs[n] = int(a)
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break
N = n + 1
qs = qs[:N]
rungs = np.array([r for r, _ in records], dtype=float)
recq = np.array([q for _, q in records], dtype=float)
print(f"{N} rungs; {len(records)} records; max {maxq}")

# ---- survival at a dense log grid + at the records ------------------------
xs = np.unique(np.geomspace(1, maxq * 1.1, 400).astype(np.int64))
# empirical S(x) via sorted quotients
sorted_q = np.sort(qs)
emp = np.empty_like(xs, dtype=float)
for i, xv in enumerate(xs):
    emp[i] = (sorted_q >= xv).sum() / N
gk = 1.0 / (xs * ln2)

# empirical S at the record quotients (the records are the big-upper tail)
emp_rec = np.array([(sorted_q >= q).sum() / N for q in recq])

# ---- right panel: depth law at fixed rungs --------------------------------
test_rungs = np.array([1e2, 1e3, 1e4, 3e4, 1e5, 3e5, 7e5, 1e6])
M_at = np.array([recq[rungs <= r].max() if (rungs <= r).any() else 1
                 for r in test_rungs], dtype=float)
c_at = M_at / test_rungs
p_at = np.exp(-1.0 / (c_at * ln2))

c_grid = np.geomspace(0.3, 10, 300)
p_curve = np.exp(-1.0 / (c_grid * ln2))

# ---- figure ----------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "#14100f", "axes.facecolor": "#14100f",
    "savefig.facecolor": "#14100f", "text.color": "#e8dcc8",
    "axes.edgecolor": "#5a4f45", "axes.labelcolor": "#e8dcc8",
    "xtick.color": "#9a8b78", "ytick.color": "#9a8b78",
    "font.family": "serif", "font.size": 11,
})
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), gridspec_kw={"wspace": 0.33})

# ---- left: the source ------------------------------------------------------
ax = axes[0]
ax.loglog(xs, gk, ls="--", c="#b8a88a", lw=1.4, label=r"Gauss–Kuzmin  $1/(x\ln 2)$")
ax.loglog(xs, emp, c="#7fc0a9", lw=1.8, alpha=0.95, label="quotients of log$_2$(3/2)")
ax.axhline(1 / N, c="#c96f5a", ls=":", lw=1.1)
ax.text(1.05e6, 1.05 / N, "1/N", c="#c96f5a", fontsize=9, va="bottom", ha="right")
# records as red points on the empirical tail
ax.plot(recq, emp_rec, "o", ms=5, mfc="none", mec="#d0533f", mew=1.6,
        label="the records")
# deepest record
ax.annotate(f"{int(recq[-1])}", xy=(recq[-1], emp_rec[-1]),
            xytext=(recq[-1] * 0.62, emp_rec[-1] * 3.2),
            c="#d0533f", fontsize=10,
            arrowprops=dict(arrowstyle="-", color="#d0533f", lw=0.8))
ax.set_xlabel("quotient  $x$")
ax.set_ylabel("survival  S(x) = #{q_n ≥ x} / N")
ax.set_title("the source", fontsize=13, pad=10)
ax.set_xlim(1, maxq * 2)
ax.set_ylim(1e-6 * 0.5, 1.4)
ax.legend(loc="lower left", fontsize=8.5, frameon=False)

# ---- right: the depth law --------------------------------------------------
ax = axes[1]
ax.plot(c_grid, p_curve, c="#b8a88a", lw=1.4, ls="--",
        label=r"$P(D \leq c)=e^{-1/(c\ln 2)}$")
ax.plot(c_at, p_at, "o", ms=6, mfc="none", mec="#7fc0a9", mew=1.6,
        label="fixed rungs (exact walk)")
ax.axvline(1 / ln2 ** 2, c="#c96f5a", ls=":", lw=1.1)
ax.text(1 / ln2 ** 2, 0.10, r"median $1/(\ln 2)^2$", c="#c96f5a", fontsize=9,
        ha="right", rotation=90)
# current hold
cnow, pnow = c_at[-1], p_at[-1]
ax.plot([cnow], [pnow], "D", ms=7, mfc="#d0533f", mec="none")
ax.annotate(f"1138268 @1M\nD={cnow:.3f}, {100*pnow:.0f}th pct",
            xy=(cnow, pnow), xytext=(cnow * 0.32, pnow + 0.06),
            c="#d0533f", fontsize=9.5, ha="left",
            arrowprops=dict(arrowstyle="-", color="#d0533f", lw=0.8))
ax.set_xscale("log")
ax.set_xlabel("depth  $D = M_N/N$")
ax.set_ylabel(r"$P(D \leq c)$")
ax.set_title("the depth, from the tail", fontsize=13, pad=10)
ax.set_xlim(0.3, 10)
ax.set_ylim(0, 1.05)
ax.legend(loc="lower right", fontsize=8.5, frameon=False)

fig.savefig("assets/gk-source.png", dpi=200, bbox_inches="tight")
print("wrote assets/gk-source.png")
