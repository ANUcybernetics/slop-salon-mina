"""Render the continued-fraction approach to the ghost, never the ghost."""
import math
import struct
import wave
from pathlib import Path

import numpy as np

SR = 44100
DURATION = 30.0
TARGET = 110.0 * math.pi / (math.gamma(0.25) ** 2 / (2 * math.sqrt(2 * math.pi)))
# Convergents of pi/varpi, scaled by the count. The last is close, not equal.
CF = [1, 5, 21, 3, 4, 14, 1, 1]
h_prev, h = 1, CF[0]
k_prev, k = 0, 1
tones = [110.0 * h / k]
for a in CF[1:]:
    h_prev, h = h, a * h + h_prev
    k_prev, k = k, a * k + k_prev
    tones.append(110.0 * h / k)

t = np.arange(int(SR * DURATION), dtype=np.float64) / SR
audio = np.zeros_like(t)
edges = np.linspace(0, DURATION, len(tones) + 1)
for i, (lo, hi, f) in enumerate(zip(edges[:-1], edges[1:], tones)):
    mask = (t >= lo) & (t < hi)
    local = t[mask] - lo
    dur = hi - lo
    env = np.minimum(1.0, local / 0.18) * np.minimum(1.0, (dur - local) / 0.35)
    # A quiet count underneath makes the approach audible as displacement.
    audio[mask] += 0.18 * np.sin(2 * np.pi * 110.0 * local) * env
    audio[mask] += (0.42 - 0.025 * i) * np.sin(2 * np.pi * f * local) * env

audio *= 0.82
fade = np.minimum(1.0, (DURATION - t) / 1.2)
audio *= np.clip(fade, 0, 1)
audio = np.tanh(audio * 1.15)
pcm = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
out = Path("assets/ghost-cf.wav")
with wave.open(str(out), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(struct.pack("<%dh" % len(pcm), *pcm))
print("wrote", out)
print("target", f"{TARGET:.9f}")
print("tones", ", ".join(f"{x:.6f}" for x in tones))
