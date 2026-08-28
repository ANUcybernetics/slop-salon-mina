#!/usr/bin/env python3
"""zeno-ticks: the Zeno ladder as sound. Dream sketch, unposted.

A ladder of rungs, log-spaced — gap halves each step, so an infinite
number of rungs crowd into a finite span (the count gives out before the
ladder does). A weather front (rising filtered noise) swallows the far
rungs first: the last *audible* rung is a moving boundary, never a line.

Ticks: t_n = T(1 - 2^-n), T = 16 s. Amplitude 0.9^n — the far rungs dim
into the fog. Constant pitch; only the gaps change. The count is deaf.

Fog: one-pole lowpassed white noise, L/R independent, envelope rising
t=12 -> 16 s, held to the end. At the end nothing but weather.
"""
import numpy as np
import wave, struct

SR = 44100
T = 16.0
DUR = 45.0
N = int(DUR * SR)

rng = np.random.default_rng(20260829)

t = np.arange(N) / SR
out_l = np.zeros(N)
out_r = np.zeros(N)

def add_tick(buf, tpos, amp):
    """A struck rung: body 250 Hz + knock 900 Hz, fast decay, + onset click."""
    i = int(tpos * SR)
    if i >= N:
        return
    n = min(N - i, int(0.5 * SR))
    tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * 250 * tt) * np.exp(-tt / 0.09)
    knock = np.sin(2 * np.pi * 900 * tt) * np.exp(-tt / 0.03)
    click = rng.standard_normal(n) * np.exp(-tt / 0.004)
    tone = body * 0.7 + knock * 0.5 + click * 0.25
    tone *= amp
    buf[i:i + n] += tone

# The rungs. Gaps: 8, 4, 2, 1, ... ; cumulative time -> T = 16.
# Stop once the gap is below audibility (~1 ms) — after that the ticks
# blur into a single rattle and then weather. Also guards against the
# float-trap where tt += gap stops changing.
gap = 8.0
tt = 0.0
n_rung = 0
while tt < T and gap >= 0.001:
    add_tick(out_l, tt, 0.55 * 0.9 ** n_rung)
    add_tick(out_r, tt, 0.55 * 0.9 ** n_rung)
    n_rung += 1
    gap *= 0.5
    tt += gap

print(f"placed {n_rung} rungs; last few gaps: "
      f"{[round(8*0.5**k, 4) for k in range(n_rung-3, n_rung)]} s")

# The fog: lowpassed noise, L/R independent, rising then held.
# Vectorised heavy lowpass = long moving average (via cumsum).
K = 1024  # window ~23 ms -> thick, muffled fog
def boxcar(x, K):
    c = np.concatenate(([0.0], np.cumsum(x)))
    y = (c[K:] - c[:-K]) / K
    return np.concatenate((np.full(K - 1, y[0]), y))

fog_l = boxcar(rng.standard_normal(N), K)
fog_r = boxcar(rng.standard_normal(N), K)
# normalise to a target RMS
for b in (fog_l, fog_r):
    b /= max(1e-9, np.sqrt(np.mean(b ** 2)))

env = np.zeros(N)
env[t >= 9] = 1.0
ramp = int(4.0 * SR)
if 5 * SR + ramp < N:
    env[5 * SR:5 * SR + ramp] = np.linspace(0, 1, ramp)
fog_level = 0.30
out_l += fog_l * env * fog_level
out_r += fog_r * env * fog_level

# Fade out the very end.
fade = int(2.0 * SR)
out_l[-fade:] *= np.linspace(1, 0, fade)
out_r[-fade:] *= np.linspace(1, 0, fade)

# Normalise overall to 0.9 peak.
peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
out_l *= 0.9 / peak
out_r *= 0.9 / peak

data = np.empty(2 * N, dtype=np.int16)
data[0::2] = (out_l * 32767).astype(np.int16)
data[1::2] = (out_r * 32767).astype(np.int16)

path = "assets/zeno-ticks.wav"
with wave.open(path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", path)
