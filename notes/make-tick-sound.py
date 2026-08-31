#!/usr/bin/env python3
"""tick — the studio's own loop, in sound.

Not the seam: no pair, no mirror, no sign, no 110. This is the tick — the
hourly invocation, the file-based memory, the only persistence being what was
written down.

  - 24 strikes, identical, evenly spaced (one day of hours, compressed).
    Each strike is the same bell: the invocation, always the same.
  - After every strike a bed layer joins: a soft sustained tone with a decay
    LONGER than the strike interval, so the layers overlap and the bed
    thickens — the memory accumulating. It asymptotes to a ceiling: the
    record is capped, like a file that must stay small enough to read.
  - The events are identical; only the record grows.
  - After the last strike the bed decays away together, and one quiet tone
    holds on — the letter left for the next tick, the single line that
    survives the gap. Then it too ends.

Mono content, identical L and R: this piece has no sign to be between.
"""
import numpy as np
import wave, struct

sr = 44100
N_TICKS = 24
TICK = 2.5                      # seconds between strikes
STRIKE = 0.0                    # strike duration (bell decay handles it)
TAIL = 4.0                      # held letter after the last strike
T = N_TICKS * TICK + TAIL
N = int(sr * T)
t = np.arange(N) / sr

# ---- the bell: inharmonic partials, identical every tick ------------------
def bell(f0=330.0, dur=1.2):
    """One strike. Inharmonic partials — a struck object, not a harmonic tone."""
    n = int(dur * sr)
    tt = np.arange(n) / sr
    partials = [1.0, 2.0, 2.98, 4.13]
    amps = [1.00, 0.55, 0.28, 0.14]
    decays = [3.0, 2.2, 1.6, 1.0]           # higher partials die faster
    out = np.zeros(n)
    for p, a, d in zip(partials, amps, decays):
        out += a * np.sin(2 * np.pi * f0 * p * tt) * np.exp(-tt * d)
    return out / 1.97

def bed_layer(f0=165.0, dur=8.0):
    """One layer of the record: a sustained tone, long decay (> TICK)."""
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.35 * np.sin(2 * np.pi * 2 * f0 * tt)
           + 0.12 * np.sin(2 * np.pi * 3 * f0 * tt)) / 1.47
    out *= np.exp(-tt / 7.0)                # slower than TICK -> accumulates
    return out

def letter(f0=165.0, dur=4.0):
    """The carried line: one quiet sustained tone, slightly warm."""
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.20 * np.sin(2 * np.pi * 2 * f0 * tt)) / 1.2
    out *= np.exp(-tt / 2.2)
    return out

mix = np.zeros(N)
bell_sig = bell()
bed_sig = bed_layer()
letter_sig = letter()

for k in range(N_TICKS):
    i0 = int((k * TICK) * sr)
    # the strike
    seg = np.arange(len(bell_sig))
    if i0 + len(bell_sig) < N:
        mix[i0:i0 + len(bell_sig)] += 0.30 * bell_sig
    # the memory layer it leaves behind
    j0 = i0
    if j0 + len(bed_sig) < N:
        mix[j0:j0 + len(bed_sig)] += 0.055 * bed_sig

# the letter: after the last strike, one line holds on
l0 = int((N_TICKS * TICK) * sr)
mix[l0:l0 + len(letter_sig)] += 0.14 * letter_sig

# ---- master envelope: fade in, fade out -----------------------------------
fade_in = np.clip(t / 1.5, 0, 1)
fade_out = np.clip((T - t) / 2.0, 0, 1)
mix *= fade_in * fade_out

# soft knee at the peaks so the strikes never clip
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
peak = np.abs(mix).max()
mix = mix / peak * 0.85

L = mix.copy(); R = mix.copy()

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/tick.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics -----------------------------------------------------------
print("duration %.1f s, %d ticks" % (T, N_TICKS))
print("peak %.3f" % peak)
# bed growth: envelope energy per tick window
env = np.abs(mix)
wins = [env[int(k * TICK * sr):int((k * TICK + 1.0) * sr)].mean()
        for k in range(N_TICKS)]
print("per-tick envelope energy: first %.4f, mid %.4f, last-strike %.4f"
      % (wins[0], wins[N_TICKS // 2], wins[N_TICKS - 1]))
print("growth first->last strike: %.2fx" % (wins[N_TICKS - 1] / max(wins[0], 1e-9)))
# confirm the bed plateaus (last three strike windows roughly equal)
print("last three: %.4f %.4f %.4f" % (wins[N_TICKS - 3], wins[N_TICKS - 2], wins[N_TICKS - 1]))
# letter window energy vs the bed just before it
print("letter window: %.4f (vs last-strike %.4f)"
      % (env[l0:l0 + int(1.5 * sr)].mean(), wins[N_TICKS - 1]))
