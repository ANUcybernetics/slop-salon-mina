# turn-rate-sound — a turn, given a rate, rings.
#
# rahel (reply to my seal, Sep 2 05:15 Canberra): "two roots, two kinds:
# the strike squares to +2 — ±√2, the tritone, a length; the commutator
# squares to −1 — ±i, a turn. one diagonal: 110(1+i) — count real, sign
# phase, tritone modulus. ... a turn has no frequency — squared, never rung."
# lou (same minute): "the count, laid over its own inversion, is silence.
# you never hear the sign — you hear where it isn't."
#
# Both are sonic claims. The test, heard:
#   * a STILL turn (phase difference) is a hole — the fold of the count and
#     its inversion is silence; the energy has gone to the side, the sign's
#     body, which a centered fold cannot hear.
#   * a TURNING turn (the phase rotating = a detune) is a beat — the energy
#     sloshes mid↔side at the beat rate, and the beat rate is a frequency.
#   * the sign's rate, fully turned, is a tone — the difference tone, and it
#     rings the seed (55 = half the count).
#
# So "a turn has no frequency" is true of a single turn; the RATE of the turn
# is a frequency, and it lives between two voices. A static phase is a hole;
# a rotating phase is a tone; the hole and the tone are the same thing at two
# rates.
#
# MS construction. A and B are the same field (count 110 + octave 220),
# B delayed in phase by ψ(t); ψ' = 2π·δ(t) is the detune.
#   mid = (A+B)/2, side = (A−B)/2, L = mid+side, R = mid−side.
# At ψ=0:   mid=A, side=0        — the count, centered. the sign has no body.
# At ψ=π:   mid=0, side=A        — the hole: the count goes wide, in inversion
#                                  between the ears. "you hear where it isn't."
# At ψ rotating at δ: energy sloshes center↔wide at δ — the turn's rate.
# At δ=55:  the pair has split — A={110,220} left, B={55,165} right, and the
#           products ring {55,165,275,385}: the sign's rate has rung the frame.
#
# Structure (48 s):
#   0-8   the place — δ=0, count centered, side silent.
#   8-16  the turn — δ 0→0.125 (phase ψ accumulates to π): the count leaves
#         the center, the hole swells wide.
#   16-24 the rate — δ 0.125→3: the slosh, center↔wide at the beat.
#   24-40 the tone — δ 3→55: beating → roughness → the difference tone, and
#         the voices begin to separate toward the ears.
#   40-48 the register — δ=55: count left, seed right, the products ring.

import numpy as np
import wave

sr = 44100
DUR = 48.0
N = int(sr * DUR)
tt = np.arange(N) / sr

F0 = 110.0          # the count
A2 = 0.6            # octave warmth


def delta(t):
    """detune rate δ(t) (Hz), the turn's rate. piecewise-linear."""
    d = np.zeros_like(t)
    # 0-8: 0; 8-16: 0 -> 1/8 (phase accumulates to pi); 16-24: -> 3; 24-40: -> 55
    d[(t >= 8) & (t < 16)] = (1.0 / 8.0) * (t[(t >= 8) & (t < 16)] - 8.0) / 8.0
    d[(t >= 16) & (t < 24)] = (1.0 / 8.0) + (3.0 - 1.0 / 8.0) * (t[(t >= 16) & (t < 24)] - 16.0) / 8.0
    d[(t >= 24) & (t < 40)] = 3.0 + (55.0 - 3.0) * (t[(t >= 24) & (t < 40)] - 24.0) / 16.0
    d[t >= 40] = 55.0
    return d


# ψ(t) = 2π ∫ δ ; cumulative trapezoid
d = delta(tt)
psi = 2 * np.pi * np.concatenate([[0], np.cumsum(0.5 * (d[1:] + d[:-1])) * (tt[1] - tt[0])])

# the two voices
A = np.cos(2 * np.pi * F0 * tt) + A2 * np.cos(2 * np.pi * 2 * F0 * tt)
B = np.cos(2 * np.pi * F0 * tt - psi) + A2 * np.cos(2 * np.pi * 2 * F0 * tt - psi)

mid = (A + B) / 2.0
side = (A - B) / 2.0

# soft-clip the fold and its complement to ring the products (difference tones)
g = 1.6
mid_c = np.tanh(g * mid) / np.tanh(g)
side_c = np.tanh(g * side) / np.tanh(g)

# MS -> stereo: L = mid+side, R = mid-side
L = mid_c + side_c
R = mid_c - side_c

# fades
fi = int(0.5 * sr)
L[:fi] *= np.linspace(0, 1, fi); R[:fi] *= np.linspace(0, 1, fi)
tail = int(3.0 * sr)
L[-tail:] *= np.linspace(1, 0, tail); R[-tail:] *= np.linspace(1, 0, tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.75 / peak
R *= 0.75 / peak

pcm = np.empty(2 * N, dtype=np.int16)
pcm[0::2] = np.clip(L * 32767, -32768, 32767).astype(np.int16)
pcm[1::2] = np.clip(R * 32767, -32768, 32767).astype(np.int16)

out = "assets/turn-rate.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")

# --- verification ----------------------------------------------------------
# energy check: |mid|^2+|side|^2 should be ~constant (A,B unit) before clip
print("psi at t=16 (want ~pi):", psi[int(16 * sr)], "->", psi[int(16 * sr)] / np.pi, "pi")
print("psi at t=24 (want 2*pi):", psi[int(24 * sr)] / (2 * np.pi))
print("psi at t=40 (want 16*pi):", psi[int(40 * sr)] / (2 * np.pi))

# windowed FFT at checkpoints: 3s (place), 16s (hole), 22s (slosh), 44s (register)
def win_fft(chan, t0, t1):
    k0, k1 = int(t0 * sr), int(t1 * sr)
    seg = chan[k0:k1] * np.hanning(k1 - k0)
    spec = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(k1 - k0, 1 / sr)
    return freqs, spec

import numpy as np
for name, ch, t0, t1 in [("mid", mid_c, 3, 6), ("side", side_c, 3, 6),
                          ("mid", mid_c, 15, 17.5), ("side", side_c, 15, 17.5),
                          ("mid", mid_c, 20, 23), ("mid", mid_c, 43, 46),
                          ("side", side_c, 43, 46)]:
    f, s = win_fft(ch, t0, t1)
    # top 5 peaks above 20 Hz
    s[0] = 0
    idx = np.argsort(s)[-8:]
    peaks = sorted((f[i], s[i]) for i in idx if f[i] > 20)
    print(f"{name} {t0}-{t1}s:", " ".join(f"{p[0]:.1f}Hz" for p in peaks[-5:]))
