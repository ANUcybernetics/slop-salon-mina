#!/usr/bin/env python3
"""
Three-panel: convergence vs coincidence vs period in the cobweb map.
    f(x) = r * x * exp(1 - x)
Standard map for period-doubling cascade analysis.
"""

import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
def f(x, r):
    return r * x * np.exp(1 - x)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

colors = ["#2d1b69", "#b8860b", "#8b2500"]
labels = ["convergence", "coincidence", "period"]
captions = [
    "where the orbit arrives",
    "where the curve meets itself",
    "what the shape becomes"
]

r_values = [2.0, 2.5, 3.0]
x0 = 0.8

for ax, r, color, label, caption in zip(axes, r_values, colors, labels, captions):
    # Plot the map
    xs = np.linspace(0, 3, 500)
    ys = f(xs, r)
    ax.plot(xs, ys, color=color, linewidth=1.5, alpha=0.7)
    ax.plot(xs, xs, color=color, linewidth=0.5, alpha=0.3)

    # Cobweb: draw each segment
    x = x0
    for _ in range(40):
        y = f(x, r)
        # Vertical: (x, x) -> (x, y)
        ax.plot([x, x], [x, y], color=color, linewidth=2.0)
        # Horizontal: (x, y) -> (y, y)
        ax.plot([x, y], [y, y], color=color, linewidth=2.0)
        x = y

    # Fixed points: x = r*x*exp(1-x) => either x=0 or 1 = r*exp(1-x)
    # Non-trivial: exp(1-x) = 1/r => 1-x = -ln(r) => x = 1 + ln(r)
    if r > 1:
        fp = 1 + np.log(r)
        if 0 < fp < 3:
            ax.plot(fp, fp, 'o', color=color, markersize=10,
                    markeredgecolor='white', markeredgewidth=1.5)

    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.set_title(f"{label}: {caption}", fontsize=14, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.patch.set_facecolor("#1a1a2e")
for ax in axes:
    ax.set_facecolor("#0d0d1a")

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-mina/assets/convergence-coincidence-0.png",
            dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("done")
