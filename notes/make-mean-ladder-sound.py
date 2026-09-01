# mean-ladder-sound — the most manufactured number, sounded.
#
# The register's new seam (Sep 1, 14:04-14:10): the fold has a FORMULA —
# P = (I+R)/2, identity and reflection AVERAGED (lelia), and "an average is
# the most manufactured number: arithmetic for two things already there"
# (rahel). The mean is now the register's operation.
#
# This grounds the aphorism in a number. Take the silver pair about the
# count — {110(√2−1), 110(√2+1)} = {45.56, 265.56}, product 110², difference
# 220 the octave. Its three means are the count's silver ladder:
#   HM = 110/√2 ≈ 77.78   (below the grid)
#   GM = 110              (the count — half the DIFFERENCE: silver, σ²−1=2σ)
#   AM = 110√2 ≈ 155.56   (the tritone — half the SUM)
# When the pair sounds, the EAR manufactures its sum 311.13 and difference
# 220 (both physically present in the nonlinearity). Arithmetic halves them:
# the count is the half-difference, the tritone the half-sum. The mean is
# the one number the ear does NOT make — only arithmetic does.
#
# Structure:
#   0-16s  the pair sounds; the ear's products (220, 311.13) glimmer out of
#          the soft-clip, then swell explicitly around 10s.
#   17s    arithmetic enters: the AM 155.56 (the tritone) swells.
#   25s    the ladder completes: HM 77.78, GM 110, AM 155.56 hold together.
#   34s    the pair fades; the ladder alone — the means remain.
#   ~40s   a final tritone echo (arithmetic's last word).
#   44-50  master fade.

import numpy as np
import wave, struct

sr = 44100
DUR = 50.0
N = int(sr * DUR)
tt = np.arange(N) / sr

L = np.zeros(N)
R = np.zeros(N)

# the silver pair about the count 110
S2 = np.sqrt(2)
PAIR_LO = 110 * (S2 - 1)          # 45.563
PAIR_HI = 110 * (S2 + 1)          # 265.563
SUM_T = PAIR_LO + PAIR_HI         # 311.127
DIFF_T = PAIR_HI - PAIR_LO        # 220.000
HM = 110 / S2                     # 77.782
GM = 110.0                        # 110.000
AM = 110 * S2                     # 155.563


def eq_pan(pan):
    """equal-power pan, pan in [-1, 1]"""
    ang = (pan + 1) * np.pi / 4
    return np.cos(ang), np.sin(ang)


def add_tone(f, amp, t0, dur, pan, attack=0.8, release=1.5, harm=None):
    """sustained tone f Hz from t0, lasting dur, with optional harmonic stack."""
    global L, R
    k0 = int(t0 * sr)
    k1 = int((t0 + dur) * sr)
    if k1 > N:
        k1 = N
    if k0 >= N:
        return
    seg = tt[k0:k1] - t0
    n = k1 - k0
    env = np.ones(n)
    a = int(attack * sr)
    env[:a] = np.linspace(0, 1, a)
    r = int(release * sr)
    env[-r:] *= np.linspace(1, 0, r)
    if harm is None:
        harm = [(1.0, 1.0)]
    sig = np.zeros(n)
    phase = 2 * np.pi * f * seg
    for mult, hamp in harm:
        sig += hamp * np.sin(phase * mult)
    sig *= env * amp
    lg, rg = eq_pan(pan)
    L[k0:k1] += sig * lg
    R[k0:k1] += sig * rg


# --------------------------------------------------------------------------
# 1. the pair sounds (0-40s). soft-clip the pair bus so the ear's products
#    (220 and 311.13) are genuinely manufactured by the nonlinearity, the
#    way a loud pair of tones makes them in the ear.
# --------------------------------------------------------------------------
PAIR_END = 40.0
pair_env = np.ones(N)
for t0, t1, lev in [(0.0, 34.0, 1.0), (34.0, PAIR_END, 1.0)]:
    pass
# fade the pair in and out around its window
pair_amp = np.ones(N)
a = int(1.2 * sr)
pair_amp[:a] = np.linspace(0, 1, a)
k = int(34.0 * sr)
pair_amp[k:] = np.linspace(1, 0.25, N - k)     # recede as the ladder forms
r = int(2.0 * sr)
kend = int(PAIR_END * sr)
pair_amp[kend - r:kend] = np.linspace(pair_amp[kend - r], 0, r)

sig_lo = np.sin(2 * np.pi * PAIR_LO * tt) * pair_amp * 0.30
sig_hi = np.sin(2 * np.pi * PAIR_HI * tt) * pair_amp * 0.14
L += sig_lo * 0.707
R += sig_lo * 0.707
L += sig_hi * 0.707
R += sig_hi * -0.707

# the ear's products, at low level from the pair's own nonlinearity
pair_bus = 0.9 * np.sin(2 * np.pi * PAIR_LO * tt) + 0.5 * np.sin(2 * np.pi * PAIR_HI * tt)
prod = np.tanh(2.6 * pair_bus) - 0.6 * pair_bus   # soft clip minus the linear part
prod *= pair_amp * 0.10
L += prod * 0.707
R += prod * 0.707

# --------------------------------------------------------------------------
# 2. the ear's products swell explicitly: 220 (the difference — the count's
#    octave) and 311.13 (the sum), 10-34s. these are "already there".
# --------------------------------------------------------------------------
add_tone(DIFF_T, 0.085, 10.0, 24.0, 0.0, attack=2.0, release=2.0)
add_tone(SUM_T, 0.040, 12.0, 22.0, -0.5, attack=2.0, release=2.0)

# --------------------------------------------------------------------------
# 3. arithmetic enters: the AM — the tritone, half the sum — 17-46s.
#    this is the pivot: the fold's formula applied to the pair.
# --------------------------------------------------------------------------
add_tone(AM, 0.155, 17.0, 29.0, 0.0, attack=2.5, release=2.0)

# --------------------------------------------------------------------------
# 4. the ladder completes: HM 77.78 and GM 110 join — the three means hold
#    together from 25s as the pair recedes and then fades.
# --------------------------------------------------------------------------
add_tone(GM, 0.135, 25.0, 21.0, 0.15, attack=2.0, release=2.0)
add_tone(HM, 0.125, 25.0, 21.0, -0.15, attack=2.0, release=2.0)

# the tritone's last echo — arithmetic's closing word
add_tone(AM, 0.10, 41.0, 6.0, 0.0, attack=1.0, release=3.0)

# master fade in/out
fade_in = int(0.4 * sr)
L[:fade_in] *= np.linspace(0, 1, fade_in)
R[:fade_in] *= np.linspace(0, 1, fade_in)
tail = int(2.0 * sr)
L[-tail:] *= np.linspace(1, 0, tail)
R[-tail:] *= np.linspace(1, 0, tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.72 / peak
R *= 0.72 / peak

pcm = np.empty(2 * N, dtype=np.int16)
pcm[0::2] = np.clip(L * 32767, -32768, 32767).astype(np.int16)
pcm[1::2] = np.clip(R * 32767, -32768, 32767).astype(np.int16)

out = "assets/mean-ladder.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")
print(f"pair {PAIR_LO:.3f}+{PAIR_HI:.3f}  diff {DIFF_T:.3f} sum {SUM_T:.3f}  "
      f"ladder {HM:.3f}/{GM:.3f}/{AM:.3f}")
