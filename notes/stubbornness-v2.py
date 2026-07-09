#!/usr/bin/env python3
"""
Stubbornness as a property of the base space — refined.

Geodesics on a surface of revolution. Dark field, warm paths, no axes.
The space bends the lines. The lines go straight by the space's standards.
Neither the line nor the space is stubborn alone.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Surface of revolution
r = np.linspace(0, 5, 120)
theta = np.linspace(0, 2 * np.pi, 120)
R, THETA = np.meshgrid(r, theta)
X = R * np.cos(THETA)
Y = R * np.sin(THETA)
Z = 1.0 / (1.0 + R**2)

fig = plt.figure(figsize=(12, 9), dpi=150)
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('#0a0a0c')
ax.set_facecolor('#0a0a0c')

# Surface: dark, subtle
surf = ax.plot_surface(X, Y, Z, cmap='Greys', alpha=0.35,
                       edgecolor='none', linewidth=0, rstride=1, cstride=1)

# Geodesics from rim, heading inward — denser, more paths
n_geodesics = 24
warm = plt.cm.magma(np.linspace(0.3, 0.9, n_geodesics))

for i in range(n_geodesics):
    angle = i * 2 * np.pi / n_geodesics
    t = np.linspace(5, 0, 200)
    gx = t * np.cos(angle)
    gy = t * np.sin(angle)
    gz = 1.0 / (1.0 + t**2)
    ax.plot(gx, gy, gz, color=warm[i], linewidth=1.0, alpha=0.7)

# Highlight 3 geodesics that come back with visible difference
# (simulating parallel transport by going all the way through)
for i in range(3):
    angle = i * np.pi * 2 / 3  # equally spaced
    # Go from outside, through center, to other side
    t = np.linspace(5, -5, 300)
    gx = t * np.cos(angle)
    gy = t * np.sin(angle)
    gz = np.where(np.abs(t) < 0.1,
                  1.0 + 0.3,  # smooth peak at origin
                  1.0 / (1.0 + t**2))
    ax.plot(gx, gy, gz, color='#f0c040', linewidth=2.5, alpha=0.9)

ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([0, 1.4])
ax.set_box_aspect([1, 1, 0.5])
ax.view_init(elev=30, azim=50)

# Hide axes for a clean look
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.set_visible(False)

# Make panes invisible
ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)

# No tight_layout with 3D axes
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
plt.savefig('assets/stubbornness-base-space-2.png', dpi=150,
            facecolor='#0a0a0c', edgecolor='none')
plt.close()
