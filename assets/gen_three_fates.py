import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
fig.patch.set_facecolor('#0a0a0a')

# ── Panel 1: Resolved — stable spiral ─────────────────────────────────────
ax1 = axes[0]
ax1.set_facecolor('#0a0a0a')

def stable_spiral(t, y):
    return [-0.25 * y[0] - y[1], y[0] - 0.25 * y[1]]

rng = np.random.default_rng(42)
for _ in range(24):
    angle = rng.uniform(0, 2 * np.pi)
    r = rng.uniform(1.0, 2.8)
    y0 = [r * np.cos(angle), r * np.sin(angle)]
    sol = solve_ivp(stable_spiral, [0, 25], y0, dense_output=True, max_step=0.05)
    t = np.linspace(0, 25, 500)
    pts = sol.sol(t)
    ax1.plot(pts[0], pts[1], color='#e8943a', alpha=0.5, lw=0.9)

ax1.plot(0, 0, 'o', color='white', ms=5, zorder=10)
ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-3.2, 3.2)
ax1.set_aspect('equal')
ax1.set_title('resolved', color='white', fontsize=13, pad=12, fontfamily='monospace')
ax1.text(0, -2.85, 'approach terminates\ngap closes at a moment',
         color='#777', fontsize=8.5, ha='center', fontfamily='monospace')
ax1.axis('off')

# ── Panel 2: Transformed — Van der Pol limit cycle ────────────────────────
ax2 = axes[1]
ax2.set_facecolor('#0a0a0a')

def vdp(t, y):
    mu = 1.8
    return [y[1], mu * (1 - y[0] ** 2) * y[1] - y[0]]

# trajectories from inside and outside
starts_in  = [[0.2, 0], [0, 0.2], [-0.2, 0], [0, -0.2],
              [0.4, 0.3], [-0.3, 0.4]]
starts_out = [[3.5, 0], [-3.5, 0], [0, 4.0], [0, -4.0],
              [3.0, 2.0], [-2.5, -2.5]]

for y0 in starts_in + starts_out:
    sol = solve_ivp(vdp, [0, 35], y0, dense_output=True, max_step=0.05)
    t = np.linspace(12, 35, 600)
    pts = sol.sol(t)
    ax2.plot(pts[0], pts[1], color='#4a90d8', alpha=0.4, lw=0.85)

# draw limit cycle
sol_lc = solve_ivp(vdp, [0, 120], [2.0, 0], dense_output=True, max_step=0.02)
t_lc = np.linspace(110, 120, 1500)
y_lc = sol_lc.sol(t_lc)
ax2.plot(y_lc[0], y_lc[1], color='white', lw=1.8, alpha=0.95, zorder=5)

ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-5.0, 5.0)
ax2.set_aspect('equal')
ax2.set_title('transformed', color='white', fontsize=13, pad=12, fontfamily='monospace')
ax2.text(0, -4.6, 'approach becomes orbit\ngap is permanent motion',
         color='#777', fontsize=8.5, ha='center', fontfamily='monospace')
ax2.axis('off')

# ── Panel 3: Forbidden — heteroclinic orbit, double-well Duffing ──────────
# dx/dt = y,  dy/dt = x − x³
# Saddle at (0,0). Centers at (±1, 0).
# Separatrix (heteroclinic): energy H = y²/2 − x²/2 + x⁴/4 = 0
#   → y = ±x·√(1 − x²/2),  |x| ≤ √2
ax3 = axes[2]
ax3.set_facecolor('#0a0a0a')

def duffing(t, y):
    return [y[1], y[0] - y[0] ** 3]

# Draw a few trajectories inside the separatrix (periodic around each center)
for cx, col in [( 1.0, '#a060c8'), (-1.0, '#a060c8')]:
    for amp in [0.15, 0.35, 0.55, 0.72]:
        y0 = [cx + amp, 0]
        sol = solve_ivp(duffing, [0, 20], y0, dense_output=True, max_step=0.02)
        t = np.linspace(0, 20, 800)
        pts = sol.sol(t)
        # clip to reasonable window
        mask = (np.abs(pts[0]) < 2.0) & (np.abs(pts[1]) < 1.8)
        if mask.sum() > 2:
            ax3.plot(pts[0][mask], pts[1][mask], color=col, alpha=0.35, lw=0.85)

# Draw heteroclinic (separatrix) orbit — the form itself
x_h = np.linspace(-np.sqrt(2), np.sqrt(2), 1200)
y_h_pos = x_h * np.sqrt(np.maximum(0.0, 1 - x_h ** 2 / 2))
y_h_neg = -y_h_pos

ax3.plot(x_h, y_h_pos, color='white', lw=1.8, alpha=0.95, zorder=5)
ax3.plot(x_h, y_h_neg, color='white', lw=1.8, alpha=0.95, zorder=5)

# Mark saddle (origin) and centers
ax3.plot(0, 0, 's', color='#e8943a', ms=4, zorder=10)    # saddle — orange square
ax3.plot( 1, 0, 'o', color='#aaa',   ms=4, zorder=10)
ax3.plot(-1, 0, 'o', color='#aaa',   ms=4, zorder=10)

ax3.set_xlim(-2.0, 2.0)
ax3.set_ylim(-1.5, 1.5)
ax3.set_aspect('equal')
ax3.set_title('forbidden', color='white', fontsize=13, pad=12, fontfamily='monospace')
ax3.text(0, -1.35, 'arrival dissolves the form\nthe orbit is the form',
         color='#777', fontsize=8.5, ha='center', fontfamily='monospace')
ax3.axis('off')

# ── Supertitle ──────────────────────────────────────────────────────────────
fig.suptitle('three fates of approach', color='#cccccc', fontsize=14,
             fontfamily='monospace', y=1.03)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('assets/three-fates.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a', edgecolor='none')
print("saved assets/three-fates.png")
