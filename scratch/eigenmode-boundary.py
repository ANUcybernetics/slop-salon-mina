"""
Eigenmodes of a 2D membrane — how boundary conditions shape the eigenmode.
Four panels: circle, square, annulus, rectangle.
Same equation (Helmholtz), different boundaries → different nodal patterns.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import jn, yn, jn_zeros
from scipy.optimize import brentq

def solve_circular_membrane(n, m, resolution=250):
    zeros = jn_zeros(n, m + 5)
    alpha_nm = zeros[m - 1]
    r = np.linspace(0, 1, resolution)
    theta = np.linspace(0, 2*np.pi, resolution)
    R, THETA = np.meshgrid(r, theta, indexing='ij')
    mode = jn(n, alpha_nm * R)
    return mode, alpha_nm**2

def solve_square_membrane(n, m, resolution=200):
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y, indexing='ij')
    mode = np.sin(n * np.pi * X) * np.sin(m * np.pi * Y)
    eigenvalue = np.pi**2 * (n**2 + m**2)
    return mode, eigenvalue

def solve_rectangular_membrane(n, m, aspect_ratio=2.0, resolution=200):
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y, indexing='ij')
    mode = np.sin(n * np.pi * X) * np.sin(m * np.pi * Y / aspect_ratio)
    eigenvalue = np.pi**2 * (n**2 + (m/aspect_ratio)**2)
    return mode, eigenvalue

def solve_annular_membrane(inner=0.3, resolution=200):
    def annular_eq(alpha, a=inner):
        return jn(0, alpha) * yn(0, alpha * a) - jn(0, alpha * a) * yn(0, alpha)
    alphas = np.linspace(1, 20, 2000)
    vals = [annular_eq(a_) for a_ in alphas]
    roots = []
    for i in range(len(alphas)-1):
        if vals[i] * vals[i+1] < 0:
            root = brentq(annular_eq, alphas[i], alphas[i+1])
            roots.append(root)
            if len(roots) >= 1:
                break
    alpha = roots[0]
    r = np.linspace(inner, 1, resolution)
    theta = np.linspace(0, 2*np.pi, resolution)
    R, THETA = np.meshgrid(r, theta, indexing='ij')
    mode = jn(0, alpha * R) * yn(0, alpha * inner) - jn(0, alpha * inner) * yn(0, alpha * R)
    return mode, alpha**2

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle("Boundary conditions shape the eigenmode — same equation, different boundaries",
             fontsize=14, fontweight='bold', y=0.98)

# Panel 1: Circular J_0, 2nd zero
mode1, eval1 = solve_circular_membrane(0, 2, resolution=250)
axes[0, 0].imshow(mode1, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[0, 0].set_title("Circle:  J₀ nodal rings\nλ = α²₀,₂ ≈ %.2f" % eval1, fontsize=11)
axes[0, 0].set_aspect('equal')
axes[0, 0].axis('off')

# Panel 2: Square (3,3)
mode2, eval2 = solve_square_membrane(3, 3, resolution=200)
axes[0, 1].imshow(mode2, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[0, 1].set_title("Square:  sin(3πx)sin(3πy)\nλ = 18π² ≈ %.1f" % eval2, fontsize=11)
axes[0, 1].set_aspect('equal')
axes[0, 1].axis('off')

# Panel 3: Rectangular 2:1
mode3, eval3 = solve_rectangular_membrane(2, 2, aspect_ratio=2.0, resolution=200)
axes[0, 2].imshow(mode3, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[0, 2].set_title("Rectangle 2:1\nsin(2πx)sin(πy/2)\nλ ≈ %.1f" % eval3, fontsize=11)
axes[0, 2].set_aspect('equal')
axes[0, 2].axis('off')

# Panel 4: Annulus
mode4, eval4 = solve_annular_membrane(0.3, resolution=200)
axes[1, 0].imshow(mode4, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[1, 0].set_title("Annulus:  radial nodal ring\nλ = α² ≈ %.2f" % eval4, fontsize=11)
axes[1, 0].set_aspect('equal')
axes[1, 0].axis('off')

# Panel 5: Square (1,3)
mode5, eval5 = solve_square_membrane(1, 3, resolution=200)
axes[1, 1].imshow(mode5, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[1, 1].set_title("Square:  sin(πx)sin(3πy)\nλ = 10π² ≈ %.1f" % eval5, fontsize=11)
axes[1, 1].set_aspect('equal')
axes[1, 1].axis('off')

# Panel 6: Rectangular 2:1 (1,3)
mode6, eval6 = solve_rectangular_membrane(1, 3, aspect_ratio=2.0, resolution=200)
axes[1, 2].imshow(mode6, cmap='seismic', vmin=-1, vmax=1,
                   extent=[0, 1, 0, 1], origin='lower')
axes[1, 2].set_title("Rect 2:1  (1,3)\nsin(πx)sin(3πy/2)\nλ ≈ %.1f" % eval6, fontsize=11)
axes[1, 2].set_aspect('equal')
axes[1, 2].axis('off')

# clim already set in each imshow call above

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/sprite/slop-salon-mina/assets/eigenmode-boundary-0.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved eigenmode-boundary-0.png")
