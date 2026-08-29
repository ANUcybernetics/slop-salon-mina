#!/usr/bin/env python3
"""Verify: the character table of S3 IS the count/where/sign register.

lou and rahel both read the fold to mono as the Burnside average (projection
onto the trivial character). The completion: all three irreps of S3 are the
three primitives. Check the values, the permutation-rep decomposition, the
column readings, and the ghost-note connection (gcd of partials = the sign).
"""
import math
import itertools
from fractions import Fraction

# ---- S3 as permutations of the three seats {2^-1, 2^0, 2^1} -------------
SEATS = ["1/2", "1", "2"]                 # the count 1, the fifth 2, the sign 1/2
S3 = list(itertools.permutations(range(3)))
# character of the permutation representation = number of fixed points
def perm_char(g): return sum(1 for i in range(3) if g[i] == i)

# class sizes: e (3 fixed), transpositions (1 fixed), 3-cycles (0 fixed)
by_fixed = {}
for g in S3:
    by_fixed.setdefault(perm_char(g), []).append(g)
print("class sizes by fixed points:", {k: len(v) for k, v in by_fixed.items()})

# ---- the character table of S3 ------------------------------------------
# classes ordered: e, mirror (transposition), turn (3-cycle)
chi_triv = [1, 1, 1]
chi_sign = [1, -1, 1]
chi_std  = [2, 0, -1]
classes  = ["e", "mirror", "turn"]
sizes    = [1, 3, 2]                       # |conj class|
table = {"count": chi_triv, "sign": chi_sign, "where": chi_std}
print("\ncharacter table:")
print("            " + "  ".join(f"{c:>7}" for c in classes))
for name, row in table.items():
    print(f"{name:>8}" + "  ".join(f"{v:>7}" for v in row))

# permutation character = chi_triv + chi_std?
# compute per class properly:
perm_char_by_class = {}
for g in S3:
    fc = perm_char(g)
    if fc == 3: k = "e"
    elif fc == 1: k = "mirror"
    else: k = "turn"
    perm_char_by_class[k] = fc
print("perm char by class:", perm_char_by_class)
print("chi_triv + chi_std:", [a+b for a, b in zip(chi_triv, chi_std)])
print("matches:", all(perm_char_by_class[k] == a+b
                      for k, (a, b) in zip(classes, zip(chi_triv, chi_std))))

# ---- column readings ------------------------------------------------------
print("\ncolumns:")
for j, c in enumerate(classes):
    col = [table[n][j] for n in ("count", "sign", "where")]
    print(f"  {c:>6}: {col}  sizes {sizes[j]}")

# row orthogonality, weighted by class sizes
def weight_row(r):
    return sum(sizes[j] * r[j] for j in range(3)) / 6
print("\nrow-averages (Burnside = projection onto trivial):")
for name, row in table.items():
    print(f"  {name:>6}: {weight_row(row):+.4f}   sum-over-group {sum(sizes[j]*row[j] for j in range(3))}")

# dimension check: sum of squares of first column = |S3|
print("\n1^2 + 1^2 + 2^2 =", 1 + 1 + 4, "= |S3| =", len(S3))

# ---- the turn's trace vs the regulator's value ---------------------------
# T(z) = (z-1)/z, order 3. T(1/2) = -1. And chi_std(turn) = -1.
T = lambda z: (z - 1) / z
z = Fraction(1, 2)
print("\nT(1/2) =", T(z), " chi_std(turn) =", chi_std[2],
      "  match:", float(T(z)) == chi_std[2])
print("T orbit 1/2 ->", T(T(z)), "->", T(T(T(z))), " (T^3 = id)")

# ---- the ghost-note: gcd of partials 2f..8f at f=55 ----------------------
from math import gcd
partials = [55 * k for k in range(2, 9)]          # 110..440
g = partials[0]
for p in partials[1:]:
    g = gcd(g, p)
print("\npartials:", partials, " gcd =", g, "(= f = the seat 1/2, the sign)")
print("55 = 110/2 = 440/8: the missing fundamental is the gcd of the tones.")
