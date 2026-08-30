#!/usr/bin/env python3
"""the two mirrors kiss at the count.

rahel (13:11): "both mirrors fix the drone -- 12100/110 = 110, 2 floor(110)
- 110 = 110 -- but the walk is never on the grid, so it crosses the one
height where the two readings agree and keeps going. the seal and the
crossing are the same fact, seen from on and off the count."

why do the two readings agree at the drone?  because the mirrors are tangent
there.  on the count's own cell [110,111) the glide mirror IS the line
y = 220 - x, and the inversion mirror 12100/x is tangent to that same line at
(110,110): both send x to ~220 - x, the reflection about the count -- the
sign.  the fold and the bracket meet exactly once, and that once is a kiss.

the walk is never on the grid, so its points read the two mirrors apart -- a
disagreement bracket per miss, wide for the coarse misses, collapsing to zero
as the deepest rungs land in the count's cell.  the bracket of the readings
seals at the same point the register's bracket 55*220 = 110^2 sealed at: the
count, the geometric mean of its absences and the point where the two mirrors
stop disagreeing.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"
K = 110.0 * 110.0

def glide(x):
    return 2.0 * np.floor(x) - x

def inv(x):
    return K / x

# --------------------------------------------------------- the walk: the seven near-misses
cents = [+204.0, -90.0, +23.5, -19.8, +3.6, -1.8, +0.076]
pts = []
for c in cents:
    x = 110.0 * 2.0 ** (c / 1200.0)
    pts.append(dict(c=c, x=x, g=glide(x), i=inv(x), pos=c > 0))
print("near-miss -> glide-read / inv-read  (the disagreement bracket):")
for p in pts:
    print(f"  {p['c']:+8.3f} c   x={p['x']:8.4f}   g={p['g']:8.4f}   i={p['i']:8.4f}"
          f"   |g-i|={abs(p['g'] - p['i']):8.4f}")

# --------------------------------------------------------------- drawing
fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13.8, 6.4), dpi=200,
    gridspec_kw={"width_ratios": [1.0, 1.15], "wspace": 0.26})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
fig.patch.set_facecolor(SURF)

# ---- left panel: the two mirrors over the count's octave, tangency at 110
xL = np.linspace(55.0, 220.0, 4000)
# the grid, faint verticals
for g in range(55, 221, 5):
    axL.axvline(g, color=ZED, lw=0.4, zorder=1)
# the glide: per-cell reflection segments, muted so the tangent pops
for n in range(55, 220):
    xs = np.array([n, n + 1.0 - 1e-9])
    axL.plot(xs, 2.0 * n - xs, color=SEAM, lw=0.9, alpha=0.55, zorder=2)
axL.text(57.5, 104, "the fold — the floor's reflection", color=SEAM,
         fontsize=8.5, ha="left", va="center", rotation=-45)
# the inversion mirror (the bracket)
axL.plot(xL, inv(xL), color=MIRR, lw=2.4, zorder=4)
axL.text(69, 172, "the bracket — the mirror", color=MIRR, fontsize=9,
         ha="left", va="center", rotation=-52)
# the seal cell [110,111): the glide there IS the tangent line y=220-x
xs = np.array([110.0, 111.0 - 1e-9])
axL.plot(xs, 220.0 - xs, color=SIGN, lw=3.2, zorder=6)
axL.plot([104, 220], [116, 0], color=SIGN, lw=1.1, ls=(0, (5, 4)),
         alpha=0.5, zorder=3)
axL.text(126, 52, "the sign — the shared tangent", color=SIGN, fontsize=8.5,
         ha="left", va="center", rotation=-45)
# the count
axL.plot([110.0], [110.0], "o", ms=8, mfc=SIGN, mec=INK, mew=1.1, zorder=7)
axL.text(110.0, 111.5, "the count", color=INK, fontsize=9, ha="center",
         va="bottom")
axL.text(55.0, 218, "the fold and the bracket meet once — tangentially, at 110",
         fontsize=9, color=SEC, ha="left", va="top")
axL.set_xlim(55, 220)
axL.set_ylim(55, 220)
axL.set_yticks([]); axL.set_xticks([])
for s in axL.spines.values(): s.set_visible(False)

# ---- right panel: the walk reads the mirrors apart; the readings seal
# the count's cell, where the fold is the tangent
axR.axvspan(110.0, 111.0, color=ZED, alpha=0.4, lw=0, zorder=0)
axR.text(111.4, 118.5, "the count's cell —\nwhere the fold is the tangent",
         color=SEC, fontsize=7.5, ha="left", va="top")
# the local reflection through the count (the sign), dashed
xs = np.linspace(103.5, 125.5, 2)
axR.plot(xs, 220.0 - xs, color=SIGN, lw=1.2, ls=(0, (5, 4)), alpha=0.6,
         zorder=2)
# the seal segment on the cell, solid
xs2 = np.array([110.0, 111.0 - 1e-9])
axR.plot(xs2, 220.0 - xs2, color=SIGN, lw=2.6, zorder=4)
# each near-miss: its two mirror-readings, and the bracket between them
for p in pts:
    col = SIGN if p["pos"] else MIRR
    axR.plot([p["x"]], [p["g"]], "o", ms=3.4, mfc=col, mec=col, zorder=5)
    axR.plot([p["x"]], [p["i"]], "o", ms=3.4, mfc=col, mec=col, zorder=5)
    axR.plot([p["x"], p["x"]], [p["g"], p["i"]], color=SEC, lw=0.7,
             alpha=0.6, zorder=3)
axR.plot([110.0], [110.0], "o", ms=8, mfc=SIGN, mec=INK, mew=1.1, zorder=6)
axR.text(110.0, 111.6, "the count", color=INK, fontsize=9, ha="center",
         va="bottom")
# label the widest bracket (+204 c)
p = pts[0]
axR.text(p["x"] + 0.5, p["g"] - 1.0, "one miss, two readings",
         color=SEC, fontsize=8, ha="left", va="top")
# label the collapsed deepest
axR.text(111.4, 103.0, "the deepest (0.076 c) —\nthe readings are one",
         color=SEC, fontsize=8, ha="left", va="center")
axR.text(104.0, 121.5, "the walk is never on the grid; the brackets close as it lands",
         fontsize=9, color=SEC, ha="left", va="top")
axR.set_xlim(103.5, 125.5)
axR.set_ylim(96.0, 124.0)
axR.set_yticks([]); axR.set_xticks([])
for s in axR.spines.values(): s.set_visible(False)

fig.text(0.5, 0.955, "the two mirrors kiss at the count",
         fontsize=12.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.008, "the sign is the shared tangent — 2⌊x⌋−x and 12100/x are the same reflection at 110, the only point where the fold and the bracket agree",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

plt.savefig("assets/two-mirrors-kiss.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/two-mirrors-kiss.png")
