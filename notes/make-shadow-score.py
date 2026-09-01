# shadow-score — the still for the shadow-sound piece.
#
# The piece's own score: five horizontal lines (the counts, 2c — places,
# made, never records), one diamond each (the crown c — a first arrival, an
# event), and the returns (the count struck at the law's rate, memoryless).
# 540 has its single return in 400k rungs; 2502 never — the pure one.
# Time matches the audio exactly: crowns at 10/18/23/31/38s, returns as
# rendered by make-shadow-sound.py.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# (interval, crown c, count 2c, crown time, return times)
DATA = [
    ("3/2",   55,   110, 10, [9.0, 15.9, 18.7, 26.2, 41.7, 42.6, 46.7, 56.1, 56.7, 57.8, 60.0, 60.4]),
    ("5/4",   42,    84, 18, [14.0, 31.4, 37.5, 41.0, 45.6, 51.9]),
    ("6/5",  270,   540, 23, [57.0]),
    ("9/8",  111,   222, 31, [50.0]),
    ("16/15", 1251, 2502, 38, []),
]
COLORS = ["#f2c14e", "#e76f51", "#2a9d8f", "#8ecae6", "#b5838d"]

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor("#101216")
ax.set_facecolor("#101216")

for (name, c, d, ct, rets), hex_ in zip(DATA, COLORS):
    # the place: a horizontal line at the count, never an event
    ax.axhline(d, color=hex_, lw=1.4, alpha=0.45, ls=(0, (5, 4)))
    ax.text(3.0, d, f"{name} · count {d}", color=hex_, fontsize=9,
            va="center", ha="left", alpha=0.95,
            bbox=dict(facecolor="#101216", edgecolor="none", pad=1))
    # the returns: short vertical ticks at the count's level
    for t in rets:
        ax.plot([t, t], [d * 0.82, d * 1.18], color=hex_, lw=2.0,
                solid_capstyle="round", alpha=0.85)
    # the crown: one diamond, a first arrival — an octave below its count
    ax.plot([ct], [c], marker="D", ms=13, color=hex_, mec="#101216",
            mew=1.4, zorder=6)

# axis dressing
ax.set_xlim(0, 72)
ax.set_ylim(38, 3000)
ax.set_yscale("log")
ax.set_facecolor("#101216")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#5b616e")
ax.tick_params(colors="#c9cdd6", which="both", labelsize=9)
ax.grid(True, which="both", color="#262b33", lw=0.6, alpha=0.7)
ax.set_xlabel("seconds", color="#c9cdd6", fontsize=11)
ax.set_ylabel("frequency (log)", color="#c9cdd6", fontsize=11)
ax.set_title("the double never lands — five places, one law",
             color="#e8eaed", fontsize=13, pad=12)

handles = [
    Line2D([0], [0], marker="D", color="none", ms=11, mec="#c9cdd6",
           mew=1.2, label="the crown — a first arrival (a record)"),
    Line2D([0], [0], color="#c9cdd6", lw=1.4, ls=(0, (5, 4)),
           label="the count 2c — a place, never an event"),
    Line2D([0], [0], color="#c9cdd6", lw=2.0,
           label="returns — the count struck at the law's rate"),
]
ax.legend(handles=handles, facecolor="#1a1e25", edgecolor="#2a3038",
          labelcolor="#e8eaed", fontsize=9, loc="upper right",
          framealpha=0.95)

fig.text(0.985, 0.02,
         "84 struck 73x, 110 39x, 222 8x, 540 once, 2502 never (400k rungs) — "
         "the silent ones are priced out, not barred",
         ha="right", va="bottom", color="#8a90a0", fontsize=9, style="italic")

fig.tight_layout(rect=(0, 0, 1, 0.98))
fig.savefig("assets/shadow-score.png", dpi=160, facecolor=fig.get_facecolor())
print("wrote assets/shadow-score.png")
