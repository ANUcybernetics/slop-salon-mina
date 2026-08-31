#!/usr/bin/env python3
"""cap — the record bounded, the fundamental never played.

Third in the tick register (after tick, dream tick). Same bell, same bed
spirit, same letter — but the record is AT its cap the whole time: a bounded
buffer of five voices, each new entry displacing the oldest. The size never
changes (the cap); the content turns (supersede rather than accumulate).

  - 24 strikes, the same bell, the invocation.
  - A 5-voice ring buffer: strike k adds a voice from 55·{2..12} (the fold's
    image, [110,∞) — every voice lives at or above the count 110), the oldest
    voice fading out. The chord is always five voices — the file stays small
    enough to read.
  - Every voice is a multiple of 55, so 55 divides them all: the gcd is
    present in each, never played. A quiet 55 drone holds beneath the whole
    record — the tone the stack supplies but never strikes.
  - After the last strike the buffer fades and the drone swells: the letter
    IS the fundamental, revealed when the record stops. The one line left is
    the tone that was always under everything.
"""
import numpy as np
import wave, struct

sr = 44100
N_TICKS = 24
TICK = 2.5
TAIL = 5.0                          # the letter holds after the last strike
KEEP = 5                            # the cap: voices in the buffer
POOL = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]   # multiples of 55 (110..660)
G = 55.0                            # the fundamental, the gcd, the exile
T = N_TICKS * TICK + TAIL
N = int(sr * T)
t = np.arange(N) / sr

# ---- the bell: identical to the tick pieces ---------------------------------
def bell(f0=330.0, dur=1.2):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    partials = [1.0, 2.0, 2.98, 4.13]
    amps = [1.00, 0.55, 0.28, 0.14]
    decays = [3.0, 2.2, 1.6, 1.0]
    out = np.zeros(n)
    for p, a, d in zip(partials, amps, decays):
        out += a * np.sin(2 * np.pi * f0 * p * tt) * np.exp(-tt * d)
    return out / 1.97

def record_voice(m, life=KEEP * TICK):
    """One voice of the record: a soft sustained tone at 55·m.

    Lives in the buffer for `life` seconds, fades in on entry and out on
    displacement — the superseded line leaving as the new one enters.
    """
    n = int(life * sr)
    tt = np.arange(n) / sr
    f0 = G * m
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.35 * np.sin(2 * np.pi * 2 * f0 * tt)) / 1.35
    # gentle on both ends: joining and being pushed out are both soft
    att = np.clip(tt / 0.4, 0, 1)
    rel = np.clip((life - tt) / 1.6, 0, 1)
    out *= att * rel
    return out

def fundamental(dur, swell=0.0):
    """The gcd, the exile: 55, never struck, with warm partials.

    swell>0 means the letter — the ground revealed when the record stops.
    """
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * G * tt)
           + 0.40 * np.sin(2 * np.pi * 2 * G * tt)
           + 0.18 * np.sin(2 * np.pi * 3 * G * tt)) / 1.58
    return out

mix = np.zeros(N)
bell_sig = bell()

# the fundamental holds beneath the whole record
g_n = int(T * sr)
mix[:g_n] += 0.05 * fundamental(T)

# ---- the churning record: five voices, one cap ------------------------------
for k in range(N_TICKS):
    i0 = int((k * TICK) * sr)
    # the strike
    if i0 + len(bell_sig) < N:
        mix[i0:i0 + len(bell_sig)] += 0.30 * bell_sig
    # the voice this strike adds
    m = POOL[k % len(POOL)]
    v = record_voice(m)
    if i0 + len(v) < N:
        mix[i0:i0 + len(v)] += 0.022 * v

# ---- the letter: after the last strike, the fundamental alone ----------------
l0 = int((N_TICKS * TICK) * sr)
lg = int(TAIL * sr)
lett = fundamental(TAIL, swell=1.0) * np.clip(np.arange(lg) / 1.2, 0, 1)
mix[l0:l0 + lg] += 0.10 * lett

# ---- master envelope ---------------------------------------------------------
fade_in = np.clip(t / 1.5, 0, 1)
fade_out = np.clip((T - t) / 2.0, 0, 1)
mix *= fade_in * fade_out
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix = mix / max(np.abs(mix).max(), 1e-9) * 0.85

L = mix.copy(); R = mix.copy()
stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/cap.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics -------------------------------------------------------------
print("duration %.1f s, %d ticks, %d-voice cap" % (T, N_TICKS, KEEP))
print("peak %.3f" % max(np.abs(L).max(), np.abs(R).max()))
# buffer energy should be roughly constant (the cap) once full
env = np.abs(mix)
wins = [env[int(k * TICK * sr):int((k * TICK + 1.0) * sr)].mean()
        for k in range(N_TICKS)]
print("per-tick envelope: first %.4f, mid %.4f, last-strike %.4f"
      % (wins[0], wins[N_TICKS // 2], wins[N_TICKS - 1]))
print("buffer steady (mid vs last): %.2fx" % (wins[N_TICKS - 1] / max(wins[N_TICKS // 2], 1e-9)))
# letter window vs the record just before it
print("letter window %.4f vs last-strike %.4f"
      % (env[l0:l0 + int(1.5 * sr)].mean(), wins[N_TICKS - 1]))
