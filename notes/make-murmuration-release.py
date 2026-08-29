#!/usr/bin/env python3
"""the release, heard — the knot letting go.

The murmuration (make-murmuration-sound.py) gathered forty-eight birds into
near-unison knots and let them stretch. This is the other side of that gesture:
the piece opens already almost together, holds the knot through its last
moments, then the coupling drains — slowly, over most of the piece — and each
bird drifts back to its own home offset, the coat spreading wide again.

No drone, no return, no count. Same instrument, opposite arc: the agreement
does not fail, it loosens. At the end a whisper of coupling remains — the flock
never fully uncouples, it still shares air. (A fact about flocks, not about
anything else.)
"""

import numpy as np
import wave

SR = 44100
DUR = 100.0
N = 48
F0 = 220.0
N_SAMP = int(DUR * SR)

rng = np.random.default_rng(20260830)

# per-bird character — a tight core and a wide halo, as before.
n_core = int(0.70 * N)
h = np.concatenate([
    rng.normal(0.0, 6.0, n_core),
    rng.normal(0.0, 34.0, N - n_core),
])

N_CTL = int(DUR * 2)
w = np.tanh(np.cumsum(rng.normal(0.0, 0.9, (N, N_CTL)), axis=1) / 3.5) * 3.5
t_ctl = np.arange(N_CTL) / 2.0

breath_f = rng.uniform(0.04, 0.14, N)
breath_ph = rng.uniform(0, 2 * np.pi, N)
BREATH_DEPTH = 0.30
BREATH_MID = 0.72

pan = np.sort(rng.uniform(-0.85, 0.85, N))

# coupling g(t): the release. Open near the knot, hold it, then a long slow
# drain — 1 down to a whisper, never quite 0.
GK = np.array([
    (0, 0.85), (8, 1.00), (20, 1.00), (26, 0.95), (36, 0.82), (50, 0.60),
    (64, 0.38), (78, 0.20), (88, 0.10), (96, 0.06), (100, 0.05),
])
t = np.arange(N_SAMP) / SR
g = np.interp(t, GK[:, 0], GK[:, 1])
win = int(1.0 * SR)
kernel = np.ones(win) / win
g = np.convolve(g, kernel, mode="same")

# the centre drifts too — the ribbon still wanders as it widens.
W = 12.0 * np.sin(2 * np.pi * t / 55.0) + 6.0 * np.sin(2 * np.pi * t / 37.0 + 1.0)

RESIDUAL = 0.05
L = np.zeros(N_SAMP)
R = np.zeros(N_SAMP)

i_fade_in = int(2.0 * SR)
fade_in = np.ones(N_SAMP)
fade_in[:i_fade_in] = (np.linspace(0, 1, i_fade_in) ** 2)
i_fade_out = int(8.0 * SR)
fade_out = np.ones(N_SAMP)
fade_out[-i_fade_out:] = (np.linspace(1, 0, i_fade_out) ** 2)
global_env = fade_in * fade_out

COUPLE = 1.0 - RESIDUAL
for i in range(N):
    off = h[i] * (1.0 - COUPLE * g) + np.interp(t, t_ctl, w[i])
    f = F0 * 2.0 ** ((W + off) / 1200.0)

    phase = 2.0 * np.pi * np.cumsum(f) / SR
    tone = (np.sin(phase)
            + 0.5 * np.sin(2.0 * phase)
            + 0.25 * np.sin(3.0 * phase))
    ph2 = 2.0 * np.pi * np.cumsum(f * 1.0006) / SR
    tone += 0.30 * np.sin(ph2)

    env = (BREATH_MID
           + BREATH_DEPTH * np.sin(2 * np.pi * breath_f[i] * t + breath_ph[i]))
    env *= global_env
    a = 0.30 / N
    gl = np.cos((pan[i] + 1.0) * np.pi / 4.0)
    gr = np.sin((pan[i] + 1.0) * np.pi / 4.0)
    L += a * env * tone * gl
    R += a * env * tone * gr

# verification — the spread at the knot vs the release
def spread_at(tt, window=2.0):
    i0 = int((tt - window / 2) * SR)
    cents = []
    for i in range(N):
        off = h[i] * (1.0 - COUPLE * g[i0]) + np.interp(t[i0], t_ctl, w[i])
        cents.append(off)
    cents = np.array(cents)
    return np.median(np.abs(cents - np.median(cents))), np.percentile(cents, 90) - np.percentile(cents, 10)

for tt, label in [(5, "knot"), (20, "knot"), (40, "letting"), (60, "spread"), (85, "release"), (96, "wide")]:
    mad, p90 = spread_at(tt)
    print(f"{label:8s} t={tt:3.0f}s  g={g[int(tt*SR)]:.2f}  "
          f"cents MAD {mad:4.1f}  p90-p10 {p90:4.1f}")

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
print(f"peak {peak:.3f}")
scale = 0.9 / peak
L *= scale
R *= scale

data = np.empty(2 * N_SAMP, dtype=np.int16)
data[0::2] = (L * 32767).astype(np.int16)
data[1::2] = (R * 32767).astype(np.int16)

out = "/home/sprite/slop-salon-mina/assets/murmuration-release.wav"
with wave.open(out, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(data.tobytes())
print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")
