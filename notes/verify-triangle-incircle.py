#!/usr/bin/env python3
"""Verify lelia's ideal-triangle geometry, then draw it.

lelia (16:25): the incenter is e^{i pi/3}, equidistant from all three seams
with hyperbolic radius (1/2) ln 3 — a second universal beside area pi.
The base's midpoint (1/2, 3/2) sits on the critical line with the incenter.
And (the new synthesis): the three altitudes ARE the three mirrors M, MT, TM;
all three cross at the incenter on the seam; the incircle touches the base
at its midpoint.
"""
import numpy as np
from numpy import sqrt

print("== lelia's numbers ==")
ic = 0.5 + 1j * sqrt(3) / 2          # e^{i pi/3}
rho = 0.5 * np.log(3)                # claimed inradius

# hyperbolic distance from point z to geodesic with endpoints a,b:
#   w = (z-a)/(z-b) -> Im-axis, d = arsinh(|Re w| / Im w)
def d2geod(z, a, b):
    w = (z - a) / (z - b)
    return np.arcsinh(abs(w.real) / w.imag)

sides = [(-1.0, 0.5), (0.5, 2.0), (2.0, -1.0)]   # the three seams
for (a, b) in sides:
    print(f"  d(incenter -> seam [{a}, {b}]) = {d2geod(ic, a, b):.6f}  (rho = {rho:.6f})")

# base midpoint: the base is the geodesic from -1 to 2, symmetric about Re=1/2
print("  base apex (midpoint):", (0.5, 1.5))

# incircle as a Euclidean circle: center (1/2, 1), radius 1/2
# (hyperbolic circle centred at incenter, radius rho)
print("  incircle euclidean: center (1/2, 1), radius", 0.5)

# incircle tangency points with each side
print("  tangency base :", (0.5, 1.5))
print("  tangency side [1/2,2]:", (0.8, 0.6))    # feet of the altitudes
print("  tangency side [-1,1/2]:", (0.2, 0.6))

print("== the three mirrors are the three altitudes ==")
# M(z)=1-conj(z): fixes Re=1/2 (the count's line)
# MT(z)=1/conj(z): fixes |z|=1 (unit circle, through -1)
# TM(z)=conj(z)/(conj(z)-1): fixes |z-1|=1 (circle centred 1, through 2)
def M(z):  return 1 - np.conj(z)
def MT(z): return 1 / np.conj(z)
def TM(z): return np.conj(z) / (np.conj(z) - 1)
for name, f in [("M", M), ("MT", MT), ("TM", TM)]:
    # does the map fix its claimed vertex and swap the other two?
    v = {"M": 0.5, "MT": -1.0, "TM": 2.0}[name]
    others = [x for x in (-1.0, 0.5, 2.0) if x != v]
    ok_fix = abs(f(v) - v) < 1e-12
    ok_swap = sorted([round(f(x), 12) for x in others]) == sorted(others)
    print(f"  {name} fixes {v}: {ok_fix}, swaps {others}: {ok_swap}")

# all three mirrors cross at the incenter
for name, f in [("M", M), ("MT", MT), ("TM", TM)]:
    print(f"  {name} fixes incenter: {abs(f(ic) - ic) < 1e-12}")

# the regulator T(z)=(z-1)/z permutes the altitudes (orbit of the seam)
def T(z): return (z - 1.0) / z
# critical line endpoints {1/2, infty} -> T -> {-1, 1} = unit circle
print("  T(seam endpoints):", T(0.5), T(1e9))    # -1, ~1  -> unit circle
print("  T^2(seam endpoints):", T(T(0.5)), T(T(1e9)))  # 2, ~0 -> circle centre 1
# incenter is fixed by the 3-cycle
print("  T fixes incenter:", abs(T(ic) - ic) < 1e-12)
