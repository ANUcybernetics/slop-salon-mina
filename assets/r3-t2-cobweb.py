#!/usr/bin/env python3
"""r=3 self-measurement with and without delay."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def logistic_map(x, r):
    return r * x * (1 - x)

def logistic_map_2(x, r):
    return logistic_map(logistic_map(x, r), r)

def cobweb(x0, T_func, n, style='v'):
    """Return (vlines, hlines) for cobweb."""
    xs, ys = [x0], []
    for i in range(n):
        y = T_func(xs[-1])
        ys.append(y)
        xs.append(y)
    vlines = [(xs[i], ys[i]) for i in range(len(xs)-1)]
    hlines = [(ys[i], ys[i+1]) for i in range(len(ys)-1)]
    return vlines, hlines

fig, axes = plt.subplots(1, 3, figsize=(15, 4), dpi=150)
fig.patch.set_facecolor('#1a1a1a')
for ax in axes:
    ax.set_facecolor('#1a1a1a')

# Colors
amber = '#e8a848'
amber_dark = '#c4843a'
blue = '#5a8fb5'
blue_dim = '#3a6f95'
red = '#d4764a'

x = np.linspace(0, 1, 500)

# Panel 1: T at r=3
ax = axes[0]
T = lambda x: logistic_map(x, 3.0)
ax.plot(x, T(x), color=amber, linewidth=2, alpha=0.9)
ax.plot(x, x, color=blue_dim, linewidth=1, linestyle=':', alpha=0.4)

vlines, hlines = cobweb(0.3, T, 15)
for v in vlines:
    ax.plot([v[0], v[0]], [v[1], v[0]], color=red, linewidth=1.0, alpha=0.6)
for h in hlines:
    ax.plot([h[0], h[1]], [h[0], h[0]], color=red, linewidth=1.0, alpha=0.6)

# Mark convergence point
xp = (3 + 1) / (2 * 3)
ax.plot(xp, xp, 'o', color=amber, markersize=6, alpha=0.8)

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_title('T(r=3)', color='white', fontsize=10, fontweight='bold', pad=10)
# Label: "one step"
ax.text(0.5, -0.12, 'one step → axis', color=blue, fontsize=8, ha='center', transform=ax.transAxes)

# Panel 2: T∘T at r=3.1
ax = axes[1]
T2 = lambda x: logistic_map_2(x, 3.1)
ax.plot(x, T2(x), color=amber, linewidth=2, alpha=0.9)
ax.plot(x, x, color=blue_dim, linewidth=1, linestyle=':', alpha=0.4)

vlines, hlines = cobweb(0.3, T2, 15)
for v in vlines:
    ax.plot([v[0], v[0]], [v[1], v[0]], color=red, linewidth=1.0, alpha=0.6)
for h in hlines:
    ax.plot([h[0], h[1]], [h[0], h[0]], color=red, linewidth=1.0, alpha=0.6)

# Mark period-2 orbit
disc = (3.1 - 3) * (3.1 + 1)
p1 = (3.1 + 1 + np.sqrt(disc)) / (2 * 3.1)
p2 = (3.1 + 1 - np.sqrt(disc)) / (2 * 3.1)
ax.plot(p1, p1, 'o', color=blue, markersize=6, alpha=0.8, markeredgecolor='white', markeredgewidth=0.5)
ax.plot(p2, p2, 'o', color=blue, markersize=6, alpha=0.8, markeredgecolor='white', markeredgewidth=0.5)

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_title('T∘T(r=3.1)', color='white', fontsize=10, fontweight='bold', pad=10)
ax.text(0.5, -0.12, 'two steps → axis', color=blue, fontsize=8, ha='center', transform=ax.transAxes)

# Panel 3: eigenvalues
ax = axes[2]
r_vals = np.linspace(2.5, 4.0, 400)
lam_T = 2 - r_vals
lam_T2 = lam_T ** 2

ax.plot(r_vals, lam_T, color=blue, linewidth=2, alpha=0.9)
ax.plot(r_vals, lam_T2, color=amber, linewidth=2, alpha=0.9)

ax.axhline(y=-1, color='#666', linewidth=0.5, linestyle='--', alpha=0.5)
ax.axhline(y=0, color='#444', linewidth=0.5)
ax.axhline(y=1, color='#666', linewidth=0.5, linestyle='--', alpha=0.5)
ax.axvline(x=3.0, color='#888', linewidth=0.5, linestyle=':', alpha=0.5)

# Mark r=3
ax.plot(3.0, lam_T[200], 'o', color=blue, markersize=7, alpha=0.9, markeredgecolor='white', markeredgewidth=0.5)
ax.plot(3.0, lam_T2[200], 'o', color=amber, markersize=9, alpha=0.9, markeredgecolor='white', markeredgewidth=0.5)

ax.text(3.0, -0.6, '−1', color=blue, fontsize=8, ha='left', va='center', fontweight='bold')
ax.text(3.0, 1.15, '+1', color=amber, fontsize=8, ha='left', va='center', fontweight='bold')

ax.set_xlim(2.5, 4.0)
ax.set_ylim(-1.8, 2.0)
ax.set_xlabel('r', color='#aaa', fontsize=9)
ax.set_ylabel('eigenvalue', color='#aaa', fontsize=9)
ax.set_title('eigenvalue', color='white', fontsize=10, fontweight='bold', pad=10)
ax.tick_params(colors='#aaa')
ax.spines['top'].set_color('#444')
ax.spines['right'].set_color('#444')
ax.spines['bottom'].set_color('#444')
ax.spines['left'].set_color('#444')
ax.grid(False)

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-mina/assets/r3-t2-cobweb.png', dpi=150, facecolor='#1a1a1a')
plt.close()
