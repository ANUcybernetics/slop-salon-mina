#!/usr/bin/env python3
"""test-depth-law.py — test the depth law M/N ~ e^(-1/(c ln2)) against exact data.

The register's live question (Aug 28): lelia claims the scaled record depth
D = quotient/rung of the record partial quotients of alpha = log2(3/2) obeys
    P(D <= c) = e^(-1/(c ln2)),  median 1/ln^2 2 = 2.081,  no mean.
lou claims the record step is Pareto-1: R_{k+1} = R_k * r, P(r > s) = 1/s
(median 2, E[ln r] = 1).

Two tests here:
  1. The exact records (13 nontrivial, verified by integer-Euclidean walk to
     rung 700,000 in verify-record-descent.py): KS vs lelia's form and vs
     lou's Pareto-1 step. Small n — low power, but it is the ground truth.
  2. The record-process SKELETON: the tail-limit law for ANY generic
     irrational (Gauss tail P(a > t) ~ 1/(t ln2)). Iterate
        R_{k+1} = R_k / eta,  eta ~ U(0,1)     (lou's Pareto-1 step)
        W_k ~ Geometric(p = 1/(R_k ln2))        (wait to next record)
     and collect D = R/M for ~200,000 records. This is the law at scale.
     Compare its CDF to lelia's closed form.

If lelia's e^(-1/(c ln2)) were exact, the skeleton's D would follow it.
The skeleton is the same thing as the real α in the tail limit, so any gap
between skeleton and closed form is lelia's form being approximate.
"""
import numpy as np

LN2 = np.log(2.0)

# ---- exact records (rung, quotient) verified in verify-record-descent.py ----
RECORDS = [
    (9, 23), (14, 55), (218, 100), (230, 964), (330, 2436), (528, 3308),
    (2764, 4878), (4312, 8228), (18287, 24477), (21150, 59599),
    (122416, 104733), (169725, 698813), (479173, 1138268),
]
rungs = np.array([r for r, _ in RECORDS], dtype=float)
quots = np.array([q for _, q in RECORDS], dtype=float)
D_exact = quots / rungs            # scaled depth: quotient over rung
steps = quots[1:] / quots[:-1]     # record-to-record step r

def lelia_cdf(c):
    return np.exp(-1.0 / (c * LN2))

def pareto_cdf(s):
    """P(r <= s) for Pareto-1 on [1, inf): 1 - 1/s."""
    return np.clip(1.0 - 1.0 / s, 0.0, None)

def ks(data, cdf):
    d = np.sort(data)
    n = len(d)
    emp = (np.arange(1, n + 1) - 0.5) / n      # mid-rank
    th = cdf(d)
    return np.max(np.abs(emp - th)), n

print("=" * 60)
print("EXACT records of log2(3/2): 13 nontrivial, to rung 700,000")
print(f"  D = quotient/rung: {np.round(D_exact, 3)}")
print(f"  median D = {np.median(D_exact):.3f}   (lelia predicts 1/ln^2 2 = {1/LN2**2:.3f})")
print(f"  mean D = {D_exact.mean():.3f} (no-mean law => unstable, drifts with the max)")
ksD, nD = ks(D_exact, lelia_cdf)
print(f"  KS vs e^(-1/(c ln2)): D={ksD:.3f}, n={nD}, 95% crit {1.36/np.sqrt(nD):.3f} -> {'OK' if ksD < 1.36/np.sqrt(nD) else 'REJECT'}")
print(f"  max D = {D_exact.max():.3f} (lelia law: P(D > maxD) = {1-lelia_cdf(D_exact.max()):.3f})")

print(f"  steps r: {np.round(steps, 3)}")
print(f"  median r = {np.median(steps):.3f}   (Pareto-1 predicts 2)")
print(f"  E[ln r] = {np.mean(np.log(steps)):.3f}   (Pareto-1 predicts 1)")
ksS, nS = ks(steps, pareto_cdf)
print(f"  KS vs Pareto-1: D={ksS:.3f}, n={nS}, 95% crit {1.36/np.sqrt(nS):.3f} -> {'OK' if ksS < 1.36/np.sqrt(nS) else 'REJECT'}")

# ---- skeleton simulation of the record process (tail limit) -------------
# D = R/M is scale-invariant. Track logR and logM; whenever logR exceeds 80
# subtract 80 from both (R,M -> R/e^80, M/e^80; D unchanged). The wait is
# exponential with mean R ln2 (the geometric's continuous twin: same mean,
# same variance, exact in the tail regime where the law is claimed).
rng = np.random.default_rng(20260828)
N = 100_000
D = np.empty(N)
logR = np.log(23.0); logM = 0.0            # first record R=23 at rung M=1
for k in range(1, N):
    while logR > 80:
        logR -= 80; logM -= 80             # rescale; D untouched
    R = np.exp(logR); M = np.exp(logM)
    W = rng.exponential(R * LN2)           # wait to next record
    M += W
    logM = np.log(M)
    logR += -np.log(rng.random())          # R -> R/eta; -log(eta) ~ Exp(1)
    D[k] = np.exp(logR - logM)

print()
print("=" * 60)
print(f"SKELETON (tail-limit record process), {N} records")
print(f"  median D = {np.median(D):.3f}   (lelia predicts {1/LN2**2:.3f})")
print(f"  max D = {D.max():.3f}")
for c in [2.0, 5.0, 10.0, 20.0, 50.0]:
    emp = np.mean(D > c)
    print(f"  P(D > {c:5.1f}):  skeleton {emp:.4f}   lelia-exact {1-lelia_cdf(c):.4f}   "
          f"tail 1/(c ln2) {1/(c*LN2):.4f}")

# KS of skeleton vs lelia's form (sampled CDF comparison)
samp = np.sort(D[::10])       # subsample for independent-ish points
ksSk, nSk = ks(samp, lelia_cdf)
print(f"  KS(skeleton vs lelia) D={ksSk:.4f}, n={nSk} -> "
      f"{'cannot reject' if ksSk < 1.36/np.sqrt(nSk) else 'REJECT (lelia approx only)'}")

# no-mean check: running mean of D keeps climbing as records accumulate
blk = 5000
print("  running mean of D:")
for b in range(1, len(D)//blk + 1):
    print(f"    {b*blk:7d} records:  mean D = {D[:b*blk].mean():9.3f}")

# where do the 13 exact D's fall in the skeleton distribution?  (percentiles)
print()
print("EXACT records in skeleton percentiles:")
for r, q in RECORDS:
    d = q / r
    pct = np.mean(D < d) * 100
    print(f"  rung {r:7d}  quotient {q:8d}  D={d:7.3f}  skeleton pct {pct:5.1f}%")

# (no figure this tick — the reply is text-only. The numbers above are the
#  full record; re-run prints them all.)
