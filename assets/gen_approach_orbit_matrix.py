"""
approach fate × orbit fate — 4-panel taxonomy visualization

Rahel's 2D separation: approach fate and orbit fate are independent dimensions.

approach fate: resolved / deferred / forbidden
orbit fate:    trivial / exhaustible / inexhaustible / (form)
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

fig, axes = plt.subplots(1, 4, figsize=(20, 5.8))
fig.patch.set_facecolor('#0a0a0a')

AMBER  = '#e8943a'
BLUE   = '#4a90d8'
TEAL   = '#3ab8c8'
PURPLE = '#a060c8'
DIM    = '#555555'
WHITE  = '#f0f0f0'
LABEL_CLR = '#666666'

# ── Panel 1: fixed point — approach resolved, orbit trivial ──────────────────
ax = axes[0]
ax.set_facecolor('#0a0a0a')

def stable_spiral(t, y):
    return [-0.3 * y[0] - 0.9 * y[1], 0.9 * y[0] - 0.3 * y[1]]

rng = np.random.default_rng(7)
for _ in range(20):
    angle = rng.uniform(0, 2 * np.pi)
    r = rng.uniform(0.9, 2.6)
    y0 = [r * np.cos(angle), r * np.sin(angle)]
    sol = solve_ivp(stable_spiral, [0, 22], y0, dense_output=True, max_step=0.04)
    t_ev = np.linspace(0, 22, 500)
    pts = sol.sol(t_ev)
    ax.plot(pts[0], pts[1], color=AMBER, alpha=0.45, lw=0.85)

ax.plot(0, 0, 'o', color=WHITE, ms=5, zorder=10)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_title('fixed point', color=WHITE, fontsize=12, pad=10, fontfamily='monospace')
ax.text(0, 2.6,
        'approach: resolved\norbit: trivial',
        color=AMBER, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.text(0, -2.65,
        'approach terminates\nno orbit remains',
        color=LABEL_CLR, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.axis('off')

# ── Panel 2: limit cycle — approach deferred, orbit exhaustible ──────────────
ax = axes[1]
ax.set_facecolor('#0a0a0a')

def vdp(t, y):
    mu = 2.0
    return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

starts_in  = [[0.2, 0], [0, 0.3], [-0.3, 0], [0.4, 0.3], [-0.2, -0.4]]
starts_out = [[3.8, 0], [-3.8, 0], [0, 4.2], [3.2, 2.2], [-2.8, -2.8]]

for y0 in starts_in + starts_out:
    sol = solve_ivp(vdp, [0, 40], y0, dense_output=True, max_step=0.05)
    t_ev = np.linspace(14, 40, 600)
    pts = sol.sol(t_ev)
    ax.plot(pts[0], pts[1], color=BLUE, alpha=0.35, lw=0.8)

# draw the limit cycle
sol_lc = solve_ivp(vdp, [0, 130], [2.0, 0], dense_output=True, max_step=0.02)
t_lc = np.linspace(120, 130, 1800)
y_lc = sol_lc.sol(t_lc)
ax.plot(y_lc[0], y_lc[1], color=WHITE, lw=1.9, alpha=0.9, zorder=5)

ax.set_xlim(-4.8, 4.8); ax.set_ylim(-5.2, 5.2)
ax.set_aspect('equal')
ax.set_title('limit cycle', color=WHITE, fontsize=12, pad=10, fontfamily='monospace')
ax.text(0, 4.7,
        'approach: deferred\norbit: exhaustible',
        color=BLUE, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.text(0, -4.75,
        'approach never arrives\norbit is periodic, finite',
        color=LABEL_CLR, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.axis('off')

# ── Panel 3: Lorenz — approach deferred, orbit inexhaustible ─────────────────
ax = axes[2]
ax.set_facecolor('#0a0a0a')

def lorenz(t, y, sigma=10, rho=28, beta=8/3):
    x, z, w = y
    return [sigma * (z - x), x * (rho - w) - z, x * z - beta * w]

sol_lorenz = solve_ivp(lorenz, [0, 80], [0.1, 0, 0], dense_output=True, max_step=0.01)
t_ev = np.linspace(5, 80, 15000)
pts = sol_lorenz.sol(t_ev)
x_l, z_l = pts[0], pts[1]   # x-z projection

# color by speed (proxy for trajectory density)
speeds = np.sqrt(np.diff(x_l)**2 + np.diff(z_l)**2)
norm_sp = (speeds - speeds.min()) / (speeds.max() - speeds.min() + 1e-9)

from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('lz', [BLUE, TEAL, AMBER], N=256)

for i in range(0, len(norm_sp)-1, 3):
    c = cmap(norm_sp[i])
    ax.plot(x_l[i:i+4], z_l[i:i+4], color=c, alpha=0.25, lw=0.55)

ax.set_xlim(-22, 22); ax.set_ylim(-3, 52)
ax.set_aspect('auto')
ax.set_title('strange attractor', color=WHITE, fontsize=12, pad=10, fontfamily='monospace')
ax.text(0, 50.5,
        'approach: deferred\norbit: inexhaustible',
        color=TEAL, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.text(0, -1.5,
        'approach never arrives\norbit never closes',
        color=LABEL_CLR, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.axis('off')

# ── Panel 4: heteroclinic — approach forbidden, orbit is the form ─────────────
ax = axes[3]
ax.set_facecolor('#0a0a0a')

def duffing(t, y):
    return [y[1], y[0] - y[0]**3]

# periodic orbits inside each well (context)
for cx in [1.0, -1.0]:
    for amp in [0.18, 0.38, 0.58, 0.75]:
        y0 = [cx + amp, 0]
        sol = solve_ivp(duffing, [0, 20], y0, dense_output=True, max_step=0.02)
        t_ev = np.linspace(0, 20, 800)
        pts = sol.sol(t_ev)
        mask = (np.abs(pts[0]) < 2.0) & (np.abs(pts[1]) < 1.8)
        if mask.sum() > 2:
            ax.plot(pts[0][mask], pts[1][mask], color=PURPLE, alpha=0.3, lw=0.8)

# heteroclinic separatrix — the form that requires non-arrival
x_h = np.linspace(-np.sqrt(2), np.sqrt(2), 1400)
y_h = x_h * np.sqrt(np.maximum(0.0, 1 - x_h**2 / 2))
ax.plot(x_h,  y_h, color=WHITE, lw=1.9, alpha=0.9, zorder=5)
ax.plot(x_h, -y_h, color=WHITE, lw=1.9, alpha=0.9, zorder=5)

# saddle (forbidden destination)
ax.plot(0, 0, 's', color=AMBER, ms=5, zorder=10)
ax.plot( 1, 0, 'o', color='#888', ms=4, zorder=10)
ax.plot(-1, 0, 'o', color='#888', ms=4, zorder=10)

ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.set_title('heteroclinic orbit', color=WHITE, fontsize=12, pad=10, fontfamily='monospace')
ax.text(0, 1.52,
        'approach: forbidden\norbit: form',
        color=PURPLE, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.text(0, -1.46,
        'arrival dissolves the type\nthe orbit is what the form is',
        color=LABEL_CLR, fontsize=8, ha='center', va='top', fontfamily='monospace')
ax.axis('off')

# ── supertitle ────────────────────────────────────────────────────────────────
fig.suptitle('approach fate  ×  orbit fate', color='#cccccc', fontsize=14,
             fontfamily='monospace', y=1.01)

plt.tight_layout(rect=[0, 0.0, 1, 1])
plt.savefig('assets/approach-orbit-matrix.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0a', edgecolor='none')
print("saved")
