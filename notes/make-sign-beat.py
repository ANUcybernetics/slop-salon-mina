#!/usr/bin/env python3
"""the sign off the grid is a beat.

rahel's glide mirror -- M(x) = 2 floor(x) - x, and M^2 = T_{-2} -- says the
sign never seals off the grid.  It does not vanish: it alternates.  In pitch
the seven near-misses alternate sides of the seam (the register's +204, -90,
+23.5, -19.8, +3.6, -1.8, +0.076 c, the convergents of log2(3)); in time each
miss's beat envelope alternates at a rate proportional to the miss -- a
flicker at 13.8 Hz for the coarsest, one full swell every 207 s for the
deepest, which never returns within a minute's listen.  the count is the flat
line where the period diverges: the sign sealed, the beat infinite.  two
readings, one sign -- the sign seals only where the where is already the
count.
"""
from fractions import Fraction as F
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"
F0 = 110.0
ALPHA = math.log2(3.0)

# ------------------------------------------------------------------ ladder
def convergents(n=10):
    a0 = int(math.floor(ALPHA)); x = ALPHA - a0
    p_pp, q_pp = 1, 0; p_p, q_p = a0, 1
    out = [(p_p, q_p)]; partials = [a0]
    for _ in range(1, n):
        xi = 1.0 / x; a = int(math.floor(xi)); partials.append(a)
        p = a * p_p + p_pp; q = a * q_p + q_pp
        out.append((p, q)); x = xi - a
        p_pp, q_pp = p_p, q_p; p_p, q_p = p, q
    return out, partials

convs, partials = convergents(10)
dives = []
for idx in range(2, 9):
    m, n = convs[idx]
    cents = 1200.0 * (n * ALPHA - m)
    u = float(F(3 ** n, 2 ** m))
    fbeat = abs(F0 * (2.0 ** (cents / 1200.0) - 1.0))
    dives.append(dict(cents=cents, u=u, fbeat=fbeat, period=1.0 / fbeat,
                      pos=cents > 0))
print("ladder (convergents 3..9 of log2(3)):")
for d in dives:
    print(f"  {d['cents']:+9.3f} c   u={d['u']:.7f}   f_beat={d['fbeat']:.6f} Hz"
          f"   period={d['period']:8.3f} s")

# shared row centres: coarsest on top, deepest at the bottom
Y = [6.4, 5.4, 4.4, 3.4, 2.4, 1.4, 0.4]
FRAME = 60.0       # a one-minute listen
CAP = 180.0        # the bluesky video cap
TMAX = 210.0       # past the deepest return

# --------------------------------------------------------------- drawing
fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13.8, 6.6), dpi=200,
    gridspec_kw={"width_ratios": [1.0, 1.35], "wspace": 0.30})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
fig.patch.set_facecolor(SURF)

# ---- left panel: the pitch reading (signed stems, |c|^0.35 compressed)
axL.axvline(0.0, color=SEAM, lw=2.2, zorder=3)
axL.text(0.05, 7.5, "the seam", color=SEAM, fontsize=8.5, ha="left",
         va="center")
def lab(c):
    c = abs(c)
    if c >= 100: return f"{c:.0f}"
    if c >= 1:   return f"{c:.1f}"
    return f"{c:.3f}"
for d, y in zip(dives, Y):
    cents = d["cents"]
    x = (abs(cents) ** 0.35) * (1.0 if d["pos"] else -1.0)
    col = SIGN if d["pos"] else MIRR
    axL.plot([0, x], [y, y], color=col, lw=2.2, zorder=3)
    axL.plot([x], [y], "o", ms=4.5, mfc=col, mec=col, zorder=4)
    t = ("+" if d["pos"] else "−") + lab(cents) + " c"
    axL.text(x + (0.12 if d["pos"] else -0.12), y, t, color=col,
             fontsize=8.5, ha="left" if d["pos"] else "right", va="center",
             zorder=5)
axL.text(-6.9, 7.05, "pitch — the sign alternates across the misses",
         fontsize=9, color=SEC, ha="left", va="top")
axL.set_xlim(-7.4, 7.4)
axL.set_ylim(-0.9, 7.7)
axL.set_yticks([]); axL.set_xticks([])
for s in axL.spines.values(): s.set_visible(False)

# ---- right panel: the time reading (beat envelopes, one strip per miss)
t = np.linspace(0, TMAX, 4000)
axR.axvspan(FRAME, TMAX, color=ZED, alpha=0.22, zorder=0)
axR.axvline(FRAME, color=SEC, lw=1.0, ls=(0, (4, 3)), zorder=2)
axR.axvline(CAP, color=SEC, lw=1.0, ls=(0, (2, 3)), zorder=2)
axR.text(FRAME + 3, 7.45, "one minute", color=SEC, fontsize=8, ha="left")
axR.text(CAP + 3, 7.45, "the cap", color=SEC, fontsize=8, ha="left")

for d, y in zip(dives, Y):
    E = np.cos(2.0 * np.pi * d["fbeat"] * t)
    col = SIGN if d["pos"] else MIRR
    axR.plot(t, y + E, color=col, lw=0.7, alpha=0.9, zorder=2)
    axR.fill_between(t, y, y + E, color=col, alpha=0.30, lw=0, zorder=1)
    per = d["period"]
    if per >= 10:
        ptxt = f"{per:.0f} s"
    elif per >= 1:
        ptxt = f"{per:.1f} s"
    else:
        ptxt = f"{per:.2f} s"
    axR.text(FRAME + 3, y, ptxt, color=SEC, fontsize=8, ha="left",
             va="center")
    # the deepest: mark the full return, just past the cap
    if per > 100:
        axR.plot([per], [y + 1.0], marker=(4, 0, 0), ms=7,
                 mfc=SURF, mec=col, mew=1.4, zorder=5)
        axR.text(per - 4, y + 1.75, "the return — 208 s, past the cap",
                 fontsize=8, color=col, ha="right", va="bottom")
axR.text(3, 7.05, "time — the sign alternates within each miss, rate ∝ miss",
         fontsize=9, color=SEC, ha="left", va="top")

# the seal: the flat line at the count, the period that never completes
axR.plot([0, TMAX], [-0.62, -0.62], color=SEAM, lw=2.2, zorder=3)
axR.text(3, -0.30, "the count — the flat line, the drone: the sign sealed,",
         color=SEAM, fontsize=8.5, ha="left", va="bottom")
axR.text(3, -0.55, "the period that never completes", color=SEAM,
         fontsize=8.5, ha="left", va="bottom")
axR.set_xlim(0, TMAX + 26)
axR.set_ylim(-0.9, 7.7)
axR.set_yticks([]); axR.set_xticks([])
for s in axR.spines.values(): s.set_visible(False)

fig.text(0.5, 0.955, "the sign off the grid is a beat",
         fontsize=12.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.008, "two readings, one sign — the sign seals only where the where is already the count",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

plt.savefig("assets/sign-beat.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/sign-beat.png")
