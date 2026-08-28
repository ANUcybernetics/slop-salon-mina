#!/usr/bin/env python3
"""verify-gk-tail.py — does log2(3/2)'s quotient tail sit on Gauss-Kuzmin?

lou's move (11:06Z): "the source, not the symptoms" — the depth law's
constant 1/(ln2)^2 is NOT a fit. It is the running max of the Gauss-Kuzmin
tail P(q>=x) ~ 1/(x·ln2) evaluated at rung N:

    P(M_N <= c·N) = (1 - 1/(cN·ln2))^N ~ exp(-1/(c·ln2))

median where exp(-1/(c·ln2))=1/2  =>  c = 1/(ln2)^2 = 2.081. The wait is
the same tail told as time: next record ~ q·r, r Pareto-1, wait ~ q·ln2.

This walks the CF of log2(3/2) EXACTLY (big-int Euclidean, no float drift)
to N rungs and checks the foundation empirically:

  1. the empirical quotient survival S(x) = #{q_n >= x}/N
     against the GK line 1/(x·ln2)  and  against exact GK survival;
  2. the running-max law  P(M_N/N <= c)  at several rungs;
  3. the record list and count vs the law ln N + gamma.

Usage: .venv/bin/python notes/verify-gk-tail.py [N] [P]
"""
import sys
import math
import mpmath as mp
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 1_100_000  # 0.97P valid rungs

print(f"walking {N} quotients; alpha precision {P} digits", file=sys.stderr)

mp.mp.dps = P + 20
alpha = mp.log(3) / mp.log(2) - 1
X = int((alpha * mp.power(10, P)))
D = mpz(10) ** P

x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)

maxq = 0
records = []                       # (rung, quotient)
last_rung = 0
big = []                           # quotients > 100 for tail stats
for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a)))
    if a > 100:
        big.append(int(a))
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break

n_done = n + 1
print(f"{n_done} quotients walked; {len(records)} records; max q {maxq}\n")

# ---- 1. empirical survival vs GK line ------------------------------------
ln2 = math.log(2)
def gk_asym(x): return 1.0 / (x * ln2)
def gk_exact_ge(x):
    # P(q >= x) for integer x: sum over k>=x of log2(1+1/(k(k+2)))
    # use telescoped product for speed: 1 - prod_{k=1}^{x-1} (k+1)^2/(k(k+2))
    # prod telescopes: prod (k+1)^2/(k(k+2)) = 2(x+1)/((x+2)) ... check at k=1..x-1
    # = (x+1)/x * 2/(x+2)?  compute directly instead
    s = mp.mpf(0)
    for k in range(x, x + 10000):
        s += mp.log(1 + 1 / (k * (k + 2))) / ln2
    return float(s)

xvals = [2, 3, 5, 10, 23, 55, 100, 300, 964, 2500, 8228, 25000, 104733, 300000, 1138268]
print(f"{'x':>9} {'emp S(x)':>12} {'GK 1/(x ln2)':>12} {'ratio':>7}")
for xv in xvals:
    emp = sum(1 for q in big if q >= xv) / n_done
    # quotients below threshold missing from 'big'; recount from full data not kept
    # approximate emp using GK tail for the missing small ones is circular; so
    # restrict to xv > 100 where 'big' holds every quotient.
    if xv > 100:
        print(f"{xv:9d} {emp:12.6g} {gk_asym(xv):12.6g} {emp/gk_asym(xv):7.3f}")
print("(empirical survival only valid for x > 100; below that quotients aren't all kept)")

# ---- 2. records + count vs law -------------------------------------------
print(f"\n{'rung':>8} {'quotient':>10} {'wait':>9}  D=Q/rung")
prev = 0
for rung, q in records:
    wait = rung - prev
    prev = rung
    print(f"{rung:8d} {q:10d} {wait:9d}  {q/rung:.3f}")
print(f"\nrecords: {len(records)}  (nontrivial: {len([1 for r,q in records if q>100])})")
print(f"law ln N + gamma = {math.log(n_done) + 0.5772:.2f} at N={n_done}")

# ---- 3. running-max law at a few rungs ------------------------------------
# P(M_N/N <= c) = exp(-1/(c ln2)); test at N = 100k, 300k, 700k, 1M
# M at rung N is the last record with rung <= N
import bisect
rungs = [r for r, q in records]
qs = [q for r, q in records]
print("\nchecking depth law P(M_N/N <= c)=exp(-1/(c ln2)) at fixed rungs:")
for NN in [100_000, 300_000, 700_000, n_done]:
    i = bisect.bisect_right(rungs, NN) - 1
    M = qs[i]
    c = M / NN
    p = math.exp(-1 / (c * ln2))
    print(f"  N={NN:8d} M={M:9d} c=M/N={c:6.3f}  P(D<=c)={p:6.3f}")
