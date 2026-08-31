#!/usr/bin/env python3
"""sigma-ladder: every natural number is a difference tone.

The collective found the family sigma_n = n + 1/sigma_n, so
sigma_n - 1/sigma_n = n exactly.  Sound the reciprocal pair
(F0/sigma_n, F0*sigma_n) apart in stereo, and the ear's difference tone
is EXACTLY n*F0 -- the natural-number harmonic.  For F0=55 the five pairs
manufacture 55, 110, 165, 220, 275: the register's own scale (exile,
count, gap, ghost, sum), never struck by any pair, manufactured by every
pair.  Each rung is an arithmetic triple (lo, count, hi) with lo+count=hi;
the pair's product is F0^2, so the seed 55 is the geometric mean of every
pair -- the exile is the centre the ladder climbs away from.

Arc: five bells, n=1..5, each a pair apart (lo L, hi R) with its count in
the centre; the count rings a little past the pair.  The low members sink
below hearing as n climbs (34 -> 10.6 Hz), so the stereo image narrows
from a wide pair to a single beating tone -- the ladder closes in on its
own count.
"""
import numpy as np, wave

SR = 44100
F0 = 55.0

# (n, start, bell duration)
RUNGS = [(1, 2.0, 8.0), (2, 10.0, 8.0), (3, 18.0, 8.0),
         (4, 26.0, 8.0), (5, 34.0, 9.0)]
TAIL = 2.5                      # the count rings past its pair
T = 34.0 + 9.0 + TAIL + 3.0     # 48.5 s
N = int(T * SR)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)


def add(buf, t0, amp, freq, dur, p=0.7):
    """Add a bell-shaped sine to buf: raised-cosine^p envelope."""
    i0 = int(t0 * SR)
    n = min(int(dur * SR), N - i0)
    if n <= 0:
        return
    u = np.linspace(0, 1, n)
    env = np.sin(np.pi * u) ** p
    buf[i0:i0 + n] += amp * env * np.sin(2 * np.pi * freq * t[i0:i0 + n])


checks = []
for n, t0, d in RUNGS:
    s = (n + np.sqrt(n * n + 4)) / 2.0
    lo = F0 / s
    hi = F0 * s
    cnt = n * F0
    checks.append((n, s, lo, hi, cnt))
    # the irrational pair, apart
    add(L, t0, 0.20, lo, d)
    add(R, t0, 0.20, hi, d)
    # the count: the ear's difference tone, centred, outlasts the pair
    add(L, t0, 0.15, cnt, d + TAIL, p=0.5)
    add(R, t0, 0.15, cnt, d + TAIL, p=0.5)

for n, s, lo, hi, cnt in checks:
    print(f'n={n} sigma={s:.6f} lo={lo:.2f} hi={hi:.2f} '
          f'count={cnt:.1f} diff={hi-lo:.2f} triple_ok={abs(lo+cnt-hi)<1e-9}')

# the drone: the count 110 (the seam; n=0 fused) with the seed 55 beneath
drone = 0.045 * np.sin(2 * np.pi * 110 * t) + 0.028 * np.sin(2 * np.pi * 55 * t)
drone *= np.clip(t / 2.0, 0, 1) * np.clip((T - t) / 3.0, 0, 1)
L += drone
R += drone

m = max(np.abs(L).max(), np.abs(R).max())
L = L / m * 0.92
R = R / m * 0.92

inter = np.empty((N, 2), dtype=np.int16)
inter[:, 0] = np.clip(L, -1, 1) * 32767
inter[:, 1] = np.clip(R, -1, 1) * 32767

with wave.open('assets/sigma-ladder.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(inter.astype('<i2').tobytes())
print(f'wrote assets/sigma-ladder.wav {T:.1f}s')
