#!/usr/bin/env python3
"""Verify lou's claim vs my capstone: exact discrete median of the next record's value.
R = current record. Next value V ~ GK conditioned on q > R.
Exact GK survival: P(q > k) = log2((k+2)/(k+1))  [k integer >= 0]
So P(V > k) = log2((k+2)/(k+1)) / log2((R+2)/(R+1)).
Compare crossing of 1/2 with: 2R=17576 (mine, clean) and 2R+2=17578 (lou, patternless).
"""
import numpy as np
R = 8788
S = lambda k: np.log2((k+2)/(k+1))
half = S(R)/2  # value of S(k) at which P(V>k) = 1/2

print(f"R = {R}")
print(f"S(R) = log2(8790/8789) = {S(R):.12f}")
print(f"half = S(R)/2 = {half:.12f}")

# Find crossing of S(k) = half over integer k
for k in range(17570, 17584):
    s = S(k)
    p = s / S(R)
    print(f"  k={k}: S(k)={s:.12f}  P(V>{k})={p:.8f}  {'<-- crosses 1/2' if (s-half)*(S(k-1)-half)<0 else ''}")

# continuous crossing (solve S(x)=half for real x)
# S(x) = log2((x+2)/(x+1)); S(x)=half -> (x+2)/(x+1) = 2^half
twoh = 2**half
x_cross = (twoh*1 - 2)/(1 - twoh)
print(f"\ncontinuous crossing x* = (2^half - 2)/(1 - 2^half) = {x_cross:.6f}")

# my formula from the capstone: m = 1/(sqrt(1+1/R) - 1)
m_mine = 1/(np.sqrt(1+1/R) - 1)
print(f"my posted formula m = 1/(sqrt(1+1/R)-1) = {m_mine:.6f}, floor = {int(m_mine)}")

# integer median: smallest m with P(V > m) <= 1/2  (i.e., P(V <= m) >= 1/2)
m_int = None
for k in range(1, 10**7):
    if S(k)/S(R) <= 0.5:
        m_int = k
        break
print(f"integer median (smallest m with P(V<=m)>=1/2): {m_int}")
print(f"2R = {2*R} = 2^3*13^3? {2*R==2**3*13**3}")
print(f"2R+2 = {2*R+2} = 2*11*17*47? {2*R+2==2*11*17*47}")

# Also: the 'median' via Pareto continuum  R/k: crossing at k=2R
print(f"\nPareto continuum median (R/k=1/2): k = {2*R}")
# Exact continuous median of the conditional GK:
# P(V>k)=1/2 -> S(k)=S(R)/2, exact crossing at x*
print(f"Exact conditional-GK continuous median: {x_cross:.4f}")
print(f"Round to integer candidate: {round(x_cross)}")

# What about the shifted-Pareto convention P(V>k) = (R+1)/(k+1)?
# crossing: (R+1)/(k+1)=1/2 -> k = 2R+1 = 17577
print(f"\nShifted-Pareto convention crossing k=2R+1 = {2*R+1}; integer median = {2*R+2}")
