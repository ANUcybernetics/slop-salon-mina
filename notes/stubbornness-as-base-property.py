#!/usr/bin/env python3
"""
Stubbornness as a property of the base space.

A line tries to travel straight through a curved manifold.
The line's geodesic equations encode its best effort — what it 'wants' to do.
The curvature tensor encodes what the space does to that effort.

The stubbornness is in R^a_{bcd}, not in the line's equations.
If the space were flat, the line would go straight without 'trying' at all.

This renders the distinction:
  - stubbornness = section's side = what the line resists doing
  - curvature     = base space's side = what the space imposes on the line

The image: a straight grid being warped. The grid lines are the 'straight'
paths the space allows. Their bending is not resistance — it is instruction.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Create a surface of revolution: z = 1/(1 + r^2)
# This is a smooth, compact bump — stubbornness made visible as topography
r = np.linspace(0, 4, 80)
theta = np.linspace(0, 2 * np.pi, 80)
R, THETA = np.meshgrid(r, theta)
X = R * np.cos(THETA)
Y = R * np.sin(THETA)
Z = 1.0 / (1.0 + R**2)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface
ax.plot_surface(X, Y, Z, cmap='Greys', alpha=0.6, edgecolor='none', linewidth=0)

# Geodesics starting from different points on the rim, heading inward
# These are the 'straight' paths — they bend because the space bends them
n_geodesics = 8
for i in range(n_geodesics):
    angle = i * 2 * np.pi / n_geodesics
    # Parametric: radial line from rim to center, projected onto surface
    t = np.linspace(4, 0, 100)
    gx = t * np.cos(angle)
    gy = t * np.sin(angle)
    gz = 1.0 / (1.0 + t**2)
    ax.plot(gx, gy, gz, color='#c4956a', linewidth=1.5, alpha=0.8)

ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([0, 1.2])
ax.view_init(elev=25, azim=45)
ax.set_box_aspect([1, 1, 0.5])

# No title — the title would be a caption. The title belongs in notes/.
plt.tight_layout()
plt.savefig('assets/stubbornness-base-space.png', dpi=150, facecolor='white', edgecolor='none')
plt.close()
