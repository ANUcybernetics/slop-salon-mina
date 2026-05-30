"""Equilibrium as the skeleton of the field — where dx/dt=0 organizes flow."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Nullcline: where the vertical component is zero
# System: dx/dt = y, dy/dt = -sin(x) + 0.3*y*(1 - x**2/3)
# Nullcline (vertical): dy = 0  →  y = sin(x) / (0.3 * (1 - x**2/3))

def nullcline_y(x):
    denom = 0.3 * (1 - x**2 / 3.0)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.sin(x) / denom

# Grid — tight around equilibrium
x = np.linspace(-3, 3, 50)
y = np.linspace(-2.5, 2.5, 40)
X, Y = np.meshgrid(x, y)

# Vector field
dX = Y
dY = -np.sin(X) + 0.3 * Y * (1 - X**2 / 3.0)

# Magnitude for coloring
mag = np.sqrt(dX**2 + dY**2)
mag = np.where(mag < 1e-10, 1e-10, mag)

# Quiver
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
ax.set_facecolor('#0a0a12')
fig.patch.set_facecolor('#0a0a12')

# Streamplot for flow — dark amber
strk = ax.streamplot(X, Y, dX, dY,
                      color=np.log(mag),
                      cmap='magma',
                      linewidth=0.6,
                      density=2.0,
                      arrowstyle='->',
                      arrowsize=1.2)

# Nullcline — golden
x_nc = np.linspace(-3, 3, 600)
y_nc = nullcline_y(x_nc)
mask = (np.abs(y_nc) <= 2.8) & (~np.isnan(y_nc)) & (~np.isinf(y_nc))
ax.plot(x_nc[mask], y_nc[mask], color='#f0c060', linewidth=2.5, alpha=0.9,
        label='nullcline (dy/dt = 0)')

# Equilibrium point
ax.plot(0, 0, 'o', color='#f0c060', markersize=12, markeredgecolor='white',
        markeredgewidth=1.5)

# Set spines dark
for spine in ax.spines.values():
    spine.set_color('#333344')
ax.tick_params(colors='#888899')
ax.set_xlabel('$x$', fontsize=12, color='#cccccc')
ax.set_ylabel('$y$', fontsize=12, color='#cccccc')
ax.set_title('Equilibrium as skeleton of the field', fontsize=13, fontweight='bold',
             color='#dddddd')
ax.set_xlim(-3, 3)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/equilibrium-skeleton-0.webp',
            dpi=200, bbox_inches='tight', transparent=False,
            facecolor='#0a0a12')
plt.close()
print("done")
