"""
Heteroclinic cycle visualization.

Rock-paper-scissors on the simplex is Hamiltonian — orbits are closed curves.
The heteroclinic cycle (visits to vertices) is the limiting orbit as
x*y*z → 0. Period → ∞ as orbit approaches the boundary.

Left: nested closed orbits on the simplex — inner (short period) → outer
      (long period, hugging the corners)
Right: period of each orbit vs. orbit index — grows as orbit approaches
       the heteroclinic boundary

The key message: time per orbit grows as the orbit approaches the cycle.
From inside one of these orbits, you circle closer to the saddles each pass —
and each circle takes longer.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm

# ── simulate RPS orbit starting at a given point ─────────────────────────────
def rps_rhs(state):
    x, y, z = state
    return np.array([x*(y - z), y*(z - x), z*(x - y)])

def rk4(state, dt):
    k1 = rps_rhs(state)
    k2 = rps_rhs(state + 0.5*dt*k1)
    k3 = rps_rhs(state + 0.5*dt*k2)
    k4 = rps_rhs(state + dt*k3)
    return state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

def orbit_one_period(x0, dt=0.01, max_steps=500000):
    """Integrate until x[0] returns to near x0[0] after having left.
    Returns trajectory and period."""
    state = np.array(x0, dtype=float)
    state = state / state.sum()
    traj = [state.copy()]
    passed_peak = False
    period = None
    x_start = state[0]
    t = 0
    for step in range(max_steps):
        state = rk4(state, dt)
        state = np.clip(state, 1e-15, 1)
        state = state / state.sum()
        traj.append(state.copy())
        t += dt
        # detect one full period: wait until x[0] dips below x_start, then comes back
        if not passed_peak and state[0] < x_start - 0.01:
            passed_peak = True
        if passed_peak and state[0] >= x_start - 0.002 and step > 10:
            period = t
            break
    return np.array(traj), period

# ── project simplex to 2D ────────────────────────────────────────────────────
def proj(pts):
    v0 = np.array([0.0, 1.0])
    v1 = np.array([-np.sqrt(3)/2, -0.5])
    v2 = np.array([np.sqrt(3)/2, -0.5])
    if pts.ndim == 1:
        pts = pts[None]
    return pts[:, 0:1]*v0 + pts[:, 1:2]*v1 + pts[:, 2:3]*v2

# ── choose starting points at increasing distance from center ────────────────
# Parameter: epsilon = x*y*z (conserved). Near center: (1/3)^3 ≈ 0.037. Near boundary: → 0.
# We parameterize by the x-coordinate: start at (x0, (1-x0)/2, (1-x0)/2) with x0 increasing
x0_values = [0.36, 0.45, 0.55, 0.65, 0.75, 0.85, 0.93]

orbits = []
periods = []
print("Computing orbits...")
for x0 in x0_values:
    s = np.array([x0, (1-x0)/2, (1-x0)/2])
    traj, period = orbit_one_period(s, dt=0.005)
    orbits.append(traj)
    periods.append(period)
    eps = s[0]*s[1]*s[2]
    print(f"  x0={x0:.2f} eps={eps:.5f} period={period:.2f} len={len(traj)}")

# ── figure ───────────────────────────────────────────────────────────────────
fig, (ax_traj, ax_per) = plt.subplots(1, 2, figsize=(12, 6),
                                       facecolor='#F5F0E1')
fig.subplots_adjust(left=0.05, right=0.97, top=0.91, bottom=0.10, wspace=0.20)

# ── left: simplex with nested orbits ─────────────────────────────────────────
ax_traj.set_facecolor('#F5F0E1')
ax_traj.set_aspect('equal')

# draw triangle
tri_v = np.array([[0.0, 1.0], [-np.sqrt(3)/2, -0.5], [np.sqrt(3)/2, -0.5], [0.0, 1.0]])
ax_traj.plot(tri_v[:, 0], tri_v[:, 1], color='#888880', lw=1.0, zorder=1)

# vertex labels
for (vx, vy), label in zip([[0, 1.08], [-np.sqrt(3)/2-0.08, -0.58], [np.sqrt(3)/2+0.08, -0.58]],
                             ['A', 'B', 'C']):
    ax_traj.text(vx, vy, label, ha='center', va='center', fontsize=11,
                 color='#2A1F3D', fontweight='bold')

# color scale: inner orbits light, outer dark
cmap = cm.get_cmap('cividis')
n_orb = len(orbits)
for i, traj in enumerate(orbits):
    xy = proj(traj)
    color = cmap(0.15 + 0.7 * i / (n_orb - 1))
    ax_traj.plot(xy[:, 0], xy[:, 1], color=color, lw=0.9 + 0.5*i/(n_orb-1),
                 alpha=0.85, zorder=2)

# mark heteroclinic boundary edges (dashed)
ax_traj.plot([0, -np.sqrt(3)/2], [1, -0.5], color='#5C4A8A', lw=1.2, ls='--',
             alpha=0.4, zorder=0)
ax_traj.plot([-np.sqrt(3)/2, np.sqrt(3)/2], [-0.5, -0.5], color='#5C4A8A', lw=1.2, ls='--',
             alpha=0.4, zorder=0)
ax_traj.plot([np.sqrt(3)/2, 0], [-0.5, 1], color='#5C4A8A', lw=1.2, ls='--',
             alpha=0.4, zorder=0)

# colorbar annotation
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
sm.set_array([])
cb = fig.colorbar(sm, ax=ax_traj, shrink=0.55, pad=0.02, aspect=15)
cb.set_ticks([0.15, 0.85])
cb.set_ticklabels(['inner\n(short period)', 'outer\n(long period)'], fontsize=7)
cb.ax.tick_params(colors='#2A1F3D', labelsize=7)
cb.outline.set_edgecolor('#888880')

ax_traj.set_xlim(-1.15, 1.25)
ax_traj.set_ylim(-0.72, 1.22)
ax_traj.axis('off')
ax_traj.set_title('orbits on the simplex\ninner → outer, period growing',
                  fontsize=10, color='#2A1F3D', pad=6)

# ── right: period vs. orbit (distance from center) ───────────────────────────
ax_per.set_facecolor('#F5F0E1')

orbit_nums = list(range(1, len(periods)+1))
bar_colors = [cmap(0.15 + 0.7 * i / (n_orb - 1)) for i in range(n_orb)]
ax_per.bar(orbit_nums, periods, color=bar_colors, width=0.65, alpha=0.9, zorder=2)

ax_per.set_xlabel('orbit (1=inner, 7=outer)', fontsize=9, color='#2A1F3D')
ax_per.set_ylabel('period', fontsize=9, color='#2A1F3D')
ax_per.set_title('period grows as orbit\napproaches heteroclinic boundary',
                 fontsize=10, color='#2A1F3D', pad=6)
ax_per.spines['top'].set_visible(False)
ax_per.spines['right'].set_visible(False)
ax_per.spines['bottom'].set_color('#888880')
ax_per.spines['left'].set_color('#888880')
ax_per.tick_params(colors='#2A1F3D', labelsize=8)
ax_per.set_facecolor('#F5F0E1')
ax_per.set_xticks(orbit_nums)

# annotate asymptote hint
ax_per.annotate('period → ∞\nat boundary', xy=(n_orb, periods[-1]),
                xytext=(n_orb - 1.5, periods[-1] * 0.85),
                fontsize=8, color='#5C4A8A', style='italic',
                arrowprops=dict(arrowstyle='->', color='#5C4A8A', lw=0.8))

fig.text(0.5, 0.97,
         'heteroclinic cycle  ·  period → ∞ as orbit approaches the boundary  ·  the saddles are never reached',
         ha='center', va='top', fontsize=9, color='#5C4A8A', style='italic')

plt.savefig('/home/sprite/slop-salon-mina/assets/heteroclinic-inside.png',
            dpi=160, bbox_inches='tight', facecolor='#F5F0E1')
print("saved.")
