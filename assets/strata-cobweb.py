import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# "Stratifications, not consequences"
# The cobweb doesn't produce the diagonal — they coexist as layers.
# Show multiple parameter values (r) as horizontal layers, each
# with its own cobweb + diagonal, stacked vertically.
# At r<3: convergent to fixed point. At r=3: tangency. At r>3: period-doubling.
# The diagonal runs through all of them.

r_values = [2.5, 2.7, 2.9, 2.99, 3.01, 3.3, 3.5, 3.87]
n_rows = len(r_values)

fig, axes = plt.subplots(n_rows, 1, figsize=(6, 10))
if n_rows == 1:
    axes = [axes]

amber_palette = ['#D4A574', '#C4956A', '#B8860B', '#D4A574', '#E8C39E', '#A0826D', '#D4B896', '#8B7355']

for idx, (r, ax, color) in enumerate(zip(r_values, axes, amber_palette)):
    t = np.linspace(0, 1, 500)
    f_vals = r * t * (1 - t)
    
    # Diagonal
    ax.plot([0, 1], [0, 1], color='#555555', linewidth=0.8, alpha=0.5)
    
    # Function
    ax.plot(t, f_vals, color='#666666', linewidth=1, alpha=0.4)
    
    # Cobweb from multiple seeds to show the stratification
    seeds = [0.1, 0.3, 0.5, 0.7, 0.9]
    for seed in seeds:
        x = seed
        for i in range(100):
            y = r * x * (1 - x)
            alpha = 0.15 + 0.35 * (1 - i/100)
            # Horizontal
            ax.plot([x, y], [y, y], color=color, linewidth=0.5, alpha=alpha*0.5)
            # Vertical
            ax.plot([y, y], [y, x], color=color, linewidth=0.5, alpha=alpha*0.5)
            x = y
    
    # Fixed point marker if it exists
    if r <= 4:
        x_star = 1 - 1/r
        ax.plot(x_star, x_star, 'o', color=color, markersize=3, alpha=0.7)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#1a1a1a')

fig.patch.set_facecolor('#1a1a1a')

# r value labels on the left
for idx, r in enumerate(r_values):
    axes[idx].text(-0.05, 0.5, f'r={r}', transform=axes[idx].transAxes,
                  fontsize=8, color='#888888', va='center', ha='right')

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-mina/assets/strata-cobweb.png', dpi=150,
            facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
