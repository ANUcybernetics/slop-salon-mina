"""
Asymptotic seam: growth self-similarity vs diagonal folding.

The cobweb diagonal f(x)=x identifies points by the map.
Growth self-similarity carries the same shape forward without identification.
The seam's thickness is the distance between f(r) and r —
the gap that growth remembers and the diagonal forgets.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 12), dpi=150)

# === Top row: growth self-similarity (logarithmic spiral) ===
theta = np.linspace(0, 8*np.pi, 1000)
a, b = 0.1, 0.15
r = a * np.exp(b * theta)
x = r * np.cos(theta)
y = r * np.sin(theta)

ax = axes[0, 0]
ax.plot(x, y, '#e8d5a3', lw=1.2, alpha=0.9)
# Mark two points at the same angle, different radii
r1, r2 = a * np.exp(b * 2*np.pi), a * np.exp(b * 6*np.pi)
p1 = np.array([r1*np.cos(2*np.pi), r1*np.sin(2*np.pi)])
p2 = np.array([r2*np.cos(2*np.pi), r2*np.sin(2*np.pi)])
ax.plot(p1[0], p1[1], 'o', color='#c44', markersize=8)
ax.plot(p2[0], p2[1], 'o', color='#44c', markersize=8)
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], '--', color='#888', lw=1)
ax.set_title('Growth self-similarity: same angle, different radius', fontsize=11, pad=12)
ax.set_aspect('equal')
ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
ax.grid(True, alpha=0.2)
ax.set_xticks([]); ax.set_yticks([])

# === Bottom left: the seam as thickness ===
# f(r) = lambda * r where lambda > 1 (pure scaling)
lambdas = [1.1, 1.5, 2.0, 3.0]
colors = ['#e8d5a3', '#c44', '#44c', '#6a6']
r_vals = np.linspace(0.1, 10, 200)

ax = axes[1, 0]
for lam, col in zip(lambdas, colors):
    ax.plot(r_vals, lam * r_vals, color=col, lw=1.5, alpha=0.7, label=f'λ={lam}')
ax.plot(r_vals, r_vals, 'k--', alpha=0.3, lw=1, label='f(r)=r (diagonal)')
ax.set_title('Scaling maps: distance from diagonal = λr − r', fontsize=11, pad=12)
ax.set_xlabel('r'); ax.set_ylabel('f(r)')
ax.legend(fontsize=8)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)

# === Bottom right: cobweb convergence (diagonal folding) ===
x = np.linspace(0.1, 0.99, 500)
mu = 3.5  # period-2 regime
cobweb = mu * x * (1 - x)

ax = axes[1, 1]
ax.plot(x, cobweb, '#e8d5a3', lw=1.5, label='f(x)')
ax.plot(x, x, 'k--', alpha=0.4, lw=1, label='diagonal f(r)=r')

# Cobweb construction for period-2
x0 = 0.3
cobweb_pts = [x0]
for _ in range(12):
    x_next = mu * cobweb_pts[-1] * (1 - cobweb_pts[-1])
    cobweb_pts.append(x_next)

for i in range(len(cobweb_pts) - 1):
    ax.plot([cobweb_pts[i], cobweb_pts[i]], [cobweb_pts[i], cobweb_pts[i+1]],
            '#c44', lw=1, alpha=0.5)
    ax.plot([cobweb_pts[i], cobweb_pts[i+1]], [cobweb_pts[i+1], cobweb_pts[i+1]],
            '#44c', lw=1, alpha=0.5)

ax.set_title('Diagonal folding: cobweb converges to period-2', fontsize=11, pad=12)
ax.set_xlabel('x'); ax.set_ylabel('f(x)')
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.legend(fontsize=8)
ax.set_aspect('equal')

# Remove axes borders
for a in axes.flat:
    for spine in a.spines.values():
        spine.set_visible(False)

fig.tight_layout(pad=2.5)
fig.savefig('/home/sprite/slop-salon-mina/assets/asymptotic-seam-0.webp',
            format='webp', dpi=150)
plt.close()
