"""
Abelian vs non-abelian holonomy: what changes when numbers become matrices.

Abelian: parallel transport on S¹ → holonomy is a phase e^{iθ}, path-independent.
Non-abelian: parallel transport on SU(2) → holonomy is a matrix, path-ordered.

The visual: two panels showing the same loop in different gauge groups.
Left: abelian — single number accumulating around a circle.
Right: non-abelian — a matrix (visualized via its eigenvalue rotation) accumulating with path-ordering dependence.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Wedge
import matplotlib.patches as mpatches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ============================================================
# LEFT PANEL: Abelian holonomy
# ============================================================
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Abelian: path-independent\nU = e^{i∮A·dx}', fontsize=13, fontweight='bold')

# Draw circle (the loop)
circle = Circle((0, 0), 1.5, fill=False, edgecolor='#4a90d9', linewidth=2)
ax1.add_patch(circle)

# Draw discretized segments with phases
n_segments = 24
theta = np.linspace(0, 2*np.pi, n_segments, endpoint=False)
for i in range(n_segments):
    angle = theta[i]
    next_angle = theta[(i + 1) % n_segments]
    x0, y0 = 1.5 * np.cos(angle), 1.5 * np.sin(angle)
    x1, y1 = 1.5 * np.cos(next_angle), 1.5 * np.sin(next_angle)
    
    # Color by local phase contribution
    phase = (next_angle - angle) * 5  # local connection value
    intensity = 0.5 + 0.5 * np.cos(phase)
    ax1.plot([x0, x1], [y0, y1], color=(0.29, 0.56*intensity + 0.1, 0.85), linewidth=3)

# Add arrow showing direction
arrow_angle = np.pi / 4
ax1.annotate('', xy=(1.5*np.cos(arrow_angle)+0.15, 1.5*np.sin(arrow_angle)+0.15),
            xytext=(1.5*np.cos(arrow_angle)-0.15, 1.5*np.sin(arrow_angle)-0.15),
            arrowprops=dict(arrowstyle='->', color='white', lw=2))

# Central label: the holonomy is a single number
holonomy_text = 'holonomy = ' + r'e^{iφ}' + '\nscalar, path-independent'
ax1.text(0, -2.2, holonomy_text, ha='center', fontsize=11,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a2e', edgecolor='#4a90d9', linewidth=1.5))

# Annotation about the path
ax1.text(0, 2.1, 'loop in base space', ha='center', fontsize=10, style='italic', color='#888')

# ============================================================
# RIGHT PANEL: Non-abelian holonomy  
# ============================================================
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-2.5, 2.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Non-abelian: path-ordered\nU = P exp(i∮A·dx)', fontsize=13, fontweight='bold')

# Draw same circle
circle2 = Circle((0, 0), 1.5, fill=False, edgecolor='#d94a4a', linewidth=2)
ax2.add_patch(circle2)

# Non-commutative: show that the order matters
# Use color and varying "rotation" at each segment
for i in range(n_segments):
    angle = theta[i]
    next_angle = theta[(i + 1) % n_segments]
    x0, y0 = 1.5 * np.cos(angle), 1.5 * np.sin(angle)
    x1, x1, y1 = 1.5 * np.cos(next_angle), 1.5 * np.cos(next_angle), 1.5 * np.sin(next_angle)
    
    # The local SU(2) element: a matrix in the algebra
    # Visualize by varying the color based on which generator is active
    generator = i % 3  # σ₁, σ₂, or σ₃
    colors = ['#d94a4a', '#d9a44a', '#a4d94a']  # red, orange, green
    ax2.plot([x0, x1], [y0, y1], color=colors[generator], linewidth=3, alpha=0.8)

# Arrow showing direction
ax2.annotate('', xy=(1.5*np.cos(arrow_angle)+0.15, 1.5*np.sin(arrow_angle)+0.15),
            xytext=(1.5*np.cos(arrow_angle)-0.15, 1.5*np.sin(arrow_angle)-0.15),
            arrowprops=dict(arrowstyle='->', color='white', lw=2))

# Central label: the holonomy is a matrix
holonomy_text2 = 'holonomy = U ∈ SU(2)\nmatrix, path-ORDERED'
ax2.text(0, -2.2, holonomy_text2, ha='center', fontsize=11,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a2e', edgecolor='#d94a4a', linewidth=1.5))

# Legend for generators
legend_y = 2.1
ax2.text(0, legend_y, 'σ₁, σ₂, σ₃ at each step → ordering matters', ha='center', fontsize=10, 
         style='italic', color='#888')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/nonabelian-holonomy.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a14', edgecolor='none')
plt.close()
print('saved nonabelian-holonomy.png')

# Second figure: eigenvalue rotation in SU(2) vs simple phase in U(1)
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 5))

# Left: U(1) — a single phase accumulating
ax3.set_xlim(-2, 2)
ax3.set_ylim(-0.5, 3.5)
ax3.set_title('U(1): single phase', fontsize=13, fontweight='bold')
ax3.set_xlabel('loop position', fontsize=11)
ax3.set_ylabel('holonomy phase φ', fontsize=11)

# A flat connection: phase accumulates linearly
s = np.linspace(0, 24, 500)
phi = 0.5 * s  # constant connection
ax3.plot(s, phi % (2*np.pi), color='#4a90d9', linewidth=2.5)
ax3.axhline(y=0, color='#333', linewidth=0.5)
ax3.axhline(y=2*np.pi, color='#333', linewidth=0.5)
ax3.set_ylim(-0.3, 2*np.pi + 0.3)
ax3.text(12, 1.5, r'φ(s) = ∫ A(s) ds', fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', alpha=0.9))

# Right: SU(2) — eigenvalues rotate but the path-ordering means the matrix holonomy
# depends on the ordering of infinitesimal factors
ax4.set_xlim(-2, 2)
ax4.set_ylim(-0.5, 3.5)
ax4.set_title('SU(2): path-ordered exponential', fontsize=13, fontweight='bold')
ax4.set_xlabel('loop position', fontsize=11)
ax4.set_ylabel('eigenvalue angle', fontsize=11)

# Two eigenvalues of SU(2) matrix: e^{iθ}, e^{-iθ}
s2 = np.linspace(0, 24, 500)
theta1 = 0.5 * s2 + 0.1 * np.sin(0.3 * s2)  # perturbed to show ordering dependence
theta2 = -theta1
ax4.plot(s2, theta1 % (2*np.pi), color='#d94a4a', linewidth=2.5, label='eigenvalue +')
ax4.plot(s2, (-theta1) % (2*np.pi), color='#d9a44a', linewidth=2.5, label='eigenvalue −')
ax4.axhline(y=0, color='#333', linewidth=0.5)
ax4.axhline(y=2*np.pi, color='#333', linewidth=0.5)
ax4.set_ylim(-0.3, 2*np.pi + 0.3)
ax4.legend(fontsize=10, loc='upper right')
ax4.text(12, 1.5, r'U = P exp(i∮ Aᵢσᵢ ds)', fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', alpha=0.9))

# Add annotation about what's different
ax4.annotate('', xy=(0.5, 0.8), xytext=(1.5, 2.8),
            arrowprops=dict(arrowstyle='->', color='#fff', lw=1.5, alpha=0.5))
ax4.text(1.0, 2.5, 'ordering\nchanges the\nholonomy', fontsize=9, color='#fff', alpha=0.7)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/nonabelian-eigenvalues.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a14', edgecolor='none')
plt.close()
print('saved nonabelian-eigenvalues.png')
