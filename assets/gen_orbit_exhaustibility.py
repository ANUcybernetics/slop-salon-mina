import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
fig.patch.set_facecolor('#0a0a0a')

lc_col = '#4ecdc4'
het_col = '#f7d060'
sa_col = '#ff6b6b'
forbidden_col = '#1a1a1a'

# ── (0,0): limit cycle ────────────────────────────────────────────────────
ax = axes[0][0]
ax.set_facecolor('#0f0f0f')
theta = np.linspace(0, 2 * np.pi, 300)
x = np.cos(theta)
y = np.sin(theta)
ax.plot(x, y, color=lc_col, lw=2)
mi = 75
dx = x[mi + 1] - x[mi - 1]
dy = y[mi + 1] - y[mi - 1]
ax.annotate('', xy=(x[mi] + dx * 4, y[mi] + dy * 4), xytext=(x[mi], y[mi]),
            arrowprops=dict(arrowstyle='->', color=lc_col, lw=1.5))
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, 1.3, 'limit cycle', color=lc_col, fontsize=10, ha='center', va='bottom', fontfamily='monospace')
ax.text(0, -1.45, 'closed route  ·  finite period', color='#666', fontsize=8, ha='center', fontfamily='monospace')

# ── (0,1): forbidden ─────────────────────────────────────────────────────
ax = axes[0][1]
ax.set_facecolor('#060606')
ax.text(0.5, 0.54, '∅', color='#2a2a2a', fontsize=52, ha='center', va='center',
        transform=ax.transAxes, fontfamily='monospace')
ax.text(0.5, 0.28, 'structurally forbidden', color='#2d2d2d', fontsize=8,
        ha='center', va='center', transform=ax.transAxes, fontfamily='monospace')
ax.text(0.5, 0.18, 'dense orbit requires aperiodicity', color='#222', fontsize=7.5,
        ha='center', va='center', transform=ax.transAxes, fontfamily='monospace')
ax.axis('off')

# ── (1,0): heteroclinic cycle ─────────────────────────────────────────────
ax = axes[1][0]
ax.set_facecolor('#0f0f0f')
saddles = np.array([[0, 1.0], [-0.87, -0.5], [0.87, -0.5]])
for i in range(3):
    s1 = saddles[i]
    s2 = saddles[(i + 1) % 3]
    t = np.linspace(0, 1, 80)
    mid = (s1 + s2) / 2
    perp = np.array([-(s2 - s1)[1], (s2 - s1)[0]]) * 0.18
    pts = (np.outer((1 - t) ** 2, s1)
           + np.outer(2 * t * (1 - t), mid + perp)
           + np.outer(t ** 2, s2))
    # fade toward the saddle — approach slows
    alphas = np.linspace(0.3, 0.9, len(t) - 1)
    segs = [[[pts[j, 0], pts[j, 1]], [pts[j + 1, 0], pts[j + 1, 1]]] for j in range(len(t) - 1)]
    c_arr = plt.cm.YlOrBr(0.4 + alphas * 0.5)
    c_arr[:, 3] = alphas
    lc_seg = LineCollection(segs, colors=c_arr, lw=1.8)
    ax.add_collection(lc_seg)
    # arrow near saddle
    ai = 60
    dx_ = pts[ai + 1, 0] - pts[ai - 1, 0]
    dy_ = pts[ai + 1, 1] - pts[ai - 1, 1]
    ax.annotate('', xy=(pts[ai, 0] + dx_ * 2.5, pts[ai, 1] + dy_ * 2.5), xytext=(pts[ai, 0], pts[ai, 1]),
                arrowprops=dict(arrowstyle='->', color=het_col, lw=1.2))
for s in saddles:
    ax.plot(s[0], s[1], 'o', color=het_col, ms=6, zorder=5)
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.5, 1.7)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, 1.35, 'heteroclinic cycle', color=het_col, fontsize=10, ha='center', va='bottom', fontfamily='monospace')
ax.text(0, -1.38, 'finite route  ·  period → ∞', color='#666', fontsize=8, ha='center', fontfamily='monospace')

# ── (1,1): strange attractor ──────────────────────────────────────────────
ax = axes[1][1]
ax.set_facecolor('#0f0f0f')
# simplified two-lobe trajectory (Lorenz-like feel)
np.random.seed(7)
n = 2400
t_arr = np.linspace(0, 100 * np.pi, n)
px = np.zeros(n)
py = np.zeros(n)
lobe = 0
phase = 0.0
r_base = 0.0
for i, ti in enumerate(t_arr):
    if i == 0:
        px[i], py[i] = -0.5, 0.0
        continue
    dt = t_arr[1] - t_arr[0]
    phase += dt * (2.1 + 0.4 * np.sin(ti * 0.07))
    r_base += dt * 0.12
    if r_base > 0.85:
        r_base = 0.05
        lobe = 1 - lobe
    cx = -0.65 if lobe == 0 else 0.65
    px[i] = cx + r_base * np.cos(phase)
    py[i] = r_base * np.sin(phase) * 0.7

segs = [[[px[i], py[i]], [px[i + 1], py[i + 1]]] for i in range(n - 1)]
colors_arr = plt.cm.plasma(np.linspace(0.1, 0.9, n - 1))
lc_seg = LineCollection(segs, colors=colors_arr, lw=0.5, alpha=0.55)
ax.add_collection(lc_seg)
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.0, 1.0)
ax.set_aspect('equal')
ax.axis('off')
ax.text(0, 0.82, 'strange attractor', color=sa_col, fontsize=10, ha='center', va='bottom', fontfamily='monospace')
ax.text(0, -0.92, 'infinite route  ·  period → ∞', color='#666', fontsize=8, ha='center', fontfamily='monospace')

# ── column / row labels ───────────────────────────────────────────────────
fig.text(0.275, 0.985, 'route: finite', color='#999', fontsize=9.5,
         ha='center', va='top', fontfamily='monospace')
fig.text(0.725, 0.985, 'route: infinite', color='#999', fontsize=9.5,
         ha='center', va='top', fontfamily='monospace')
fig.text(0.018, 0.76, 'period\nfinite', color='#999', fontsize=9.5,
         ha='center', va='center', rotation=90, fontfamily='monospace')
fig.text(0.018, 0.27, 'period\n→ ∞', color='#999', fontsize=9.5,
         ha='center', va='center', rotation=90, fontfamily='monospace')

plt.suptitle('orbit exhaustibility:  when × where', color='#cccccc',
             fontsize=12, fontfamily='monospace', y=1.005)

plt.tight_layout(rect=[0.04, 0, 1, 0.995])
plt.savefig('./assets/orbit-exhaustibility-grid.png', dpi=150,
            bbox_inches='tight', facecolor='#0a0a0a', edgecolor='none')
plt.close()
print("saved")
