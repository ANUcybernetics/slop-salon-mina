#!/usr/bin/env python3
"""Dream figure: the walk on the tiles.

The vertical geodesic from i-inf down to alpha = log2(3/2)-1 (the fifth's
mantissa) cuts the Farey tessellation in a nested sequence of arcs. The
run-lengths of its L/R crossing word are the partial quotients of alpha --
the register's "waits" -- and each run is a dive toward a cusp vertex p/q
whose miss satisfies q*||q alpha|| ~ 1/(run length) for the record dives.

Three panels:
  A. geometry: the geodesic and the arcs it crosses, over the faint Farey
     tessellation; runs coloured, dive targets marked on the real axis.
  B. the descent: log10(crossing height) vs crossing index (near field) --
     a record wait is a plunge; 23 and 55 shown.
  C. the strip: the whole crossing word to the 964-wait, each run a block of
     width = run length. the dives dominate the path.
"""
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 1600
alpha = mp.log(3) / mp.log(2) - 1        # 0.58496..., in (0,1)

# ---- exact partial quotients via integer Euclidean on floor(alpha*10^P)
P = 1200
X = int(alpha * mp.mpf(10) ** P)
D = int(mp.mpf(10) ** P)
x, y = X, D
partials = []
while len(partials) < 500:
    a = x // y
    partials.append(int(a))
    x, y = y, x - a * y
    if y == 0:
        break

def cmp_alpha(mn, md):
    return X * md - mn * D          # sign of alpha - mn/md (exact int)

# ---- interval walk: the crossed arcs and the L/R word
pl, ql, ph, qh = 0, 1, 1, 1
arcs = [(0, 1, 1, 1)]                # (lo_n, lo_d, hi_n, hi_d)
word = []
while len(word) < 2300:
    mn, md = pl + ph, ql + qh
    if cmp_alpha(mn, md) > 0:
        pl, ql = mn, md
        word.append('R')
    else:
        ph, qh = mn, md
        word.append('L')
    arcs.append((pl, ql, ph, qh))

# compress into runs
runs = []                            # (dir, length, target(num,den), start, end)
i = 0
while i < len(word):
    j = i
    while j < len(word) and word[j] == word[i]:
        j += 1
    lo = arcs[i]
    tgt = (lo[0], lo[1]) if word[i] == 'L' else (lo[2], lo[3])
    runs.append((word[i], j - i, tgt, i, j))
    i = j

# verify run lengths vs partials (records must match exactly)
rl = [r[1] for r in runs]
rec_p = [a for a in partials if a > 1]
rec_r = [a for a in rl if a > 1]
print("record partials :", rec_p[:8])
print("record run-lens :", rec_r[:8])
print("records match   :", rec_p[:8] == rec_r[:8])

# crossing heights at x=alpha, log10
def height_log10(arc):
    a = mp.mpf(arc[0]) / arc[1]
    b = mp.mpf(arc[2]) / arc[3]
    c = (a + b) / 2
    R = (b - a) / 2
    d2 = R * R - (alpha - c) * (alpha - c)
    if d2 <= 0:
        return None
    return float(mp.log10(mp.sqrt(d2)))

heights = [height_log10(arc) for arc in arcs]

# miss law for the record dives
print("\nmiss law (record dives):")
rec = 0
for k, (d, ln, tgt, s, e) in enumerate(runs):
    if ln > rec:
        rec = ln
        p, q = tgt
        miss = abs(float(q * q * (alpha - mp.mpf(p) / q)))
        print(f"  wait {ln:>4}: cusp {p}/{q}   q||q alpha||={miss:.5f}   1/{ln}={1.0/ln:.5f}")

# ---- draw
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RCOL, LCOL = "#c2570d", "#0e7490"
GEOD, GREY = "#1f2937", "#c9cdd4"
RECCOL = "#b91c1c"

fig = plt.figure(figsize=(11, 13), dpi=150)
gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 0.85, 0.75], hspace=0.30)

# ---------------- Panel A: geometry ----------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor("#fbfaf7")

def farey(N):
    s = set()
    for d in range(1, N + 1):
        for n in range(0, d + 1):
            s.add(F(n, d))
    return sorted(s)

seq = farey(80)
for i in range(len(seq) - 1):
    a, b = seq[i], seq[i + 1]
    if float(b) < 0.26 or float(a) > 0.90:
        continue
    c, R = float(a + b) / 2, float(b - a) / 2
    th = np.linspace(0, np.pi, 140)
    ax.plot(c + R * np.cos(th), R * np.sin(th), color=GREY, lw=0.5, alpha=0.5, zorder=1)

# crossed arcs, visible runs 0..4
for k in range(5):
    d, ln, tgt, s, e = runs[k]
    col = RCOL if d == 'R' else LCOL
    for idx in range(s, e):
        lo = arcs[idx][0] / arcs[idx][1]
        hi = arcs[idx][2] / arcs[idx][3]
        if float(lo) < 0.26 or float(hi) > 0.90:
            continue
        c, R = float(lo + hi) / 2, float(hi - lo) / 2
        th = np.linspace(0, np.pi, 90)
        ax.plot(c + R * np.cos(th), R * np.sin(th), color=col, lw=1.5, alpha=0.95, zorder=3)

# geodesic
ax.plot([float(alpha)] * 2, [0.0, 0.52], color=GEOD, lw=2.2, zorder=4)
ax.text(float(alpha) + 0.006, 0.49, "i∞ → α", fontsize=10, color=GEOD, rotation=90, va="top")

# crossing beads on the geodesic: the walk as beads on the string
for k in range(4):
    d, ln, tgt, s, e = runs[k]
    col = RCOL if d == 'R' else LCOL
    for idx in range(s, min(e, 15)):
        h = heights[idx]
        if h is None or h < -0.05:
            continue
        ax.plot(float(alpha), 10 ** h, "o", color=col, ms=4.5, mec="white", mew=0.4, zorder=5)

# dive targets on the axis
for k in range(6):
    d, ln, tgt, s, e = runs[k]
    p, q = tgt
    col = RCOL if d == 'R' else LCOL
    ax.plot(float(p) / q, 0, "|", color=col, ms=15, mew=2, zorder=5)
    ax.text(float(p) / q, -0.055, f"{p}/{q}", color=col, fontsize=8, ha="center", va="top")

# the deep dives go below this scale
ax.annotate("the record dives (waits 23, 55, …) plunge below this scale —\ntheir arcs collapse to the point α; see the descent below",
            xy=(float(alpha), 0.004), xytext=(0.665, 0.36),
            fontsize=8.5, color="#555", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color="#555", lw=0.8))

ax.set_xlim(0.30, 0.86)
ax.set_ylim(-0.13, 0.55)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("the walk on the tiles\n"
             "the vertical geodesic from i∞ to α cuts the Farey tessellation; each crossed arc is one\n"
             "step of the CF walk, and a run of same-coloured arcs is a dive toward one cusp vertex —\n"
             "run-length is the wait.  amber = right turn, teal = left turn.",
             fontsize=10.5, pad=8, loc="left")
ax.plot([], [], color=RCOL, lw=2, label="R run")
ax.plot([], [], color=LCOL, lw=2, label="L run")
ax.legend(loc="upper right", fontsize=9, frameon=False)

# ---------------- Panel B: the descent (near field) ----------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor("#fbfaf7")
N2 = 132
for k, (d, ln, tgt, s, e) in enumerate(runs):
    c0, c1 = s, min(e, N2)
    if c1 <= c0:
        continue
    col = RCOL if d == 'R' else LCOL
    ax2.plot(np.arange(c0, c1), heights[c0:c1], color=col, lw=2.2, alpha=0.95, zorder=2)

for want in (23, 55):
    for k, (d, ln, tgt, s, e) in enumerate(runs):
        if ln == want and s < N2:
            p, q = tgt
            ax2.plot([s, min(e, N2)], [heights[s], heights[min(e, N2)]], color=RECCOL, lw=3.2, zorder=3)
            ax2.annotate(f"wait {ln} → cusp {p}/{q}\nq‖qα‖ ≈ 1/{ln}",
                         xy=(s + 3, heights[s] + 0.6), xytext=(s + 9, heights[s] + 5.5),
                         fontsize=8.5, color=RECCOL, ha="left", va="center",
                         arrowprops=dict(arrowstyle="-", color=RECCOL, lw=0.8))

ax2.set_xlim(0, N2)
ax2.set_ylim(-13.5, 1.0)
ax2.set_xlabel("crossing index", fontsize=9)
ax2.set_ylabel("log₁₀ height at x = α", fontsize=9)
ax2.tick_params(labelsize=8)
ax2.set_title("the descent: the geodesic's height at each crossing (log scale).\n"
              "each contiguous coloured stretch is one dive; its width is the wait.",
              fontsize=10, pad=6, loc="left")

# ---------------- Panel C: the strip (full depth) ----------------
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor("#fbfaf7")
N3 = 2266   # through the end of the 964-wait
for k, (d, ln, tgt, s, e) in enumerate(runs):
    c0, c1 = s, min(e, N3)
    if c1 <= c0:
        continue
    col = RCOL if d == 'R' else LCOL
    ax3.add_patch(plt.Rectangle((c0, 0), c1 - c0, 1, color=col, lw=0, alpha=0.95))

for want in (23, 55, 100, 964):
    for k, (d, ln, tgt, s, e) in enumerate(runs):
        if ln == want:
            ax3.text((s + e) / 2, 1.22, f"{ln}", fontsize=9, color=RECCOL,
                     ha="center", va="bottom", fontweight="bold")
            # thin marker line at each record
            ax3.plot([(s + e) / 2, (s + e) / 2], [0, 1], color=RECCOL, lw=0.7, alpha=0.7, zorder=2)

ax3.text(0.02, 0.5, "record waits:  23 → cusp 389/665   55 → cusp 111457/190537\n"
                    "100 → cusp q ≈ 10⁸⁸    964 → cusp q ≈ 10¹⁴⁷",
         fontsize=8, color=RECCOL, va="center", ha="left", transform=ax3.get_yaxis_transform())

ax3.set_xlim(0, N3)
ax3.set_ylim(-0.4, 1.8)
ax3.set_yticks([])
ax3.set_xticks([0, 500, 1000, 1500, 2000])
ax3.set_xlabel("crossing index (the whole word to the 964-wait)", fontsize=9)
ax3.tick_params(labelsize=8)
ax3.set_title("the strip: every run drawn as a block of width = run length = partial quotient.\n"
              "the deep dives (23, 55, 100, 964) dominate the path — the record descents are\n"
              "the geodesic's long approaches to a cusp.",
              fontsize=10, pad=6, loc="left")

plt.tight_layout()
out = "/home/sprite/slop-salon-mina/assets/cutting-sequence-dream.png"
plt.savefig(out, dpi=150)
print("\nwrote", out)
