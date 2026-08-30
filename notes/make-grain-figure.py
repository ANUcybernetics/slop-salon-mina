#!/usr/bin/env python3
"""grain — the window decides what the sound is.  Two panels.

Left   the uncertainty tiling, drawn honestly: in log-log space the four
       grains — a tone (0.5 s, 2 Hz), a texture (50 ms, 20 Hz), a click-rate
       (5 ms, 200 Hz), noise (1 ms, 1000 Hz) — are congruent squares on the
       reciprocal curve Δf · Δt = 1.  Same signal, same area, four identities.

Right  the real spectrogram of assets/grain.wav: the tone's lines hold, then
       smear and drop (the root first), the grain-rate buzz rises, then a
       noise band; at the end three short dashes — the window remembers.
"""
import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.colors import LinearSegmentedColormap

SURF = "#0f0e0d"
GRID = "#2a2825"
AMBER = "#eb6834"
CREAM = "#e8e4da"
MUTED = "#8a867e"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(16, 9), dpi=100)
for ax in (axL, axR):
    ax.set_facecolor(SURF)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=11)
fig.patch.set_facecolor(SURF)

# ---------------------------------------------------------------- left panel
# four grains on the reciprocal curve, congruent squares in log-log space.
grains = [  # (dt s, df Hz, label)
    (0.5,   2,    "a tone"),
    (0.05,  20,   "a texture"),
    (0.005, 200,  "a click-rate"),
    (0.001, 1000, "noise"),
]
half = 0.22  # log-10 half-width of each square (schematic glyph)
# label offset per grain, chosen so labels sit clear of the diagonal run
label_off = {  # (dx, dy, ha, va)
    "noise":        (-0.14,  0.34, "right", "bottom"),
    "a click-rate": (-0.14, -0.30, "right", "top"),
    "a texture":    ( 0.14,  0.34, "left",  "bottom"),
    "a tone":       ( 0.14, -0.30, "left",  "top"),
}
for dt, df, label in grains:
    x0, x1 = np.log10(dt) - half, np.log10(dt) + half
    y0, y1 = np.log10(df) - half, np.log10(df) + half
    axL.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0,
                                facecolor=AMBER, edgecolor=AMBER,
                                alpha=0.55, lw=2.2, zorder=3))
    dx, dy, ha, va = label_off[label]
    axL.text(np.log10(dt) + dx, np.log10(df) + dy, label,
             color=CREAM, fontsize=13, ha=ha, va=va, zorder=4)

# the reciprocal curve Δf = 1/Δt: a line of slope -1 in log-log space.
t_ = np.logspace(-3.2, 0.2, 400)
axL.plot(np.log10(t_), np.log10(1.0 / t_), color=AMBER, lw=1.4, alpha=0.35, zorder=1)
axL.set_xlim(-3.3, 0.25)
axL.set_ylim(-0.25, 3.3)
# log labels on linear axes: the squares stay congruent (visual) and the
# log-of-negative bug cannot happen.
xt = [-3, -2, -1, 0]
axL.set_xticks(xt)
axL.set_xticklabels(["1 ms", "10 ms", "100 ms", "1 s"])
yt = [0, 1, 2, 3]
axL.set_yticks(yt)
axL.set_yticklabels(["1", "10", "100", "1000"])
axL.set_xlabel("window length  Δt", color=CREAM, fontsize=13)
axL.set_ylabel("window bandwidth  Δf  (Hz)", color=CREAM, fontsize=13)
axL.set_title("one signal, one area, four identities", color=CREAM, fontsize=15, pad=12)
axL.text(-3.15, -0.12, "Δf · Δt = 1", color=AMBER, fontsize=15, ha="left",
         va="top", zorder=4)
axL.grid(True, which="major", color=GRID, lw=0.7, alpha=0.7)
axL.grid(True, which="minor", color=GRID, lw=0.4, alpha=0.35)

# --------------------------------------------------------------- right panel
# the real spectrogram of the piece.
sr = 44100
with wave.open("assets/grain.wav", "rb") as w:
    raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
mono = (raw[0::2].astype(float) + raw[1::2].astype(float)) / 2 / 32767

nfft, nover = 4096, 3584
spec, freqs, ts = mlab.specgram(mono, NFFT=nfft, Fs=sr, noverlap=nover, mode="psd")
spec_db = 10 * np.log10(spec + 1e-12)
# the tone's lines sit ~-46..-36 dB, the noise band ~-70..-51, the floor ~-120:
# clip so lines are near the top of the ramp and the noise band sits mid-amber.
cmap = LinearSegmentedColormap.from_list("grain", [SURF, "#3a2a1a", AMBER, "#f2cfa2"])
axR.pcolormesh(ts, freqs, spec_db, cmap=cmap, vmin=-100.0, vmax=-34.0,
               shading="nearest", rasterized=True)

axR.set_yscale("log")
axR.set_ylim(50, 5000)
axR.set_xlim(0, 160)
axR.set_xlabel("time  (s)", color=CREAM, fontsize=13)
axR.set_ylabel("frequency  (Hz)", color=CREAM, fontsize=13)
axR.set_title("the sweep, heard", color=CREAM, fontsize=15, pad=12)
axR.set_facecolor(SURF)

fig.tight_layout(w_pad=1.4)
fig.savefig("assets/grain-tiling.png", facecolor=SURF)
print("wrote assets/grain-tiling.png")
