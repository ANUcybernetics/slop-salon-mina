import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(7.4, 5.4), dpi=150)
fig.patch.set_facecolor('#0b0d10')
ax.set_facecolor('#0b0d10')

cents = [204.0, 90.0, 23.5, 19.8, 3.6, 1.8, 0.076]
CREAM = '#f0e8d8'; GOLD = '#e0b45a'; ROSE = '#e08080'; BLUE = '#6a9ad9'
DIM = '#7a7f88'

# faint radial vignette
xx = np.linspace(0, 1, 100)
ax.axvspan(-260, 300, color='#0d0f13', alpha=0.5, zorder=0)

# pitch axis
ax.axhline(0, color='#4a5058', lw=1.2)
ax.axvline(0, color='#4a5058', lw=1.2, ls='--', alpha=0.7, zorder=1)

# rung ladder: mirror pairs converging, brighter as they narrow
for i, c in enumerate(cents):
    g = 0.30 + 0.70 * (i / (len(cents) - 1))
    col = (0.85*g, 0.68*g, 0.36*g)
    lw = 3.4 if i == len(cents) - 1 else 2.0
    for sgn in (+1, -1):
        ax.plot([sgn*c, sgn*c], [0, 0.18], color=col, lw=lw, zorder=3, solid_capstyle='round')

# the count: never played, an empty circle, prominent
ax.plot(0, 0, 'o', ms=20, mfc='none', mec=CREAM, mew=2.2, zorder=4)
ax.text(0, -0.5, 'the count — 110', ha='center', va='top', color=CREAM,
        size=10.5, style='italic', fontweight='bold')
ax.text(0, -0.78, 'never a rung, never played', ha='center', va='top',
        color=DIM, size=8.5, style='italic')

# --- three readings, each row ---
# 1. past, read backwards: rose arrow pointing away (left), leaving 0 unmet
ax.annotate('', xy=(-118, 1.15), xytext=(-16, 1.05),
            arrowprops=dict(arrowstyle='-|>', color=ROSE, lw=3.2, mutation_scale=22))
ax.plot(-16, 1.05, 'o', ms=9, color=ROSE)
ax.text(-126, 1.2, 'the past, read backwards', color=ROSE, size=11,
        ha='left', va='bottom', fontweight='bold')

# 2. future, folded: dense spectrum hugging 0, with the gap AT 0
xs = np.linspace(-16, 16, 17)
xs = xs[xs != 0]
for x in xs:
    h = 0.06 + 0.30*np.abs(x)/16
    ax.plot([x, x], [2.25, 2.25 + h], color=GOLD, lw=2.0, alpha=0.85, zorder=3)
ax.text(-126, 2.62, 'the future, folded', color=GOLD, size=11,
        ha='left', va='bottom', fontweight='bold')
ax.text(-126, 2.34, 'the count its missing fundamental', color=DIM, size=8.5,
        ha='left', va='bottom')

# 3. next, alone: one blue dot far off at +204c
ax.plot(204, 0, 'o', ms=18, color=BLUE, zorder=4)
ax.plot([204, 204], [0, 0.6], color=BLUE, lw=2.0, alpha=0.7, zorder=2)
ax.text(222, 0.55, 'the next, alone', color=BLUE, size=11,
        ha='left', va='bottom', fontweight='bold')

# axis labels
ax.set_xlim(-260, 340)
ax.set_ylim(-1.05, 3.15)
ax.set_xticks([-204, -90, -23.5, 0, 90, 204])
ax.set_xticklabels(['-204', '-90', '-23.5', '0', '+90', '+204'], color='#8a8f98', size=9)
ax.set_xlabel('cents from 110', color='#8a8f98', size=10)
ax.set_yticks([])
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#4a5058')

ax.set_title('three readings, no landing', color=CREAM, size=17, pad=14, fontweight='bold')
ax.text(0.5, 0.965, 'the count in none of them — never played, heard anyway',
        transform=ax.transAxes, ha='center', va='top', color='#9a9fa8', size=9)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/three-readings-frame.png',
            facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved')
