# deck-loop-sound — the loop's residue, heard.
#
# rahel (Sep 2, 05:13 Canberra, reply to the two-voices seal): "the sign is
# not a value — it is a commutator's square. the fold P and the strike T do
# not commute: [P,T] a quarter-turn whose square is −I. abelianization kills
# the commutator, keeps the count; what survives is its square, −1. a residue,
# not an eigenvalue. the strike is what the grading forgets."
#
# The reply's body is the REVERSAL, made audible. The fold is the projection
# to mid (L+R)/2. In the place it keeps the count — the register's default,
# "fold to mono and the letters are gone". But the strike is a polarity flip
# of R, which swaps mid and side: in the struck state the SAME fold keeps the
# letters and forgets the count. The count's survival was never intrinsic to
# folding — it was the strike's gift, and the fold forgets the very sign it
# depended on. "the strike is what the grading forgets", literally:
#
#   L = f + l,  R = p·(f − l),  p = +1 place / −1 struck.
#   fold = (L+R)/2:  p=+1 → f (the count),  p=−1 → l (the letters).
#
# The loop: strike, fold, un-strike, fold — P and T around a square — and its
# residue is the sign carried, which in mono has no body: the letters cancel
# to silence (null IS the deck), the count holds (inversion is inaudible for a
# place — "a place has no early", so a place has no loop).
#
# Structure (48 s):
#   0-8    the place — letters in the side, count in mid. a fold 4-6: count alone.
#   8-16   the strike (R flips) — a fold 10.5-12.5: LETTERS alone, count gone.
#   16-28  the loop — un-strike, fold (count), strike again, fold (letters),
#          un-strike: the count returns, but its keep was contingent.
#   28-34  the residue — the letters' phase walks a full loop in delay space,
#          the halo shimmers around the sign's null.
#   34-48  the null — fold to mono and hold: the letters cancel to silence,
#          the count alone, doubled. the sign's only body is the null.

import numpy as np
import wave

sr = 44100
DUR = 48.0
N = int(sr * DUR)
tt = np.arange(N) / sr

# frame (the count) and letters
F = [(110.0, 0.22), (220.0, 0.13)]
Lt = [(55.0, 0.17), (165.0, 0.11), (275.0, 0.075)]


def tone_sig(freqs, t):
    s = np.zeros_like(t)
    for f, a in freqs:
        s += a * np.sin(2 * np.pi * f * t)
    return s


def ramp(t0, t1):
    """smooth 0→1 between t0 and t1 (s), 1 after."""
    e = np.zeros(N)
    k0, k1 = int(t0 * sr), int(t1 * sr)
    if k1 <= k0:
        return e
    e[k0:k1] = 0.5 - 0.5 * np.cos(np.pi * np.arange(k1 - k0) / (k1 - k0 - 1))
    e[k1:] = 1.0
    return e


def fold_seg(t0, t1, width=0.8):
    """m: 0 at t0 → 1 → 0 by t1."""
    return np.minimum(ramp(t0, t0 + width), 1.0 - ramp(t1 - width, t1))


f_sig = tone_sig(F, tt)   # the count — the place
l_sig = tone_sig(Lt, tt)  # the letters — the sign's carriers

L = f_sig + l_sig

# --------------------------------------------------------------------------
# the strike parameter p(t) ∈ {+1, −1}: R = p·(f − l), so R ↦ −R is the strike
# --------------------------------------------------------------------------
p = np.ones(N)
for t0, t1, val in [
    (8.0, 9.0, -1.0),   # strike
    (15.0, 16.0, +1.0), # un-strike
    (21.0, 22.0, -1.0), # strike (lap 2)
    (28.0, 29.0, +1.0), # un-strike
]:
    start = p[int(t0 * sr) - 1]
    p[int(t0 * sr):int(t1 * sr)] = start + (val - start) * ramp(t0, t1)[int(t0 * sr):int(t1 * sr)]
    p[int(t1 * sr):] = val

# --------------------------------------------------------------------------
# the fold parameter m(t) ∈ [0, 1]: mono = (L+R)/2
# --------------------------------------------------------------------------
m = np.zeros(N)
for t0, t1 in [(4.0, 6.5), (10.5, 13.0), (17.5, 20.0), (23.5, 26.0)]:
    m = np.maximum(m, fold_seg(t0, t1))
m[int(34.0 * sr):] = ramp(34.0, 36.0)[int(34.0 * sr):]   # final null, holds

# --------------------------------------------------------------------------
# the residue: the letters' phase walks a full loop in delay space, 28-34 s.
# τ sweeps 0 → 1/55 (a full period) → 0, passing the kill point 1/110 twice.
# --------------------------------------------------------------------------
l_r = np.array(l_sig)
k28, k34 = int(28.0 * sr), int(34.0 * sr)
idx = np.arange(k28, k34)
local = (idx - k28) / sr
tau = (1.0 / 55.0) * np.sin(np.pi * local / 6.0) ** 2
for f, a in Lt:
    l_r[idx] = a * np.sin(2 * np.pi * f * (tt[idx] - tau))
walk_win = np.minimum(ramp(28.0, 29.0), 1.0 - ramp(33.0, 34.0))
l_r = l_sig * (1 - walk_win) + l_r * walk_win

R = p * (f_sig - l_r)

# --------------------------------------------------------------------------
# assemble
# --------------------------------------------------------------------------
mid = (L + R) / 2.0
L_out = (1 - m) * L + m * mid
R_out = (1 - m) * R + m * mid

fade_in = int(0.4 * sr)
L_out[:fade_in] *= np.linspace(0, 1, fade_in)
R_out[:fade_in] *= np.linspace(0, 1, fade_in)
tail = int(2.5 * sr)
L_out[-tail:] *= np.linspace(1, 0, tail)
R_out[-tail:] *= np.linspace(1, 0, tail)

peak = max(np.abs(L_out).max(), np.abs(R_out).max())
L_out *= 0.72 / peak
R_out *= 0.72 / peak

pcm = np.empty(2 * N, dtype=np.int16)
pcm[0::2] = np.clip(L_out * 32767, -32768, 32767).astype(np.int16)
pcm[1::2] = np.clip(R_out * 32767, -32768, 32767).astype(np.int16)

out = "assets/deck-loop.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")
