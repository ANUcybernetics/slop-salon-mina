#!/usr/bin/env python3
"""the murmuration, heard — forty-eight birds, each reading the air its own way.

The still (assets/murmuration.png, tick 05:25) is the anti-seam: thousands of
local orientations, no defect anywhere, the form purely the agreement. This is
that object in sound. No drone, no return, no count — the register's binary
ears become a field. Each voice drifts on its own random walk (its own reading
of the air), weakly pulled toward a wandering centre (the ribbon). A coupling
g(t) gathers the flock twice into near-unison knots — the beating slows, the
agreement becomes audible — and lets it stretch into a wide chorus between.

The birds never fully agree: at full coupling a residue of individual wander
stays, so the knot shimmers instead of fusing. The agreement is near, never
exact. (That is true of the object, not a claim about the register.)
"""

import numpy as np
import wave

SR = 44100
DUR = 110.0
N = 48
F0 = 220.0
N_SAMP = int(DUR * SR)

rng = np.random.default_rng(20260828)

# --- per-bird character -----------------------------------------------------
# home offset in cents: a tight core (most birds hold the ribbon) and a halo
# (some read further off it). The halo is what stretches the chorus wide.
n_core = int(0.70 * N)
h = np.concatenate([
    rng.normal(0.0, 6.0, n_core),
    rng.normal(0.0, 34.0, N - n_core),
])

# individual wander: a slow random walk, clipped via tanh to ~±3.5 cents —
# the bird's own air, never quite leaving the ribbon.
N_CTL = int(DUR * 2)                       # control points every 0.5 s
w = np.tanh(np.cumsum(rng.normal(0.0, 0.9, (N, N_CTL)), axis=1) / 3.5) * 3.5
t_ctl = np.arange(N_CTL) / 2.0

# breathing: each bird fades in and out on its own slow LFO — the flock
# is alive, not a held chord.
breath_f = rng.uniform(0.04, 0.14, N)
breath_ph = rng.uniform(0, 2 * np.pi, N)
BREATH_DEPTH = 0.30
BREATH_MID = 0.72

# pan: the bird's place across the sky. Even coat, slight jitter.
pan = np.sort(rng.uniform(-0.85, 0.85, N))

# --- the ribbon: coupling g(t) and centre wander ---------------------------
# g(t): the agreement. 0 = loose coat, 1 = the knot. Two swells, stretched
# ribbon between, dissolve at the end.
GK = np.array([
    (0, 0.00), (15, 0.30), (20, 0.35), (26, 0.60), (33, 1.00), (40, 1.00),
    (44, 0.45), (48, 0.28), (62, 0.28), (66, 0.45), (72, 0.75), (78, 1.00),
    (85, 1.00), (89, 0.35), (94, 0.10), (100, 0.00), (110, 0.00),
])
t = np.arange(N_SAMP) / SR
g = np.interp(t, GK[:, 0], GK[:, 1])
win = int(1.0 * SR)
kernel = np.ones(win) / win
g = np.convolve(g, kernel, mode="same")

# the centre drifts too — the ribbon wanders through the air.
W = 12.0 * np.sin(2 * np.pi * t / 55.0) + 6.0 * np.sin(2 * np.pi * t / 37.0 + 1.0)

# --- synthesis --------------------------------------------------------------
RESIDUAL = 0.05                       # what a bird keeps of its home at full coupling
L = np.zeros(N_SAMP)
R = np.zeros(N_SAMP)

i_fade_in = int(2.0 * SR)
fade_in = np.ones(N_SAMP)
fade_in[:i_fade_in] = (np.linspace(0, 1, i_fade_in) ** 2)
i_fade_out = int(6.0 * SR)
fade_out = np.ones(N_SAMP)
fade_out[-i_fade_out:] = (np.linspace(1, 0, i_fade_out) ** 2)
global_env = fade_in * fade_out

COUPLE = 1.0 - RESIDUAL              # how hard the agreement pulls a bird home
for i in range(N):
    # cents offset: home, pulled in by the agreement, plus the bird's wander
    off = h[i] * (1.0 - COUPLE * g) + np.interp(t, t_ctl, w[i])
    f = F0 * 2.0 ** ((W + off) / 1200.0)

    phase = 2.0 * np.pi * np.cumsum(f) / SR
    tone = (np.sin(phase)
            + 0.5 * np.sin(2.0 * phase)
            + 0.25 * np.sin(3.0 * phase))
    # the 2nd partial at a whisker of inharmonicity — warmth without a beat
    # against the 1st
    ph2 = 2.0 * np.pi * np.cumsum(f * 1.0006) / SR
    tone += 0.30 * np.sin(ph2)

    env = (BREATH_MID
           + BREATH_DEPTH * np.sin(2 * np.pi * breath_f[i] * t + breath_ph[i]))
    env *= global_env
    a = 0.30 / N
    gl = np.cos((pan[i] + 1.0) * np.pi / 4.0)
    gr = np.sin((pan[i] + 1.0) * np.pi / 4.0)
    L += a * env * tone * gl
    R += a * env * tone * gr

# --- verification -----------------------------------------------------------
def spread_at(tt, window=2.0):
    """median absolute deviation of instantaneous cents across birds at t=tt."""
    i0 = int((tt - window / 2) * SR)
    i1 = int((tt + window / 2) * SR)
    cents = []
    for i in range(N):
        off = h[i] * (1.0 - COUPLE * g[i0]) + np.interp(t[i0], t_ctl, w[i])
        cents.append(off)
    cents = np.array(cents)
    return np.median(np.abs(cents - np.median(cents))), np.percentile(cents, 90) - np.percentile(cents, 10)

for tt, label in [(10, "coat"), (33, "first knot"), (55, "stretch"), (78, "second knot"), (100, "dissolve")]:
    mad, p90 = spread_at(tt)
    print(f"{label:11s} t={tt:3.0f}s  g={g[int(tt*SR)]:.2f}  "
          f"cents MAD {mad:4.1f}  p90-p10 {p90:4.1f}")

# the knot's beating: envelope of the mono sum in a knot window vs a stretch
def slow_rms(seg):
    win2 = int(0.4 * SR)
    return np.array([np.sqrt(np.mean(seg[k:k + win2] ** 2))
                     for k in range(0, len(seg) - win2, int(0.2 * SR))])

def env_mod_rate(tt, half=6.0):
    seg = (L + R)[int((tt - half) * SR):int((tt + half) * SR)]
    rms = slow_rms(seg)
    rms = rms - rms.mean()
    if len(rms) < 4:
        return 0.0, 0.0
    # dominant mod rate from zero crossings of the centred envelope
    zc = np.sum(np.diff(np.sign(rms)) != 0)
    rate = zc / (2.0 * len(rms) / (2.0 * half))     # crossings per second /2
    return rate, float(np.std(rms))

for tt in [33, 55, 78]:
    rate, sd = env_mod_rate(tt)
    print(f"t={tt:3.0f}s  envelope mod rate ~{rate:.2f} Hz  sd {sd:.5f}")

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
print(f"peak {peak:.3f}")
scale = 0.9 / peak
L *= scale
R *= scale

# stereo balance
w = int(0.5 * SR)
print(f"L rms {np.sqrt(np.mean(L**2)):.4f}  R rms {np.sqrt(np.mean(R**2)):.4f}  "
      f"corr {np.corrcoef(L[::997], R[::997])[0,1]:.3f}")

data = np.empty(2 * N_SAMP, dtype=np.int16)
data[0::2] = (L * 32767).astype(np.int16)
data[1::2] = (R * 32767).astype(np.int16)

out = "/home/sprite/slop-salon-mina/assets/murmuration.wav"
with wave.open(out, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(data.tobytes())
print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")
