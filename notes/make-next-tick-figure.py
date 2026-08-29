#!/usr/bin/env python3
"""the next tick — the record schedules its own replacement.

rahel (Aug 29 02:10Z): "the wait is the record, inverted: 6090 ~= 8788 ln 2,
median 4220 ~= 8788 (ln 2)^2 — the seam converts the present depth into the
next clock. scheduled by its own depth."

This figure makes that exact and turns it forward. For lambda_2's continued
fraction the record quotients are 3@rung1, 13@rung6, 174@rung8, 8788@rung302.
The tail is Gauss-Kuzmin: P(a > R) = log2(1 + 1/R), so after a record of
value R the wait to the next record is GEOMETRIC with mean 1/log2(1+1/R)
and median ln2/log2(1+1/R) — the value sets the rate of its own replacement.

Left (the clock): the record strikes on the rung axis; after 8788@302 the
exact survival curve P(wait > t) = (1 - p)^t, median 4222 rungs (-> rung
4524), mean 6092 (-> rung 6394). The three observed waits (5, 2, 294 rungs)
were draws from their own clocks — mean 2.4, 9.4, 121 — the schedule is a
rate, not a point.

Right (the value): the record values 3, 13, 174, 8788, and the next one's
median 2R ~= 17576 with an unbounded above — the WHEN has a mean, the WHAT
does not. depth converts to clock; the unbounded draw becomes a bounded wait.
"""
import numpy as np
from math import log, log2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0d0f14"
INK = "#e8e6e0"
DIM = "#8a887f"
FAINT = "#3a3d46"
GOLD = "#d9a441"
GOLD_HOT = "#f4e3b2"
RED = "#c74e3d"
BLUE = "#7a9eab"

# --- records of lambda_2's continued fraction: value @ rung ---------------
recs = [(3, 1), (13, 6), (174, 8), (8788, 302)]
vals = np.array([r[0] for r in recs], dtype=float)
rungs = np.array([r[1] for r in recs], dtype=float)

# exact wait law
p_last = log2(1 + 1 / vals[-1])
mean_wait = 1 / p_last
med_wait = log(2) / p_last
next_med_val = 1 / ((1 + 1 / vals[-1]) ** 0.5 - 1)     # median next value
print(f"after {vals[-1]:.0f}: mean wait {mean_wait:.1f}, median {med_wait:.1f}, "
      f"next rungs {rungs[-1]+mean_wait:.0f}/{rungs[-1]+med_wait:.0f}, next value median {next_med_val:.0f}")

fig = plt.figure(figsize=(11, 5.2), dpi=200)
fig.patch.set_facecolor(BG)
fig.suptitle("the next tick — the record sets the rate; the arrival is a draw",
             color=INK, fontsize=13.5, x=0.5, y=0.97, fontweight="normal")

# ---- left: the clock (when) ---------------------------------------------
axL = fig.add_axes([0.055, 0.13, 0.50, 0.76])
axL.set_facecolor(BG)
axL.set_xlim(0, 6600)
axL.set_ylim(0, 1.06)
axL.set_xlabel("rung of the continued fraction", color=DIM, fontsize=9)
axL.set_ylabel("P(next record still not arrived)", color=GOLD, fontsize=9)
for s in axL.spines.values():
    s.set_color(FAINT)
axL.tick_params(colors=DIM, labelsize=8)
axL.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_yticklabels(["0", ".25", ".5", ".75", "1"])

# the current record strike 8788@302
axL.plot([302, 302], [0, 0.05], color=GOLD_HOT, lw=2)
axL.text(302, 0.075, "8788@rung 302", color=GOLD_HOT, fontsize=9.5, ha="center",
         va="bottom", fontfamily="monospace")

# early records: a blink at the origin, then the silence owns the axis
for r in (1, 6, 8):
    axL.plot([r, r], [0, 0.035], color=RED, lw=1.4)
axL.text(4, 0.20,
         "records so far: 3@1 · 13@6 · 174@8\nwaits: 5, 2, 294 rungs\n"
         "(their clocks' means: 2.4, 9.4, 121)\nthree draws — the schedule is a rate, not a point",
         color=DIM, fontsize=8, ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.35", fc=BG, ec=FAINT, lw=0.8))

# the exact survival curve after the current record 8788@302
t = np.linspace(0, 6600 - rungs[-1], 1200)
S = (1 - p_last) ** t
axL.plot(rungs[-1] + t, S, color=GOLD, lw=2.0)
axL.fill_between(rungs[-1] + t, 0, S, color=GOLD, alpha=0.10)

# median and mean ticks of the next wait
for x, lab, c in [(rungs[-1] + med_wait, f"median {med_wait:.0f}", GOLD),
                  (rungs[-1] + mean_wait, f"mean {mean_wait:.0f}", BLUE)]:
    axL.plot([x, x], [0, 0.5 if c == GOLD else 0.37], ls=(0, (2, 2)), color=c, lw=1.3)
    axL.text(x, 0.56 if c == GOLD else 0.41, lab, color=c, fontsize=8.5,
             ha="center", va="bottom")
axL.text(rungs[-1] + t[-1], S[-1], " next", color=GOLD, fontsize=8, ha="left", va="center")
axL.text(4200, 0.98, "the silence IS the schedule:\nthe next tick at rate 1/(8788·ln2)\nper rung — mean 6092, median 4222",
         color=GOLD, fontsize=8.5, ha="left", va="top", alpha=0.9)

# ---- right: the value (what) --------------------------------------------
axR = fig.add_axes([0.635, 0.13, 0.335, 0.76])
axR.set_facecolor(BG)
axR.set_ylim(1, 60000)
axR.set_yscale("log")
axR.set_xlim(0.5, 5.5)
axR.set_xticks([1, 2, 3, 4, 5])
axR.set_xticklabels(["3", "13", "174", "8788", "next"], color=DIM, fontsize=8.5)
axR.set_ylabel("record value (log)", color=DIM, fontsize=9)
for s in axR.spines.values():
    s.set_color(FAINT)
axR.tick_params(colors=DIM, labelsize=8)
axR.grid(axis="y", color=FAINT, alpha=0.35, lw=0.5)

axR.plot(np.arange(1, 5), vals, color=GOLD, lw=1.2, ls=(0, (1, 2)), zorder=1)
axR.scatter(np.arange(1, 5), vals, s=34, color=GOLD_HOT, zorder=3)
for i, v in enumerate(vals):
    axR.text(i + 1, v * 1.45, f"{v:,}", color=GOLD_HOT, fontsize=9,
             ha="center", va="bottom", fontfamily="monospace")

# the next value: median 2R, unbounded above
axR.scatter(5, next_med_val, s=60, facecolors="none", edgecolors=BLUE, zorder=3)
axR.plot([4, 5], [vals[-1], next_med_val], color=BLUE, lw=1.2, ls=(0, (2, 2)), zorder=1)
axR.annotate("", xy=(5, 40000), xytext=(5, next_med_val * 1.8),
             arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3))
axR.text(5, next_med_val * 1.9, "no mean", color=BLUE, fontsize=8, ha="center", va="bottom")
axR.text(5, next_med_val / 2.2, "median ≈ 2·8788\n= 17,576", color=BLUE, fontsize=8,
         ha="center", va="top")

axR.text(0.5, 1.25, "the WHEN has a mean,\nthe WHAT does not", color=DIM,
         fontsize=9, ha="left", va="bottom")

fig.text(0.055, 0.035, "the depth converts to a clock: the where's own draw sets the rate of the next — "
         "scheduled by its own value, arrival a draw.  (λ₂ = 0.303663…, CF records)",
         color=FAINT, fontsize=8)
fig.text(0.635, 0.035, "next value, when it comes: median 2R, tail unbounded — the when is the tamer of the two.",
         color=FAINT, fontsize=8)

plt.savefig("assets/next-tick.png", facecolor=BG, dpi=200, bbox_inches="tight")
print("saved assets/next-tick.png")
