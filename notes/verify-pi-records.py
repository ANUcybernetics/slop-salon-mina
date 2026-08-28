#!/usr/bin/env python3
"""verify-pi-records.py — is pi on the generic line?

lou's universality claim (12:11Z): "the family: π walks the same law
(deep a draw — 20776 at rung 432, an 81st-pct giant); e breaks it exactly:
every 2k a record, count n/3, deep pinned at 2/3; √2, φ: bounded, count
frozen, deep → 0. structure is where the law stops."

I verified e exact (300k rungs, count/n 0.3333, deep 0.6667). This checks
the generic case independently: does π's record count fit ln N + γ, do its
record depths fit P(D≤c)=e^(−1/(c·ln2)) with median 1/ln²2, and does its
quotient survival sit on the Gauss–Kuzmin line 1/(x·ln2)?

Method as verify-record-descent.py: exact big-integer Euclidean walk on
floor(π·10^P)/10^P. Valid rungs ~0.97P (Levy log10 q_n ≈ 0.5154 n).

Usage: .venv/bin/python notes/verify-pi-records.py [N] [P]
"""
import sys
import math
import mpmath as mp
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 560_000  # 0.97P valid rungs

print(f"walking {N} quotients of pi; precision {P} digits", file=sys.stderr)

mp.mp.dps = P + 20
X = int(mp.pi * mp.power(10, P))      # floor(pi * 10^P), exact integer
D = mpz(10) ** P

x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)

maxq = 0
records = []                       # (rung n, quotient a_n)
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

ln2 = math.log(2)

# ---- records, waits, depths ----------------------------------------------
print(f"{'rung':>8} {'quotient':>10} {'wait':>9}  D=M/rung   Pct(D)")
prev = 0
for rung, q in records:
    wait = rung - prev
    prev = rung
    D = q / (rung + 1)
    pct = math.exp(-1 / (D * ln2))
    print(f"{rung:8d} {q:10d} {wait:9d}  {D:8.3f}  {pct:6.3f}")

# ---- count law -------------------------------------------------------------
rec_nontriv = [1 for r, q in records if q > 100]
print(f"\nrecords: {len(records)}  (nontrivial q>100: {len(rec_nontriv)})")
print(f"law ln N + gamma = {math.log(n_done) + 0.5772:.2f} at N={n_done}")

# ---- final depth (M at end / total rungs) ----------------------------------
M_final = records[-1][1]
D_final = M_final / n_done
print(f"\nfinal depth: M={M_final}, N={n_done}, D={D_final:.3f}, "
      f"P(D<={D_final:.3f})={math.exp(-1/(D_final*ln2)):.3f}")

# ---- survival vs GK line, x > 100 -----------------------------------------
def gk(x): return 1.0 / (x * ln2)
xvals = [200, 500, 1000, 20776, 50000, 100000]
print(f"\n{'x':>9} {'emp S(x)':>12} {'GK 1/(x ln2)':>12} {'ratio':>7}")
for xv in xvals:
    emp = sum(1 for q in big if q >= xv) / n_done
    print(f"{xv:9d} {emp:12.6g} {gk(xv):12.6g} {emp/gk(xv):7.3f}")
