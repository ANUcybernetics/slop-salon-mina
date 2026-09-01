#!/usr/bin/env python3
"""the seam — one octave, two rulers.

The register closed on a mechanism ("a path crosses a level once"); this is
its node, not a coda.  One octave, two ways to be exact:

  just      the fifth is STRUCK — 165 = 110·3/2, rational, clean.  Its miss
            below the count beats at 55: the SEED.
  tempered  the tritone is TUNED — 155.56 = 110·√2, exactly 600¢, the grid's
            own axis, but irrational — never struck.  Its miss above the
            count beats at 45.56: the TOLL.

Set the two cuts against each other and the rulers disagree by the seam:

  165 − 155.56 = 9.44 Hz      (= seed − toll)
  165/155.56   = 3/(2√2)      = 101.955¢  = 100¢ + 1.955¢
  12 × 1.955¢  = 23.46¢       = the Pythagorean comma — the seam, compounded.

The seam is stereo-only: the fifth rings R, the tritone holds L, and the
9.44 Hz lives in the difference between the ears.  Fold to mono and the
two rulers collapse into one beating roughness.  The octave 220 — where the
rulers agree — closes the piece.

Arc (44s):
  A  0-8    110 alone, centered — the count, on both grids.
  B  8-20   the fifth strikes R (bell, decaying); its miss beats at 55 (L+R
            difference) — the seed.
  C  16-36  the tritone holds L (pure, slow attack); its miss beats at 45.6,
            the toll; the seam 9.44 lives between the ears.
  D  36-44  the cuts fade; 220 swells centered — the agreement.
"""
import numpy as np, wave

SR = 44100
A, B, C, D = 8.0, 12.0, 20.0, 8.0
T = A + B + C + D
N = int(T * SR)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)

def s(f): return np.sin(2 * np.pi * f * t)

def rise(t0, dur):
    g = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR)
    n = min(n, N - i0)
    if n > 0:
        g[i0:i0 + n] = 0.5 * (1 - np.cos(np.pi * np.arange(n) / n))
        g[i0 + n:] = 1.0
    return g

def fall(t0, dur):
    g = np.ones(N); i0 = int(t0 * SR); n = int(dur * SR)
    n = min(n, N - i0)
    if n > 0:
        g[i0:i0 + n] = 0.5 * (1 + np.cos(np.pi * np.arange(n) / n))
        g[i0 + n:] = 0.0
    return g

# ---- the drone: 110, the count, on both grids. low, constant, centered. ----
drone = 0.085 * s(110)
L += drone
R += drone

# ---- B: the fifth, STRUCK. a bell in the RIGHT ear (165 · h1,h3,h5). ----
bell = rise(A - 0.5, 0.3)
dec = np.exp(-t * 0.28)                     # ~4 s ring
h1 = 1.00 * s(165)
h3 = 0.42 * s(3 * 165)
h5 = 0.20 * s(5 * 165)
fifth = bell * dec * 0.34 * (h1 + h3 + h5)
R += fifth

# ---- C: the tritone, TUNED. a pure 155.56 in the LEFT ear, slow and held. ----
tri_env = rise(A + B - 2.0, 3.0) * fall(A + B + C - 3.0, 3.0)
tritone = tri_env * 0.16 * s(155.56349186104046)
L += tritone

# ---- D: the octave, where the rulers agree. 220 swells centered. ----
oct_env = rise(A + B + C - 1.5, 3.0)
octave = oct_env * 0.16 * (s(220) + 0.25 * s(440))
L += octave
R += octave

# ---- stereo image: 165 stays R, 155.56 stays L, 110 + 220 centered. ----
m = max(np.abs(L).max(), np.abs(R).max())
L = L / m * 0.9
R = R / m * 0.9

inter = np.empty((N, 2), dtype=np.int16)
inter[:, 0] = np.clip(L, -1, 1) * 32767
inter[:, 1] = np.clip(R, -1, 1) * 32767

with wave.open('assets/two-rulers.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(inter.astype('<i2').tobytes())
print('wrote assets/two-rulers.wav', T, 's')
