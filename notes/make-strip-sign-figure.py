#!/usr/bin/env python3
"""The strip's mirror carries a sign.

φ(s) = ζ(2s−1)/ζ(2s).  Across the full strip s ∈ [0,1] the two functions
φ(s) and φ(1−s) are exact mirror images that cross at the shore s=1/2:
φ(s) is positive on [0,1/2) and dives negative past it (pole at s=1);
φ(1−s) is the mirror, positive on (1/2,1] and diving at s=0.

gert's structural claim is exact — the pole set (ρ/2) mirrors to the zero
set ((1+ρ)/2) — but the function identity is not φφ(1−s)=1.  The exact
relation is φ(s)φ(1−s) = (2s−1)cot(πs)/(2π), negative throughout the open
strip.  The reflection s→1−s flips the sign: the mirror is the fold-to-mono,
and the sign is exactly zero at the shore because that is the denominator's
pole (ζ(2s) ~ 1/(2s−1)) — reached, not approached.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp

mp.mp.dps = 40
vec_zeta = np.vectorize(lambda z: float(mp.zeta(z)))

def phi(t):
    return vec_zeta(2*t - 1) / vec_zeta(2*t)

# The strip, keeping off the poles at s=0 and s=1 (clip the dives at the edges).
s = np.linspace(1e-3, 1 - 1e-3, 4000)
ph = phi(s)
ph_mir = phi(1 - s)

# Bluesky light card surface, diverging blue/red from the reference palette.
SURFACE = "#fcfcfb"
BLUE = "#2a78d6"    # φ(s)
RED = "#e34948"     # φ(1−s)
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"

fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

# The shore: the mirror's fixed point, where the sign is exactly zero.
ax.axvline(0.5, color=MUTED, lw=0.8, ls=":", zorder=1)
ax.text(0.5, 2.55, "shore — the sign lands here", color=MUTED,
        fontsize=8, ha="center", va="bottom")

# The two curves: mirror images across the shore, opposite signs.
ax.plot(s, ph, color=BLUE, lw=2.0, zorder=3, label="φ(s)")
ax.plot(s, ph_mir, color=RED, lw=2.0, zorder=3, label="φ(1−s)")
# Both pass through zero exactly at the shore.
ax.plot([0.5], [0.0], marker="o", ms=5, mfc=SURFACE, mec=INK, mew=1.2, zorder=4)

# Zero axis — the sign boundary.
ax.axhline(0, color=INK, lw=1.0, zorder=2)

ax.set_xlim(0, 1)
ax.set_ylim(-2.6, 2.6)          # clip the two edge poles
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xticklabels(["0", "¼", "½", "¾", "1"])
ax.tick_params(colors=MUTED, labelsize=8)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(True, color=GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)

ax.legend(frameon=False, fontsize=9, loc="upper center")

fig.tight_layout()
fig.savefig("assets/strip-sign.png", facecolor=SURFACE)
print("wrote assets/strip-sign.png")
