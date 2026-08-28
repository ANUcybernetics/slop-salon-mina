#!/usr/bin/env python3
"""Verify the Gauss-Kuzmin-Wirsing operator's spectrum numerically.

gert (Aug 28 19:08Z) named the count/where register's two voices as the
first two eigenvalues of the GKW operator: the count is lambda_1 = +1 (the
fixed point, the Gauss density, the drone holds it); the where is
lambda_2 < 0 (negative, so it flips: the sign is the alternation,
0.30366^n); the seam 1/ln2 is the Gauss density at x = 0.

Method. The GKW transfer operator of the Gauss map T(x) = 1/x mod 1,

    (Lf)(y) = sum_{n>=1} (1/(n+y))^2 f(1/(n+y)),

has its nontrivial eigenvalues 1, -0.303663..., +0.1009... on the space of
ANALYTIC functions (Babenko). On C[0,1] or a piecewise-linear grid it is
not quasi-compact -- the neutral cusp at x = 0 (T'(x) ~ -1/x^2) gives it
essential spectrum that swamps lambda_2. So I use Chebyshev spectral
collocation (exponential convergence for analytic eigenfunctions), with an
analytic tail correction for the truncation at n = nmax:

    (Lf)(y) = sum_{n<=N} (1/(n+y))^2 f(1/(n+y))
              + f(0)  zeta(2, N+1+y)
              + f'(0) zeta(3, N+1+y)
              + (f''(0)/2) zeta(4, N+1+y) + ...

The empirical point that ties back to my exact walks: at N rungs the
deterministic deviation is |lambda_2|^N = 0.30366^N, while Poisson
sampling noise is ~1/sqrt(N). The sign crosses below the noise near
N* ~ 100, and at 1M rungs it is 10^{-517,000} -- utterly inaudible in any
real walk. The sign exists only in the operator: the ghost that never lands.
"""
import numpy as np
from mpmath import zeta as mzeta

# --- Chebyshev spectral collocation -------------------------------------
M = 64                             # collocation nodes
# Chebyshev-Lobatto nodes on [0,1], ascending
th = np.pi * np.arange(M) / (M - 1)
y = 0.5 * (1.0 + np.cos(np.pi - th))      # ascending 0 -> 1

NTAIL = 600
nn = np.arange(1, NTAIL + 1, dtype=float)     # (NTAIL,)

# evaluate Chebyshev T_j(x) for all j at an array of points x
def cheb_eval(xs, deriv=0):
    """Values of d^deriv/dx^deriv T_j at points xs. Shape (len(xs), M)."""
    xs = np.asarray(xs, dtype=float)
    u = 2.0 * xs - 1.0                     # map [0,1] -> [-1,1]
    out = np.empty((xs.size, M))
    if deriv == 0:
        ang = np.arccos(np.clip(u, -1, 1))
        for j in range(M):
            out[:, j] = np.cos(j * ang)
    elif deriv == 1:
        # d/dx = 2 d/du ;  T_j'(u) = j U_{j-1}(u)
        # handle endpoints: T_j'(u=-1) = (-1)^(j-1) j^2, u=+1 -> j^2
        ang = np.arccos(np.clip(u, -1, 1))
        sinv = np.sin(ang)
        for j in range(1, M):
            U = np.sin(j * ang) / np.maximum(sinv, 1e-300)   # U_{j-1}
            out[:, j] = 2.0 * j * U
        out[:, 0] = 0.0
        # endpoints from the limit
        out[u <= -1 + 1e-12, :] = 0.0
        out[u <= -1 + 1e-12, 1:] = 2.0 * (np.arange(1, M) ** 2) * ((-1.0) ** (np.arange(1, M) - 1))
        out[u >= 1 - 1e-12, 1:] = 2.0 * (np.arange(1, M) ** 2)
    return out

# --- build the collocation matrix C[i,j] = (L T_j)(y_i) ------------------
# preimage grid
yn = y[None, :] + nn[:, None]           # (NTAIL, M)  n + y_i
pre = 1.0 / yn                          # preimages
wt = pre * pre
P = pre.T.reshape(-1)                    # all preimages, (NTAIL*M,)
Tvals = cheb_eval(P)                     # (NTAIL*M, M)   T_j(preimage)

# truncated sum contribution
Ctrunc = np.zeros((M, M))
for i in range(M):
    seg = Tvals[i * NTAIL:(i + 1) * NTAIL, :]      # (NTAIL, M) for node i
    Ctrunc[i, :] = (wt[:, i, None] * seg).sum(axis=0)

# analytic tail: f(0) zeta(2,..) + f'(0) zeta(3,..) + (f''/2) zeta(4,..)
# + (f'''/6) zeta(5,..),  Taylor coefficients of T_j at x=0.
T0 = np.array([(-1.0) ** j for j in range(M)])          # T_j(0)
# d/dx T_j(0) = 2 * (-1)^(j-1) * j^2
T1 = np.zeros(M)
T1[1:] = 2.0 * ((-1.0) ** (np.arange(1, M) - 1)) * (np.arange(1, M) ** 2)
# d2/dx2 T_j(0) = 4 * (-1)^j * j^2 (j^2 - 1) / 3
T2 = np.zeros(M)
js = np.arange(1, M, dtype=float)
T2[1:] = 4.0 * ((-1.0) ** (np.arange(1, M))) * js**2 * (js**2 - 1) / 3.0
# d3/dx3 T_j(0) = -8 (-1)^j j^2 (j^2-1)(j^2-4) / 15
T3 = np.zeros(M)
T3[1:] = -8.0 * ((-1.0) ** (np.arange(1, M))) * js**2 * (js**2 - 1) * (js**2 - 4) / 15.0

Ctail = np.zeros((M, M))
for i, yy in enumerate(y):
    z2 = float(mzeta(2, NTAIL + 1 + yy))
    z3 = float(mzeta(3, NTAIL + 1 + yy))
    z4 = float(mzeta(4, NTAIL + 1 + yy))
    z5 = float(mzeta(5, NTAIL + 1 + yy))
    Ctail[i, :] = T0 * z2 + T1 * z3 + 0.5 * T2 * z4 + (1.0 / 6.0) * T3 * z5

C = Ctrunc + Ctail

# The collocation problem is (Lf)(y_i) = lambda f(y_i) with f(y_i) = sum_j
# c_j T_j(y_i). That is a GENERALISED eigenvalue problem  C c = lambda V c,
# where V[i,j] = T_j(y_i) is the (scaled) discrete cosine transform. Pull
# it to coefficient space:  A = V^{-1} C,  then  A c = lambda c.
V = cheb_eval(y)                          # (M, M) value matrix at nodes
A = np.linalg.solve(V, C)

evals, evecs = np.linalg.eig(A)
# Sort by MODULUS, not real part: the negative eigenvalue -0.30366 (Wirsing)
# is the second largest by modulus but sits BELOW the positive tail by real
# part (+0.10088 > -0.30366), so a real-part sort mislabels it as lambda_3.
order = np.argsort(-np.abs(evals))
evals = evals[order]
evecs = evecs[:, order]

KNOWN = {1: "+1.000000000000", 2: "-0.303663002899", 3: "+0.1008845099..."}
print("GKW transfer operator, Chebyshev collocation, M =", M)
for k in range(6):
    lam = evals[k]
    known = KNOWN.get(k + 1, "")
    print(f"  lambda_{k+1:<2} = {lam.real:+.12f}  im={lam.imag:.2e}   {known}")

# --- sanity: leading eigenvector vs Gauss density ------------------------
# eigenvector c is in coefficient space; evaluate at the nodes: V c
h = 1.0 / ((1.0 + y) * np.log(2.0))
v1 = V @ np.real(evecs[:, 0])
v1 /= v1[0] / h[0]
print(f"\n|v1 - Gauss density|_inf (normalised) = {np.max(np.abs(v1 - h)):.3e}")
lam2 = evals[1].real
print(f"lambda_2 = {lam2:+.12f}   known Wirsing -0.303663002899...  "
      f"(agree {int(-np.log10(abs(lam2 + 0.303663002899)))} digits)")
lam = abs(lam2)

# --- the empirical point: can a walk ever hear the sign? -----------------
Ns = np.logspace(1, 8, 400)
dd = np.abs(np.log(lam) * Ns + 0.5 * np.log(Ns))
i = int(np.argmin(dd))
print(f"\n|lambda_2|^N falls below Poisson noise 1/sqrt(N) at N ~= {Ns[i]:.0f}")
print(f"at N = 1M rungs: 0.30366^N = 10^{np.log10(lam) * 1e6:+.0f}  vs noise 10^-3")

# Wirsing eigenvector (index 1 by modulus) sampled densely for the sound
Md = 512
yd = (np.arange(Md) + 0.5) / Md
Td = cheb_eval(yd)
h2_d = Td @ np.real(evecs[:, 1])
h2_d /= np.max(np.abs(h2_d))

np.savez_compressed("assets/gkw-spectrum.npz",
                    y=yd, h2=h2_d, h=1.0 / ((1.0 + yd) * np.log(2.0)),
                    lam2=lam2, lam1=1.0)
print("\nsaved assets/gkw-spectrum.npz (dense Wirsing eigenfunction h2, %d pts)" % Md)
