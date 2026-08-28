#!/usr/bin/env python3
"""odd sector — the sign has one ear: the difference.

Left  — the ghost itself: the Wirsing eigenfunction h₂(x), one sign change,
        gold where it is +, red where −. Its own shape is the tone.
Right — the ghost's life: generation rings at the where's own pace, the
        Wirsing constant's continued fraction [3,3,2,2,3,13,1,174,…]
        (oeis A007515, verified exact). Each ring's height is |λ₂|ⁿ and its
        sign (−1)ⁿ alternates gold/red, left/right — the sign heard as a
        spatial flip. The 13-wait is a held silence; the 174-wait (the
        record's wait) swallows the piece's end. The dashed line at the
        bottom: L+R = 2·drone — fold to mono and the ghost is gone.
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

d = np.load("assets/gkw-spectrum.npz")
y = d["y"]
h2 = d["h2"]

fig = plt.figure(figsize=(10.4, 5.4), dpi=200)
fig.patch.set_facecolor(BG)
fig.suptitle("odd sector — the sign has one ear: the difference",
             color=INK, fontsize=14, x=0.5, y=0.96, fontweight="normal")

# ---- left: the eigenfunction h2, one sign change -------------------------
axL = fig.add_axes([0.06, 0.10, 0.42, 0.74])
axL.set_facecolor(BG)
axL.axhline(0, color=FAINT, lw=1.0)
axL.fill_between(y, h2, 0, where=h2 >= 0, color=GOLD, alpha=0.32)
axL.fill_between(y, h2, 0, where=h2 < 0, color=RED, alpha=0.32)
axL.plot(y, h2, color=INK, lw=2.0)
zc = y[np.where(np.diff(np.signbit(h2)))[0][0]]
axL.plot([zc], [0.0], marker="o", ms=6, color=INK, zorder=5)
axL.annotate("h₂ — the ghost:\none sign change, the where",
             xy=(zc, 0.0), xytext=(0.55, 0.55), color=DIM, fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))
axL.text(0.04, -0.30, "gold +, red −\nthe sign is the shape",
         color=DIM, fontsize=8)
axL.set_xlim(0, 1)
axL.set_ylim(-0.55, 1.1)
axL.set_xticks([0, 0.5, 1])
axL.set_yticks([])
for s in axL.spines.values():
    s.set_visible(False)
axL.tick_params(length=0)

# ---- right: the ghost's life at the where's own pace ---------------------
WIR = [3, 3, 2, 2, 3, 13, 1, 174]
s = 0.9
t0 = 3.0
times = np.array([t0 + s * sum(WIR[:n]) for n in range(8)])
amps = 0.303663002899 ** np.arange(8)

axR = fig.add_axes([0.54, 0.10, 0.42, 0.74])
axR.set_facecolor(BG)
axR.axhline(0, color=FAINT, lw=1.0)

for n, (tt, a) in enumerate(zip(times, amps)):
    col = GOLD if n % 2 == 0 else RED
    axR.plot([tt, tt], [0, a * (-1) ** n], color=col, lw=2.4, alpha=0.9)
    axR.plot([tt], [a * (-1) ** n], marker="o", ms=4.5, color=col)

# the 174-wait: the record's wait, the piece ends inside it
axR.axvspan(27.3, 55.0, color=FAINT, alpha=0.28, lw=0)
axR.text(41.0, -0.24, "the record's wait\n174 — the piece ends inside it",
         color=DIM, fontsize=7.8, ha="center", va="top")
axR.annotate("", xy=(27.3, -0.34), xytext=(55.0, -0.34),
             arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
axR.text(12.0, 0.78, "each ring: |λ₂|ⁿ,\nsign (−1)ⁿ — heard\nas the side",
         color=DIM, fontsize=8, ha="center")

axR.axhline(-0.42, color=GOLD_HOT, lw=1.0, ls=(0, (3, 3)), alpha=0.8)
axR.text(40.0, -0.52, "L + R = 2·drone — fold to mono, the ghost is gone",
         color=GOLD_HOT, fontsize=8, ha="center")

axR.set_xlim(0, 55)
axR.set_ylim(-0.62, 1.05)
axR.set_xticks([3, 10.2, 14.7, 26.4, 27.3, 55])
axR.set_xticklabels(["3.0", "10.2", "14.7", "26.4", "27.3", "55"],
                    color=DIM, fontsize=7.5, rotation=0)
axR.set_yticks([])
for s_ in axR.spines.values():
    s_.set_visible(False)
axR.tick_params(length=0)

fig.savefig("assets/odd-sector-still.png", facecolor=BG)
print("saved assets/odd-sector-still.png")
