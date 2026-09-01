#!/usr/bin/env python3
"""verify-storm-count.py — the decisive walk: does the count 110 ever appear?

The storm register's open question: log2(3/2)'s CF keeps the seed 55 (twice,
at rungs 14 and 46) but never the count 110. My 9000-rung walk found no 110;
lou extended to 18287 and found none. Under Gauss, P(q=110) = log2(111^2/
(110*112)) ~ 1/8540, so in 100k rungs ~11.7 count-110s are expected — a zero
result would make "root without octave" structure, not a draw.

This walks the exact CF (integer Euclidean on floor(alpha*10^P), gmpy2) to N
rungs, and:
  * counts every quotient == 110 (the count) and == 55 (the seed)
  * prints ALL new-max records with rungs (to check lou's list against mine:
    lou omits 3308 and 4878 which my Aug 30 walk verified)
  * tracks the closest the skyline comes to 110 at each rung
"""
import sys
import mpmath as mp
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 130000   # supports ~0.97*P rungs

print(f"walking {N} quotients; alpha precision {P} digits", file=sys.stderr)

mp.mp.dps = P + 20
alpha = mp.log(3) / mp.log(2) - 1
X = int((alpha * mp.power(10, P)))
D = mpz(10) ** P

x, y = mpz(X), D
pm2, pm1 = mpz(0), mpz(1)
qm2, qm1 = mpz(1), mpz(0)

maxq = 0
records = []
count110 = 0
count55 = 0
count100 = 0
closest = (0, None)   # (distance from 110, quotient)
first_110 = None
hits110 = []
near110 = []          # quotients in [100, 120]

for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a == 110:
        count110 += 1
        if first_110 is None:
            first_110 = n
        hits110.append(n)
        near110.append((n, int(a)))
    elif 100 <= a <= 120:
        near110.append((n, int(a)))
    elif a == 55:
        count55 += 1
    elif a == 100:
        count100 += 1
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a)))
    d = abs(a - 110)
    if d < closest[0] or closest[1] is None:
        closest = (d, (n, int(a)))
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break

nwalked = n + 1
print(f"{nwalked} quotients walked; {len(records)} records; max {maxq}")
print(f"quotient 110 (the count): {count110}  {'FIRST at rung ' + str(first_110) if first_110 is not None else 'NEVER'}")
print(f"  110 at rungs: {hits110}")
print(f"quotient 55 (the seed):   {count55}")
import json
json.dump({"hits110": hits110, "near110": near110, "records": records,
           "count110": count110, "count55": count55, "N": nwalked},
          open("/tmp/storm-near110.json", "w"))
print(f"  wrote /tmp/storm-near110.json ({len(near110)} near-misses in [100,120])")
print(f"quotient 100:             {count100}")
print(f"closest approach to 110:  at rung {closest[1][0]}, quotient {closest[1][1]}, distance {closest[0]}")
print()
print(f"{'rung':>8} {'quotient':>10}")
for rung, a in records:
    print(f"{rung:8d} {a:10d}")
