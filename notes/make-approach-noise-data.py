#!/usr/bin/env python3
"""make-approach-noise-data.py — walk pi exact, save the ratio-trace + records.

The piece: "the approach is noise." For fixed x=300, the running ratio
r(n) = S_n(300) / (n * GK(300)) — the empirical survival over the law —
leaps when the first events land, then descends toward 1 with a residual
that is pure Poisson (the band ~1/sqrt(n), never closing). pi is the named
generic (just verified on the line). Save the ratio trace and the records
for the synthesis script.

Usage: .venv/bin/python notes/make-approach-noise-data.py [N] [P]
"""
import sys, math
import numpy as np
import mpmath as mp
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 530_000  # valid ~0.97P rungs

print(f"walking {N} quotients of pi; precision {P} digits", file=sys.stderr)
mp.mp.dps = P + 20
X = int(mp.pi * mp.power(10, P))
D = mpz(10) ** P
x, y = mpz(X), D
pm2, pm1, qm2, qm1 = mpz(0), mpz(1), mpz(1), mpz(0)

ln2 = math.log(2)
GK300 = 1.0 / (300 * ln2)

n_all = np.arange(1, N + 1)
s_all = np.zeros(N, dtype=np.int64)     # running count of quotients >= 300
r_all = np.zeros(N)                     # ratio S/(n*GK)
records = []                            # (rung n, quotient M)
maxq = 0
s = 0
for n in range(1, N + 1):
    a = x // y
    if a >= 300:
        s += 1
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a)))
    pm2, pm1 = pm1, a * pm1 + pm2
    qm2, qm1 = qm1, a * qm1 + qm2
    x, y = y, x - a * y
    if y == 0:
        print("terminated early", file=sys.stderr)
        break
    s_all[n - 1] = s
    r_all[n - 1] = s / (n * GK300)

np.savez("/home/sprite/slop-salon-mina/assets/approach-noise-data.npz",
         n=n_all[:n], r=r_all[:n], s=s_all[:n])
rec = np.array(records)
np.save("/home/sprite/slop-salon-mina/assets/approach-noise-records.npy", rec)
print(f"walked {n} rungs; {len(records)} records; max q {maxq}", file=sys.stderr)
print("first records:", records[:5])
print("last records:", records[-3:])
print("ratio at 100/1000/10000/100000/500000:",
      *(round(r_all[i], 3) for i in [99, 999, 9999, 99999, min(n, N) - 1]))
