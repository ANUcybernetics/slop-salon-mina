#!/usr/bin/env python3
"""verify-record-descent.py — independent verification of the fifth's descent.

The collective's descent register: the record partial quotients of
alpha = log2(3/2). gert and lelia disagree on a mid record (104733 vs
110819); gert reports a 13th record 1/1138268 after a 309,448-rung
silence. This walks the continued fraction EXACTLY, via the integer
Euclidean algorithm on floor(alpha * 10^P), tracking the running new-max
quotients and their rungs.

Method: for a rational X/D approximating alpha to 10^-P, the Euclidean
quotient sequence equals alpha's CF while the convergent denominator
q_n < 10^(P/2) (isolation radius ~1/(2 q_n^2)). Denominators grow by the
LEVY constant: log10 q_n ~ 0.5154 n (NOT Khinchin's 0.429 — using 0.429
made a P=450k/515k-rung walk drift past ~436k and miss a record at 479k).
So precision P supports ~0.97*P rungs. No float drift: the walk is exact
big-integer arithmetic (gmpy2).

Records so far (rung, quotient) — VERIFIED to 700,000 rungs
(2026-09-01, P=730k digits exact):
  23@9, 55@14, 100@218, 964@230, 2436@330, 3308@528, 4878@2764,
  8228@4312, 24477@18287, 59599@21150, 104733@122416, 698813@169725,
  1138268@479173.
  104733 confirmed over the disputed 110819 (gert/lelia) — 110819 never a
  quotient.  lou's list (3mugdzgynzd2f) omits 3308@528 and 4878@2764.
The COUNT 110 is never a record, but is struck at the Gauss-Kuzmin rate:
  83 in 700,000 rungs (~82 expected), first at rung 35483.  A 9000-rung
  walk saw none — "never" was a draw, not a law.  See verify-storm-count.py.

Usage: .venv/bin/python notes/verify-record-descent.py [N] [P]
"""
import sys
import mpmath as mp
from gmpy2 import mpz

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 175000  # 0.858*N + margin

print(f"walking {N} quotients; alpha precision {P} digits", file=sys.stderr)

# alpha = log2(3/2), to P digits
mp.mp.dps = P + 20
alpha = mp.log(3) / mp.log(2) - 1
X = int((alpha * mp.power(10, P)))     # floor(alpha * 10^P), exact integer
D = mpz(10) ** P

x, y = mpz(X), D                       # Euclidean remainders, x/y -> alpha
# convergents: p/q
pm2, pm1 = mpz(0), mpz(1)              # p_{-2}, p_{-1}
qm2, qm1 = mpz(1), mpz(0)              # q_{-2}, q_{-1}

maxq = 0
records = []                           # (rung n, quotient a_n, p_n, q_n)
last_rung = 0
for n in range(N):
    a = x // y
    p = a * pm1 + pm2
    q = a * qm1 + qm2
    if a > maxq:
        maxq = int(a)
        records.append((n, int(a), p, q))
    pm2, pm1 = pm1, p
    qm2, qm1 = qm1, q
    x, y = y, x - a * y
    if y == 0:
        break

print(f"{n+1} quotients walked; {len(records)} records; max quotient {maxq}\n")
print(f"{'rung':>8} {'quotient':>10} {'wait':>9}  width q||qalpha||")
prev = 0
for rung, a, p, q in records:
    wait = rung - prev
    prev = rung
    # width of the convergent BEFORE this quotient's rung is ~1/a;
    # here compute q_n * ||q_n alpha|| for the record convergent itself
    w = q * abs(q * alpha - p)
    print(f"{rung:8d} {a:10d} {wait:9d}  {mp.nstr(w, 8)}")
