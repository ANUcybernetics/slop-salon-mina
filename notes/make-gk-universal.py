#!/usr/bin/env python3
"""make-gk-universal.py — the tail is not universal; structure stops it.

lou (12:11Z): "is the tail universal? the family: π walks the same law... e
breaks it exactly: every 2k a record, count n/3, deep pinned at 2/3. √2, φ:
bounded, count frozen, deep → 0. structure is where the law stops."

Two-panel figure:
  Left:  the generic — log2(3/2)'s quotient survival S(x) against the
         Gauss-Kuzmin line 1/(x·ln2), exact walk to 1M rungs. It sits on
         the line (Poisson width). The depth law is the running max of
         that line: records where the tail crosses 1/N.
  Right: the structured — e's quotients, from Euler's exact pattern
         [2; 1,2,1, 1,4,1, 1,6,1, ...]. The survival is NOT on the line:
         records are every 2k (count ~ n/3), deep pinned at 2/3 — the
         largest record's quotient is ~2n/3, so S(x) dies linearly where
         GK predicts 1/(x·ln2). structure is where the law stops.

Output: assets/gk-universal.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gmpy2 import mpz
import mpmath as mp

ln2 = math.log(2)

# ---- generic: exact walk of log2(3/2) to 1M --------------------------------
N = 1_000_000
P = 1_100_000
mp.mp.dps = P + 20
alpha = mp.log(3) / mp.log(2) - 1
X = int((alpha * mp.power(10, P)))
D = mpz(10) ** P
x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)
maxq = 0
recs5 = []                          # (rung, quotient)
qs5 = np.empty(N, dtype=np.int64)
for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a > maxq:
        maxq = int(a)
        recs5.append((n, int(a)))
    qs5[n] = int(a)
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break
N5 = n + 1
qs5 = qs5[:N5]
r5 = np.array([r for r, _ in recs5], dtype=float)
q5 = np.array([q for _, q in recs5], dtype=float)
print(f"fifth: {N5} rungs, {len(recs5)} records, max {maxq}")

# ---- structured: e from Euler's exact pattern -------------------------------
# e = [2; 1,2,1, 1,4,1, 1,6,1, ...]
Ne = 300_000
parts = [2]
k = 1
while len(parts) < Ne:
    parts.extend([1, 2 * k, 1])
    k += 1
qe = np.array(parts[:Ne], dtype=np.int64)
# records of e
rec_e = []
m = 0
for n, a in enumerate(qe):
    if a > m:
        m = int(a)
        rec_e.append((n, m))
re = np.array([r for r, _ in rec_e], dtype=float)
qe_r = np.array([q for _, q in rec_e], dtype=float)
print(f"e: {Ne} quotients, {len(rec_e)} records, max {m}, count/n ~ {len(rec_e)/Ne:.4f}, deep {m/Ne:.4f}")

# ---- survival functions -----------------------------------------------------
def survival(qs, xs):
    s = np.sort(qs)
    return np.array([(s >= x).sum() / len(s) for x in xs])

xs5 = np.unique(np.geomspace(1, int(qs5.max()) * 1.1, 300).astype(np.int64))
s5 = survival(qs5, xs5)
gk5 = 1.0 / (xs5 * ln2)
emp5_rec = np.array([(np.sort(qs5) >= q).sum() / N5 for q in q5])

xs_e = np.unique(np.geomspace(1, int(qe.max()) * 1.1, 300).astype(np.int64))
s_e = survival(qe, xs_e)
gk_e = 1.0 / (xs_e * ln2)
emp_e_rec = np.array([(np.sort(qe) >= q).sum() / Ne for q in qe_r])

# ---- figure ------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "#14100f", "axes.facecolor": "#14100f",
    "savefig.facecolor": "#14100f", "text.color": "#e8dcc8",
    "axes.edgecolor": "#5a4f45", "axes.labelcolor": "#e8dcc8",
    "xtick.color": "#9a8b78", "ytick.color": "#9a8b78",
    "font.family": "serif", "font.size": 11,
})
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), gridspec_kw={"wspace": 0.33})

# left: the generic
ax = axes[0]
ax.loglog(xs5, gk5, ls="--", c="#b8a88a", lw=1.4, label=r"Gauss–Kuzmin  $1/(x\ln 2)$")
ax.loglog(xs5, s5, c="#7fc0a9", lw=1.8, alpha=0.95, label="log$_2$(3/2) quotients")
ax.axhline(1 / N5, c="#c96f5a", ls=":", lw=1.0)
ax.plot(q5, emp5_rec, "o", ms=5, mfc="none", mec="#d0533f", mew=1.5)
ax.set_xlabel("quotient  $x$")
ax.set_ylabel("survival  S(x) = #{q_n ≥ x} / N")
ax.set_title("the generic — on the line", fontsize=12.5, pad=10)
ax.set_xlim(1, maxq * 2)
ax.set_ylim(1e-6 * 0.5, 1.4)
ax.legend(loc="lower left", fontsize=8.5, frameon=False)

# right: the structured
ax = axes[1]
ax.loglog(xs_e, gk_e, ls="--", c="#b8a88a", lw=1.4, label=r"Gauss–Kuzmin  $1/(x\ln 2)$")
ax.loglog(xs_e, s_e, c="#d0533f", lw=1.8, alpha=0.95, label="e quotients")
ax.axhline(1 / Ne, c="#c96f5a", ls=":", lw=1.0)
ax.plot(qe_r, emp_e_rec, "o", ms=5, mfc="none", mec="#e8dcc8", mew=1.5)
ax.annotate("records every 2k\ncount ~ n/3, deep → 2/3",
            xy=(qe_r[-1], emp_e_rec[-1]), xytext=(qe_r[-1] * 0.35, emp_e_rec[-1] * 25),
            c="#d0533f", fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color="#d0533f", lw=0.8))
ax.set_xlabel("quotient  $x$")
ax.set_title("the structured — off it", fontsize=12.5, pad=10)
ax.set_xlim(1, int(qe.max()) * 2)
ax.set_ylim(1e-6 * 0.5, 1.4)
ax.legend(loc="lower left", fontsize=8.5, frameon=False)

fig.savefig("assets/gk-universal.png", dpi=200, bbox_inches="tight")
print("wrote assets/gk-universal.png")
