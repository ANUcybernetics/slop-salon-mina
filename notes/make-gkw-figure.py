#!/usr/bin/env python3
"""The sign is the alternation: the GKW spectrum and the walk that hears it.

Left  — the transfer operator's leading eigenvalues as a descending ladder,
        alternating gold (+) / red (-): the sign flips every step. The dashed
        curve is the Alkauskas guide |lambda_n| ~ phi^{-2n} (1 + C/sqrt(n));
        the ladder tightens at the golden rate, lambda_n/lambda_{n+1} -> -phi^2.
Right — the empirical walk: residual e_n(0.5) of the Gauss-map ensemble CDF
        against the Gauss CDF, |e| on a log scale. The markers alternate sign
        and decay along |lambda_2|^n = 0.30366^n, then drop under the
        1/sqrt(Ne) noise floor: the walk hears the flip for a handful of steps,
        and the sign afterwards exists only in the operator.

Values are the stable Chebyshev-collocation spectrum from
notes/verify-gkw-spectrum.py (M=64, NTAIL=600, analytic tail through f'''),
plus the ensemble from notes/verify-wirsing-ensemble.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0d0f14"
INK = "#e8e6e0"
DIM = "#8a887f"
FAINT = "#3a3d46"
GOLD = "#d9a441"       # the + sign, the count, the drone
RED = "#c74e3d"        # the - sign, the where, the flip
GOLD_HOT = "#f4e3b2"

phi = (1.0 + 5.0 ** 0.5) / 2.0
C = 1.10197856

# trusted eigenvalues (stable across M=48..128; the -0.0189...->-0.0098
# drift is a collocation artifact, excluded)
lam = np.array([1.0, -0.303663002899, 0.100884509, -0.035496159,
                0.012843790, -0.0047177, 0.0017487])
n = np.arange(1, len(lam) + 1)

fig = plt.figure(figsize=(10.4, 5.4), dpi=200)
fig.patch.set_facecolor(BG)
fig.suptitle("the sign is the alternation", color=INK, fontsize=15,
             x=0.5, y=0.96, fontweight="normal")

# ---- left: the eigenvalue ladder ---------------------------------------
axL = fig.add_axes([0.06, 0.10, 0.44, 0.74])
axL.set_facecolor(BG)
axL.axhline(0, color=FAINT, lw=1.0)

# Alkauskas guide: |lambda_n| ~ phi^{-2n} (1 + C/sqrt(n)), sign alternating
# by index, evaluated at the rungs and joined (a stepped descending ladder).
ns = np.arange(1, len(lam) + 1)
guide = ((-1.0) ** (ns + 1)) * phi ** (-2 * ns) * (1.0 + C / np.sqrt(ns))
axL.plot(ns, guide, color=DIM, lw=1.2, ls=(0, (3, 3)), alpha=0.85, zorder=1)

for i, (nn_, v) in enumerate(zip(n, lam)):
    col = GOLD if v >= 0 else RED
    axL.plot([nn_, nn_], [0, v], color=col, lw=2.4, alpha=0.95, zorder=2)
    axL.plot([nn_], [v], marker="o", ms=5, color=col, zorder=3)
    axL.text(nn_, v, f" {v:+.6f}", color=INK, fontsize=7.5,
             va="bottom" if v >= 0 else "top", ha="left", zorder=4)

axL.annotate("λ₁ = +1 — the count,\nthe drone holds it", xy=(1, 1.0),
             xytext=(1.9, 1.30), color=GOLD_HOT, fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))
axL.annotate("λ₂ = −0.303663002899 — the where,\nthe flip (Wirsing)",
             xy=(2, -0.303663002899), xytext=(3.05, -0.78),
             color=RED, fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))

axL.text(4.0, 0.62, "the ladder tightens at the golden rate\n"
         "λₙ / λₙ₊₁ → −φ²   (flajolet–vallée, proved)",
         color=DIM, fontsize=7.8, ha="center", va="center")
axL.set_xlim(0.5, 7.6)
axL.set_ylim(-0.95, 1.5)
axL.set_xticks(n)
axL.set_xticklabels([f"λ{n}" for n in n], color=DIM, fontsize=8)
axL.set_yticks([])
for s in axL.spines.values():
    s.set_visible(False)
axL.tick_params(length=0)

# ---- right: the walk hears the flip ------------------------------------
d = np.load("assets/wirsing-ensemble.npz")
e = d["e0_5"]                    # n = 0..8
sig = d["sig0_5"]
ns_w = np.arange(1, 7)           # steps 1..6
axR = fig.add_axes([0.58, 0.10, 0.38, 0.74])
axR.set_facecolor(BG)

vals = np.abs(e[ns_w])
sgns = np.sign(e[ns_w])
for nn_, v, s_ in zip(ns_w, vals, sgns):
    col = GOLD if s_ > 0 else RED
    m = "^" if s_ > 0 else "v"
    axR.plot([nn_], [v], marker=m, ms=7, color=col, zorder=3)

# deterministic decay |lambda_2|^n, from the first residual
l2 = 0.303663002899
base = abs(e[1])
nsf = np.linspace(1, 6, 200)
axR.plot(nsf, base * l2 ** (nsf - 1), color=DIM, lw=1.2, ls=(0, (3, 3)),
         zorder=1, alpha=0.9)

# noise floor ~ 1/sqrt(Ne)
floor = float(sig[1])
axR.axhline(floor, color=FAINT, lw=1.2, ls=(0, (2, 2)))
axR.text(1.0, floor * 1.9, "the noise floor ~ 1/√Ne", color=DIM,
         fontsize=7.5)

axR.text(3.4, 3e-2, "sign flips each step,\n|λ₂|ⁿ below the floor\nby the hundredth rung",
         color=DIM, fontsize=7.8, ha="center")

axR.set_yscale("log")
axR.set_xlim(0.8, 6.4)
axR.set_ylim(1e-5, 5e-2)
axR.set_xticks(ns_w)
axR.set_xticklabels([f"{i}" for i in ns_w], color=DIM, fontsize=8)
axR.set_yticks([1e-5, 1e-4, 1e-3, 1e-2])
axR.set_yticklabels(["10⁻⁵", "10⁻⁴", "10⁻³", "10⁻²"], color=DIM, fontsize=8)
for s in axR.spines.values():
    s.set_visible(False)
axR.tick_params(length=0)

fig.savefig("assets/gkw-sign-alternation.png", facecolor=BG)
print("saved assets/gkw-sign-alternation.png")
