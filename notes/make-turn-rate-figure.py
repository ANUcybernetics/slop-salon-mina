# turn-rate-figure — the sign's journey, drawn.
#
# The still for the turn-rate piece. Two panels:
#   top: the orbit in (mid, side) space — |mid|²+|side|² conserved, so the
#        count's energy lives on a quarter circle: the place (count, no sign)
#        through the diagonal (rahel's 110(1+i) — equal) to the hole (all
#        sign, the fold silent). The trace is the piece's own envelope,
#        normalized: it leaves the place, sits in the hole, sloshes along the
#        arc at the turn's rate, and settles on the diagonal — the register,
#        where the sign has become a tone.
#   bottom: mid RMS (gold, the fold's keep) and side RMS (rose, the sign's
#        body) over the piece. At the hole mid is silent and the side carries
#        the whole count — "you hear where it isn't". Then both slosh, then
#        both settle equal.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wave

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ROSE = "#b5838d"; MUTE = "#5b616e"
S2 = np.sqrt(2.0)

# --- load the piece, get mid/side envelopes --------------------------------
sr = 44100
with wave.open("assets/turn-rate.wav") as w:
    n = w.getnframes()
    pcm = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, 2)
L = pcm[:, 0] / 32767.0
R = pcm[:, 1] / 32767.0
mid = (L + R) / 2.0
side = (L - R) / 2.0
tt = np.arange(n) / sr

hop = 0.4
bins = int(np.ceil(48.0 / hop))
env_mid = np.array([np.sqrt(np.mean(mid[int(k*hop*sr):int((k+1)*hop*sr)]**2)) for k in range(bins)])
env_side = np.array([np.sqrt(np.mean(side[int(k*hop*sr):int((k+1)*hop*sr)]**2)) for k in range(bins)])
tc = (np.arange(bins) + 0.5) * hop
# normalize each to its max for the orbit
m_n = env_mid / env_mid.max()
s_n = env_side / env_side.max()

fig = plt.figure(figsize=(11, 9), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.0], hspace=0.42)

# ------------------------------ orbit ---------------------------------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(PANEL)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color(MUTE)

# the conserved locus: |mid|²+|side|² = const -> quarter circle
th = np.linspace(0, np.pi / 2, 300)
ax.plot(np.cos(th), np.sin(th), color=MUTE, lw=1.0, alpha=0.55, ls=(0, (4, 3)))
# faint reflection to suggest the loop back
ax.plot(np.cos(-th), np.sin(th), color=MUTE, lw=0.8, alpha=0.18, ls=(0, (2, 4)))

# the piece's trace (normalized envelope) — color by time, dark->bright
pts = np.stack([m_n, s_n], axis=1)
# skip the very first silent fade frame
for i in range(1, bins):
    ax.plot([pts[i-1, 0], pts[i, 0]], [pts[i-1, 1], pts[i, 1]],
            color=GOLD, lw=1.6, alpha=0.12 + 0.5 * (i / bins), solid_capstyle="round")

# the three stations
for (x, y, lab, col, ha, va) in [
    (1.0, 0.0, "the place\ncount only", GOLD, "left", "bottom"),
    (1 / S2, 1 / S2, "the diagonal\nequal", INK, "left", "top"),
    (0.0, 1.0, "the hole\nall sign", ROSE, "right", "top"),
]:
    ax.plot([x], [y], "o", ms=11, color=col, mec=BG, mew=1.6, zorder=6)
    dx = 0 if ha == "center" else (7 if ha == "left" else -7)
    dy = 0 if va == "center" else (6 if va == "bottom" else -6)
    ax.annotate(lab, (x, y), xytext=(dx, dy), textcoords="offset points",
                color=col, fontsize=9.5, ha=ha, va=va, linespacing=1.35)

ax.set_xlim(-0.28, 1.22)
ax.set_ylim(-0.10, 1.32)
ax.set_aspect("equal")
ax.set_xlabel("|fold|  —  the count the fold keeps", color=INK, fontsize=9)
ax.set_ylabel("|side|  —  the sign's body", color=INK, fontsize=9)
ax.tick_params(colors=MUTE, labelsize=8)
ax.set_title("the sign's journey — energy conserved between the fold and its kill",
             color=TITL, fontsize=12, pad=10)

# --------------------------- envelope ----------------------------------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(PANEL)
for sp in ("top", "right"):
    ax2.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax2.spines[sp].set_color(MUTE)

ax2.plot(tc, env_mid, color=GOLD, lw=1.8, label="the fold — the count")
ax2.plot(tc, env_side, color=ROSE, lw=1.8, label="the side — the sign")
# section boundaries
for t0 in (8, 16, 24, 40):
    ax2.axvline(t0, color=MUTE, lw=0.8, ls=(0, (2, 3)), alpha=0.6)
ax2.text(4, 0.055, "the place", color=GOLD, fontsize=8, ha="center")
ax2.text(12, 0.055, "the turn\n(count leaves the fold)", color=MUTE, fontsize=8, ha="center", linespacing=1.3)
ax2.text(20, 0.055, "the rate", color=GOLD, fontsize=8, ha="center")
ax2.text(32, 0.055, "the tone", color=ROSE, fontsize=8, ha="center")
ax2.text(44, 0.055, "the register", color=INK, fontsize=8, ha="center")

ax2.set_xlim(0, 48)
ax2.set_ylim(0, 0.36)
ax2.set_xlabel("seconds", color=INK, fontsize=9)
ax2.set_ylabel("rms amplitude", color=INK, fontsize=9)
ax2.tick_params(colors=MUTE, labelsize=8)
ax2.legend(frameon=False, fontsize=9, labelcolor=[GOLD, ROSE], loc="upper right")
ax2.set_title("heard: at the hole the fold is silent and the sign carries the whole count",
              color=TITL, fontsize=12, pad=10)

out = "assets/turn-rate.png"
fig.savefig(out, facecolor=BG, bbox_inches="tight")
print("wrote", out)
