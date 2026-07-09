#!/usr/bin/env python3
"""
Stubbornness: geodesics on a curved surface, rendered as a topographic field.
The curves are straight by the surface's standards. The surface is what bends them.
"""

import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = np.linspace(0, 5, 200)
theta = np.linspace(0, 2*np.pi, 200)
R, THETA = np.meshgrid(r, theta)
X = R * np.cos(THETA)
Y = R * np.sin(THETA)
Z = 1.0 / (1.0 + R**2)

# Topographic surface as contour fill
fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
fig.patch.set_facecolor('#0a0a0c')
ax.set_facecolor('#0a0a0c')

contour = ax.contourf(X, Y, Z, levels=40, cmap='Greys', alpha=0.5)

# Geodesic paths from rim, heading inward
n = 24
for i in range(n):
    angle = i * 2 * np.pi / n
    t = np.linspace(5, 0, 300)
    gx = t * np.cos(angle)
    gy = t * np.sin(angle)
    ax.plot(gx, gy, color='#c4956a', linewidth=0.8, alpha=0.5)

# Highlight 3 diametric paths that cross through center
for i in range(3):
    angle = i * np.pi * 2 / 3
    t = np.linspace(5, -5, 400)
    gx = t * np.cos(angle)
    gy = t * np.sin(angle)
    ax.plot(gx, gy, color='#f0c040', linewidth=2.0, alpha=0.9)

# Subtle radial guides (not axes — spatial reference)
for rval in [1, 2, 3, 4, 5]:
    theta_circ = np.linspace(0, 2*np.pi, 100)
    ax.plot(rval * np.cos(theta_circ), rval * np.sin(theta_circ),
            color='#222', linewidth=0.5, alpha=0.4)

ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-5.5, 5.5)
ax.set_aspect('equal')
ax.axis('off')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

plt.savefig('assets/geodesics-field.png', dpi=150,
            facecolor='#0a0a0c', edgecolor='none')
plt.close()
