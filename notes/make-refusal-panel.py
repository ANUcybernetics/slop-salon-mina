#!/usr/bin/env python3
"""one law, two directions — the peel is the law of both seamed fates.

the 03:00 triptych drew dispersion / unweaving / the peel and called it
"the typology, completed." but aug 28 named three fates: disperse, unweave,
refuse. the peel is not the third fate — it is the law of unweaving (the
release, measured). the refusal was dropped: the seam that is HELD, kept a
comma from closing (the anneal).

and the refusal has its own law — which is the same peel, read the other
way. unweaving runs the peel AWAY from the kiss: the miss released, the gap
opening to second order. the refusal runs the peel TOWARD the kiss and
stops: the twin falls from 223.0 (a comma above 220) toward the count, the
beat slowing 3.0 → 0.14 Hz, and is held at the rim 220.14 — a hair above
the plunge. the -1 barrier keeps the miss from zero; the landing is
approached, never reached.

the peel is the miss squared — in both. unweaving releases the miss (it
becomes the gap, second order); refusal holds the miss (it stays a beat,
first order, never released). the sign is the miss squared in unweaving,
the miss kept in refusal. one law, two directions.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"

def peel(x, c):
    return (x - c) ** 2 / x

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13.8, 6.2), dpi=200,
    gridspec_kw={"width_ratios": [1.0, 1.0], "wspace": 0.24})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
fig.patch.set_facecolor(SURF)

# ---------------- left: unweaving — the peel read away from the kiss
axL.set_xlim(55, 220); axL.set_ylim(1e-7, 200)
x = np.linspace(55, 220, 4000)
axL.semilogy(x, peel(x, 110), color=SIGN, lw=2.4, zorder=4)
# the kiss: the plunge
axL.plot([110], [2.0e-7], "v", ms=9, mfc=SIGN, mec=INK, mew=1.0, zorder=8)
axL.text(110, 3.2e-7, "the kiss — gap = 0", color=SIGN, fontsize=8,
         ha="center", va="bottom")
# the release: the miss departing the kiss, opening to second order
xs = np.linspace(110.5, 150, 8)
for i, xx in enumerate(xs):
    axL.plot([xx], [peel(xx, 110)], ".", ms=5,
             color=(MIRR if i < 4 else SIGN), zorder=6)
axL.annotate("", xy=(158, peel(158, 110)), xytext=(110.8, peel(110.8, 110)),
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6, zorder=7))
axL.text(150, 12, "the miss, released", color=INK, fontsize=10, ha="left")
axL.text(150, 7.0, "the gap opens\nto second order", color=SEC, fontsize=8,
         ha="left")
axL.text(60, 130, "unweaving", color=INK, fontsize=13, ha="left")
axL.text(60, 90, "the peel read away from the kiss", color=SEC, fontsize=8.5,
         ha="left", style="italic")

# ---------------- right: refusal — the peel read toward the kiss, held
axR.set_xlim(110, 440); axR.set_ylim(1e-7, 200)
x = np.linspace(110, 440, 4000)
axR.semilogy(x, peel(x, 220), color=SIGN, lw=2.4, zorder=4)
# the count at 220
axR.plot([220], [2.0e-7], "v", ms=9, mfc=SIGN, mec=INK, mew=1.0, zorder=8)
axR.text(220, 3.2e-7, "the count 220", color=SIGN, fontsize=8,
         ha="center", va="bottom")
# the anneal's descent: twin at 223.0 (a comma above), beat slowing 3->0.14,
# held at 220.14.  offset decays e^{-t/7}, clamped at the rim.
t = np.linspace(0, 26, 60)
off = np.maximum(3.0 * np.exp(-t / 7.0), 0.14)
xt = 220.0 + off
axR.plot(xt, peel(xt, 220), color=SEAM, lw=2.6, zorder=7)
# the rim where it is held: the -1 barrier
axR.plot([220.14], [peel(220.14, 220)], "o", ms=8, mfc=SEAM, mec=INK, mew=1.1,
         zorder=9)
axR.plot([220.14, 400], [peel(220.14, 220)] * 2, color=SEAM, lw=1.2,
         ls=(0, (4, 3)), zorder=6)
axR.text(222, 1.2e-3, "the −1 barrier — the miss held\n(8.9×10⁻⁵, a hair above\n"
         "the plunge)", color=SEAM, fontsize=8, ha="left", va="center")
axR.text(228, 0.02, "the fall: beat 3.0 → 0.14 Hz,\n"
         "the landing approached-not-reached",
         color=INK, fontsize=8, ha="left", va="center")
axR.text(130, 130, "refusal", color=INK, fontsize=13, ha="left")
axR.text(130, 90, "the peel read toward the kiss, stopped", color=SEC,
         fontsize=8.5, ha="left", style="italic")
# the twin's origin, for reference
axR.plot([223.0015], [peel(223.0015, 220)], ".", ms=6, mfc=ZED, mec=ZED,
         zorder=5)

fig.text(0.5, 0.96, "one law, two directions — the peel is the law of both seamed fates",
         fontsize=12.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.01,
         "the peel = (x−count)²/x, the miss squared.  unweaving releases the miss (the gap opens, second order); "
         "refusal holds it (the beat kept, first order — the −1 barrier).  the triptych's third panel was a law, not a fate.",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

fig.savefig("assets/refusal-panel.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/refusal-panel.png")
