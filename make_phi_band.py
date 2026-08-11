"""the count in the winding register.

Left:  the wait — the partial quotients (run-lengths) of phi, e, log2(3).
       phi flat at 1 (the metronome, never a long run); e a patterned pulse;
       log2(3) with the 23-run — the near-return that almost closes.
Right: the miss — q^2 |x - p/q| for the convergents, with the Hurwitz floor
       1/sqrt(5) dashed. phi hugs the floor (worst-approximated, never even
       nearly returning); log2(3) plunges at the near-return; e dips mildly.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG = "#0b0d10"
CREAM = "#e8e0d0"
GOLD = "#d4a437"
STEEL = "#7ea8c9"
CRIMSON = "#c0553f"
GREY = "#6a6f76"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor": GREY, "text.color": CREAM,
    "axes.labelcolor": CREAM, "xtick.color": GREY, "ytick.color": GREY,
    "font.family": "serif", "font.size": 10,
})


def cf_digits(x, n):
    digs = []
    for _ in range(n):
        a = int(np.floor(x))
        digs.append(a)
        x = x - a
        if abs(x) < 1e-13:
            break
        x = 1.0 / x
    return digs


def convergents(x, n):
    digs = cf_digits(x, n)
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    out = []
    for a in digs:
        p2, q2 = a * p1 + p0, a * q1 + q0
        p0, q0 = p1, q1
        p1, q1 = p2, q2
        out.append((p2, q2, a))
    return out


phi = (1 + np.sqrt(5)) / 2
e = np.e
log23 = np.log(3) / np.log(2)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5), width_ratios=[1, 1.25])

# ---- LEFT: the wait (partial quotients as bars) ----
xL = 0.06
for i, (name, color, digs) in enumerate([
    ("phi", GOLD, cf_digits(phi, 14)),
    ("e", STEEL, cf_digits(e, 14)),
    ("log2 3", CRIMSON, cf_digits(log23, 14)),
]):
    d = np.array(digs[:13])
    xs = np.arange(len(d))
    axL.bar(xs, d, width=0.62, color=color, alpha=0.85)
    axL.text(xL, 1.02 - i * 0.015, name, transform=axL.transAxes,
             color=color, fontsize=11, ha="left", va="bottom")
    if name == "phi":
        axL.text(len(d) - 0.2, 1.28, "the wait is always one",
                 color=CREAM, fontsize=8.5, ha="right", style="italic")
    if name == "log2 3":
        axL.annotate("the 23 — a near-return",
                     xy=(np.where(d == 23)[0][0], 23), xytext=(7.5, 21),
                     color=CRIMSON, fontsize=8.5,
                     arrowprops=dict(arrowstyle="-", color=CRIMSON, lw=0.7))
axL.set_xlim(-0.7, 12.7)
axL.set_ylim(0, 26)
axL.set_xlabel("step", fontsize=9)
axL.set_ylabel("partial quotient — the wait", fontsize=9)
axL.set_title("the wait", fontsize=13, color=CREAM, pad=6)
axL.set_yticks([1, 5, 10, 15, 20, 23])
axL.spines["top"].set_visible(False)
axL.spines["right"].set_visible(False)

# ---- RIGHT: the miss q^2|x-p/q| vs q ----
floor = 1 / np.sqrt(5)
for (name, color, x) in [("phi", GOLD, phi), ("e", STEEL, e), ("log2 3", CRIMSON, log23)]:
    c = convergents(x, 18)
    qs = np.array([q for p, q, a in c])
    miss = np.array([q * q * abs(x - p / q) for p, q, a in c])
    axR.plot(qs, miss, "-o", color=color, ms=4, lw=1.2, label=name, alpha=0.9)
    axR.annotate(name, xy=(qs[-1], miss[-1]), xytext=(qs[-1] * 1.06, miss[-1]),
                 color=color, fontsize=10, va="center")

axR.axhline(floor, color="white", ls=(0, (5, 3)), lw=0.9, alpha=0.75)
axR.text(1.05, floor * 1.14, "1/√5 — the Hurwitz floor", color="white",
         fontsize=8.5, style="italic")
axR.annotate("the near-return: miss plunges\nat the 23-run", xy=(15601, 0.042),
             xytext=(60, 0.16), color=CRIMSON, fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=CRIMSON, lw=0.7))
axR.annotate("phi hugs the floor —\nnever even nearly", xy=(610, 0.447),
             xytext=(120, 0.62), color=GOLD, fontsize=8.5,
             arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.7))
axR.set_xscale("log")
axR.set_ylim(0.03, 0.85)
axR.set_xlabel("denominator q", fontsize=9)
axR.set_ylabel("q² · |x − p/q|  — the miss", fontsize=9)
axR.set_title("the miss", fontsize=13, color=CREAM, pad=6)
axR.spines["top"].set_visible(False)
axR.spines["right"].set_visible(False)
axR.grid(axis="y", color=GREY, lw=0.3, alpha=0.35)

fig.suptitle("three ways a return ends — the count, in the winding register",
             color=CREAM, fontsize=13, y=1.02)
fig.tight_layout()
out = "assets/phi-band-count.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print("wrote", out)
