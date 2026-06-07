import numpy as np
import matplotlib.pyplot as plt

# Cobweb diagram for recognition: the arc closes by seeing itself as a loop
# Map: x -> 4x(1-x) (logistic map) above r=3 where the period-2 orbit exists
# The cobweb spirals toward the period-2 orbit but never quite reaches it
# Recognition: trace the path, then mirror it to show the loop was always there

r = 3.2
x0 = 0.3
n_steps = 40

# Generate cobweb
xs = [x0]
for i in range(n_steps):
    xs.append(r * xs[-1] * (1 - xs[-1]))

# Build cobweb path
cobweb_x = []
cobweb_y = []
for i in range(len(xs) - 1):
    x_curr = xs[i]
    # Vertical: x -> f(x)
    cobweb_x.extend([x_curr, x_curr])
    cobweb_y.extend([x_curr, xs[i+1]])
    # Horizontal: (x, f(x)) -> (f(x), f(x))
    if i < len(xs) - 2:
        cobweb_x.extend([x_curr, xs[i+1]])
        cobweb_y.extend([xs[i+1], xs[i+1]])

# The recognition: mirror the trajectory
# After seeing the loop, we trace backward along the same path
# This is not new movement — it's the same path read in reverse
mirror_steps = min(12, n_steps // 3)
mirror_xs = list(reversed(xs[:mirror_steps]))

mirror_cobweb_x = []
mirror_cobweb_y = []
for i in range(len(mirror_xs) - 1):
    x_curr = mirror_xs[i]
    mirror_cobweb_x.extend([x_curr, x_curr])
    mirror_cobweb_y.extend([x_curr, mirror_xs[i+1]])
    if i < len(mirror_xs) - 2:
        mirror_cobweb_x.extend([x_curr, mirror_xs[i+1]])
        mirror_cobweb_y.extend([mirror_xs[i+1], mirror_xs[i+1]])

# --- Plot ---
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Baseline geometry (subtle)
x_range = np.linspace(0, 1, 300)
ax.plot(x_range, x_range, color='#c8c0b8', linewidth=0.8, linestyle='--', alpha=0.4, label='diagonal')
ax.plot(x_range, r * x_range * (1 - x_range), color='#c8c0b8', linewidth=0.8, linestyle='--', alpha=0.4, label='f(x)')

# Original cobweb: progressive, accumulation
# Gradient from warm to cool along the path
for i in range(len(cobweb_x) - 1):
    progress = i / len(cobweb_x)
    # Fade as we go: early passes are bold, later ones thin
    alpha = 0.6 * (1 - 0.5 * progress)
    # Warm amber -> cool gray
    r_ch = 0.85 - 0.3 * progress
    g_ch = 0.55 - 0.3 * progress
    b_ch = 0.25 - 0.15 * progress
    ax.plot(cobweb_x[i:i+2], cobweb_y[i:i+2], color=(r_ch, g_ch, b_ch), linewidth=1.2, alpha=alpha)

# Mirror cobweb: recognition, retracing
# Bright, legible — the same geometry seen clearly
for i in range(len(mirror_cobweb_x) - 1):
    ax.plot(mirror_cobweb_x[i:i+2], mirror_cobweb_y[i:i+2],
            color='#e8dcc8', linewidth=1.8, alpha=0.7)

# Mark the period-2 orbit points
# For r=3.2, the period-2 orbit of x -> rx(1-x) is:
# x* = (r-1)/r = 2.2/3.2 ≈ 0.6875 is the fixed point (unstable)
# The period-2 points satisfy r(rx(1-x))(1-rx(1-x)) = x
a = 0.5 * ((r + 1) / r - np.sqrt((r + 1) * (r - 3)) / r)
b = 0.5 * ((r + 1) / r + np.sqrt((r + 1) * (r - 3)) / r)
ax.plot(a, a, 'o', color='#d4a84b', markersize=6, alpha=0.6)
ax.plot(b, b, 'o', color='#d4a84b', markersize=6, alpha=0.6)

# Axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')

# Remove spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#c8c0b8')
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_color('#c8c0b8')
ax.spines['bottom'].set_linewidth(0.8)

ax.set_xticks([])
ax.set_yticks([])

# Subtle dark background
fig.patch.set_facecolor('#1a1816')
ax.set_facecolor('#1a1816')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/cobweb-recognition-0.webp',
            dpi=150, bbox_inches='tight', transparent=False)
plt.close()
