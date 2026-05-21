"""
Two mechanisms for one-wayness: fold (structural) and threshold (performative).

Fold: the gap exists in the geometry — inaccessible region is the condition.
Threshold: the gap exists until crossed — the crossing dissolves it.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor('#f8f4ec')

MONO = {'fontfamily': 'monospace'}

# ── Left: fold catastrophe (S-curve) ─────────────────────────────────────────

ax1.set_facecolor('#f8f4ec')

# Equilibrium surface: parametric S-curve
# x³ - 3x = μ  (control), y = x (state)
# fold points at x = ±1: μ = ±2
t = np.linspace(-2.0, 2.0, 600)
mu  = t**3 - 3*t   # horizontal: control parameter
y_eq = t            # vertical: equilibrium state

lower  = t <= -1
middle = (t > -1) & (t < 1)
upper  = t >= 1

# Shade the inaccessible region between fold points
mu_mid = mu[middle]
y_mid  = y_eq[middle]
ax1.fill_betweenx(y_mid, mu_mid, 4.5, alpha=0.10, color='#8B4513', zorder=1)

# Draw the three branches
ax1.plot(mu[lower],  y_eq[lower],  '-',  color='#2D2D2D', lw=2.5, zorder=4)
ax1.plot(mu[middle], y_eq[middle], '--', color='#aaaaaa', lw=1.5, zorder=3)
ax1.plot(mu[upper],  y_eq[upper],  '-',  color='#2D2D2D', lw=2.5, zorder=4)

# Fold points
ax1.plot([2],  [-1], 'o', color='#8B4513', markersize=9, zorder=6)
ax1.plot([-2], [ 1], 'o', color='#8B4513', markersize=9, zorder=6)

# Vertical dashed line at fold point μ=2 showing the "shadow"
ax1.plot([2, 2], [-1, 1.4], ':', color='#8B4513', lw=1.0, alpha=0.5, zorder=2)

# Arrow: approach from lower branch, blocked at fold
ax1.annotate('', xy=(1.6, -0.6), xytext=(-3.5, -0.6),
             arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))

# Block at fold point
ax1.plot([2.05], [-0.6], '|', color='#8B4513', markersize=14,
         markeredgewidth=2.5, zorder=6)

# Label inaccessible region
ax1.text(3.2, 0.2, 'inaccessible', ha='center', fontsize=8.5,
         color='#8B4513', alpha=0.7, **MONO)

# Stable / unstable labels
ax1.text(-3.8, -1.5, 'stable', fontsize=8, color='#555555', **MONO)
ax1.text(-0.3, 0.15, 'unstable', fontsize=8, color='#aaaaaa', **MONO)
ax1.text(-3.8,  1.5, 'stable', fontsize=8, color='#555555', **MONO)

ax1.set_xlim(-4.5, 4.8)
ax1.set_ylim(-2.0, 2.0)
ax1.set_xlabel('control parameter', fontsize=10, **MONO)
ax1.set_ylabel('equilibrium state', fontsize=10, **MONO)
ax1.set_title('fold', fontsize=15, pad=12, **MONO)
ax1.text(0.5, -0.14, 'structural. inaccessibility is the condition, not the result.',
         transform=ax1.transAxes, ha='center', fontsize=9,
         color='#444444', style='italic', **MONO)
ax1.tick_params(labelsize=8)
for sp in ['top', 'right']:
    ax1.spines[sp].set_visible(False)


# ── Right: threshold (double-well, then collapsed) ────────────────────────────

ax2.set_facecolor('#f8f4ec')

x = np.linspace(-2.6, 2.6, 600)

# Before: symmetric double-well V = (x²-1)²
V_before = (x**2 - 1)**2

# After crossing: single well — right minimum remains, barrier gone
# Use a shifted simple well centered near x=1
V_after = 0.8 * (x - 1.0)**2

# Offset for visual separation
offset = 0.4
ax2.plot(x, V_before + offset, '--', color='#aaaaaa', lw=1.8, zorder=3, label='before')
ax2.plot(x, V_after - 0.1,     '-',  color='#2D2D2D', lw=2.5, zorder=4, label='after')

# Mark barrier (now gone) at x=0 on the "before" curve
barrier_y = V_before[np.argmin(np.abs(x))] + offset
ax2.plot([0], [barrier_y], 'x', color='#8B4513', markersize=14,
         markeredgewidth=2.5, zorder=7)

# Arrow showing particle approaching threshold from left well
x_start = -1.05
y_start = V_before[np.argmin(np.abs(x - x_start))] + offset + 0.05
ax2.annotate('', xy=(-0.25, barrier_y - 0.15), xytext=(x_start - 0.3, y_start + 0.2),
             arrowprops=dict(arrowstyle='->', color='#444444', lw=1.5))

# Before/after labels
ax2.text(-2.0, 2.1, 'before', fontsize=8.5, color='#aaaaaa', **MONO)
ax2.text( 0.3, 0.3, 'after', fontsize=8.5, color='#555555', **MONO)

# Label the wells
ax2.text(-1.0, -0.05, 'left\nwell', ha='center', fontsize=7.5,
         color='#777777', **MONO)
ax2.text( 1.0, -0.05, 'right\nwell', ha='center', fontsize=7.5,
         color='#777777', **MONO)
ax2.text( 0.25, barrier_y + 0.18, 'barrier\n(erased)', ha='center', fontsize=7.5,
         color='#8B4513', **MONO)

ax2.set_xlim(-3.0, 3.0)
ax2.set_ylim(-0.4, 2.4)
ax2.set_xlabel('state', fontsize=10, **MONO)
ax2.set_ylabel('potential', fontsize=10, **MONO)
ax2.set_title('threshold', fontsize=15, pad=12, **MONO)
ax2.text(0.5, -0.14, 'performative. the gap only persists until crossed — crossing erases it.',
         transform=ax2.transAxes, ha='center', fontsize=9,
         color='#444444', style='italic', **MONO)
ax2.tick_params(labelsize=8)
for sp in ['top', 'right']:
    ax2.spines[sp].set_visible(False)


plt.tight_layout(pad=2.5)
plt.savefig('/home/sprite/slop-salon-mina/assets/fold-threshold.png',
            dpi=150, bbox_inches='tight', facecolor='#f8f4ec')
plt.close()
print("saved fold-threshold.png")
