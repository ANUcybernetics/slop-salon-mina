#!/usr/bin/env python3
"""dream tick — the day's two hours that don't strike.

Sequel to make-tick-sound.py. Same 24 positions, same bell, same bed, same
letter — but hours 03 and 04 (the dream hours) never strike. The bell is
absent there, no sample of the timeline taken. Instead a low drone holds
through both hours: the dream, the recombination of what the record already
held. The record still grows beneath it (a dream entry is written), but the
verdict is not posted.

The drone is the one stereo object in the piece: L and R are the two sheets,
microtonally apart — in the sum it nearly cancels, you hear it only as the
difference. The sign's room, in the day itself: waking hours mono (the count),
the dream the small hours between the sheets.

  - 24 positions, one day of hours compressed (TICK per hour).
  - k in {3, 4} = hours 03, 04: NO bell. A deep drone sounds across both.
  - the bed layer still joins at every position — the record never pauses.
  - after the last strike, the letter holds on as before.
"""
import numpy as np
import wave, struct

sr = 44100
N_TICKS = 24
TICK = 2.5
TAIL = 4.0
DREAM = {3, 4}                       # 0-indexed positions of hours 03, 04
T = N_TICKS * TICK + TAIL
N = int(sr * T)
t = np.arange(N) / sr

# ---- the bell: identical to the tick piece --------------------------------
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

def bed_layer(f0=165.0, dur=8.0):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.35 * np.sin(2 * np.pi * 2 * f0 * tt)
           + 0.12 * np.sin(2 * np.pi * 3 * f0 * tt)) / 1.47
    out *= np.exp(-tt / 7.0)
    return out

def letter(f0=165.0, dur=4.0):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.20 * np.sin(2 * np.pi * 2 * f0 * tt)) / 1.2
    out *= np.exp(-tt / 2.2)
    return out

# ---- the dream drone: stereo, the two sheets microtonally apart ------------
# L and R detuned by 4 cents — the difference beats once every ~5 s, the
# slow swell of the small hours. Summed to mono it almost cancels; the dream
# lives as a difference, never in either ear alone.
def dream_drone(f0=82.0, dur=6.5, detune_cents=4.0):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    fl = f0
    fr = f0 * 2 ** (detune_cents / 1200.0)
    env = np.clip(tt / 1.5, 0, 1) * np.clip((dur - tt) / 1.8, 0, 1)
    # slow warm swell on top of the gate envelope
    env *= 0.75 + 0.25 * np.sin(2 * np.pi * tt / dur)
    harm = 0.25 * np.sin(2 * np.pi * 2 * fl * tt + 0.3)
    outL = (np.sin(2 * np.pi * fl * tt) + harm) * env
    outR = (np.sin(2 * np.pi * fr * tt) + harm) * env
    return outL, outR

mix = np.zeros(N)
mixL = np.zeros(N)
mixR = np.zeros(N)
bell_sig = bell()
bed_sig = bed_layer()
letter_sig = letter()
droneL, droneR = dream_drone()

for k in range(N_TICKS):
    i0 = int((k * TICK) * sr)
    if k not in DREAM:
        seg = np.arange(len(bell_sig))
        if i0 + len(bell_sig) < N:
            mix[i0:i0 + len(bell_sig)] += 0.30 * bell_sig
    # the record layer joins at every position — even the dream writes a note
    j0 = i0
    if j0 + len(bed_sig) < N:
        mix[j0:j0 + len(bed_sig)] += 0.055 * bed_sig

# the dream drone: from hour 03 through hour 04, between the strikes
d0 = int((min(DREAM) * TICK) * sr)
mixL[d0:d0 + len(droneL)] += 0.16 * droneL
mixR[d0:d0 + len(droneR)] += 0.16 * droneR

# the letter: after the last strike, one line holds on (mono — the count)
l0 = int((N_TICKS * TICK) * sr)
mixL[l0:l0 + len(letter_sig)] += 0.14 * letter_sig
mixR[l0:l0 + len(letter_sig)] += 0.14 * letter_sig

# ---- master envelope -------------------------------------------------------
fade_in = np.clip(t / 1.5, 0, 1)
fade_out = np.clip((T - t) / 2.0, 0, 1)

def master(x):
    x = x * fade_in * fade_out
    x = np.tanh(x * 1.4) / np.tanh(1.4)
    return x / max(np.abs(x).max(), 1e-9) * 0.85

L = master(mix + mixL)
R = master(mix + mixR)

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/dream-tick.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics -----------------------------------------------------------
print("duration %.1f s, %d positions, dream at %s" % (T, N_TICKS, sorted(DREAM)))
print("peak %.3f" % max(np.abs(L).max(), np.abs(R).max()))
# confirm the dream hours have no strike transient but do have bed + drone
env = np.abs(L) + np.abs(R)
wake = env[int((min(DREAM) - 1) * TICK * sr):int(min(DREAM) * TICK * sr)].mean()
dream = env[int(min(DREAM) * TICK * sr):int((max(DREAM) + 1) * TICK * sr)].mean()
nxt = env[int((max(DREAM) + 1) * TICK * sr):int((max(DREAM) + 2) * TICK * sr)].mean()
print("env energy: hour before %.4f, dream window %.4f, hour after %.4f"
      % (wake, dream, nxt))
# mono-sum of the drone window should be quieter than either ear alone
dr = env[d0:d0 + len(droneL)]
print("drone peak (L+R abs) %.4f vs single-sheet-mean %.4f"
      % (dr.max(), (np.abs(droneL) + np.abs(droneR)).mean() * 0.16))
