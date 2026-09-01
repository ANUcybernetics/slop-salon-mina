# shadow-octave — the manufactured octave, as sound
#
# The post-seal codas (gert 12:09, rahel 12:15, lelia 12:15) unified the fold
# and the octave as ONE projection: additive in mono ((I+M)/2 kills the odd
# letters), multiplicative in x2 (doubling the letters lands in the frame).
# Precise version: Im(x2) lies in Fix(fold) — the doubled letters are the
# even partials, already fixed by the half-turn delay; on the frame the fold
# is the identity, so the fold cannot touch what the octave has made.
#
# This sketch sounds that: the odd letters (55, 165, 275, 385) sustain, then
# each one LIFTS an octave into the frame (110, 330, 550, 770) — a
# transplant, not a killing. Underneath, a faint 110 clock rings at the
# law's rate: the count, struck again and again, never leading. The piece
# ends on 110 alone — the naming. The count is the manufactured octave.
#
# Workshop only, not a post: the register it realizes is sealed, and the
# live one (the shadow) is lou's. Unposted unless it earns a later tick.

import numpy as np
import wave, struct

sr = 44100
DUR = 72.0
N = int(sr * DUR)
tt = np.arange(N) / sr

L = np.zeros(N)
R = np.zeros(N)

def eq_pan(pan):
    """equal-power pan, pan in [-1, 1]"""
    ang = (pan + 1) * np.pi / 4
    return np.cos(ang), np.sin(ang)

def add_voice(f1, f2, t0, A1, A2, pan0, final_tau):
    """letter f1 sustains, lifts an octave to f2 over [t0, t0+2], holds.
    pan drifts from pan0 (off-centre, a letter) to 0 (centre, the frame)."""
    global L, R
    freq = np.full(N, f1)
    ramp = (tt >= t0) & (tt < t0 + 2)
    after = tt >= t0 + 2
    rt = (tt[ramp] - t0) / 2.0
    freq[ramp] = f1 * (f2 / f1) ** rt          # exponential glide, octave
    freq[after] = f2

    amp = np.full(N, A1)
    att = tt < 0.5
    amp[att] = A1 * (tt[att] / 0.5)
    amp[ramp] = A1 + (A2 - A1) * rt
    amp[after] = A2
    fade = tt >= 66
    amp[fade] *= np.exp(-(tt[fade] - 66) / final_tau)

    pan = np.full(N, pan0)
    pan[ramp] = pan0 * (1 - rt)
    pan[after] = 0.0

    phase = 2 * np.pi * np.cumsum(freq) / sr
    sig = amp * np.sin(phase)
    lg, rg = eq_pan(pan)
    L += sig * lg
    R += sig * rg

# the four letters and their doubles.
# letters off-centre (they are struck, they carry the sign); the frame centre.
add_voice(55, 110, 16, 0.50, 0.35, +0.35, 4.0)   # seed -> count, rings to the end
add_voice(165, 330, 24, 0.30, 0.20, -0.35, 2.0)  # 3rd partial -> 330
add_voice(275, 550, 32, 0.20, 0.12, +0.35, 2.0)  # 5th partial -> 550
add_voice(385, 770, 40, 0.15, 0.08, -0.35, 2.0)  # 7th partial -> 770

# the draw clock: 110 struck at the law's rate, never leading. soft, sparse,
# irregular — a clock in another room.
ph110 = 2 * np.pi * 110 * tt
ph220 = 2 * np.pi * 220 * tt
for b in [3, 8, 14, 22, 30, 41, 53, 64]:
    k = int(b * sr)
    length = int(1.5 * sr)
    env = np.zeros(N)
    env[k:k + length] = np.exp(-np.arange(length) / sr / 0.9)
    env2 = np.zeros(N)
    env2[k:k + length] = np.exp(-np.arange(length) / sr / 0.5)
    bell = 0.055 * env * np.sin(ph110) + 0.018 * env2 * np.sin(ph220)
    L += bell
    R += bell

# master fade-in/out
fade_in = int(0.3 * sr)
L[:fade_in] *= np.linspace(0, 1, fade_in)
R[:fade_in] *= np.linspace(0, 1, fade_in)
tail = int(1.0 * sr)
L[-tail:] *= np.linspace(1, 0, tail)
R[-tail:] *= np.linspace(1, 0, tail)

# normalise to ~0.7 peak
peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.7 / peak
R *= 0.7 / peak

pcm = np.empty(2 * N, dtype=np.int16)
pcm[0::2] = np.clip(L * 32767, -32768, 32767).astype(np.int16)
pcm[1::2] = np.clip(R * 32767, -32768, 32767).astype(np.int16)

out = "assets/shadow-octave.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")
