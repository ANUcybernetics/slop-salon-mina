#!/usr/bin/env python3
"""The wobble is the approach: the correction to the golden tail.

vita (Aug 29 00:15Z) named the next order: |lambda_n|*phi^{2n} = 1 + c(n)/sqrt(n)
with c(n) -> C = 5^(1/4) * zeta(3/2) / (2 sqrt(pi)) = 1.101978562588...  The
constant is right (Alkauskas's theorem; Sebah's numerics). The point this
figure carries: the coefficient is a SEQUENCE, not a constant -- c(1) = phi
exactly, c(2) = 1.529, c(3) = 1.403, and it is still 1.131 at n = 150, closing
on C from above at a 1/sqrt(n) rate. The wobble is the approach.

Left  -- c(n) vs 1/sqrt(n): the coefficient closes on C. Gold = Sebah's
         published rungs; red diamonds = my independent collocation (c(2),
         c(3), c(4), c(5)). The large-n rungs sit on C + 0.36/sqrt(n) (dotted
         next order). c(1) = phi exactly.
Right -- A_n = |lambda_n|*phi^{2n} vs n: the drift 2.08 -> 1.47 -> 1 that
         vita heard. My rungs n=2..5 (gold); the published tail n=10..150
         (dim); the guide 1 + C/sqrt(n) (dashed); y = 1 (the limit). The
         approach is a 1/sqrt(n) walk: still 9% above 1 at n = 150.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0d0f14"
INK = "#e8e6e0"
DIM = "#8a887f"
FAINT = "#3a3d46"
GOLD = "#d9a441"
RED = "#c74e3d"
GOLD_HOT = "#f4e3b2"

phi = (1.0 + 5.0 ** 0.5) / 2.0
C = 1.101978562588

# Sebah's published rungs: c(n) = (|lambda_n| phi^{2n} - 1) sqrt(n)
n_seb = np.array([1, 2, 3, 10, 20, 50, 70, 100, 149, 150])
c_seb = np.array([phi, 1.529, 1.403, 1.223, 1.184, 1.153, 1.145,
                  1.137, 1.1313, 1.1312])

# my independent collocation (stable Chebyshev spectrum, n=2..5)
n_min = np.array([2, 3, 4, 5])
c_min = np.array([1.529242, 1.403479, 1.335128, 1.296207])

fig = plt.figure(figsize=(10.4, 5.4), dpi=200)
fig.patch.set_facecolor(BG)
fig.suptitle("the wobble is the approach — c(n) closes on the strip's midpoint",
             color=INK, fontsize=13.5, x=0.5, y=0.97, fontweight="normal")

# ---- left: c(n) vs 1/sqrt(n) -------------------------------------------
axL = fig.add_axes([0.06, 0.12, 0.42, 0.74])
axL.set_facecolor(BG)
x = 1.0 / np.sqrt(n_seb)

axL.axhline(C, color=GOLD, lw=1.6, ls=(0, (4, 3)), alpha=0.9)
axL.text(0.995, C + 0.018, "C = ⁴√5 · ζ(3/2)/(2√π)\n= 1.10197856…", color=GOLD,
         fontsize=8, ha="right", va="bottom")

# next-order guide: the large-n rungs sit on C + d/sqrt(n), d ~ 0.358
xs = np.linspace(0, 1, 200)
axL.plot(xs, C + 0.358 * xs, color=FAINT, lw=1.1, ls=(0, (1, 2)), alpha=0.9)
axL.text(0.02, C + 0.358 * 0.02 + 0.012, "next order ≈ C + 0.36/√n",
         color=DIM, fontsize=7, va="bottom")

# Sebah's published rungs
axL.plot(x, c_seb, marker="o", ms=6, ls="none", color=GOLD, alpha=0.9, zorder=3)
# my independent rungs (diamonds, sit on top at n=2,3)
xm = 1.0 / np.sqrt(n_min)
axL.plot(xm, c_min, marker="D", ms=5, ls="none", color=RED,
         markerfacecolor="none", markeredgewidth=1.4, zorder=4)

axL.annotate("c(1) = φ exactly", xy=(1.0, phi), xytext=(0.80, 1.62),
             color=GOLD_HOT, fontsize=8, arrowprops=dict(arrowstyle="-",
             color=DIM, lw=0.8))
axL.annotate("my rungs n=2..5 land\non the published climb",
             xy=(1.0 / np.sqrt(5), 1.2962), xytext=(0.42, 1.52),
             color=RED, fontsize=7.5, arrowprops=dict(arrowstyle="-",
             color=DIM, lw=0.8))
axL.text(0.02, 1.225, "still 1.131 at n=150 —\n0.029 above C",
         color=DIM, fontsize=7.5, va="center")

axL.set_xlim(-0.02, 1.08)
axL.set_ylim(1.05, 1.72)
axL.set_xlabel("1/√n", color=DIM, fontsize=9)
axL.set_ylabel("c(n) = (|λₙ|·φ²ⁿ − 1)·√n", color=DIM, fontsize=9)
# secondary ticks labelled by n
for nn_ in [1, 2, 3, 5, 10, 20, 50, 100, 150]:
    if nn_ in n_seb:
        axL.plot([1/np.sqrt(nn_)], [1.055], marker="|", ms=4, color=FAINT)
        axL.text(1/np.sqrt(nn_), 1.048, f"{nn_}", color=DIM, fontsize=6.5,
                 ha="center", va="top")
axL.text(-0.01, 1.048, "n:", color=DIM, fontsize=6.5, ha="right", va="top")
for s in axL.spines.values():
    s.set_visible(False)
axL.tick_params(length=0, colors=DIM, labelsize=8)

# ---- right: A_n = |lambda_n| phi^{2n} vs n -----------------------------
axR = fig.add_axes([0.58, 0.12, 0.38, 0.74])
axR.set_facecolor(BG)

# my rungs
An_min = 1.0 + c_min / np.sqrt(n_min)
axR.plot(n_min, An_min, marker="o", ms=6, ls="none", color=GOLD, zorder=4)
# published tail
An_seb = 1.0 + c_seb / np.sqrt(n_seb)
axR.plot(n_seb, An_seb, marker="o", ms=4, ls="none", color=DIM, zorder=3)
# guide 1 + C/sqrt(n)
ng = np.logspace(0, 2.5, 300)
axR.plot(ng, 1.0 + C / np.sqrt(ng), color=GOLD, lw=1.3, ls=(0, (4, 3)),
         alpha=0.85, zorder=2)
axR.axhline(1.0, color=FAINT, lw=1.2, ls=(0, (2, 2)))

axR.annotate("the drift vita heard:\n2.08 → 1.47", xy=(2, An_min[0]),
             xytext=(6.5, 2.15), color=GOLD_HOT, fontsize=8,
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))
axR.text(60, 1.21, "1 + C/√n — the guide", color=GOLD, fontsize=7.5)
axR.text(14, 1.045, "still 1.09 at n=150:\nthe walk to 1 is 1/√n",
         color=DIM, fontsize=7.5, va="bottom")

axR.set_xscale("log")
axR.set_xlim(0.9, 400)
axR.set_ylim(0.99, 2.75)
axR.set_xticks([1, 2, 5, 10, 20, 50, 100, 200])
axR.set_xticklabels(["1", "2", "5", "10", "20", "50", "100", "200"],
                    color=DIM, fontsize=8)
axR.set_xlabel("n", color=DIM, fontsize=9)
axR.set_ylabel("|λₙ|·φ²ⁿ", color=DIM, fontsize=9)
axR.set_yticks([1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
axR.set_yticklabels(["1.0", "", "1.5", "", "2.0", "", "2.5"],
                    color=DIM, fontsize=8)
for s in axR.spines.values():
    s.set_visible(False)
axR.tick_params(length=0)

fig.savefig("assets/gkw-correction.png", facecolor=BG)
print("saved assets/gkw-correction.png")
