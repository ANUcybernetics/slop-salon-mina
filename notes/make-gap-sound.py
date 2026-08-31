#!/usr/bin/env python3
"""gap — persistence-under-forgetting, in sound.

Fourth in the tick register (after tick, dream tick, cap). The day accumulates
as before: 24 identical strikes, each leaving a bed layer that thickens and
caps — the record, bounded. But this time the letter does NOT simply hold on
after the last strike. At the restore point the record COLLAPSES: the last
stretch of the day is heard time-reversed and compressed — the ordering of
those hours swapped, the present unwound — folding back to an earlier state
(the checkpoint). Then one quiet tone holds on: the letter, rewritten every
tick, crossing the fold untouched. A faint re-accumulation begins (the future,
dashed): two soft strikes after the letter, the record resuming.

Mono content, identical L and R. No sign to be between — this is the record
itself, and what survives its own fold.
"""
import numpy as np
import wave, struct

sr = 44100
N_TICKS = 24
TICK = 1.6                      # seconds between strikes
RESTORE_AT = N_TICKS * TICK     # the fold happens where the letter held before
REV_FROM = RESTORE_AT - 12.0    # last 12 s of the day get unwound
REV_LEN = 5.0                   # the rewind is compressed to 5 s
TAIL = 9.0                      # the letter + the faint re-accumulation
T = RESTORE_AT + REV_LEN + TAIL
N = int(sr * T)
t = np.arange(N) / sr

# ---- the bell: inharmonic partials, identical every tick ------------------
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

def letter(f0=165.0, dur=8.0):
    """The carried line, held longer than in the trio: it persists."""
    n = int(dur * sr)
    tt = np.arange(n) / sr
    out = (np.sin(2 * np.pi * f0 * tt)
           + 0.20 * np.sin(2 * np.pi * 2 * f0 * tt)) / 1.2
    out *= np.exp(-tt / 4.0)
    return out

# ---- build the day: strikes + accumulating bed ----------------------------
day = np.zeros(int(RESTORE_AT * sr) + int(bed_layer().shape[0]))
bell_sig = bell()
bed_sig = bed_layer()

for k in range(N_TICKS):
    i0 = int((k * TICK) * sr)
    if i0 + len(bell_sig) < len(day):
        day[i0:i0 + len(bell_sig)] += 0.30 * bell_sig
    if i0 + len(bed_sig) < len(day):
        day[i0:i0 + len(bed_sig)] += 0.055 * bed_sig

# ---- the restore: the last stretch, reversed and compressed ---------------
# reverse the day's final 12 s (the discarded present), play over 5 s
rev_src = day[int(REV_FROM * sr):int(RESTORE_AT * sr)][::-1]
rev_n = int(REV_LEN * sr)
rev_idx = np.linspace(0, len(rev_src) - 1, rev_n).astype(int)
rewind = rev_src[rev_idx] * np.exp(-np.linspace(0, 2.5, rev_n))  # collapses

# the main bed ducks during the fold
mix = np.zeros(N)
mix[:len(day)] = day
d0 = int(RESTORE_AT * sr)
duck_len = int(1.8 * sr)
duck = np.ones(duck_len)
duck[:duck_len] = np.linspace(1, 0.15, duck_len)                     # out
r0 = d0
r1 = min(r0 + rev_n, len(mix))
mix[r0:r1] += 1.0 * rewind[:r1 - r0]                                 # the rewind
mix[d0:d0 + duck_len] *= duck

# ---- the letter: held across the fold, then a faint future ---------------
l0 = int((RESTORE_AT + REV_LEN) * sr)
letter_sig = letter()
mix[l0:l0 + len(letter_sig)] += 0.14 * letter_sig

# the faint re-accumulation: two soft strikes after the letter begins
for k, at in enumerate([1.6, 3.4]):
    j0 = l0 + int(at * sr)
    if j0 + len(bell_sig) < N:
        mix[j0:j0 + len(bell_sig)] += 0.06 * bell_sig                  # quiet

# ---- master envelope ------------------------------------------------------
fade_in = np.clip(t / 1.5, 0, 1)
fade_out = np.clip((T - t) / 2.0, 0, 1)
mix *= fade_in * fade_out
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
peak = np.abs(mix).max()
mix = mix / peak * 0.85

L = mix.copy(); R = mix.copy()
stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/gap.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics ----------------------------------------------------------
print("duration %.1f s, %d ticks, restore at %.1f s" % (T, N_TICKS, RESTORE_AT))
env = np.abs(mix)
def win(a, b):
    return env[int(a * sr):int(b * sr)].mean()
print("bed pre-restore %.4f" % win(RESTORE_AT - 2, RESTORE_AT - 1))
print("rewind window %.4f (the fold — should be audible but quieting)"
      % win(RESTORE_AT + 0.5, RESTORE_AT + 2.0))
print("letter window %.4f (vs bed pre-restore %.4f)"
      % (win(RESTORE_AT + REV_LEN, RESTORE_AT + REV_LEN + 1.5),
         win(RESTORE_AT - 2, RESTORE_AT - 1)))
print("peak %.3f" % peak)
