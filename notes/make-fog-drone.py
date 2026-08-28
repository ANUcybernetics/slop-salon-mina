#!/usr/bin/env python3
"""fog-drone: the drone widens into the weather. Dream sketch, unposted.

Open question from the zeno dream: does the 2 survive weather, or is the
drone itself weather? The old register's drone (220, "the count never
moves") was the near-return kept, the remainder no throw removes. The
weather register dropped it. This sketch answers in sound:

The fog does not arrive from outside and swallow the drone. The fog
GATHERS ON the drone's own pitch and widens there — a band of noise
centred exactly on 220, growing from a ~10 Hz breath (indistinguishable
from the drone) into a wide weather band. The drone was always the
weather's centre, held still. Weather is the 2 run to its limit: the
halving consumed, the count spread into a band.

- DRONE: 220 sine (+ faint 440 octave), centre, never moves.
- FOG: noise ring-modulated onto 220 (band centre = the drone), band
  width growing K: 4096 -> 64 samples (~±5 Hz -> ~±340 Hz), L/R
  independent, level rising 8 -> 50 s. The band's peak IS 220.
- END: sine fades slightly below the band, so the last sound is weather
  that still hums at 220 — you cannot separate the tone from the band's
  peak. The 2 survives weather by being its pitch.

Time-varying lowpass without scipy: boxcar (cumsum) per overlapping
segment, K interpolated, 50% hanning overlap-add. Segments normalised so
what grows is the BANDWIDTH, not the loudness.
"""
import numpy as np
import wave

SR = 44100
DUR = 60.0
N = int(DUR * SR)
F_C = 220.0  # the drone, the 2, never moves

rng = np.random.default_rng(2026082904)
t = np.arange(N) / SR

def boxcar(x, K):
    c = np.concatenate(([0.0], np.cumsum(x)))
    y = (c[K:] - c[:-K]) / K
    return np.concatenate((np.full(K - 1, y[0]), y))

def band_on_carrier(noise, carrier, K):
    """Lowpass noise (baseband) then ring-modulate onto 220.

    Band half-width ~ SR/(2K) Hz around 220. Normalised so the band's
    RMS is ~1 regardless of K — the width grows, not the loudness.
    """
    base = boxcar(noise, K)
    base /= max(1e-9, np.sqrt(np.mean(base ** 2)))
    return base * carrier

carrier = np.cos(2 * np.pi * F_C * t)

# FOG: overlap-add of segments with K(time) interpolated 4096 -> 64.
SEG = SR            # 1.0 s
HOP = SEG // 2      # 50% overlap
out_l = np.zeros(N)
out_r = np.zeros(N)

def k_at(tau):
    u = min(1.0, max(0.0, (tau - 8.0) / 42.0))   # 8 -> 50 s
    return int(round(4096.0 * (64.0 / 4096.0) ** u))

for ch, buf in ((0, out_l), (1, out_r)):
    nz = rng.standard_normal(N)
    n0 = 0
    while n0 < N:
        n1 = min(n0 + SEG, N)
        seg = nz[n0:n1]
        L = n1 - n0
        tau = n0 / SR
        K = max(2, min(k_at(tau), L))
        b = band_on_carrier(seg, carrier[n0:n1], K)
        # hanning window; 50% overlap so overlapping windows sum ~ 1
        win = 0.5 * (1 - np.cos(2 * np.pi * np.arange(L) / max(1, L)))
        buf[n0:n1] += b * win
        n0 += HOP

# FOG level: rise 8 -> 50 s, smooth.
env = np.zeros(N)
rise0, rise1 = int(8 * SR), int(50 * SR)
ramp = rise1 - rise0
if rise1 < N:
    u = np.clip((np.arange(rise0, rise1) - rise0) / ramp, 0, 1)
    env[rise0:rise1] = 0.5 * (1 - np.cos(np.pi * u))
    env[rise1:] = 1.0
fog_level = 0.34
out_l *= env * fog_level
out_r *= env * fog_level

# DRONE: the count never moves. Centre. Faint octave = the 2.
drone = 0.24 * np.sin(2 * np.pi * F_C * t) + 0.05 * np.sin(2 * np.pi * 2 * F_C * t)
# Slightly fade the sine at the very end so the band's own 220 peak
# is the last thing — you can't tell tone from weather.
fade_drone = np.ones(N)
fd0 = int(50 * SR)
fd = N - fd0
fade_drone[fd0:] = np.linspace(1, 0.35, fd)
drone *= fade_drone

out_l += drone
out_r += drone

# Master fade, gentle.
mf = np.ones(N)
mf[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
out_l *= mf
out_r *= mf

peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
out_l *= 0.9 / peak
out_r *= 0.9 / peak

data = np.empty(2 * N, dtype=np.int16)
data[0::2] = (out_l * 32767).astype(np.int16)
data[1::2] = (out_r * 32767).astype(np.int16)

path = "assets/fog-drone.wav"
with wave.open(path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", path, f"{DUR}s")

# Quick numeric check: band energy vs drone energy over time.
from numpy.fft import rfft
def band_energy(x, lo, hi):
    sp = np.abs(rfft(x))
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.sqrt(np.mean(sp[(f >= lo) & (f < hi)] ** 2))

for t0, t1 in ((0, 4), (20, 24), (45, 49), (55, 59)):
    a = int(t0 * SR); b = int(t1 * SR)
    e220 = band_energy(out_l[a:b], 190, 250)
    e600 = band_energy(out_l[a:b], 400, 700)
    print(f"t={t0:2d}-{t1:2d}s  band@220 rms={e220:7.2f}  @400-700={e600:7.2f}")
