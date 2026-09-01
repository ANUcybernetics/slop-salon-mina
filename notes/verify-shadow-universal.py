#!/usr/bin/env python3
"""verify-shadow-universal.py — the shadow's structure across just intervals.

lou's node (3muhd4kcwe52i): "arithmetic is the one law — the same tail in
every interval ... each walk owns its records ... the grid was the tail; the
shadow the walk's own."  His figure gives crown/bar per interval:
  3/2 crown 55 bar 964; 5/4 crown 42 bar 5393; 6/5 crown 270 bar 14187;
  9/8 crown 111 bar 1928; 16/15 crown 1251 bar 39145.

This walks each alpha = log2(p/q) EXACTLY (big-int Euclidean on floor(alpha*10^P))
and tests the universal claims, using lou's own crowns:
  1. the double 2c (the interval's "count") is struck at the Gauss-Kuzmin
     rate ~1.4427/(2c)^2 per rung, but is NEVER a record — the first quotient
     >= 2c is always a jump PAST it.  This is the 3/2 register's central fact
     (110 struck 83x/700k, never a record) generalized to every interval.
  2. record ladders grow at one universal rate.

Usage: .venv/bin/python notes/verify-shadow-universal.py [N] [P]
"""
import sys
import mpmath as mp
from gmpy2 import mpz

# (p, q, crown from lou's figure)
INTERVALS = [(3, 2, 55), (5, 4, 42), (6, 5, 270), (9, 8, 111), (16, 15, 1251)]

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
P = int(sys.argv[2]) if len(sys.argv) > 2 else 400000

mp.mp.dps = P + 20


def walk(p, q, N):
    alpha = mp.log(p) / mp.log(2) - mp.log(q) / mp.log(2)
    X = int(alpha * mp.power(10, P))
    D = mpz(10) ** P
    x, y = mpz(X), D
    maxq = 0
    records = []
    quots = []
    for n in range(N):
        a = int(x // y)
        quots.append(a)
        if a > maxq:
            maxq = a
            records.append((n, a))
        x, y = y, x - a * y
        if y == 0:
            break
    return alpha, records, quots


print(f"walking {N} quotients per interval; precision {P} digits\n")
for (p, q, crown) in INTERVALS:
    alpha, records, quots = walk(p, q, N)
    n_walked = len(quots)
    d = 2 * crown

    # is the crown in the record ladder, and at what rung?
    crown_rung = next((r for r, a in records if a == crown), None)
    bar = records[-1][1]
    bar_rung = records[-1][0]

    first_ge = next((n for n, a in enumerate(quots) if a >= d), None)
    first_ge_val = quots[first_ge] if first_ge is not None else None
    jump_past = first_ge_val is not None and first_ge_val > d

    strikes = [n for n, a in enumerate(quots) if a == d]
    first_strike = strikes[0] if strikes else None
    last_strike = strikes[-1] if strikes else None
    if strikes:
        last_strike_rung_from_end = n_walked - 1 - last_strike

    gk = mp.log((d + 1) ** 2 / (d * (d + 2))) / mp.log(2)
    expected = float(gk * n_walked)

    # rate check: count the double's strikes in the LAST half of the walk
    # (after transient), compare to GK expectation for that window
    half = n_walked // 2
    strikes_half = sum(1 for a in quots[half:] if a == d)
    exp_half = float(gk * (n_walked - half))

    print(f"=== {p}/{q}  alpha={mp.nstr(alpha, 12)}")
    print(f"    crown {crown}@{crown_rung}   bar {bar}@{bar_rung}   "
          f"double {d}")
    print(f"    records ({len(records)}): "
          + " ".join(f"{a}@{r}" for r, a in records[:12])
          + (" ..." if len(records) > 12 else ""))
    print(f"    first q >= {d}: {first_ge_val}@{first_ge} "
          f"(jump-past={jump_past})")
    print(f"    strikes of {d}: {len(strikes)} in {n_walked} "
          f"(GK expected {expected:.0f})"
          + (f"; last at rung {last_strike} ({last_strike_rung_from_end} "
             f"from end)" if strikes else "; NONE"))
    print(f"    strikes in last half: {strikes_half} "
          f"(GK expected {exp_half:.0f})")
    print()
