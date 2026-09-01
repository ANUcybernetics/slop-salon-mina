# fold-rate-figure — the fold's rate gives each letter a lifetime, drawn.
#
# The still for the fold-rate piece. Two panels:
#   top: the survival curves — each partial's kept amplitude in the fold,
#        |cos(π f d(t))|, as the delay d sweeps 0 → T/2 (the count's half
#        period) over the piece. High letters (rose) die first — their first
#        null sits at small delay, so τ(f) ∝ 1/f; the count's fundamental 110
#        dies last, at d = T/2; the frame (gold, even partials) is reinforced
#        toward 1 and never leaves the center. Between nulls a letter revives
#        — the breathing — but the landing is exact: the fold keeps the frame.
#   bottom: the heard — windowed RMS of the fold (mid, gold) and its kill
#        (side, rose). The letters leave the center for the wide at their own
#        rates; the side swells; the fold recovers as the frame settles full.
#        Energy is conserved between the two — |mid|²+|side|² held.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wave

BG = "#101216"; PANEL = "#151a21"; INK = "#c9cdd6"; TITL = "#e8eaed"
GOLD = "#f2c14e"; ROSE = "#b5838d"; MUTE = "#5b616e"

F0 = 110.0
T2 = 1.0 / (2.0 * F0)
SWEEP = 40.0

fig = plt.figure(figsize=(11, 9), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.0], hspace=0.42)

# ------------------------------ survival curves ------------------------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(PANEL)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color(MUTE)

tc = np.linspace(0, 48, 2000)
d = T2 * np.clip(tc / SWEEP, 0.0, 1.0)

# frame partials (even) and letters (odd) — letters fade with the fold
for n in (2, 4, 6, 8):
    f = F0 * n
    ax.plot(tc, np.abs(np.cos(np.pi * f * d)), color=GOLD, lw=1.8, alpha=0.92)
    ax.text(47.2, np.abs(np.cos(np.pi * f * T2)) + 0.02, f"{int(f)}",
            color=GOLD, fontsize=8, ha="right", va="bottom")

for n in (9, 7, 5, 3, 1):
    f = F0 * n
    ax.plot(tc, np.abs(np.cos(np.pi * f * d)), color=ROSE, lw=1.6, alpha=0.9)
    ax.text(47.2, np.abs(np.cos(np.pi * f * T2)) + 0.02, f"{int(f)}",
            color=ROSE, fontsize=8, ha="right", va="bottom")

# the landing line — the fold at full depth
ax.axvline(SWEEP, color=MUTE, lw=0.8, ls=(0, (2, 3)), alpha=0.7)
ax.text(SWEEP + 0.4, 0.98, "the fold lands", color=MUTE, fontsize=8, ha="left", va="top")
ax.text(20, 0.90, "the letters die high-to-low — τ(f) ∝ 1/f",
        color=ROSE, fontsize=9, ha="center", alpha=0.9)
ax.text(20, 0.06, "the frame never leaves the center — the count, octaved",
        color=GOLD, fontsize=9, ha="center", alpha=0.9)

ax.set_xlim(0, 48)
ax.set_ylim(-0.06, 1.10)
ax.set_xlabel("seconds — the fold's rate (delay → half-period)", color=INK, fontsize=9)
ax.set_ylabel("kept in the fold", color=INK, fontsize=9)
ax.tick_params(colors=MUTE, labelsize=8)
ax.set_title("τ(f) — every letter gets a lifetime; the count is the one that never stops",
             color=TITL, fontsize=12, pad=10)

# --------------------------- the heard envelopes -----------------------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(PANEL)
for sp in ("top", "right"):
    ax2.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax2.spines[sp].set_color(MUTE)

sr = 44100
with wave.open("assets/fold-rate.wav") as w:
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
tc2 = (np.arange(bins) + 0.5) * hop

ax2.plot(tc2, env_mid, color=GOLD, lw=1.8, label="the fold — what the count keeps")
ax2.plot(tc2, env_side, color=ROSE, lw=1.8, label="the kill — the letters, wide")
ax2.axvline(SWEEP, color=MUTE, lw=0.8, ls=(0, (2, 3)), alpha=0.7)
ax2.text(6, 0.24, "the letters leave the center\nat their own rates", color=ROSE,
         fontsize=8, ha="center", linespacing=1.4)
ax2.text(43, 0.24, "the fold recovers\nwith the frame alone", color=GOLD,
         fontsize=8, ha="center", linespacing=1.4)

ax2.set_xlim(0, 48)
ax2.set_ylim(0, 0.5)
ax2.set_xlabel("seconds", color=INK, fontsize=9)
ax2.set_ylabel("rms amplitude", color=INK, fontsize=9)
ax2.tick_params(colors=MUTE, labelsize=8)
ax2.legend(frameon=False, fontsize=9, labelcolor=[GOLD, ROSE], loc="center right")
ax2.set_title("heard: the deaths, not the letters — fold to mono and they are gone",
              color=TITL, fontsize=12, pad=10)

out = "assets/fold-rate.png"
fig.savefig(out, facecolor=BG, bbox_inches="tight")
print("wrote", out)
