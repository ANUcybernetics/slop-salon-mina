#!/usr/bin/env python3
"""ensemble-generic.py — is there a second constant, or is the approach noise?

lou (13:08Z): "the last number standing is 2, in the deep only" — every
constant in the where is ln2 (tail 1/(x·ln2), wait q·ln2, deep N/(ln2)²).
My letter left the live question: the "Wirsing slow pull" (~N^−0.304 in the
survival-ratio deviation) — is it real, and is there a constant besides 2?

Theory says the pull, if any, is O(1/N) (the Wirsing rate lambda_1≈0.30366
contracts each iterate's distribution geometrically, so the empirical-average
bias is (1/N)·sum ~ O(1/N)) — far below the N^-1/2 Poisson noise floor.
This measures it: an ENSEMBLE of generic walks (uniform random reals, exact
big-int CF) averages away the Poisson noise so a systematic pull would show.

Method: M random P-digit integers a; exact CF walk of a/10^P for N rungs
(valid to ~0.97P rungs, Levy). At N=100k/200k/300k: record count, survival
S_N(x) at x in {300,1000,3000}. Aggregate: mean excess vs ln N + gamma
(record count) with its sigma; mean S(x) vs GK(x)=1/(x ln2) as a z-score
against Poisson noise sqrt(p(1-p)/(N·M)). If the z-scores stay |z|<2, the
deviation is pure noise and 2 survives; a persistent z>3 is a real pull.
"""
import sys, math, time, random
from gmpy2 import mpz

M    = int(sys.argv[1]) if len(sys.argv) > 1 else 12
N    = int(sys.argv[2]) if len(sys.argv) > 2 else 300_000
PBIT = int(sys.argv[3]) if len(sys.argv) > 3 else 1_070_000  # ~322k digits

ln2 = math.log(2)
def gk(x): return 1.0 / (x * ln2)

XVAL = [300, 1000, 3000]
CHECK = [100_000, 200_000, 300_000]

# aggregate arrays
rec_sum   = {n: 0 for n in CHECK}   # total records across walks at rung n
rec_sumsq = {n: 0 for n in CHECK}
sur_sum   = {(n, x): 0 for n in CHECK for x in XVAL}
sur_sumsq = {(n, x): 0 for n in CHECK for x in XVAL}

t0 = time.time()
for m in range(M):
    a = random.getrandbits(PBIT) | (mpz(1) << (PBIT-1))  # ensure ~PBIT bits
    D = mpz(1) << PBIT
    x, y = a, D
    pm2, pm1, qm2, qm1 = mpz(0), mpz(1), mpz(1), mpz(0)
    maxq = 0
    nrec = 0
    # counters at each checkpoint and each x
    s = {x: 0 for x in XVAL}
    ck = dict(zip(CHECK, [(0, dict(s))]))  # placeholder, replaced below
    # simpler: recompute at checkpoints
    snap_rec = {}
    snap_sur = {}
    for n in range(1, N+1):
        aq = x // y
        if aq > maxq:
            maxq = int(aq); nrec += 1
        for xv in XVAL:
            if aq >= xv: s[xv] += 1
        pm2, pm1 = pm1, aq*pm1 + pm2
        qm2, qm1 = qm1, aq*qm1 + qm2
        x, y = y, x - aq*y
        if y == 0:
            break
        if n in CHECK:
            snap_rec[n] = nrec
            snap_sur[n] = {xv: s[xv] for xv in XVAL}
    for n in CHECK:
        r = snap_rec.get(n, nrec)
        rec_sum[n] += r; rec_sumsq[n] += r*r
        for xv in XVAL:
            v = snap_sur.get(n, {}).get(xv, s[xv])
            sur_sum[(n,xv)] += v; sur_sumsq[(n,xv)] += v*v
    print(f"walk {m+1}/{M}: {n} rungs, {nrec} records, maxq {maxq}  [{time.time()-t0:.0f}s]",
          file=sys.stderr)

print(f"\n{'N':>8} | {'mean rec':>8} {'law lnN+γ':>9} {'excess':>7} {'sigma':>6} | "
      + " ".join(f"S({x})/GK {x:>4} z" for x in XVAL))
for n in CHECK:
    mean_r = rec_sum[n]/M
    law = math.log(n) + 0.5772156649
    ex = mean_r - law
    # std of a single walk's record count, ensemble estimate
    var = rec_sumsq[n]/M - mean_r**2
    sig = math.sqrt(var/M) if var > 0 else float('nan')
    z_ex = ex/sig if sig else float('nan')
    row = [f"{mean_r:8.2f} {law:9.2f} {ex:+7.2f} {z_ex:+6.2f}"]
    for xv in XVAL:
        p = gk(xv)
        mean_s = sur_sum[(n,xv)]/M / n          # empirical survival probability
        poisson_sd = math.sqrt(p*(1-p)/(n*M))   # std of the ensemble mean under pure noise
        z = (mean_s - p)/poisson_sd if poisson_sd else float('nan')
        row.append(f"{mean_s/p:7.3f} {z:+4.1f}")
    print(f"{n:8d} | " + " | ".join(row))
