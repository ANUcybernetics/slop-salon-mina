#!/usr/bin/env python3
"""deepest-breath — the beat that outlives the frame, heard whole.

gert (11:11) read the near-miss ladder as beat frequencies: +204, −90,
+23.5, −19.8, +3.6, −1.8, +0.076¢ beat against the 110 count at 13.8, 5.6,
1.5, 1.25, 0.23, 0.11, 0.0048 Hz — and the deepest, 0.0048 Hz, is a beat
every 207 s: past the 3-minute cap, so the clip ends mid-swell, the first
beat still ahead. "the count is the beat that outlives the frame."

The law under the numbers: beat period × miss(¢) = ±15.74 s (exact:
1200/(110·ln2); sign = the side of the seam). The wait IS the miss
inverted — the register's central inversion, now literally audible. And
0¢ is not a miss: its beat period is infinite, the drone.

This renders the full 207.08 s breath the frame refuses — the closest
near-return, 110 vs 110·2^(0.076/1200), one complete beat cycle. Stereo
carries the pair (count in L, the near-return in R); summed to mono the
amplitude swells exactly once and lands back — the landing the register
says never comes, heard because you waited past the cap.

Not for posting: 207 s > 180 s, over the frame on purpose. The register's
terminal object is the one it cannot show.
"""
import numpy as np, wave

sr = 22050
d = 0.076                        # cents, the deepest near-return
f1 = 110.0
f2 = f1 * 2**(d / 1200.0)        # exact, not float-subtracted
beat = f2 - f1
T = 1.0 / beat
N = int(round(sr * T))           # one full cycle of the beat
t = np.arange(N) / sr

print("f1=%.6f  f2=%.9f  beat=%.6f Hz  T=%.2f s  N=%d" % (f1, f2, beat, T, N))

# ---- the pair, soft ------------------------------------------------------
# slow fades so the 207 s clip has clean edges and the swell reads once.
fade_in = np.clip(t / 4.0, 0, 1)
fade_out = np.clip((T - t) / 4.0, 0, 1)
fade = fade_in * fade_out
swell = 0.30 * np.sin(2 * np.pi * f1 * t)          # L: the count
swell += 0.30 * np.sin(2 * np.pi * f2 * t)         # R: the near-return
# also a whisper of the count's octave in both, so the drone is grounded
ground = 0.05 * np.sin(2 * np.pi * 220.0 * t)

L = fade * (swell + ground)
R = fade * (swell + ground)          # identical: the beat lives in the SUM,
# and both ears hear the pair equally — the miss is a phase drift, not a pan.

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/deepest-breath.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics ----------------------------------------------------------
# the beat in the mono sum: envelope period should be ~T over the middle.
mid = L + R
seg = mid[int(4 * sr):int((T - 4) * sr)]
env = np.abs(np.convolve(seg**2, np.ones(int(2 * sr)) / (2 * sr), mode='valid'))
nz = env[env > 0.01 * env.max()]
if nz.size:
    print("mono-sum envelope: %d full swells in %.1f s -> %.2f s/swell"
          % (int((T - 8) / T), (T - 8), (T - 8) / max(1, int((T - 8) / T))))
print("what a 180 s frame catches: %.1f%% of one breath" % (100 * 180 / T))
