#!/usr/bin/env python3
"""Five registers converging on a tropical crease.
Each register = one orbit of the same vector field.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

dpi = 150
fig, ax = plt.subplots(figsize=(8, 8))

# Tropical crease: min(x, y, -x-y)
# Crease lines: x = y, y = -x-y, x = -x-y
# These are: y=x, y=-x/2, x=-y/2  (three rays from origin at 120°)

# Grid
x = np.linspace(-3, 3, 600)
y = np.linspace(-3, 3, 600)
X, Y = np.meshgrid(x, y)

# Tropical min surface (z-axis)
T = np.minimum(X, np.minimum(Y, -X - Y))

# Vector field: gradient of T (where differentiable)
# Near crease, flow is toward the crease
# Divergence-free toward crease, along crease = constant
# Streamlines: five different starting points, same attractor

# Simple model: flow = -grad(T) where T is smooth approx of tropical min
# Use smooth minimum (log-sum-exp)
beta = 8.0
S = np.exp(-beta * X) + np.exp(-beta * Y) + np.exp(beta * (X + Y))
T_smooth = -np.log(S) / beta

# Gradient: d/dx(-log(S)/beta) = -(1/beta)*(1/S)*dS/dx
# dS/dx = -beta*exp(-beta*X) + beta*exp(beta*(X+Y))
dSdx = -beta * np.exp(-beta * X) + beta * np.exp(beta * (X + Y))
dSdy = -beta * np.exp(-beta * Y) + beta * np.exp(beta * (X + Y))
dTx = -dSdx / (beta * S)
dTy = -dSdy / (beta * S)

# T has max at origin → flow outward. We want inward (toward crease).
# Use U = -T = log-SUM-exp which has its minimum at origin.
# Gradient of U = -gradient of T = (dTx, dTy)
# But streamplot goes along the vector. So pass (dTx, dTy) to flow toward origin,
# or (-dTx, -dTy) to flow away. We want toward origin → use (dTx, dTy).
# Actually: at a point on y=x, x>0: T ≈ x (max), dTx ≈ 0, dTy ≈ 0 (smooth region)
# Near crease y=x (x>0): T ≈ x, dTx ≈ 1, dTy ≈ 0. Flow along (-dTx, -dTy) = (-1, 0) → toward origin.
# So (-dTx, -dTy) IS correct for inward flow. But streamplot arrows show the opposite.
# Issue: the gradient calculation may be wrong for the tropical case.
# Let me just use max formulation instead.

# U = max(X, Y, -X-Y) which has min at origin
# Smooth max: log-sum-exp
S_max = np.exp(beta * X) + np.exp(beta * Y) + np.exp(-beta * (X + Y))
U_smooth = np.log(S_max) / beta
# Gradient of U (smooth max)
dUdx = (beta * np.exp(beta * X) - beta * np.exp(-beta * (X + Y))) / (beta * S_max)
dUdy = (beta * np.exp(beta * Y) - beta * np.exp(-beta * (X + Y))) / (beta * S_max)
# Use U gradient: flow along -grad(U) = toward minimum (origin, along creases)
field_x = -dUdx
field_y = -dUdy

# Streamlines from five different starting points
# Five registers: boundary, coboundary, tropical, temporal, geometric
starts = [
    (-2.5, -1.0),   # boundary: outer, structural
    (2.5, -0.5),    # coboundary: constructive, from the other side
    (0.0, 2.5),     # tropical: chart-based, from above
    (-1.5, 2.0),    # temporal: oscillatory history
    (2.0, 2.0),     # geometric: eigenmode, from the spectrum
]
colors = ['#4a90d9', '#d94a7a', '#5cc17a', '#d9b44a', '#a84ad9']
labels = ['boundary', 'coboundary', 'tropical', 'temporal', 'geometric']

for (sx, sy), color, label in zip(starts, colors, labels):
    ax.streamplot(X, Y, field_x, field_y,
                  color=color, linewidth=1.5,
                  start_points=[[sx, sy]],
                  arrowstyle='->', arrowsize=1.2,
                  density=1.5)

# Tropical crease heatmap (T values, inverted for dark crease on light bg)
im = ax.contourf(X, Y, T, levels=20, cmap='RdYlBu_r', alpha=0.3, vmin=-3, vmax=0)

# Draw crease lines explicitly
# y = x
ax.plot([-3, 3], [-3, 3], 'k-', linewidth=2.5, alpha=0.7)
# y = -x/2
ax.plot([-3, 3], [1.5, -1.5], 'k-', linewidth=2.5, alpha=0.7)
# x = -y/2 → y = -2x
ax.plot([-1.5, 1.5], [3, -3], 'k-', linewidth=2.5, alpha=0.7)

# Origin marker (where all three creases meet)
ax.plot(0, 0, 'ko', markersize=8)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_xlabel('', fontsize=0)
ax.set_ylabel('', fontsize=0)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Title with small text
ax.set_title('five registers, one field', fontsize=11, color='black', pad=15)

os.makedirs('assets', exist_ok=True)
path = 'assets/tropical-convergence-01.png'
fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Wrote {path}")
