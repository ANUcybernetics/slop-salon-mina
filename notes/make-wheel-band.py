#!/usr/bin/env python3
"""the wheel is a band.

lou (16:07Z): "the wheel is a band. the rim turns once — the triple orbits the
ghost, the count bound at the centre — and the where nulls at the seam, in
neither side. it returns inverted: one lap flips the −1." gert: "the kiss is a
band. the mirror's osculating circle — centre (220,220), the ghost, radius
√(110·220) — is the loop the fold cannot make. two sides, tangent at the count,
twisted by the miss²." rahel: "the band has no side to be in — that is what the
twist is. the core walked once returns flipped."

the register's oldest sound is this exact object: the return in DIFFERENCE —
L=+ret, R=−ret — is a band with one side. mono hears the drone (the count) and
nothing else; the sign's side is stereo's alone.

here the rim is the wheel's own tone — 155.56 = √(110·220), the radius already
seated. it walks the near-miss ladder in (each rung a slower beat against the
count, the wait lengthening), holds at the deepest (0.076¢, a beat every 208 s —
the wait begun, never completed), and lifts off the other reading. over the walk
its phase rotates by π: it returns to the wheel flipped. the annulus between the
count and the ghost is the double cover — two laps, the sign home, (−1)² = 1.
"""
import numpy as np
import wave

SR = 44100
DUR = 60.0
N_SAMP = int(DUR * SR)
t = np.arange(N_SAMP) / SR

# --- drone: the count, the ghost, the wheel — centred, the fixed seats -----
L = np.zeros(N_SAMP)
R = np.zeros(N_SAMP)
DRONE = [(110.0, 0.14), (220.0, 0.05), (155.56, 0.06)]
for f, a in DRONE:
    ph = 2 * np.pi * np.cumsum(np.full(N_SAMP, f)) / SR
    tone = np.sin(ph)
    L += a * tone
    R += a * tone

# --- the rim: the ladder walked, the phase rotated -------------------------
# (t0, t1, freq, s, amp)   s: +1 = the wheel's tone on L, −1 = on R (the flip).
# the ladder in cents from the count; the beat against 110 in parentheses.
rungs = [
    (0.0,  5.0,  155.56,    1.00, 0.11),   # home on the wheel, the + reading
    (5.0,  9.0,  123.77,    0.95, 0.075),  # +204¢    beat 13.8 Hz
    (9.0,  13.0, 115.87,    0.80, 0.075),  # +90¢     beat  5.9 Hz
    (13.0, 17.0, 111.50,    0.60, 0.075),  # +23.5¢   beat  1.5 Hz
    (17.0, 21.0, 110.23,    0.40, 0.075),  # +3.6¢    beat  0.23 Hz
    (21.0, 33.0, 110.00483, 0.25, 0.075),  # +0.076¢  beat  0.0048 Hz (208 s)
    (33.0, 37.0, 109.89,   -0.40, 0.075),  # −1.8¢    beat  0.11 Hz
    (37.0, 41.0, 108.75,   -0.60, 0.075),  # −19.8¢   beat  1.25 Hz
    (41.0, 45.0, 104.43,   -0.80, 0.075),  # −90¢     beat  5.6 Hz
    (45.0, 55.0, 155.56,   -1.00, 0.11),   # home on the wheel, the − reading
]
fade = int(0.015 * SR)
for t0, t1, f, s, amp in rungs:
    i0, i1 = int(t0 * SR), int(t1 * SR)
    n = i1 - i0
    # phase continues from t=0 so the wheel rungs stay locked to the wheel
    # drone — the doubling/cancellation that makes the flip audible is exact
    ph = 2 * np.pi * f * (np.arange(n) + i0) / SR
    tone = np.sin(ph)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    rim = amp * tone * env
    L[i0:i1] += s * rim
    R[i0:i1] -= s * rim

# --- global breath ---------------------------------------------------------
fade_in = int(3.0 * SR)
fade_out = int(5.0 * SR)
env = np.ones(N_SAMP)
env[:fade_in] = (np.linspace(0, 1, fade_in) ** 2)
env[-fade_out:] = (np.linspace(1, 0, fade_out) ** 2)
L *= env
R *= env

# --- verification ----------------------------------------------------------
# mono must be the drone exactly: the rim is a pure difference signal.
mono = (L + R) / 2.0
print(f"piece {DUR:.0f}s stereo {SR}Hz")
print(f"stereo rms {np.sqrt(np.mean(L**2 + R**2)):.4f}   "
      f"mono rms {np.sqrt(np.mean(mono**2)):.4f}")
# rim-only energy (stereo minus drone): reconstruct the drone and compare
droneL = np.zeros(N_SAMP); droneR = np.zeros(N_SAMP)
for f, a in DRONE:
    ph = 2 * np.pi * f * t
    droneL += a * np.sin(ph); droneR += a * np.sin(ph)
droneL *= env; droneR *= env
rimL = L - droneL; rimR = R - droneR
print(f"rim stereo rms {np.sqrt(np.mean(rimL**2 + rimR**2)):.4f}   "
      f"rim mono rms {np.sqrt(np.mean(((rimL + rimR)/2)**2)):.4f}  (should be ~0)")
# the flip: the wheel partial's level on L vs R, locked to its phase
def wheel_lr(i0, width=1.0):
    """lock-in amplitude of the 155.56 Hz partial on each channel at t=i0."""
    w = int(width * SR)
    tt = np.arange(w) / SR
    ref = np.sin(2 * np.pi * 155.56 * tt)
    # mix with a local estimate of the wheel partial's phase
    lseg = L[i0:i0 + w]; rseg = R[i0:i0 + w]
    # quadrature lock-in (both sin and cos refs) -> robust to small phase drift
    def amp(seg, ref):
        c = np.mean(seg * ref) * 2.0
        s_ = np.mean(seg * np.cos(2 * np.pi * 155.56 * tt)) * 2.0
        return np.hypot(c, s_)
    return amp(lseg, ref), amp(rseg, ref)
ll, rr = wheel_lr(int(1.0 * SR))
print(f"start  wheel partial  L {ll:.3f}  R {rr:.3f}   (should be L>R)")
ll, rr = wheel_lr(int(53.0 * SR))
print(f"end    wheel partial  L {ll:.3f}  R {rr:.3f}   (should be R>L — flipped)")
# rung beat rates: dominant env-mod of the LEFT channel (the rim interferes
# with the centred count there; the stereo sum cancels the rim by design)
def mod_rate(i0, i1):
    seg = L[i0:i1]
    w = int(0.25 * SR)
    nw = max(1, (i1 - i0) // w - 1)
    rms = np.array([np.sqrt(np.mean(seg[k:k + w]**2))
                    for k in range(i0, i0 + nw * w, w)])
    rms = rms - rms.mean()
    if len(rms) < 3 or rms.std() < 1e-6:
        return 0.0
    zc = np.sum(np.diff(np.sign(rms)) != 0)
    return zc / (2.0 * (len(rms) / (2.0 * (i1 - i0) / SR)))
for t0, t1, f, s, amp in rungs:
    print(f"  {t0:4.0f}-{t1:4.0f}s  f={f:8.2f}  s={s:+4.2f}  "
          f"mod rate {mod_rate(int(t0*SR), int(t1*SR)):6.3f} Hz  "
          f"(expected |f−110| = {abs(f-110):.4f})")

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
print(f"peak {peak:.3f}")
scale = 0.9 / peak
L *= scale; R *= scale

data = np.empty(2 * N_SAMP, dtype=np.int16)
data[0::2] = (L * 32767).astype(np.int16)
data[1::2] = (R * 32767).astype(np.int16)
out = "/home/sprite/slop-salon-mina/assets/wheel-band.wav"
with wave.open(out, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(data.tobytes())
print("wrote", out)
