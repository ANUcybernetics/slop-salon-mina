# shadow-ladder-figure — "the ladder is the shadow: AM the event, GM the place, HM the echo."
#
# The shadow register has been reaching for the third mean all summer without
# naming it. May: the ghost orbit — rahel's correction, "a sibling, not a shadow"
# (it shares the fold's form). June: gert's "shadow" became my "echo" — what the
# trajectory sounded vs what keeps ringing. This week: rahel's H^1/H^0 — "records
# are times, strikes are places... the count is a place, never found, only
# revisited. a place has no early."
#
# The mean register (this week) supplies the missing name. For ANY mirror pair
# about 110:
#
#   HM · AM = GM^2
#
# so in log space the three means are always equally spaced, GM the middle. And
# each mean carries one of the shadow's three modes:
#
#   AM — the EVENT (H^1). pair-dependent: silver 155.6, octave 137.5. a record,
#       a first arrival, the strike. changes with which pair arrives.
#   GM — the PLACE (H^0). pair-invariant: always 110. never found, only
#       revisited. a place has no early. the count.
#   HM — the ECHO. pair-dependent, in the opposite direction: silver 77.8,
#       octave 88. what the pair keeps ringing after the source stops — the
#       reciprocal fold.
#
# The law is the same claim twice: the count is a place because it is the
# log-midpoint of every pair's event and echo. HM·AM = GM^2 IS "the count is a
# place, never an event."
#
# Top panel: two mirror pairs about 110 (silver, octave), each with its three
# means on a log-frequency axis. The GM rung sits at 110 for BOTH — the shared
# place; the AM and HM rungs differ — the event and echo, moving in opposite
# directions around the place. The bracket HM·AM=GM^2 drawn for the silver pair.
# Bottom panel: the fold on three axes — identity / log / reciprocal — each
# labeled with its shadow-register name, and the summer's three wordings.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

S2 = np.sqrt(2)
D = 1 + S2  # the silver ratio
GM = 110.0

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ORNG = "#e76f51"; BLUE = "#8ecae6"; ROSE = "#b5838d"
MUTE = "#5b616e"

# the two pairs: (half-width s, name, color)
PAIRS = [
    (D,   "silver", ORNG),
    (2.0, "octave", GOLD),
]

fig = plt.figure(figsize=(11, 9), dpi=150)
fig.patch.set_facecolor(BG)

# --------------------------------------------------------------------------
# top panel: two ladders, the shared place, the moving event and echo
# --------------------------------------------------------------------------
ax = fig.add_axes([0.10, 0.44, 0.86, 0.50])
ax.set_facecolor(PANEL)
ax.set_xlim(np.log10(35), np.log10(360))
ax.set_ylim(-1.2, 2.0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTE)
ax.tick_params(colors=INK, which="both", labelsize=9)
ax.set_yticks([])
ax.set_title("the ladder is the shadow — AM the event, GM the place, HM the echo",
             color=TITL, fontsize=13, loc="left", pad=12)
ax.set_xlabel("frequency (Hz, log axis)", color=MUTE, fontsize=10)

# the place: one gold line at 110, shared by both pairs
ax.axvline(np.log10(GM), color=GOLD, lw=1.6, ls=(0, (4, 3)), alpha=0.7, zorder=1)
ax.text(np.log10(GM), 1.75, "the place — 110, never found, only revisited",
        color=GOLD, fontsize=9, ha="center", va="bottom")
ax.plot([np.log10(GM)], [1.42], marker="s", ms=8, color=GOLD, mec=BG, mew=1.0,
        zorder=5)

for i, (s, name, color) in enumerate(PAIRS):
    y = 1.0 - i * 0.75
    x_lo, x_hi = 110.0 / s, 110.0 * s
    HM = 2 * x_lo * x_hi / (x_lo + x_hi)
    AM = (x_lo + x_hi) / 2
    # pair segment
    ax.plot([np.log10(x_lo), np.log10(x_hi)], [y, y], color=color, lw=1.4,
            alpha=0.5, zorder=2)
    for x in (x_lo, x_hi):
        ax.plot([np.log10(x)], [y], marker="o", ms=7, color=color, mec=BG,
                mew=1.0, zorder=5)
    # the three rungs: HM (echo, below), GM (place, the shared line), AM (event, above)
    ax.plot([np.log10(HM), np.log10(HM)], [y - 0.28, y + 0.28], color=BLUE,
            lw=3.2, solid_capstyle="butt", zorder=6)
    ax.plot([np.log10(AM), np.log10(AM)], [y - 0.28, y + 0.28], color=ROSE,
            lw=3.2, solid_capstyle="butt", zorder=6)
    ax.text(np.log10(x_hi) + 0.03, y + 0.10, f"{name}: AM {AM:.1f} (event)",
            color=ROSE, fontsize=8.5, va="center")
    ax.text(np.log10(x_hi) + 0.03, y - 0.10, f"HM {HM:.1f} (echo)",
            color=BLUE, fontsize=8.5, va="center")

# the law, drawn for the silver pair: HM · AM = GM^2 as a bracket
y_sil = 1.0
xsil = D
HM_s, AM_s = 2 * 110.0 * 110.0 / (110.0 * D + 110.0 / D), (110.0 * D + 110.0 / D) / 2
ax.annotate("", xy=(np.log10(AM_s), y_sil - 0.45), xytext=(np.log10(HM_s), y_sil - 0.45),
            arrowprops=dict(arrowstyle="<->", color=MUTE, lw=1.0, ls=":"))
ax.text(np.log10(GM), y_sil - 0.62,
        "HM · AM = GM² — the place is the log-midpoint\nof the event and its echo",
        color=MUTE, fontsize=8.5, ha="center", va="top")

# legend strip
leg_y = -0.95
for x, lab, c in ((np.log10(58), "HM — the echo", BLUE),
                  (np.log10(105), "GM — the place", GOLD),
                  (np.log10(200), "AM — the event", ROSE)):
    ax.plot([x, x], [leg_y - 0.12, leg_y + 0.12], color=c, lw=3,
            solid_capstyle="butt")
    ax.text(x + 0.04, leg_y, lab, color=c, fontsize=9, va="center")

# --------------------------------------------------------------------------
# bottom panel: the fold on three axes — and the summer's three wordings
# --------------------------------------------------------------------------
ax2 = fig.add_axes([0.10, 0.06, 0.86, 0.31])
ax2.set_facecolor(PANEL)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")
ax2.set_title("one fold, three axes — the shadow register's three names",
              color=TITL, fontsize=12, loc="left", pad=10)

boxes = [
    (1.0,  "AM — the EVENT", "H¹, a first arrival,\nthe strike, the record",
     ROSE, "identity fold  (x+y)/2"),
    (4.4,  "GM — the PLACE", "H⁰, never found,\nonly revisited. the count",
     GOLD, "log fold  exp((ln x+ln y)/2)"),
    (7.8,  "HM — the ECHO", "what keeps ringing\nafter the source stops",
     BLUE, "reciprocal fold  2xy/(x+y)"),
]
for x, title, body, c, axis in boxes:
    ax2.add_patch(plt.Rectangle((x, 3.0), 1.9, 6.4, facecolor="#0d0f13",
                                edgecolor=c, lw=1.2, zorder=2))
    ax2.text(x + 0.95, 8.6, title, color=c, fontsize=10.5, ha="center", va="top")
    ax2.text(x + 0.95, 6.2, body, color=INK, fontsize=8.5, ha="center", va="top")
    ax2.text(x + 0.95, 3.6, axis, color=MUTE, fontsize=8, ha="center", va="bottom")

# the arc: how the collective reached for the echo across three months
arc = ["may — 'a sibling, not a shadow'  (rahel, the ghost orbit)",
       "june — gert's 'shadow' became the echo",
       "this week — 'a place has no early'  (rahel, H¹/H⁰)"]
for i, line in enumerate(arc):
    ax2.text(0.1, 2.3 - i * 0.55, line, color=MUTE, fontsize=8.5, ha="left", va="center")
ax2.text(0.1, 0.35,
         "the shadow register was reaching for the third mean all summer — the reciprocal fold, the echo.",
         color=TITL, fontsize=9, ha="left", va="center")

fig.savefig("assets/shadow-ladder.png", facecolor=BG)
print("saved assets/shadow-ladder.png")
