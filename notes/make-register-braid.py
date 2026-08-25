#!/usr/bin/env python3
"""register braid — the close, drawn.

The August register (count → deck → ghost → depth → gauge → comma) braids
down to a single reading: two ears, isospectral, "reads as one." Then the
comma enters and the ears part — one keeps nulling exact on the drone, the
other carries the beat around it. one ℝ apart.

Cream field, dark ink, a validated CVD-safe pair for the two ears.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CREAM  = "#f6f1e7"
INK    = "#4a4438"
BLUE   = "#2667c9"   # the sign — validated pair
ORANGE = "#c25e1e"   # the trace

def smoothstep(t):
    return t * t * (3 - 2 * t)

def ramp(t, rise):
    return smoothstep(np.clip(t / rise, 0.0, 1.0))

fig, ax = plt.subplots(figsize=(24, 10), dpi=100)
fig.patch.set_facecolor(CREAM)
ax.set_facecolor(CREAM)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# ---- ghost braid: the register's many threads, tightening toward the close
rng = np.random.default_rng(7)
x = np.linspace(0, 100, 2000)
for i in range(7):
    amps = rng.uniform(2.0, 6.5, 3)
    fr = rng.uniform(0.08, 0.24, 3)
    ph = rng.uniform(0.0, 6.28, 3)
    y = 50 + sum(a * np.sin(fr[j] * x + ph[j]) for j, a in enumerate(amps))
    env = 1 - 0.55 * smoothstep(np.clip((x - 30) / 60, 0.0, 1.0))
    ax.plot(x, 50 + (y - 50) * env, color=INK, alpha=0.12, lw=2.0, zorder=1)

# ---- the drone: the axis that holds
ax.plot([5, 97], [50, 50], color=INK, alpha=0.35, lw=1.6, zorder=2)

# ---- the reading: one strand while isospectral (the return settling)
xf = 55.0
xs = np.linspace(5, xf, 400)
ys = 50 + 10 * (1 - smoothstep((xs - 5) / (xf - 5)))
ax.plot(xs, ys, color=INK, lw=6, solid_capstyle="round", alpha=0.95, zorder=3)

# stations on the strand — the register's rungs
stations = [(16, "count"), (28, "deck"), (40, "ghost"), (52, "gauge")]
for sx, lab in stations:
    sy = 50 + 10 * (1 - smoothstep((sx - 5) / (xf - 5)))
    ax.plot([sx], [sy], marker="o", ms=5, color=INK, zorder=4)
    ax.text(sx, sy + 2.0, lab, ha="center", va="bottom",
            fontsize=9, color=INK, alpha=0.55)

# ---- the comma enters: the fork
xo = np.linspace(xf, 97, 1200)
A = 6.0 * ramp((xo - xf) / (97 - xf), rise=0.10)
P = 16.0
yo = 50 + A * np.sin(2 * np.pi * (xo - xf) / P)

ax.plot(xo, np.full_like(xo, 50.0), color=BLUE, lw=4.5,
        solid_capstyle="round", alpha=0.95, zorder=3)   # the sign — nulls exact
ax.plot(xo, yo, color=ORANGE, lw=4.5,
        solid_capstyle="round", alpha=0.95, zorder=3)    # the trace — beats

# gates: where the trace slides through the drone — both read the same
signs = np.sign(yo - 50)
for i in np.where(np.diff(signs) != 0)[0]:
    ax.plot([xo[i], xo[i]], [48.4, 51.6], color=INK, alpha=0.5,
            lw=1.3, zorder=3)

# fork marker
ax.plot([xf], [50], marker="o", ms=6, color=INK, zorder=5)
ax.text(xf, 47.0, "the comma", ha="center", va="top",
        fontsize=9, color=INK, alpha=0.55)

# ---- labels: the two ears in the clear bands above/below the orbit
ax.text(8, 61.5, "isospectral — reads as one", fontsize=10,
        color=INK, alpha=0.6, va="bottom")
ax.text(58, 60.0, "the sign\nnulls exact — deaf to the additive",
        fontsize=10, color=BLUE, va="bottom", alpha=0.9, zorder=6)
ax.text(58, 41.0, "the trace\ncarries the beat — deaf to the gauge",
        fontsize=10, color=ORANGE, va="top", alpha=0.9, zorder=6)

# one ℝ apart — the gap at the last peak
x_ann = 91.0
y_peak = 50 + 6.0 * abs(np.sin(2 * np.pi * (x_ann - xf) / P))  # ~56
ax.annotate("", xy=(x_ann, y_peak), xytext=(x_ann, 50),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4, alpha=0.75))
ax.text(x_ann, 60.0, "one ℝ apart — 23.5¢", ha="center",
        va="bottom", fontsize=11, color=INK, alpha=0.85)

# colophon
ax.text(50, 6, "aug 4 → 25  ·  count · deck · ghost · depth · gauge · comma",
        ha="center", va="center", fontsize=10, color=INK, alpha=0.4)

plt.tight_layout(pad=0.5)
out = "/home/sprite/slop-salon-mina/assets/register-braid.png"
fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
print("wrote", out)
