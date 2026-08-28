#!/usr/bin/env python
"""Verify/extend the record descent of alpha = log_2(3/2).

Record widths q*||q*alpha|| at convergents. Each record depth lands just
below 1/(next partial quotient), and the record quotients ARE the running
new-max quotients of the CF. To reach 4500 quotients you need ~6000 dps
(max denominator ~10^2234).

Records so far (convergent index, quotient):
  i=8→23, i=13→55, i=217→100, i=229→964, i=329→2436, i=527→3308,
  i=2763→4878, i=4311→8228.
1/114 never lands. Expected wait for the next record after max M ~ M*ln2
rungs (Gauss-Kuzmin); single waits scatter widely (204 rungs at M=55,
12 at M=100).

Run: .venv/bin/python notes/verify-future-records.py [NQ] [DPS]
"""
import sys
import mpmath as mp

NQ = int(sys.argv[1]) if len(sys.argv) > 1 else 4500
mp.mp.dps = int(sys.argv[2]) if len(sys.argv) > 2 else 6000

ALPHA = mp.log(3) / mp.log(2) - 1  # fractional part, ~0.58496

C = []
x = ALPHA
for _ in range(NQ):
    a = int(mp.floor(x))
    C.append(a)
    x = x - a
    x = 1 / x if x else 0

p0, q0 = 0, 1
p1, q1 = 1, 0
records = []
maxq = 0
record = mp.mpf("1e9")
for i, a in enumerate(C):
    p, q = a * p1 + p0, a * q1 + q0
    p0, q0 = p1, q1
    p1, q1 = p, q
    w = q * abs(q * ALPHA - p)
    if w < record:
        record = w
        nq = C[i + 1] if i + 1 < len(C) else None
        records.append((i, nq, w))
        maxq = nq if nq and nq > maxq else maxq

print(f"{len(C)} quotients; current max quotient {maxq}")
print("record depth set at convergent i, named 1/nextQ, width:")
for i, nq, w in records:
    print(f"  i={i:5d}  1/{nq:<5}  w={mp.nstr(w, 8)}")
