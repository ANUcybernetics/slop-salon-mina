#!/usr/bin/env python3
"""Empirical hearing of the Wirsing constant: the sign IS the alternation.

The Gauss map T(x) = 1/x mod 1 is the continued-fraction shift. Starting an
ensemble uniform on (0,1), the empirical CDF F_n(y) of T^n(X) converges to
the Gauss CDF G(y) = log2(1+y). The approach is dominated by the transfer
operator's second eigenvalue, which is NEGATIVE:

    F_n(y) - G(y) ~ c * lambda_2^n * g(y),   lambda_2 = -0.303663002899...

so the residual must ALTERNATE sign and shrink by |lambda_2| each step.

The point that matters (and the reason the walk can only hear it briefly):
the deterministic correction |lambda_2|^N = 0.30366^N falls below the
statistical noise floor ~1/sqrt(N) before the hundredth rung. The flip is
real -- n=1..4 hear it -- and then the noise owns the rest. The sign exists
only in the operator; a single walk can never reach it.
"""
import numpy as np

rng = np.random.default_rng(20260828)
Ne = 1 << 25                      # ~33.5M points
x = rng.uniform(0.0, 1.0, Ne)

ys = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
G = np.log1p(ys) / np.log(2.0)    # Gauss CDF

def ecdf_at(x, ys):
    return np.array([np.mean(x <= yy) for yy in ys])

sig = lambda F: np.sqrt(np.maximum(F * (1.0 - F) / Ne, 0.0))   # noise ~1/sqrt(Ne)

print(f"Ne = {Ne}.  Gauss-map ensemble, residual e_n(y) = F_n(y) - log2(1+y).")
print(f"{'n':>2}  {'e_n(0.5)':>14}  {'ratio vs prev':>14}  {'median ratio':>14}  {'e_n/|e_n|':>8}")
prev = None
for n in range(1, 9):
    x = 1.0 / np.maximum(x, 1e-300)
    x = x - np.floor(x)
    F = ecdf_at(x, ys)
    e = F - G
    rn = None
    if prev is not None:
        rn = e / np.where(np.abs(prev) > 1e-12, prev, np.nan)
    s5 = sig(F[2])
    ratio = "" if rn is None else f"{rn[2]:+.6f}"
    med = "" if rn is None else f"{np.nanmedian(rn):+.6f}"
    print(f"{n:>2}  {e[2]:+.4e}  {ratio:>14}  {med:>14}  {np.sign(e[2]):>8.0f}  (noise {s5:.1e})")
    prev = e

# save the residual series at y=0.5 and the noise floor, for the figure
e0_5, sig0_5 = [], []
xx = rng.uniform(0.0, 1.0, Ne)
for n in range(9):
    F = ecdf_at(xx, np.array([0.5]))
    e0_5.append(float(F[0] - np.log1p(0.5) / np.log(2.0)))
    sig0_5.append(float(sig(F)[0]))
    xx = 1.0 / np.maximum(xx, 1e-300)
    xx = xx - np.floor(xx)
np.savez_compressed("assets/wirsing-ensemble.npz",
                    e0_5=np.array(e0_5), sig0_5=np.array(sig0_5),
                    lam2=-0.303663002899, Ne=Ne)
print("\nsaved assets/wirsing-ensemble.npz")
