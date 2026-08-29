#!/usr/bin/env python3
"""Verify lou's generalization: exact discrete median of next record after K
is 2(K+1) for every K. Exact GK survival S(k)=log2((k+2)/(k+1)).
Continuous crossing of S(k)/S(K)=1/2 is at k*=(K+1)(1+sqrt(1+1/(K+1)))-1
~ 2K + 3/2. Integer median (smallest m with P(V>m)<=1/2) should be 2(K+1).
"""
import numpy as np
S = lambda k: np.log2((k+2)/(k+1))
bad = []
for K in range(1, 4001):
    half = S(K)/2
    twoh = 2**half
    kstar = (twoh - 2)/(1 - twoh)
    # integer median: smallest m with S(m)/S(K) <= 0.5; search up from K
    m = K
    while S(m)/S(K) > 0.5:
        m += 1
    if m != 2*(K+1):
        bad.append((K, m, 2*(K+1), round(float(kstar),4)))
    if not (abs(kstar - (2*K + 1.5)) < 0.5):
        bad.append((K, 'kstar', round(float(kstar),4), 2*K+1.5))
print(f"checked K=1..4000: integer median == 2(K+1) always? {not bad}")
if bad: print("violations (first 5):", bad[:5])
for K in [1, 3, 13, 174, 8788]:
    half = S(K)/2; twoh = 2**half
    kstar = (twoh-2)/(1-twoh)
    m = K
    while S(m)/S(K) > 0.5: m += 1
    print(f"K={K}: crossing {kstar:.4f}, median {m}, 2(K+1)={2*(K+1)}, ok={m==2*(K+1)}")
