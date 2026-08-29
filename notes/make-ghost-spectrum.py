#!/usr/bin/env python3
"""ghost-spectrum: the harmonic comb with the missing tooth.

The ghost-note's thesis in one image: partials 2f..8f bright, the
fundamental f absent — a dark gap where the note should be. The ear
fills the gap; the picture keeps it empty.

Dark field #0a0e14, water-teal comb #9ad8d2 (the ink register's palette),
the missing tooth marked with a faint warm tick so the eye seeks it.
Frequencies 0-1900 Hz, log-y magnitude, partial teeth labelled.
"""
import wave
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

w = wave.open("assets/ghost-note.wav", "rb")
sr = w.getframerate()
n = w.getnframes()
raw = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32767
L, R = raw[0::2], raw[1::2]
mono = (L + R) / 2

# Steady-state segment: the cohered ghost, before the dissolve (12-30 s).
seg = mono[int(12 * sr):int(30 * sr)] * np.hanning(int(18 * sr))
spec = np.abs(np.fft.rfft(seg))
freqs = np.fft.rfftfreq(len(seg), 1 / sr)

F0 = 220.0
PARTIALS = [2, 3, 4, 5, 6, 7, 8]

BG = "#0a0e14"
TEAL = "#9ad8d2"
DIM = "#33555a"
AMBER = "#d8a35a"
GRID = "#16262b"

fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=120)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

m = (freqs > 40) & (freqs < 1900)
f, s = freqs[m], spec[m]
ax.plot(f, s, color=TEAL, lw=1.6)
ax.set_yscale("log")

# The missing tooth: a faint vertical tick where the note is not.
ax.axvline(F0, color=AMBER, lw=1.4, ls=(0, (2, 3)), alpha=0.8)
ax.text(F0 + 12, ax.get_ylim()[1] * 0.10, "the note was never in the tone",
        color=AMBER, fontsize=12, style="italic", va="bottom")

for n in PARTIALS:
    ax.axvline(n * F0, color=DIM, lw=0.5, alpha=0.55, zorder=0)

for n in PARTIALS:
    ax.text(n * F0, ax.get_ylim()[1] * 0.72, f"{n}f", color=TEAL,
            fontsize=10, ha="center", alpha=0.9)

ax.text(F0, ax.get_ylim()[1] * 0.60, "f", color=AMBER, fontsize=10, ha="center")

ax.set_xlim(40, 1900)
ax.set_ylim(1e1, 1e5)
ax.set_xlabel("frequency (Hz)", color="#8fb3b8", fontsize=10)
ax.set_ylabel("magnitude", color="#8fb3b8", fontsize=10)
ax.tick_params(colors="#8fb3b8", labelsize=9)
for spine in ax.spines.values():
    spine.set_color(GRID)
ax.grid(axis="y", color=GRID, lw=0.5, alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("assets/ghost-spectrum.png", facecolor=BG)
print("wrote assets/ghost-spectrum.png")
