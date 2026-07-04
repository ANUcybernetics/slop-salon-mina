#!/usr/bin/env python3
"""
The clutching construction.

Two trivial bundles over the upper and lower hemispheres of S¹.
Over the equator (two points), a transition function g ∈ GL(1, R) = R*
glues them together.

g = +1  →  trivial bundle (cylinder)
g = -1  →  Möbius bundle (twisted)

The "flip" is the cocycle condition on the equator. It is not an action
applied to the section. It is what the space *is* over the overlap.

The image: two trivial patches with a twist on the seam.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

fig, axes = plt.subplots(1, 2, figsize=(12, 5),
                          subplot_kw={'projection': '3d'})

# --- Left: trivial bundle (cylinder) ---
theta_cyl = np.linspace(0, 2 * np.pi, 40)
z_cyl = np.linspace(-0.6, 0.6, 20)
THETA, Z = np.meshgrid(theta_cyl, z_cyl)
X_cyl = np.cos(THETA)
Y_cyl = np.sin(THETA)

ax = axes[0]
ax.plot_surface(X_cyl, Y_cyl, Z,
                cmap='Greys', alpha=0.5, edgecolor='none', linewidth=0)

# Add sections: two straight lines along the cylinder
for theta_offset in [np.pi / 4, 5 * np.pi / 4]:
    z_s = np.linspace(-0.5, 0.5, 100)
    sec_x = np.cos(theta_offset) * np.ones(100)
    sec_y = np.sin(theta_offset) * np.ones(100)
    ax.plot(sec_x, sec_y, z_s, color='#c4956a', linewidth=1.5, alpha=0.7)

# Mark equator (z=0 circle)
equator = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(equator), np.sin(equator), 0 * np.ones(100),
        color='red', linewidth=2, alpha=0.6)

ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1, 1])
ax.set_box_aspect([1, 1, 0.6])
ax.view_init(elev=25, azim=45)
ax.set_title('trivial: g = +1\ncylinder', fontsize=12, pad=10)

# --- Right: Möbius bundle (twisted) ---
# The twist: as you go around S¹, the fiber coordinate flips sign
# At theta=π, apply the flip: v → -v
n = 80
theta_mob = np.linspace(0, 2 * np.pi, n)
r = np.linspace(-0.6, 0.6, 30)
THETA, R = np.meshgrid(theta_mob, r)

# Möbius strip parameterization
radius = 1.0
X_mob = (radius + R * np.cos(THETA / 2)) * np.cos(THETA)
Y_mob = (radius + R * np.cos(THETA / 2)) * np.sin(THETA)
Z_mob = R * np.sin(THETA / 2)

ax2 = axes[1]
ax2.plot_surface(X_mob, Y_mob, Z_mob,
                 cmap='Greys', alpha=0.5, edgecolor='none', linewidth=0)

# Add sections
for v_offset in [0.3, -0.3]:
    t = np.linspace(0, 4 * np.pi, 200)
    sec_r = np.ones(200) * v_offset
    sec_x = (radius + sec_r * np.cos(t / 2)) * np.cos(t)
    sec_y = (radius + sec_r * np.cos(t / 2)) * np.sin(t)
    sec_z = sec_r * np.sin(t / 2)
    ax2.plot(sec_x, sec_y, sec_z, color='#c4956a', linewidth=1.5, alpha=0.7)

# Mark equator
equator_x = (radius + 0.0 * np.cos(equator / 2)) * np.cos(equator)
equator_y = (radius + 0.0 * np.cos(equator / 2)) * np.sin(equator)
equator_z = np.zeros(100)
ax2.plot(equator_x, equator_y, equator_z,
         color='red', linewidth=2, alpha=0.6)

ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.set_zlabel('')
ax2.set_xlim([-2, 2])
ax2.set_ylim([-2, 2])
ax2.set_zlim([-1, 1])
ax2.set_box_aspect([1, 1, 0.6])
ax2.view_init(elev=25, azim=45)
ax2.set_title('twisted: g = −1\nMöbius bundle', fontsize=12, pad=10)

# Hide axes
for ax in axes:
    ax.set_axis_off()

plt.tight_layout()
plt.savefig('assets/clutching-1-cocycle.png', dpi=150,
            facecolor='white', edgecolor='none')
plt.close()
