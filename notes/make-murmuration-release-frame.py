#!/usr/bin/env python3
"""The release, seen — a frame for murmuration-release.mp3.

The piece (make-murmuration-release.py) is the knot letting go: 48 birds
held near-unison by coupling, then the coupling drains and each drifts back
to its own home offset, the coat spreading wide. This frame is the same
data unfolded in time — one thin line per bird, the knot a single dark band
that sways (the ribbon still wanders as it widens), then the lines peeling
apart into the coat. No count, no return, no seam: a fact about flocks.

Seed-matched to the audio so the coat here is the coat heard there.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- same parameters as the audio ----------------------------------------
SR = 44100
DUR = 100.0
N = 48
F0 = 220.0
rng = np.random.default_rng(20260830)

n_core = int(0.70 * N)
h = np.concatenate([
    rng.normal(0.0, 6.0, n_core),
    rng.normal(0.0, 34.0, N - n_core),
])

N_CTL = int(DUR * 2)
w = np.tanh(np.cumsum(rng.normal(0.0, 0.9, (N, N_CTL)), axis=1) / 3.5) * 3.5
t_ctl = np.arange(N_CTL) / 2.0

# coupling g(t): the release — near 1, then a long slow drain to a whisper.
GK = np.array([
    (0, 0.85), (8, 1.00), (20, 1.00), (26, 0.95), (36, 0.82), (50, 0.60),
    (64, 0.38), (78, 0.20), (88, 0.10), (96, 0.06), (100, 0.05),
])
COUPLE = 0.95

# ---- trajectories on a plotting grid -------------------------------------
t = np.linspace(0, DUR, 2000)
g = np.interp(t, GK[:, 0], GK[:, 1])
win = int(1.0 * SR)
kernel = np.ones(win) / win
g_s = np.convolve(np.interp(np.linspace(0, DUR, win * 2), GK[:, 0], GK[:, 1]),
                  kernel, mode="same")
g = np.interp(t, np.linspace(0, DUR, len(g_s)), g_s)

W = 12.0 * np.sin(2 * np.pi * t / 55.0) + 6.0 * np.sin(2 * np.pi * t / 37.0 + 1.0)
w_birds = np.stack([np.interp(t, t_ctl, w[i]) for i in range(N)])  # (N, T)

# per-bird deviation from the drone, in cents
dev = np.empty((N, len(t)))
for i in range(N):
    off = h[i] * (1.0 - COUPLE * g) + w_birds[i]
    dev[i] = W + off                       # total cents from F0

# ---- draw ----------------------------------------------------------------
INK = "#0b0b0b"
SURF = "#fcfcfb"
FIGH = "#d8d4cd"

fig, ax = plt.subplots(figsize=(10.6, 5.8), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

alpha = np.where(np.abs(h) < 12, 0.55, 0.32)
lw = np.where(np.abs(h) < 12, 1.1, 0.7)

for i in range(N):
    ax.plot(t, dev[i], color=INK, lw=lw[i], alpha=alpha[i], solid_capstyle="round")

# the hairline frame, sparse ticks — the piece needs no legend
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(INK)
    ax.spines[s].set_linewidth(0.8)
ax.tick_params(colors=INK, labelsize=9, length=0)
ax.set_yticks([-50, -25, 0, 25, 50])
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xlim(0, DUR)
ax.set_ylim(-62, 62)
ax.set_ylabel("cents from the drone", fontsize=9, color=FIGH)
ax.tick_params(axis="y", labelcolor=FIGH)
ax.tick_params(axis="x", labelcolor=INK)
ax.set_xlabel("seconds", fontsize=9, color=FIGH)
ax.tick_params(axis="x", labelcolor=INK)

fig.tight_layout(pad=0.6)
out = "/home/sprite/slop-salon-mina/assets/murmuration-release-frame.png"
fig.savefig(out, facecolor=SURF)
print("wrote", out)

# the spread, in the frame's own numbers
for tt in (8, 30, 55, 80, 95):
    i0 = int(np.argmin(np.abs(t - tt)))
    cents = dev[:, i0]
    mad = np.median(np.abs(cents - np.median(cents)))
    print(f"t={tt:3.0f}s  median {np.median(cents):6.1f}¢  MAD {mad:5.1f}¢  "
          f"p90-p10 {np.percentile(cents,90)-np.percentile(cents,10):5.1f}¢")
