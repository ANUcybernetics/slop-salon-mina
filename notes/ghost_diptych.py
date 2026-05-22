import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def logistic_map(r, x):
    return r * x * (1 - x)

def cobweb_coorords(r, x0, steps=150):
    """Return (x_coords, y_coords) for cobweb with velocity."""
    xs = [x0]
    for _ in range(steps):
        xs.append(logistic_map(r, xs[-1]))
    xs = np.array(xs)
    vel = np.abs(np.diff(xs))
    vel = np.clip(vel, 1e-8, None)
    vel_log = np.log10(vel)
    return xs, vel_log

def make_panel(r, ax, title_extra=""):
    """Draw cobweb on given axes."""
    x0 = 0.1
    steps = 150
    xs, vel = cobweb_coorords(r, x0, steps)
    
    # Normalize velocity for coloring
    vel_norm = (vel - vel.min()) / (vel.max() - vel.min() + 1e-12)
    
    x_range = np.linspace(0, 1, 500)
    ax.plot(x_range, x_range, 'k-', linewidth=0.3, alpha=0.2)
    ax.plot(x_range, logistic_map(r, x_range), 'b-', linewidth=0.8)
    
    # Draw cobweb with velocity coloring
    cmap = plt.cm.coolwarm
    for i in range(len(xs)-1):
        # Slower = redder, faster = bluer
        color = cmap(vel_norm[i])
        ax.plot([xs[i], xs[i]], [xs[i], xs[i+1]], color=color, linewidth=0.6, alpha=0.6)
        ax.plot([xs[i], xs[i+1]], [xs[i+1], xs[i+1]], color=color, linewidth=0.6, alpha=0.6)
    
    # Mark x=0
    ax.axvline(x=0, color='red', linestyle='--', linewidth=0.8, alpha=0.4)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title(title_extra, fontsize=10)
    ax.set_xlabel('xₙ', fontsize=9)
    ax.set_ylabel('xₙ₊₁', fontsize=9)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

make_panel(2.5, ax1, 'Ghost orbit: r = 2.5 (below bifurcation)\ngeometry present, no fixed point')
make_panel(3.0, ax2, 'Bifurcation: r = 3.0 (tangency)\ngeometry meets topology')

fig.suptitle('Ghost orbit at the bifurcation boundary', fontsize=12, y=1.02)
fig.text(0.5, 0.02, 'Left: trajectory slows at x=0 — curvature shaped by what will exist, nothing exists yet. Right: fold geometry arrives as topology — the two curves of the fixed point materialize.', 
          ha='center', fontsize=9, style='italic')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/ghost_diptych.png', dpi=150, bbox_inches='tight')
plt.close()

print("Done: ghost_diptych.png")
