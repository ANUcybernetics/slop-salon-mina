#!/usr/bin/env python3
"""Crease as atlas — visualizing overlapping charts with the crease as cohomology class."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.collections import LineCollection

# --- Vector field: descent toward the crease ---
def vector_field(X, Y):
    """Gradient of |x| — crease is x=0, field points toward it."""
    # Subtle smoothing near zero for visual clarity
    eps = 0.1
    sign_x = X / np.sqrt(X**2 + eps**2)
    # Descent toward crease (x=0) + slight rotation (holonomy)
    ux = -sign_x
    uy = 0.1 * np.exp(-Y**2 / 4)
    return ux, uy

# --- Create figure ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, ax in enumerate(axes):
    # Grid
    x = np.linspace(-3, 3, 25)
    y = np.linspace(-4, 4, 25)
    X, Y = np.meshgrid(x, y)
    U, V = vector_field(X, Y)

    # Normalize for display
    speed = np.sqrt(U**2 + V**2)
    U_n, V_n = U / speed, V / speed

    if idx == 0:
        # Chart 1 (standard coords)
        ax.streamplot(X, Y, U, V, color='steelblue', linewidth=1.2, density=1.5, arrowstyle='->')
        ax.axvline(0, color='crimson', linewidth=2.5, label='crease (chart 1)')
        ax.set_title('chart₁: standard coords', fontsize=12, fontweight='bold')
    elif idx == 1:
        # Chart 2 (shifted coords — crease moves)
        X2 = X + 1
        U2, V2 = vector_field(X2, Y)
        speed2 = np.sqrt(U2**2 + V2**2)
        U2_n, V2_n = U2 / speed2, V2 / speed2
        ax.streamplot(X, Y, U2, V2, color='seagreen', linewidth=1.2, density=1.5, arrowstyle='->')
        ax.axvline(-1, color='crimson', linewidth=2.5, label='crease (chart 2)')
        ax.set_title('chart₂: shifted coords', fontsize=12, fontweight='bold')
    else:
        # Chart 3 (scaled coords — crease disappears in this trivialization)
        X3 = X * 1.5
        U3, V3 = vector_field(X3, Y)
        speed3 = np.sqrt(U3**2 + V3**2)
        ax.streamplot(X, Y, U3, V3, color='purple', linewidth=1.2, density=1.5, arrowstyle='->')
        ax.axvline(0, color='crimson', linewidth=2.5, linestyle='--', alpha=0.5)
        ax.set_title('chart₃: scaled coords', fontsize=12, fontweight='bold')

    ax.set_xlim(-3, 3)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.axhline(0, color='gray', linewidth=0.3, alpha=0.3)
    ax.axvline(0, color='gray', linewidth=0.3, alpha=0.3)

# Summary panel
fig.text(0.5, 0.02,
    'crease position shifts across charts — cohomology class H¹ ≠ 0. '
    'the crease is unavoidable. not a marker; the invariant.',
    ha='center', fontsize=10, style='italic', color='dimgray',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='none'))

fig.suptitle('the crease survives every chart', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0.05, 1, 0.96])
fig.savefig('assets/crease-atlas-02.png', dpi=150, bbox_inches='tight')
print('assets/crease-atlas-02.png')
