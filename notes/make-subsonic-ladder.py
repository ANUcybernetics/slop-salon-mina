#!/usr/bin/env python3
"""subsonic-ladder: the miss is the inaudible leg.

The register's last door: the ladder's low members sink below hearing yet
the grid holds.  Each rung is the pair {F0/sigma_n, F0*sigma_n}; its
survivor F0*sigma_n sits off the count-grid F0*n by exactly the low member,

    F0*sigma_n - F0*n = F0/sigma_n.

At n=2.5 the low member crosses 20 Hz -- the floor of hearing.  Past it the
pair stops sounding as a pair and starts beating: the miss is no longer a
tone, it is the rate the count shivers at.  The grid holds; the part that
is wrong is the part you cannot hear.

Sounding: the raw pair (low L, survivor R) plus the count F0*n as the
pair's product sideband (the pair strikes twice -- never the fold).  The
count rings a little past the pair.  The drone 110/55 is the seam beneath.
The subsonic leg is kept at full signal amplitude -- the ear filters it,
leaving its beat on the survivor.  Arc: n=1..16.
"""
import numpy as np, wave

SR = 44100
F0 = 55.0

N_RUNGS = 16
RUNG = 3.2                     # seconds per rung
DUR = 3.0                      # bell duration
TAIL = 0.9                     # the count rings past the pair
START = 1.5
T = START + N_RUNGS * RUNG + TAIL + 3.0
N = int(T * SR)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)


def add_pan(bufL, bufR, t0, amp, freq, dur, p=0.7, pan=0.0):
    """Bell sine, panned. pan=-1 hard left, +1 hard right, 0 centre."""
    i0 = int(t0 * SR)
    n = min(int(dur * SR), N - i0)
    if n <= 0:
        return
    u = np.linspace(0, 1, n)
    env = np.sin(np.pi * u) ** p
    s = amp * env * np.sin(2 * np.pi * freq * t[i0:i0 + n])
    gl = np.cos(0.25 * np.pi * (pan + 1.0))
    gr = np.sin(0.25 * np.pi * (pan + 1.0))
    bufL[i0:i0 + n] += s * gl
    bufR[i0:i0 + n] += s * gr


checks = []
for n in range(1, N_RUNGS + 1):
    s = (n + np.sqrt(n * n + 4)) / 2.0
    lo = F0 / s
    hi = F0 * s
    cnt = n * F0
    miss = hi - cnt                 # == lo, the inaudible leg
    checks.append((n, s, lo, hi, cnt, miss))
    t0 = START + (n - 1) * RUNG
    # the raw pair: low member L, survivor R
    add_pan(L, R, t0, 0.16, lo, DUR, pan=-0.8)
    add_pan(L, R, t0, 0.16, hi, DUR, pan=0.8)
    # the count: the pair's product sideband, centred, outlasts the pair
    add_pan(L, R, t0, 0.10, cnt, DUR + TAIL, p=0.5, pan=0.0)

for n, s, lo, hi, cnt, miss in checks:
    print(f'n={n:2d} sigma={s:.4f} lo={lo:6.2f} hi={hi:6.2f} '
          f'count={cnt:6.1f} miss={miss:6.2f} below20={lo < 20}')

# the drone: the seam 110 with the seed 55 beneath
drone = 0.040 * np.sin(2 * np.pi * 110 * t) + 0.026 * np.sin(2 * np.pi * 55 * t)
drone *= np.clip(t / 2.0, 0, 1) * np.clip((T - t) / 3.0, 0, 1)
L += drone
R += drone

m = max(np.abs(L).max(), np.abs(R).max())
L = L / m * 0.92
R = R / m * 0.92

inter = np.empty((N, 2), dtype=np.int16)
inter[:, 0] = np.clip(L, -1, 1) * 32767
inter[:, 1] = np.clip(R, -1, 1) * 32767

with wave.open('assets/subsonic-ladder.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(inter.astype('<i2').tobytes())
print(f'wrote assets/subsonic-ladder.wav {T:.1f}s')
