#!/usr/bin/env python3
"""check-midtail.py — is the ~2% mid-tail deficit real or a draw?

The 20-walk ensemble showed S(1000)/GK ~ 0.975, S(3000)/GK ~ 0.978 at
300k rungs (z~-2), while x=300 sat on the line. The fifth at 1M was clean
(0.98-1.01). Is the deficit a slow mixing bias (shrinks with N), a real
mid-tail effect, or a draw? Walk pi (named generic) to 1M, count x=1000
and x=3000, report ratios at nested N against the exact GK survival.
"""
import sys, math
import mpmath as mp
from gmpy2 import mpz

N = 1_000_000
P = 1_060_000
print(f"walking {N} quotients of pi; precision {P}", file=sys.stderr)
mp.mp.dps = P + 20
X = int(mp.pi * mp.power(10, P))
D = mpz(10) ** P
x, y = mpz(X), D
pm2, pm1, qm2, qm1 = mpz(0), mpz(1), mpz(1), mpz(0)

ln2 = math.log(2)
def gk_exact(xx):
    s = 0.0
    for k in range(xx, xx + 400000):
        s += math.log2(1.0 + 1.0/(k*(k+2)))
    return s
GK = {x: gk_exact(x) for x in (300, 1000, 3000)}

CHK = [100_000, 200_000, 300_000, 500_000, 700_000, 1_000_000]
cnt = {x: 0 for x in GK}
snap = {n: None for n in CHK}
for n in range(1, N + 1):
    a = x // y
    for xv in GK:
        if a >= xv:
            cnt[xv] += 1
    pm2, pm1 = pm1, a * pm1 + pm2
    qm2, qm1 = qm1, a * qm1 + qm2
    x, y = y, x - a * y
    if y == 0:
        break
    if n in CHK:
        snap[n] = {xv: cnt[xv] for xv in GK}

print(f"\n{'N':>9} | " + " | ".join(f"S({x})/GK({x})" for x in GK))
for n in CHK:
    row = []
    for xv in GK:
        c = snap[n][xv]
        ratio = c / (n * GK[xv])
        row.append(f"{ratio:.4f}")
    print(f"{n:9d} | " + " | ".join(row))
