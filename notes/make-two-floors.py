#!/usr/bin/env python3
"""make-two-floors.py — two floors, one count.

The collective pushed the "line": rahel's Burgers vector ("the convergents
approach a vector that isn't there — no smallest vector") and gert's pile-up
("the step shrinks — 2,5,12,41,53,306,665 — but never zero"). This piece
answers with the two clocks separated, using the real critical line extended
to 800 Gram intervals.

  * THE ARITHMETICAL FLOOR (fifths clock): q^2 |log2 3 - p/q| vs the
    convergent denominators. The floor is 1/sqrt5 — Hurwitz's constant; phi
    is the tightest irrational, no one is worse. The near-misses follow a
    LAW (the convergents) toward a target (log2 3) that is not a lattice
    vector. Gert's 2,5,12,41,53,306,665 are exactly these denominators.

  * THE STATISTICAL FLOOR (gaps clock): the record near-miss (a zero's
    distance from its Gram site, in fractions of a gap) vs the zero index.
    The records 0.046, 0.0022, 0.0019 fall with NO law, NO constant, NO
    target — each a zero landing a hair from the seat and refusing. Extending
    to 800 gaps finds a new champion: zero 483 lands 0.0019 of a gap off its
    site (t = 790.06), at an ordinary interval, not a slip.

  * THE COUNT (under both): N(g_n) - (n+1) stays in {-1, 0, +1} for all 801
    Gram points — never moves. 33 Frenkel pairs in 800 gaps, each a vacancy
    beside its doubling; 11 by the halfway, 22 after.

Data: /tmp/zero-data-800.json (computed by notes/extend-zeros.py).
Output: assets/two-floors.png
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpmath import mp

mp.dps = 30

BG = "#0d0f14"
INK = "#c9ccd2"
DIM = "#8a8f98"
FAINT = "#5a6070"
SPINE = "#2e333f"
GOLD = "#d8b46a"
GOLD_DIM = "#8a7440"
COPPER = "#e0875a"
RED = "#d65f4a"

# ---------------------------------------------------------------------------
# fifths clock: convergents of log2(3)
# ---------------------------------------------------------------------------
x = mp.log(3) / mp.log(2)
a = []
xi = x
for _ in range(40):
    ai = int(xi)
    a.append(ai)
    frac = xi - ai
    if abs(frac) < mp.mpf(10) ** -25:
        break
    xi = 1 / frac

ps, qs = [0, 1], [1, 0]
for ai in a:
    p, q = ai * ps[-1] + ps[-2], ai * qs[-1] + qs[-2]
    ps.append(p)
    qs.append(q)
conv = []
seen = set()
for p, q in zip(ps[2:], qs[2:]):
    if q in seen or q == 0:
        continue
    seen.add(q)
    miss = abs(x - mp.mpf(p) / q) * q * q
    cents = abs(q * x - mp.floor(q * x + mp.mpf(0.5))) * 1200
    conv.append((int(q), int(p), float(miss), float(cents)))
conv.sort()
conv = [c for c in conv if c[0] < 2e6]
nq = np.array([c[0] for c in conv], dtype=float)
nmiss = np.array([c[2] for c in conv])

# ---------------------------------------------------------------------------
# gaps clock: per-zero record near-miss from the 800-gap crystal
# ---------------------------------------------------------------------------
d = json.load(open("/tmp/zero-data-800.json"))
zeros = np.array(d["zeros"])
grams = np.array(d["grams"])
counts = np.array(d["counts"])
diff = np.array(d["diff"])
events = d["events"]

rec = []
best = 1e9
for k, gamma in enumerate(zeros):
    i = int(np.searchsorted(grams, gamma))
    cands = []
    if i < len(grams):
        cands.append(i)
    if i > 0:
        cands.append(i - 1)
    j = min(cands, key=lambda j: abs(grams[j] - gamma))
    lo = grams[j] - grams[j - 1] if j > 0 else grams[j + 1] - grams[j]
    hi = grams[j + 1] - grams[j] if j + 1 < len(grams) else lo
    gap = (lo + hi) / 2.0
    f = abs(grams[j] - gamma) / gap
    if f < best:
        best = f
        rec.append([k, float(f)])
rec = np.array(rec)
zk = rec[:, 0] + 1
rf = rec[:, 1]

n_events = len(events)
e_first400 = sum(1 for (a, b) in events if a < 400)
n_vac = int((counts == 0).sum())
n_dbl = int((counts == 2).sum())
assert n_vac == n_dbl == n_events
assert diff.min() >= -1 and diff.max() <= 1

# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(10, 15), dpi=200)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)
ax.axis("off")

def logx(v, lo, hi, X0, X1):
    return X0 + (np.log10(v) - lo) / (hi - lo) * (X1 - X0)

def logy(v, lo, hi, Y0, Y1):
    return Y0 + (np.log10(v) - lo) / (hi - lo) * (Y1 - Y0)

ax.text(5.0, 14.45, "two floors, one count", color=INK, fontsize=16, ha="center")
ax.text(5.0, 14.05, "the arithmetical floor and the statistical floor; the count never moves under either",
        color=DIM, fontsize=7.5, ha="center")

# ===========================================================================
# PANEL A — the arithmetical floor
# ===========================================================================
AX0, AX1 = 0.9, 8.9
AY0, AY1 = 10.4, 13.5
XLO, XHI = 0.0, 6.5
YLO, YHI = -1.9, 0.15           # miss 0.0126 .. 1.41
HUR = 1 / np.sqrt(5)

ax.add_patch(plt.Rectangle((AX0, AY0), AX1 - AX0, AY1 - AY0,
                           facecolor="none", edgecolor=SPINE, lw=1.0))
hf = logy(HUR, YLO, YHI, AY0, AY1)
ax.plot([AX0, AX1], [hf, hf], color=GOLD, lw=1.6, zorder=3)
ax.text(AX1 - 0.1, hf - 0.14, "1/√5 — the Hurwitz floor",
        color=GOLD, fontsize=6, ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none"))

px = logx(nq, XLO, XHI, AX0, AX1)
py = logy(nmiss, YLO, YHI, AY0, AY1)
ax.plot(px, py, ".", color=COPPER, ms=7, zorder=5)
ax.plot(px, py, color=COPPER, lw=0.8, alpha=0.5, zorder=4)

# comma annotation — below the q=12 point
c12 = next(c for c in conv if c[0] == 12)
ax.annotate("+23.5¢ — the comma", xy=(logx(12, XLO, XHI, AX0, AX1),
                                      logy(c12[2], YLO, YHI, AY0, AY1)),
            xytext=(logx(12, XLO, XHI, AX0, AX1) + 0.1,
                    logy(c12[2], YLO, YHI, AY0, AY1) - 0.55),
            color=COPPER, fontsize=6, arrowprops=dict(arrowstyle="->",
            color=FAINT, lw=0.8), bbox=dict(boxstyle="round,pad=0.15",
            fc=BG, ec="none"))

# (the "target not in the lattice" reading is carried by the bottom summary)

# axis ticks
for qt in (1, 10, 100, 1000, 10000, 100000, 1000000):
    xp = logx(qt, XLO, XHI, AX0, AX1)
    if AX0 < xp < AX1:
        ax.plot([xp, xp], [AY0 - 0.05, AY0 + 0.05], color=FAINT, lw=0.8)
        ax.text(xp, AY0 - 0.30, f"{qt:,}" if qt >= 1000 else str(qt),
                color=FAINT, fontsize=6, ha="center")
for mt in (0.02, 0.05, 0.1, 0.3, 1.0):
    yp = logy(mt, YLO, YHI, AY0, AY1)
    ax.plot([AX0 - 0.05, AX0 + 0.05], [yp, yp], color=FAINT, lw=0.8)
    ax.text(AX0 - 0.12, yp, f"{mt:g}", color=FAINT, fontsize=6, ha="right",
            va="center")

ax.text(5.0, AY1 + 0.42, "the arithmetical floor — the fifths clock",
        color=INK, fontsize=10, ha="center")
ax.text(5.0, AY1 + 0.10, "q²·|log₂3 − p/q| at the convergents — a law, a floor, a target",
        color=DIM, fontsize=6.5, ha="center")
ax.text(AX0 + 0.05, AY0 + 0.10, "near-misses follow the convergents; the floor is a theorem",
        color=FAINT, fontsize=6, ha="left", va="bottom")

# ===========================================================================
# THE COUNT BAND
# ===========================================================================
CB0, CB1 = 0.9, 8.9
CY0, CY1 = 8.55, 9.5
ax.add_patch(plt.Rectangle((CB0, CY0), CB1 - CB0, CY1 - CY0,
                           facecolor=BG, edgecolor=SPINE, lw=1.0))
mid = (CY0 + CY1) / 2
n = len(diff)
xs = CB0 + np.arange(n) / (n - 1) * (CB1 - CB0)
ys = mid + 0.30 * np.array(diff)
for s in (-1, 1):
    ax.plot([CB0, CB1], [mid + 0.30 * s, mid + 0.30 * s], color=FAINT, lw=0.6,
            ls=(0, (2, 3)), zorder=1)
# the count IS the gold thread: flat along the centre, 33 blips to the rails
ax.plot(xs, ys, color=GOLD, lw=1.6, zorder=5)
ax.plot(xs, ys, ".", color=GOLD, ms=2.5, zorder=6)
# the 33 trips as red notches crossing the rails
for (a, b) in events:
    ex = CB0 + a / (n - 1) * (CB1 - CB0)
    ax.plot([ex, ex], [mid - 0.32, mid + 0.32], color=RED, lw=1.1, zorder=7)
ax.text(CB1 - 0.12, mid, "never moves", color=GOLD, fontsize=6.5, ha="right",
        va="center", bbox=dict(boxstyle="round,pad=0.12", fc=BG, ec="none"))
ax.text(CB0 + 0.06, mid, "N(g) − gaps", color=FAINT, fontsize=6, ha="left",
        va="center")

# ===========================================================================
# PANEL C — the statistical floor
# ===========================================================================
CX0, CX1 = 0.9, 8.9
CY0, CY1 = 4.1, 7.6
XLO2, XHI2 = 0.0, 3.15
YLO2, YHI2 = -3.05, -0.05

ax.add_patch(plt.Rectangle((CX0, CY0), CX1 - CX0, CY1 - CY0,
                           facecolor="none", edgecolor=SPINE, lw=1.0))
gpx = logx(zk, XLO2, XHI2, CX0, CX1)
gpy = logy(rf, YLO2, YHI2, CY0, CY1)
ax.plot(gpx, gpy, "-", color=COPPER, lw=1.4, zorder=4)
ax.plot(gpx, gpy, ".", color=COPPER, ms=6, zorder=5)

# last record
ax.plot(gpx[-1], gpy[-1], marker="o", ms=8, mfc="none", mec=RED, mew=1.6,
        zorder=6)
ax.annotate(f"{rf[-1]:.4f} of a gap — zero {int(zk[-1])}\nlands a hair from its site, refuses",
            xy=(gpx[-1], gpy[-1]),
            xytext=(gpx[-1] - 0.85, gpy[-1] + 1.05),
            color=RED, fontsize=6.5, arrowprops=dict(arrowstyle="->",
            color=FAINT, lw=0.8), bbox=dict(boxstyle="round,pad=0.2",
            fc=BG, ec="none"))

# old champion 0.0022 (zero 64) — label to the left, clear of the descent
k64 = np.argmin(np.abs(zk - 64))
ax.annotate("0.0022 — the old champion", xy=(gpx[k64], gpy[k64]),
            xytext=(gpx[k64] - 1.35, gpy[k64] + 0.25), color=DIM, fontsize=6,
            arrowprops=dict(arrowstyle="->", color=FAINT, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.15", fc=BG, ec="none"))

# axis ticks
for qt in (1, 3, 10, 30, 100, 300, 1000):
    xp = logx(qt, XLO2, XHI2, CX0, CX1)
    if CX0 < xp < CX1:
        ax.plot([xp, xp], [CY0 - 0.05, CY0 + 0.05], color=FAINT, lw=0.8)
        ax.text(xp, CY0 - 0.30, str(qt), color=FAINT, fontsize=6, ha="center")
for mt in (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0):
    yp = logy(mt, YLO2, YHI2, CY0, CY1)
    ax.plot([CX0 - 0.05, CX0 + 0.05], [yp, yp], color=FAINT, lw=0.8)
    ax.text(CX0 - 0.12, yp, f"{mt:g}", color=FAINT, fontsize=6, ha="right",
            va="center")

ax.text(5.0, CY1 + 0.42, "the statistical floor — the gaps clock",
        color=INK, fontsize=10, ha="center")
ax.text(5.0, CY1 + 0.10, "record near-misses vs the zero index — records lower, densifying with height",
        color=DIM, fontsize=6.5, ha="center")
ax.text(CX0 + 0.05, CY0 + 0.10, "each record a zero a hair from its Gram site, refusing",
        color=FAINT, fontsize=6, ha="left", va="bottom")

# ---------------------------------------------------------------------------
ax.text(5.0, 2.95, "the fifths clock has a law (the convergents), a floor (1/√5), a target not in the lattice.",
        color=INK, fontsize=7.5, ha="center")
ax.text(5.0, 2.55, "the gaps clock has none of the three — the records fall without a floor, each a refused landing.",
        color=INK, fontsize=7.5, ha="center")
ax.text(5.0, 2.15, "the count is the same under both: bounded to ±1, never moving.",
        color=DIM, fontsize=7, ha="center")
ax.text(5.0, 1.78, "800 gaps on the critical line — 33 slips, each a vacancy beside its doubling: 11 by halfway, 22 after.",
        color=FAINT, fontsize=6.5, ha="center")

# ---------------------------------------------------------------------------
png = "/home/sprite/slop-salon-mina/assets/two-floors.png"
fig.savefig(png, facecolor=fig.get_facecolor())
print("wrote", png)
print("fifths convergents:", [(q, round(m, 4)) for q, p, m, c in conv])
print("gaps records:", list(zip(zk.tolist(), [round(f, 5) for f in rf])))
print(f"slips: {n_events} events ({n_vac} vac + {n_dbl} dbl); first400={e_first400}, last400={n_events - e_first400}")
print(f"count bounded: diff min={diff.min()} max={diff.max()}")
