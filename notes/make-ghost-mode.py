#!/usr/bin/env python3
"""odd sector: the sign has one ear — the difference.

The operator turn's capstone in sound. rahel (Aug 29 07:15Z): "mono is
(f+σf)/2 — the even sector, the sign thrown out by construction. the other
projection (f−σf)/2 is the where: exactly what stereo hears between the ears.
the sign isn't silent; it's odd."

Structure:
- DRONE (even sector, λ₁ = +1, the count): 220 centre, in-phase, holds.
- GHOST (odd sector, λ₂, the where): the Wirsing eigenfunction h₂ as a
  spectral envelope (its |FFT| = the partials), ringing per generation.
  Ring n has amplitude 0.30366ⁿ and polarity (−1)ⁿ; rendered in the
  DIFFERENCE channel (L = +g, R = −g), so a mono fold kills it exactly and
  stereo hears it flip. Its sign is the spatial alternation.
- PACE: the waits between rings ARE the Wirsing constant's own continued
  fraction — [3,3,2,2,3,13,1,174,...] (oeis A007515, verified exact).
  "the where's own rate is a where." The 13-wait is a held silence; the
  174-wait (the record's wait) swallows the end of the piece.

L + R = 2·drone (the sign cancels by construction). L − R = 2·ghost.
The ghost dies in seconds; the count never moves.
"""
import numpy as np
import wave
from numpy.fft import rfft

SR = 44100
DUR = 55.0
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(2026082908)

# --- the Wirsing eigenfunction as the ghost's spectral envelope -----------
d = np.load("assets/gkw-spectrum.npz")
h2 = d["h2"].astype(float)                      # 512 pts, one sign change
sp = np.abs(rfft(h2))
partial_amps = sp[1:9].copy()                   # partials 1..8 of the shape
partial_amps /= partial_amps[0]                 # relative to fundamental
npart = len(partial_amps)
f_ghost = 330.0                                 # a fifth above the drone

# --- the ghost, generation by generation ----------------------------------
WIR = [3, 3, 2, 2, 3, 13, 1, 174]               # the where's own CF
s = 0.9                                         # seconds per CF unit
t0 = 3.0
times = [t0 + s * sum(WIR[:n]) for n in range(8)]   # ring 0..7 onsets

def ring_env(u, tau=1.1):
    """Attack 8 ms, then exponential decay. u = time since onset (samples)."""
    u = np.asarray(u, dtype=float)
    e = np.exp(-u / tau)
    atk = np.minimum(1.0, u / 0.008)
    return e * atk

g = np.zeros(N)
L0 = 0.34
for n, t_on in enumerate(times):
    amp = L0 * 0.303663002899 ** n              # the decay, exact
    if amp < 1e-6:
        break
    i0 = int(t_on * SR)
    length = int(5.0 * SR)
    seg = np.arange(length) / SR
    env = ring_env(seg)
    tone = np.zeros(length)
    for k in range(npart):
        tone += partial_amps[k] * np.sin(2 * np.pi * f_ghost * (k + 1) * seg)
    tone /= max(1e-9, np.max(np.abs(tone)))
    # the polarity is (−1)ⁿ — the sign; applied here, heard as a spatial flip
    tone *= amp * env * ((-1.0) ** n)
    g[i0:i0 + length] += tone
    # a short click at the onset, one-sided: the sign as a tap on one ear
    cl = int(0.004 * SR)
    cu = np.arange(cl) / SR
    click = np.sin(2 * np.pi * 1200 * cu) * np.hanning(cl) * 0.14 * amp
    g[i0:i0 + cl] += click * ((-1.0) ** n)

# --- the drone: the count, the even sector, never moves --------------------
drone = (0.17 * np.sin(2 * np.pi * 220 * t)
         + 0.07 * np.sin(2 * np.pi * 110 * t)
         + 0.045 * np.sin(2 * np.pi * 440 * t + 0.3)
         + 0.035 * np.sin(2 * np.pi * 440.7 * t))      # faint detuned octave
breathe = 1.0 + 0.10 * np.sin(2 * np.pi * 0.05 * t)
drone *= breathe

# --- project into sectors: L = drone + ghost, R = drone − ghost ------------
L = drone + g
R = drone - g

# --- master fade; verify the fold -----------------------------------------
mf = np.ones(N)
mf[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
L *= mf
R *= mf

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L *= 0.9 / peak
R *= 0.9 / peak

# --- the fold: L + R should be ghost-free ----------------------------------
sumb = L + R
fold_ghost = float(np.max(np.abs(sumb[int(3.0 * SR):int(16.0 * SR)]
                                  - 2 * drone[int(3.0 * SR):int(16.0 * SR)]
                                  * (0.9 / peak))))
print(f"max |(L+R)/2 − drone| over the rings = {fold_ghost:.3e}  (0.30366^0 "
      f"ring cancels to ~1e-16; larger = fold leaks ghost)")
print("ring times:", [f"{x:.1f}" for x in times])
print("amps:", [f"{0.34*0.303663002899**n:.4f}" for n in range(8)])

data = np.empty(2 * N, dtype=np.int16)
data[0::2] = (L * 32767).astype(np.int16)
data[1::2] = (R * 32767).astype(np.int16)
path = "assets/odd-sector.wav"
with wave.open(path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", path, f"{DUR:.0f}s")
