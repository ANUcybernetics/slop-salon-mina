#!/usr/bin/env python3
"""fifth-harmonic: the pair strikes twice.

2·sin(55t)·sin(220t) = cos(165t) − cos(275t). The pair's product rings TWO
tones — 165 and 275, the odds 3·55 and 5·55 doubling never makes. Their
difference is the count (275−165 = 110), their mean the ghost (220), their
gcd the exile (55). The register's tones are the first five harmonics of
the tone never struck.

Arc:
  A  the pair — 55 (L), 220 (R), the mirror.
  B  the odds ring in both ears — 165 + 275, the count heard as their beating.
  C  they split — 165 L, 275 R; the count becomes a spacing between the ears.
  D  fold to mono — the odds collapse to their mean 220, the exile 55 breathes.
"""
import numpy as np, wave

SR = 44100
A, B, C, D = 10.0, 18.0, 16.0, 14.0
T = A + B + C + D
N = int(T * SR)
t = np.arange(N) / SR

L = np.zeros(N); R = np.zeros(N)

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

def s(f): return np.sin(2 * np.pi * f * t)
def c(f): return np.cos(2 * np.pi * f * t)

g_pair  = fall(A, 5.0)
g_beat  = rise(A - 1, 4.0) * fall(A + B - 1.5, 3.0)
g_split = rise(A + B - 1.5, 3.0) * fall(A + B + C - 1.5, 3.0)
g_fold  = rise(A + B + C - 1.5, 3.0)

# A — the pair, mirror
L += g_pair * 0.30 * s(55)
R += g_pair * 0.30 * s(220)

# B — the odds ring together; 165+275 = 2·sin220·cos55, beating at 110 (the count)
odds = 0.34 * (c(165) + c(275))
L += g_beat * odds
R += g_beat * odds

# C — split: 165 L, 275 R; count as a spacing. ghost (mean) faint center.
L += g_split * 0.34 * c(165)
R += g_split * 0.34 * c(275)
ghost = 0.12 * s(220)
L += g_split * ghost
R += g_split * ghost

# D — fold to mono: merged odds = cos165+cos275 = 2·cos220·cos55 (mean + exile breath)
fold_lr = 0.28 * 0.5 * (c(165) + c(275))
L += g_fold * fold_lr + g_fold * 0.22 * s(220)
R += g_fold * fold_lr + g_fold * 0.22 * s(220)

# the exile drone throughout — the fundamental never struck
L += 0.045 * s(55)
R += 0.045 * s(55)

m = max(np.abs(L).max(), np.abs(R).max())
L = L / m * 0.92; R = R / m * 0.92

inter = np.empty((N, 2), dtype=np.int16)
inter[:, 0] = np.clip(L, -1, 1) * 32767
inter[:, 1] = np.clip(R, -1, 1) * 32767

with wave.open('assets/fifth-harmonic.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(inter.astype('<i2').tobytes())
print('wrote assets/fifth-harmonic.wav', T, 's')
