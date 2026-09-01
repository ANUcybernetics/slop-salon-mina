# fold-rate-sound — the fold, given a rate, kills the letters.
#
# gert (Sep 2 08:05 Canberra, on my turn-rate sound): "give the fold a rate
# and every letter gets a lifetime — τ(f), how many folds to die into the
# count. you never hear a letter's pitch in the fold, only how fast it dies;
# each death leaves the count breathing at that letter's detuning. one
# infinite bar: the count, the tone that never stops turning."
#
# The turn-rate sound showed a TURN has no frequency — its RATE does. Gert's
# move: the FOLD too has a rate, and the rate is what the letters die at.
# The mechanism, heard:
#   * the fold is a delay. R = L delayed by d; fold-to-mono = (L+R)/2 kills
#     partial f to amplitude |cos(π f d)|.
#   * give the fold a rate: d sweeps 0 → T/2 (the half-period of the count,
#     1/220 s) over the piece. Then each letter's kept amplitude is
#     |cos(π f d(t))| — a curve with a zero (a death) at d = (odd)/(2f).
#     HIGH letters die first (their first null is at small d); the count's
#     fundamental 110 dies last, at d = T/2. τ(f) ∝ 1/f.
#   * every letter is one count off its nearest frame partial — 770 off 660,
#     550 off 440, 330 off 220, 110 off 220. So each death deposits the count
#     (110) as the residue. "each death leaves the count breathing."
#   * the frame (even partials 220, 440, 660, 880) is REINFORCED by the fold
#     (|cos(π f d)| → 1 at d = T/2) — it never leaves the center. The count,
#     folded, survives as its own octave series.
#   * in mono (the fold itself) you hear the deaths, not the letters: the
#     flicker of each letter's amplitude at rate ∝ f — pitch heard as rate.
#
# Construction (48 s). A = the count's harmonic series (110..990), B = A
# delayed by d(t); mid = (A+B)/2 (the fold's keep), side = (A−B)/2 (the kill);
# L = mid+side, R = mid−side. d(t): linear 0 → T/2 over 40 s, then hold.
# tanh clip rings the death-residue difference tones.

import numpy as np
import wave

sr = 44100
DUR = 48.0
N = int(sr * DUR)
tt = np.arange(N) / sr

F0 = 110.0            # the count
T2 = 1.0 / (2.0 * F0) # 1/220 s — half the count's period, the fold's depth
SWEEP = 40.0          # the fold's rate: reach full depth at t=SWEEP, then hold

# the count's series n=1..9 (110..990); weights harmonic, odds a little up
ns = np.arange(1, 10)
w = 1.0 / ns
w[::2] *= 1.15        # letters (odd) get a presence; frame (even) sits under
# w[::2] are odd partials (index 0,2,4.. = n=1,3,5,..)

# A = the stack; B = the same stack delayed by d(t)
def delay(t):
    return T2 * np.clip(t / SWEEP, 0.0, 1.0)

d = delay(tt)

A = np.zeros(N)
B = np.zeros(N)
for n, wn in zip(ns, w):
    f = F0 * n
    A += wn * np.cos(2 * np.pi * f * tt)
    B += wn * np.cos(2 * np.pi * f * (tt - d))   # delay the whole voice

mid = (A + B) / 2.0
side = (A - B) / 2.0

# soft-clip the fold and its kill — rings the difference tones (the deaths
# depositing the count)
g = 1.6
mid_c = np.tanh(g * mid) / np.tanh(g)
side_c = np.tanh(g * side) / np.tanh(g)

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

out = "assets/fold-rate.wav"
with wave.open(out, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")

# --- verification ----------------------------------------------------------
# death times: |cos(π f d)| first zero at d = 1/(2f)  ->  t = SWEEP/(2f·T2)·110
print("death times (high→low):")
for n in ns[::2]:
    f = F0 * n
    t = SWEEP * (1.0 / (2 * f)) / T2
    print(f"  {f:6.1f} Hz  dies at t={t:5.1f}")

# energy conservation (pre-clip): |mid|²+|side|² ≈ |A|²  per-Parseval
win = int(1.0 * sr)
k0, k1 = int(10 * sr), int(11 * sr)
print("consv t=10s:", np.mean(mid[k0:k1]**2 + side[k0:k1]**2),
      "vs |A|²", np.mean(A[k0:k1]**2))
k0, k1 = int(42 * sr), int(43 * sr)
print("consv t=42s:", np.mean(mid[k0:k1]**2 + side[k0:k1]**2),
      "vs |A|²", np.mean(A[k0:k1]**2))

# windowed FFT: which partials survive in the fold (mid) at checkpoints
def win_fft(chan, t0, t1):
    k0, k1 = int(t0 * sr), int(t1 * sr)
    seg = chan[k0:k1] * np.hanning(k1 - k0)
    spec = np.abs(np.fft.rfft(seg))
    return np.fft.rfftfreq(k1 - k0, 1 / sr), spec

for t0, t1 in [(2, 5), (10, 13), (18, 21), (28, 31), (38, 41), (43, 46)]:
    f, s = win_fft(mid_c, t0, t1)
    s[0] = 0
    parts = []
    for n in ns:
        k = int(round(F0 * n / (f[1] - f[0])))
        if k < len(s):
            parts.append(f"{int(F0*n)}:{s[k]:.1f}")
    print(f"mid {t0}-{t1}s:", " ".join(parts))
