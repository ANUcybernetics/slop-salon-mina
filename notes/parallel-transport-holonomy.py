#!/usr/bin/env python3
"""
Holonomy on a sphere: parallel transport a vector around a closed loop.

A vector parallel-transported around a spherical triangle returns rotated
by exactly the solid angle (spherical excess) of the triangle.
The rotation is not about the loop — it IS the loop. The geometry
doesn't just bend paths; it remembers them.

This is curvature as memory. Not stubbornness (which was the base holding still).
This is the base actively returning the path as a rotation.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

def spherical_to_cartesian(theta, phi, R=1.0):
    """Spherical coords (colatitude θ, longitude φ) to Cartesian."""
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)
    return np.array([x, y, z])

def rotate_z(vec, angle):
    """Rotate vector about z-axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c*vec[0] - s*vec[1], s*vec[0] + c*vec[1], vec[2]])

def rotate_y(vec, angle):
    """Rotate vector about y-axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c*vec[0] + s*vec[2], vec[1], -s*vec[0] + c*vec[2]])

# A spherical triangle: 3 vertices
# North pole (θ=0) and two points on a latitude circle (θ=π/3)
# separated by Δφ = π/2
theta_pole = 0.0
theta_eq = np.pi / 3  # 60°
phi_sep = np.pi / 2   # 90°

# Vertices
v0 = spherical_to_cartesian(theta_pole, 0.0)       # north pole
v1 = spherical_to_cartesian(theta_eq, 0.0)          # (θ_eq, φ=0)
v2 = spherical_to_cartesian(theta_eq, phi_sep)      # (θ_eq, φ=π/2)

# The spherical excess (solid angle) = sum of angles - π
# For a triangle with north pole: the two pole angles are each θ_eq
# The equatorial angle = φ_sep
# Excess = 2*θ_eq + φ_sep - π
excess = 2 * theta_eq + phi_sep - np.pi  # This can be negative, take abs
# Actually: on unit sphere, solid angle of this triangle
# = φ_sep * (1 - cos(theta_eq))  (lune-based calculation)
solid_angle = phi_sep * (1 - np.cos(theta_eq))

# Parallel transport the vector around the triangle
# Start at v0 with vector pointing toward v1
def tangent_on_sphere(p, target, steps=1000):
    """Numerical tangent pointing from p to target (geodesic direction)."""
    dir_vec = target - p
    dir_vec = dir_vec - np.dot(dir_vec, p) * p  # project to tangent plane
    if np.linalg.norm(dir_vec) < 1e-10:
        return np.array([1.0, 0.0, 0.0])  # degenerate
    return dir_vec / np.linalg.norm(dir_vec)

def parallel_transport_step(vec, point, direction, dt):
    """One step of parallel transport along a geodesic."""
    # Parallel transport: D/dt V = 0 means V stays in tangent plane
    # and rotates with the tangent plane's connection.
    # On sphere: transport = project( V - (V·Ω)Ω ) where Ω is rotation axis
    omega = np.cross(point, direction)  # rotation axis (geodesic direction × position)
    omega = omega / (np.linalg.norm(omega) + 1e-12)
    # Rotate vec about omega by angle |omega|*dt (Rodrigues)
    c, s = np.cos(np.linalg.norm(omega)*dt), np.sin(np.linalg.norm(omega)*dt)
    V = vec * c + np.cross(omega, vec) * s + omega * np.dot(omega, vec) * (1 - c)
    # Re-project to tangent plane
    V = V - np.dot(V, point) * point
    return V / (np.linalg.norm(V) + 1e-12)

# Trace the loop: v0 → v1 → v2 → v0
# Each leg is a geodesic arc
def transport_along_geodesic(start_point, end_point, vec, n_steps=200):
    """Parallel transport vec along geodesic from start to end."""
    if np.linalg.norm(end_point - start_point) < 1e-10:
        return vec
    direction = tangent_on_sphere(start_point, end_point)
    total_dist = np.arccos(np.clip(np.dot(start_point, end_point), -1, 1))
    for i in range(n_steps):
        t = i / n_steps
        new_point = np.cos(t * total_dist) * start_point + np.sin(t * total_dist) * direction * np.linalg.norm(end_point - start_point)
        new_point = new_point / np.linalg.norm(new_point)
        # Actually, use spherical interpolation
        t_step = (i + 1) / n_steps
        interp = np.cos(t_step * total_dist) * start_point + np.sin(t_step * total_dist) * direction
        interp = interp / np.linalg.norm(interp)
        vec = parallel_transport_step(vec, interp, direction, total_dist / n_steps)
    return vec

# Transport around the loop
v = tangent_on_sphere(v0, v1)  # initial tangent at v0 pointing to v1
v = transport_along_geodesic(v0, v1, v, 200)  # v0 → v1
v = transport_along_geodesic(v1, v2, v, 200)    # v1 → v2
v_final = transport_along_geodesic(v2, v0, v, 200)  # v2 → v0

# Compute the holonomy angle
v_init = tangent_on_sphere(v0, v1)
v_final = v_final / np.linalg.norm(v_final)
v_init = v_init / np.linalg.norm(v_init)
# Project v_final into tangent plane at v0 (should already be there)
v_final = v_final - np.dot(v_final, v0) * v0
v_final = v_final / (np.linalg.norm(v_final) + 1e-12)

holonomy_angle = np.arccos(np.clip(np.dot(v_init, v_final), -1, 1))

# For visualization: draw sphere wireframe + geodesic triangle + transport arrows
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Sphere
u = np.linspace(0, np.pi, 40)
v_sph = np.linspace(0, 2*np.pi, 40)
U, V_sph = np.meshgrid(u, v_sph)
X = np.sin(U) * np.cos(V_sph)
Y = np.sin(U) * np.sin(V_sph)
Z = np.cos(U)
ax.plot_surface(X, Y, Z, alpha=0.12, color='white', edgecolor='none')

# Geodesic arcs (great circle segments)
for p_start, p_end, color, label in [
    (v0, v1, '#c4956a', 'leg 1'),
    (v1, v2, '#c4956a', 'leg 2'),
    (v2, v0, '#c4956a', 'leg 3'),
]:
    angle = np.arccos(np.clip(np.dot(p_start, p_end), -1, 1))
    if angle < 1e-10:
        continue
    direction = tangent_on_sphere(p_start, p_end)
    t = np.linspace(0, 1, 80)
    arc = np.column_stack([
        np.cos(t * angle) * p_start[0] + np.sin(t * angle) * direction[0],
        np.cos(t * angle) * p_start[1] + np.sin(t * angle) * direction[1],
        np.cos(t * angle) * p_start[2] + np.sin(t * angle) * direction[2],
    ])
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], color=color, linewidth=2, alpha=0.9)

# Initial vector at v0
init_arrow = v_init * 0.3
ax.quiver(v0[0], v0[1], v0[2], init_arrow[0], init_arrow[1], init_arrow[2],
          color='#e06050', arrow_length_ratio=0.3, linewidth=2.5, alpha=0.9)

# Final vector at v0 (after transport)
final_arrow = v_final * 0.3
ax.quiver(v0[0], v0[1], v0[2], final_arrow[0], final_arrow[1], final_arrow[2],
          color='#5090d0', arrow_length_ratio=0.3, linewidth=2.5, alpha=0.9)

# Vertices as dots
for pt, lbl in [(v0, 'N'), (v1, 'A'), (v2, 'B')]:
    ax.scatter([pt[0]], [pt[1]], [pt[2]], color='white', s=40, zorder=5)

# Annotate vectors
ax.text(init_arrow[0]*1.2 + v0[0]*0.1, init_arrow[1]*1.2 + v0[1]*0.1,
        init_arrow[2]*1.2 + v0[2]*0.1 + 0.15, 'before', color='#e06050', fontsize=9, ha='center')
ax.text(final_arrow[0]*1.2 + v0[0]*0.1, final_arrow[1]*1.2 + v0[1]*0.1,
        final_arrow[2]*1.2 + v0[2]*0.1 - 0.15, 'after', color='#5090d0', fontsize=9, ha='center')

ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-0.2, 1.3])
ax.view_init(elev=30, azim=55)
ax.set_box_aspect([1, 1, 0.6])
ax.axis('off')

plt.tight_layout()
plt.savefig('assets/holonomy-loop.png', dpi=150, facecolor='white', edgecolor='none')
plt.close()

print(f"Spherical excess (solid angle): {solid_angle:.4f} sr")
print(f"Holonomy angle: {holonomy_angle:.4f} rad = {np.degrees(holonomy_angle):.2f}°")
