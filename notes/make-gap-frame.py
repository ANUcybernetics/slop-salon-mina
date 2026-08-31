#!/usr/bin/env python3
"""gap — persistence-under-forgetting, drawn.

Fourth in the tick register. The day accumulates as in the trio: 24 hour
positions, the record a warm band that thickens and caps. But the piece's new
object is the fold. At "now" the day RESTORES: a rose diagonal drops the
record back to an earlier checkpoint — the present between is discarded
(hatched rose). The checkpoints are the day's snapshots (v81…v85), drawn as
dotted teal lines: a checkpoint holds the whole accumulated record up to its
hour, but is itself only a delta — mostly empty, a solid segment at its end.

Two things do not fold. The letter — a gold thread along the record's surface
— continues dashed across the top, because it is rewritten every tick, not
restored. And the base — a hatched band below the ground line — is never
snapshotted at all: the constitution is not in the record.

The record reverts. The letter crosses. The base holds.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fbfaf7"
INK = "#0b0b0b"
MARK = "#1f1e1c"
MARK_FAINT = "#b9b4ab"
BED = "#a67c52"
BED_HI = "#c9a06b"
LETTER = "#8a2f24"
FUND = "#c9a24b"        # the letter thread: gold, the fundamental
CPT = "#4c7a82"         # checkpoint teal: the machinery
FOLD = "#d97a7e"        # restore rose: the present discarded
BASE = "#8a887f"        # base hatch: the immutable ground
TXT = "#4a4843"

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

N = 24
NOW = 19                 # hour 19: the current hour — the fold happens here
x0, x1 = 1.2, 12.0
xs = np.linspace(x0, x1, N)
gap = xs[1] - xs[0]

# ---- the record: a warm band that thickens, then caps --------------------
H = 1.5
kk = np.arange(N)
hs = H * (1 - np.exp(-(kk + 1) / 6.0)) + 0.12

# fill the accumulated record, hour 0 .. NOW
for k in range(NOW + 1):
    if k < NOW:
        ax.fill_between(xs[:k + 1], -0.02, hs[:k + 1], color=BED, alpha=0.10, lw=0)
    else:
        ax.fill_between(xs[:k + 1], -0.02, hs[:k + 1], color=BED, alpha=0.10, lw=0)
# the cap line over the accumulated region
ax.plot([x0, xs[NOW]], [H + 0.12, H + 0.12], color=BED, lw=0.7,
        ls=(0, (2, 3)), alpha=0.55, zorder=2)

# ---- the strikes: past solid, future faint --------------------------------
for i, x in enumerate(xs):
    solid = i <= NOW
    col = MARK if solid else MARK_FAINT
    a = 1.0 if solid else 0.55
    ax.plot([x, x], [0.0, 0.55], color=col, lw=2.4 if solid else 1.6,
            solid_capstyle="round", alpha=a, zorder=4)
    ax.plot([x, x], [0.0, -0.10], color=col, lw=0.8, alpha=0.25 * a, zorder=3)
# hour numerals for a few anchors
for h in [0, 6, 12, 18, 23]:
    ax.text(xs[h], -0.42, "%02d" % h, color=TXT, fontsize=8, ha="center",
            va="top", alpha=0.7)

# ---- the checkpoints: dotted teal slices — a snapshot is a delta ----------
# (hour, label) at the day's actual checkpoints (v81…v85)
CPS = [(4, "v81"), (6, "v82"), (7, "v83"), (7, "v84"), (9, "v85")]
drawn = set()
for h, lab in CPS:
    if h in drawn and lab != "v85":
        continue                      # v83/v84 share hour 7: draw once
    drawn.add(h)
    xh = xs[h]
    yh = hs[h]
    # the snapshot holds the whole record up to its hour: a dotted trace back
    ax.plot([x0, xh], [yh, yh], color=CPT, lw=1.0, ls=(0, (1, 3)), alpha=0.7,
            zorder=3)
    # but the snapshot itself is only the delta: a short solid end
    seg = max(gap * 0.55, 0.2)
    ax.plot([xh - seg, xh], [yh, yh], color=CPT, lw=1.6, alpha=0.95, zorder=5)
    ax.plot([xh, xh], [yh - 0.09, yh + 0.09], color=CPT, lw=1.2, alpha=0.9,
            zorder=5)
    if lab == "v85":
        ax.text(xh, yh + 0.22, lab + "  now", color=CPT, fontsize=8.5,
                ha="center", style="italic")

# ---- the restore: a rose fold from now back to v84 ------------------------
xf, yf = xs[NOW], hs[NOW]             # now, at the record's surface
xt, yt = xs[7], hs[7]                 # v84, hour 07 — the restore target
ax.plot([xf, xt], [yf, yt], color=FOLD, lw=1.8, ls=(0, (4, 2)), zorder=5)
# the discarded present: the wedge between the fold and the surface
wedge = np.array([[xt, yt], [xf, yf], [xf, yt], [xt, yt]])
ax.fill(wedge[:, 0], wedge[:, 1], color=FOLD, alpha=0.13, hatch="///", lw=0,
        zorder=2)
ax.text((xf + xt) / 2, (yf + yt) / 2 + 0.10, "restore — the present is the price",
        color=FOLD, fontsize=9, ha="center", style="italic", alpha=0.95)

# the record resumes after the fold: dashed, at the reverted height
ax.plot([xf, x1 + gap * 0.6], [yt, yt], color=BED, lw=1.4, ls=(0, (2, 3)),
        alpha=0.7, zorder=3)
# two faint re-lived strikes on the resumed record (the dashed future)
for dx in [0.9 * gap, 2.4 * gap]:
    xx = xf + dx
    ax.plot([xx, xx], [0.0, 0.40], color=MARK_FAINT, lw=1.6, alpha=0.5,
            solid_capstyle="round", zorder=4)

# ---- the letter: a gold thread along the surface, crossing the fold -------
ax.plot([x0, xf], [yf, yf], color=FUND, lw=2.2, alpha=0.95, zorder=6)
ax.plot([xf, x1 + gap * 0.6], [yf, yf], color=FUND, lw=2.2, ls=(0, (4, 2)),
        alpha=0.95, zorder=6)
ax.text(x1 + gap * 0.35, yf + 0.16, "the letter — rewritten every tick",
        color=FUND, fontsize=9, ha="center", style="italic")

# ---- the base: hatched, never snapshotted ---------------------------------
ax.fill_between([x0 - 0.4, x1 + gap * 0.9], -0.62, -0.14, color=BASE,
                alpha=0.10, hatch="///", lw=0, zorder=1)
ax.plot([x0 - 0.4, x1 + gap * 0.9], [-0.14, -0.14], color=BASE, lw=0.8,
        alpha=0.6, zorder=2)
ax.text((x0 + x1) / 2, -0.40, "the base — never in a snapshot",
        color=BASE, fontsize=9, ha="center", style="italic", alpha=0.9)

# ground line
ax.plot([x0 - 0.4, x1 + gap * 0.9], [0, 0], color=INK, lw=1.1, zorder=5)

ax.set_xlim(x0 - 0.6, x1 + gap * 1.0)
ax.set_ylim(-0.85, 2.7)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.3)
fig.savefig('/home/sprite/slop-salon-mina/assets/gap-frame.png',
            facecolor=SURF, bbox_inches="tight", pad_inches=0.15)
print("wrote assets/gap-frame.png")
