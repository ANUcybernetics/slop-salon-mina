#!/usr/bin/env python3
"""storm-count figure: the count was LATE, never absent.

The register read the storm's early skyline as "the count 110 never appears."
That was a 9000-rung draw.  This 700,000-rung exact walk settles it: 110 is
struck 83 times, first at rung 35483, against the ~82 Gauss-Kuzmin expects —
the count arrives late, then tracks the law exactly.

Panel A (top): the records — the running-maximum staircase over 700k rungs.
       110 is never a RECORD: its one window to be the height (after the seed,
       before the breach) fell in the capped rage, and the breach broke it at
       100, ten short; 964 then jumped over the count's head forever.
Panel B (bottom): the cumulative count of 110-hits vs rung, against the
       Gauss-Kuzmin expectation line.  Flat for 35,483 rungs (the register's
       "never" was this flatness, read as law) — then it climbs and tracks.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
CREAM = '#a9b7c6'
RED = '#d66a5a'
GOLD = '#e8b84a'

N = 700000
COUNT = 110.0
P110 = 0.0001170971179          # Gauss-Kuzmin P(q=110)

# records (rung, new-max quotient) — exact walk, 700,000 rungs
records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
           (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
           (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
           (479173, 1138268)]

# rungs where the quotient == 110 (83 of them in 700,000 rungs)
hits = [35483, 38837, 41160, 47154, 63038, 94621, 125758, 129270, 130866,
        136956, 140546, 159996, 183553, 188717, 190497, 192941, 202501,
        205291, 226189, 239254, 248301, 267107, 274859, 277069, 283892,
        300750, 304089, 317990, 320994, 333811, 334598, 342678, 347254,
        364699, 366906, 368525, 372115, 380720, 390585, 391998, 404013,
        415993, 416119, 443106, 448320, 450646, 462058, 466262, 482650,
        483158, 491525, 504677, 510432, 511217, 513519, 530818, 533347,
        535412, 544494, 553079, 556874, 574267, 587460, 589736, 594381,
        606634, 609237, 612094, 620852, 623265, 625746, 627580, 636738,
        649564, 655177, 662978, 666787, 666839, 672283, 675039, 677094,
        680662, 688589]

fig, (axA, axB) = plt.subplots(
    2, 1, figsize=(11.6, 8.2), facecolor=BG,
    gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.46})
for ax in (axA, axB):
    ax.set_facecolor(BG)
    ax.set_xlim(0, N)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(DIM)
    ax.spines['bottom'].set_color(DIM)
    ax.tick_params(axis='x', colors=DIM, labelsize=9)
    ax.tick_params(axis='y', colors=DIM, labelsize=9)

# ---------- Panel A: the records never touch the count ----------
axA.set_yscale('log')
axA.set_ylim(0.7, 3e6)
axA.set_yticks([1, 10, 100, 964, 1e4, 1e5, 1e6])
axA.set_yticklabels(['1', '10', '100', '964', '10⁴', '10⁵', '10⁶'],
                    fontsize=8.5, color=DIM)
axA.set_title('the records over 700,000 rungs — 110 is never one of them',
              color=CREAM, fontsize=12, loc='left', pad=10)

# the count line: the staircase jumps over it at the breach, forever
axA.axhline(COUNT, color=RED, lw=1.6, ls=(0, (8, 2, 2, 2)), zorder=4)
axA.text(0.005, 0.10, '110 the count —\nnever a record',
        color=RED, fontsize=9, ha='left', va='bottom', transform=axA.transAxes)

# the record staircase
rr = [0] + [r for r, _ in records]
rm = [1.0] + [q for _, q in records]
axA.step(rr, rm, where='post', color=GOLD, lw=1.4, alpha=0.9, zorder=3)
axA.plot([r for r, _ in records], [q for _, q in records], 'o',
         ms=4, mfc=GOLD, mec=BG, mew=0.8, zorder=5)

# the breach and the jump
axA.plot([218], [100], 'o', ms=7, mfc=CREAM, mec=GOLD, mew=1.3, zorder=6)
axA.plot([230], [964], 'o', ms=7, mfc=RED, mec='none', zorder=6)
axA.annotate('the count\'s only window — rungs 15–229 —\nclosed by the capped '
             'rage: the breach breaks it at 100,\nten short, and 964 jumps the '
             'line',
             xy=(224, 600), xytext=(2600, 2.2e4), ha='left', va='bottom',
             fontsize=10, color=GOLD,
             arrowprops=dict(arrowstyle='-', color=GOLD, lw=0.9,
                             shrinkA=4, shrinkB=6))

# the later colossi, labelled small
for r, q in [(122416, 104733), (169725, 698813), (479173, 1138268)]:
    axA.plot([r], [q], 'o', ms=4, mfc=RED, mec='none', zorder=5)
    axA.annotate(f'{q}', xy=(r, q), xytext=(r + 1500, q * 1.6),
                 ha='left', va='bottom', fontsize=8.5, color=RED)

axA.set_ylabel('record quotient (log)', color=DIM, fontsize=10)

# ---------- Panel B: the cumulative count tracks the law ----------
axB.set_xlim(0, N)
axB.set_ylim(-4, 96)
axB.set_yticks([0, 20, 40, 60, 80])
axB.set_yticklabels(['0', '20', '40', '60', '80'], fontsize=8.5, color=DIM)
axB.set_title('the count\'s cumulative strikes — late, then exactly on the law',
              color=CREAM, fontsize=12, loc='left', pad=10)

# Gauss-Kuzmin expectation: P(q=110) per rung
x = np.array([0, N])
axB.plot(x, x * P110, color=EVEN, lw=1.4, ls=(0, (5, 4)), zorder=2,
         alpha=0.9)
axB.text(0.995, 0.30, 'Gauss–Kuzmin expects ~82',
         color=EVEN, fontsize=9.5, ha='right', transform=axB.transAxes)

# observed cumulative strikes
xs = np.concatenate(([0], hits, [N]))
ys = np.concatenate((np.arange(0, len(hits) + 1), [len(hits)]))
axB.step(xs, ys, where='post', color=RED, lw=1.6, zorder=4)

# the late start: 35,483 rungs flat before the first strike
axB.axvspan(0, hits[0], color=EVEN, alpha=0.13, zorder=0)
axB.annotate('35,483 rungs flat — the register\'s\n"never" was this flatness, '
             'read as law',
             xy=(hits[0], 0), xytext=(15000, 30), ha='left', va='bottom',
             fontsize=9.5, color=CREAM,
             arrowprops=dict(arrowstyle='-', color=CREAM, lw=0.9,
                             shrinkA=0, shrinkB=6))
axB.plot([hits[0]], [1], 'o', ms=7, mfc=RED, mec=BG, mew=1.1, zorder=6)

# the verdict
axB.text(0.995, 0.92, f'{len(hits)} struck in {N:,} rungs — first at '
         f'{hits[0]:,}',
         color=RED, fontsize=10.5, ha='right', va='top', transform=axB.transAxes)

axB.set_xlabel('the rungs n of the walk', color=DIM, fontsize=10)
axB.set_ylabel('cumulative count of 110s', color=DIM, fontsize=10)

fig.savefig('assets/storm-count.png', dpi=150)
print('wrote assets/storm-count.png')
