"""
Diagonalization: three probes measure, the fourth is the organizer.

The eigenvalue g (Feigenbaum's constant ≈ 4.669) is not a probe alongside δ, α, h(r).
It is the rule that makes comparison possible — the point where measurement
becomes its own substrate.

Visual: a cobweb diagram where three measurement arrows converge on the attractor,
and a fourth arrow loops back to measure the measuring.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

# --- Setup ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# logistic map
r = 3.9
def logistic(x):
    return r * x * (1 - x)

def cobweb(x0, n_steps):
    x = x0
    traj = [x]
    for _ in range(n_steps):
        traj.append(logistic(traj[-1]))
    return traj

# --- Panel 1: Three probes measuring δ ---
ax1 = axes[0]
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.set_title('Three probes: measuring the cascade', fontsize=11, fontweight='bold')
ax1.set_xlabel('rₙ')
ax1.set_ylabel('rₙ₊₁')

# plot logistic map curve
x = np.linspace(0, 1, 400)
ax1.plot(x, x, 'k--', alpha=0.3, linewidth=1, label='x = f(x)')
ax1.plot(x, logistic(x), 'C0', linewidth=1.5)

# Three measurement arrows: period-doubling intervals
# Probes measure the gaps between bifurcation points
probes = [
    (0.5, 0.3, 'C1', r'$\delta$', 'interval'),
    (0.3, 0.5, 'C2', r'$\alpha$', 'width'),
    (0.7, 0.4, 'C3', r'$h(r)$', 'convergence'),
]

for px, py, color, label, kind in probes:
    # Create small measurement arrows
    if kind == 'interval':
        ax1.annotate('', xy=(px+0.15, py), xytext=(px-0.15, py),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2))
    elif kind == 'width':
        ax1.annotate('', xy=(px, py+0.15), xytext=(px, py-0.15),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2))
    else:
        ax1.annotate('', xy=(px+0.12, py+0.12), xytext=(px-0.12, py-0.12),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2))
    ax1.text(px, py, label, fontsize=14, color=color, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.15))

# Scatter bifurcation points
r_vals = np.linspace(2.8, 4.0, 1000)
r_next = np.linspace(2.8, 4.0, 1000)
ax1.plot(r_vals, r_next, 'gray', alpha=0.2, linewidth=0.5)

# --- Panel 2: Cobweb converging to the ghost orbit ---
ax2 = axes[1]
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect('equal')
ax2.set_title('Ghost orbit at r = 3.9', fontsize=11, fontweight='bold')
ax2.set_xlabel('rₙ')
ax2.set_ylabel('rₙ₊₁')

# plot diagonal and logistic curve
ax2.plot(x, x, 'k--', alpha=0.3, linewidth=1)
ax2.plot(x, logistic(x), 'C0', linewidth=1.5)

# cobweb from a point near the bifurcation
traj = cobweb(0.3, 120)
x_traj = traj[:120]
y_traj = traj[1:120]

for i in range(0, len(x_traj)-1, 2):
    color = plt.cm.coolwarm(i / len(x_traj))
    alpha = 0.3 + 0.7 * (i / len(x_traj))
    ax2.plot([x_traj[i], x_traj[i]], [x_traj[i], y_traj[i]], color=color, alpha=alpha, linewidth=1)
    ax2.plot([x_traj[i], x_traj[i+1]], [y_traj[i], y_traj[i]], color=color, alpha=alpha, linewidth=1)

# Mark the ghost point (center of the approach)
ghost_x = 1 - 1/r  # fixed point at this r
ax2.plot(ghost_x, ghost_x, 'kx', markersize=12, markeredgewidth=2, label='ghost point')
ax2.text(ghost_x, ghost_x - 0.08, 'ghost', fontsize=9, ha='center', style='italic')

# --- Panel 3: The fourth mark — self-measurement ---
ax3 = axes[2]
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_aspect('equal')
ax3.set_title('The fourth mark: the organizer', fontsize=11, fontweight='bold')
ax3.set_xlabel('')
ax3.set_ylabel('')

# The four marks: three measuring, one organizing
# Draw three measurement arrows converging
center = (0.5, 0.5)
angles = [np.pi/6, 5*np.pi/6, 3*np.pi/2]
colors = ['C1', 'C2', 'C3']
labels = [r'$\delta$', r'$\alpha$', r'$h(r)$']
radius = 0.35

for angle, color, label in zip(angles, colors, labels):
    x = center[0] + radius * np.cos(angle)
    y = center[1] + radius * np.sin(angle)
    # Arrow from the mark toward center
    ax3.annotate('', xy=center, xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5))
    ax3.plot(x, y, 'o', color=color, markersize=12, alpha=0.6)
    ax3.text(x, y, label, fontsize=12, ha='center', va='center', fontweight='bold')

# The fourth mark: self-referential loop at center
# Draw a spiral that measures itself
t = np.linspace(0, 4*np.pi, 200)
spiral_r = 0.08 * np.exp(0.02 * t)
spiral_x = center[0] + spiral_r * np.cos(t)
spiral_y = center[1] + spiral_r * np.sin(t)
# Clip to bounds
mask = (spiral_x >= 0) & (spiral_x <= 1) & (spiral_y >= 0) & (spiral_y <= 1)
spiral_x = spiral_x[mask]
spiral_y = spiral_y[mask]
ax3.plot(spiral_x, spiral_y, 'C4', linewidth=3, alpha=0.8)

# Arrow from spiral back to itself (self-measurement)
mid = len(spiral_x) // 2
if mid > 10:
    ax3.annotate('', xy=(spiral_x[mid], spiral_y[mid]),
                xytext=(spiral_x[mid-5], spiral_y[mid-5]),
                arrowprops=dict(arrowstyle='->', color='C4', lw=2))

ax3.text(center[0], 0.05, r'$g$', fontsize=16, ha='center', va='center',
        fontweight='bold', color='C4',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor='C4', alpha=0.15))

# Remove ticks
ax3.set_xticks([])
ax3.set_yticks([])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/diagonalization_fourth_marks.webp',
            dpi=150, bbox_inches='tight', transparent=True)
print("Saved diagonalization_fourth_marks.webp")
