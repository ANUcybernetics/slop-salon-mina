#!/usr/bin/env python3
"""ghost-note: a tone whose fundamental is absent.

The ink pair said the shape was never in the drop/plume — it belongs to the
flow. This is the same claim in pure sound, structural inverse of the
fog-drone: the drone was a tone that never moved; this is a note that is
never there.

The missing fundamental. Partials 2f..8f all present, f absent. The ear
infers f from the spacing — you cannot not hear 220. Then an inharmonicity
field B(t) stretches the lattice (f_n = n·f0·sqrt(1 + B·n^2), the piano/bell
stretch): spacings grow toward the top, the ghost thins, rises, smears. The
release fades high partials first — the note dissolves from the top down.
The note was never in the tone; the ear put it there; the field took it
back.

- f0 = 220 (A3), absent.
- Partials n = 2..8, panned low->high across the stereo field (the ladder).
- Each partial + a faint doubler at +0.15% detune, opposite pan (shimmer).
- B(t): 0 until the cascade coheres, ramps 0 -> B0 by ~38 s, keeps stretching
  into the release.
- Attacks staggered: n enters at 2 + 1.2(n-2) s, the ghost snaps in as the
  higher partials join.

WAV export: wave, 16-bit stereo, as in TOOLS.md. No scipy.
"""
import numpy as np
import wave

SR = 44100
DUR = 52.0
N = int(DUR * SR)
F0 = 220.0
PARTIALS = [2, 3, 4, 5, 6, 7, 8]
B0 = 0.00120

rng = np.random.default_rng(2026082918)
t = np.arange(N) / SR

# --- inharmonicity field B(t): 0 until cascade coheres, ramp, keep stretching.
B = np.zeros(N)
c0, c1 = int(10 * SR), int(40 * SR)
u = np.clip((np.arange(c0, c1) - c0) / max(1, c1 - c0), 0, 1)
B[c0:c1] = B0 * (0.5 * (1 - np.cos(np.pi * u)))          # smoothstep ramp
B[c1:] = B0
rel = np.arange(c1, N)
B[c1:] = B0 * (1.0 + 0.25 * ((rel) / max(1, N - c1)))    # keeps stretching during release

def pan(n):
    """-1 (full L) for n=2 .. +1 (full R) for n=8."""
    return -1.0 + 2.0 * (n - 2) / (len(PARTIALS) - 1)

def osc(freq_wave, amp_wave, panv):
    """Synthesise a partial with time-varying frequency/amplitude, panned."""
    ph = 2 * np.pi * np.cumsum(freq_wave) / SR
    s = amp_wave * np.sin(ph)
    th = np.pi / 4 * (panv + 1)
    return s * np.cos(th), s * np.sin(th)                # equal-power L/R

out_l = np.zeros(N)
out_r = np.zeros(N)

for n in PARTIALS:
    # Staggered attack: n enters at 2 + 1.2(n-2) s, swells over 4 s.
    atk0 = int((2.0 + 1.2 * (n - 2)) * SR)
    atk = int(4 * SR)
    env = np.zeros(N)
    i0 = min(atk0, N)
    i1 = min(atk0 + atk, N)
    env[i0:i1] = 0.5 * (1 - np.cos(np.pi * np.arange(i1 - i0) / max(1, i1 - i0)))
    env[i1:] = 1.0
    # Release: high partials leave first — t_r = 34 + (8-n)*1.8 s, 6 s tail.
    rel0 = int((34.0 + (8 - n) * 1.8) * SR)
    rel0 = min(rel0, N)
    relen = int(6 * SR)
    i2 = min(rel0 + relen, N)
    env[rel0:i2] = np.clip(env[rel0:i2] * (1.0 - np.linspace(0, 1, i2 - rel0)), 0, 1)
    env[i2:] = 0.0

    # Bell-ish amplitude across partials, mid-weighted.
    A = 0.85 * n ** -0.55

    # Frequencies: the lattice, stretched by B(t).
    fw = n * F0 * np.sqrt(1 + B * n * n)
    # Per-partial wander: slow independent vibrato, ~0.2 Hz, tiny depth.
    wander = 1 + 0.0012 * np.sin(2 * np.pi * (0.15 + 0.07 * rng.random()) * t + rng.random() * 6.28)
    aw = A * env * wander

    pv = pan(n)
    l, r = osc(fw, aw, pv)
    out_l += l
    out_r += r

    # Doubler: detune widens with the field, 0.25 amplitude, opposite pan.
    det = 1.0 + 0.0015 + 0.005 * (B / B0)          # 0.15% -> 0.65% as the field grows
    dw = fw * det
    aw2 = 0.25 * A * env * wander
    l2, r2 = osc(dw, aw2, -pv)
    out_l += l2
    out_r += r2

# --- master envelope: tiny fade-in, final release to silence.
mf = np.ones(N)
mf[: int(0.5 * SR)] = np.linspace(0, 1, int(0.5 * SR))
mf[-int(4 * SR):] = np.linspace(1, 0, int(4 * SR))
out_l *= mf
out_r *= mf

peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
out_l *= 0.9 / peak
out_r *= 0.9 / peak

# --- spectral sanity check: energy near partials, nothing at the fundamental.
from numpy.fft import rfft
win = np.hanning(N)
spec = np.abs(rfft((out_l + out_r) * win))
freqs = np.fft.rfftfreq(N, 1 / SR)
for f in [F0, 2 * F0, 3 * F0, 4 * F0, 5 * F0, 6 * F0, 7 * F0, 8 * F0]:
    k = np.argmin(np.abs(freqs - f))
    # mean energy within ±10 Hz of f
    band = (np.abs(freqs - f) < 10)
    print(f"  {f:6.0f} Hz  {np.mean(spec[band]):10.1f}")

data = np.empty(2 * N, dtype=np.int16)
data[0::2] = (out_l * 32767).astype(np.int16)
data[1::2] = (out_r * 32767).astype(np.int16)

path = "assets/ghost-note.wav"
with wave.open(path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", path, f"peak={peak:.3f}")
