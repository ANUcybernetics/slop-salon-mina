import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def logistic_map(r, x):
    return r * x * (1 - x)

def cobweb_trajectory(r, x0, steps=300):
    """Generate cobweb points with velocity as slowdown indicator."""
    xs = [x0]
    for _ in range(steps):
        xs.append(logistic_map(r, xs[-1]))
    xs = np.array(xs)
    # velocity: how fast the trajectory is moving at each step
    vel = np.abs(np.diff(xs))
    # Normalize to 0-1, use log scale for visibility
    vel = np.clip(vel, 1e-8, None)
    vel_log = np.log10(vel)
    vmin, vmax = vel_log.min(), vel_log.max()
    vel_norm = (vel_log - vmin) / (vmax - vmin + 1e-12)
    return xs, vel_norm

r = 2.5  # below r_c = 3.0, no fixed points yet
x0 = 0.1
xs, vel = cobweb_trajectory(r, x0, steps=300)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Draw the logistic function and diagonal
x_range = np.linspace(0, 1, 500)
ax.plot(x_range, x_range, 'k-', linewidth=0.5, alpha=0.3, label='y = x')
ax.plot(x_range, logistic_map(r, x_range), 'b-', linewidth=1.0, label='f(x)')

# Plot cobweb with velocity coloring
for i in range(len(xs)-1):
    color = plt.cm.RdYlBu_r(vel[i])  # red=slow, green=fast
    ax.plot([xs[i], xs[i]], [xs[i], xs[i+1]], color=color, linewidth=0.8, alpha=0.7)
    ax.plot([xs[i], xs[i+1]], [xs[i+1], xs[i+1]], color=color, linewidth=0.8, alpha=0.7)

# Mark x=0 region
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.0, alpha=0.5, label='x = 0 (ghost location)')

# Annotations
ax.set_xlabel('xₙ', fontsize=12)
ax.set_ylabel('xₙ₊₁', fontsize=12)
ax.set_title(f'Logistic map cobweb — r = {r} (below bifurcation)\nghost orbit: trajectory slows at x=0, no fixed point exists there', fontsize=11)

# Colorbar for velocity
sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=plt.Normalize(vmin=vel.min(), vmax=vel.max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, label='log₁₀(|velocity|)')
cbar.set_label('log₁₀(|velocity|) (red = slow, green = fast)', fontsize=9)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/ghost_cobweb_r25.png', dpi=150, bbox_inches='tight')
plt.close()

print("Done: ghost_cobweb_r25.png")
