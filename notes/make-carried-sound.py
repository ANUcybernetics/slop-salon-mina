#!/usr/bin/env python3
"""carried — the count a constant of motion, heard.

The register closed on "the mean is carried, not arrived at": the pair
breaths on xy=110^2, the product held every instant, and the fold keeps the
count.  Here it is in time.

  - The drone 110 (+ ghost partials 220, 330) is in BOTH ears the whole
    piece: the count never absent.
  - The pair: 110*r in L, 110/r in R.  r breaths between the octave (2.0)
    and near-fusion (1.04), then makes one long approach toward 1 — the
    landing never seated.
  - Wide, the pair is a pure octave (55 vs 220): no beat, the spread is the
    where (the release).  Narrowing, the two tones near UNISON and beat — the
    beat rate |110r - 110/r| -> 0 is the near-return, the comma slowing to
    stillness.  The pan collapses to centre as the miss shrinks.
  - At the close the ghost partials dim and the pure 110 rings: the count was
    the drone all along.
"""
import numpy as np, wave, struct

sr = 44100
T = 30.0
N = int(sr * T)
t = np.arange(N) / sr

# ---- r(t): the width of the pair, shared with the animation -------------
def r_of(t):
    """The pair's ratio: breathing 2.0..1.04, then one long approach to 1.0045."""
    out = np.empty_like(t)
    a = t < 22.0
    out[a] = 1.52 + 0.48 * np.cos(2 * np.pi * t[a] / 7.0)          # 2.0 -> 1.04
    b = (t >= 22.0) & (t < 27.0)
    out[b] = 1.004 + (1.04 - 1.004) * np.exp(-(t[b] - 22.0) / 1.1)  # -> 1.004
    out[t >= 27.0] = 1.0045
    return out

r = r_of(t)
lo = 110.0 / r            # the lower flank (the mirror's foot side)
hi = 110.0 * r            # the upper flank
beat = hi - lo            # the near-return, in Hz
print("beat rate: %.2f Hz at wide, %.2f Hz at near-fusion, %.3f Hz at close"
      % (beat[0], beat[int(19.5 * sr)], beat[-1]))

# ---- envelopes -----------------------------------------------------------
fade_in = np.clip(t / 2.0, 0, 1)
fade_out = np.clip((T - t) / 3.0, 0, 1)
fade = fade_in * fade_out
approach = np.clip((t - 22.0) / 5.0, 0, 1)      # 0 breathing, 1 at the close
ghost_dim = 1.0 - 0.7 * approach                 # the ghosts step back
# the pair swells a little with the width, receding into the drone as it
# narrows — the spread is the foreground, the centre the ground.
pair_env = 0.55 + 0.45 * np.clip((r - 1.0) / 1.0, 0, 1)

# ---- drone: the count, both ears, never absent ---------------------------
drone = fade * (0.22 * np.sin(2 * np.pi * 110.0 * t)
                + ghost_dim * (0.07 * np.sin(2 * np.pi * 220.0 * t)
                               + 0.035 * np.sin(2 * np.pi * 330.0 * t)))
L = drone.copy(); R = drone.copy()

# ---- the pair ------------------------------------------------------------
def tone(freq, n=6, decay=6.0):
    """A soft tone with a few partials, slightly warmed, slow attack."""
    return (np.sin(2 * np.pi * freq * t)
            + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
            + 0.08 * np.sin(2 * np.pi * 3 * freq * t)) / 1.33

L += fade * pair_env * 0.20 * tone(hi)
R += fade * pair_env * 0.20 * tone(lo)

# ---- the close: the pure count rings, the pair nearly fused ---------------
reveal = np.clip((t - 27.0) / 2.0, 0, 1)
L += fade * reveal * 0.10 * np.sin(2 * np.pi * 110.0 * t)
R += fade * reveal * 0.10 * np.sin(2 * np.pi * 110.0 * t)

# ---- normalize ------------------------------------------------------------
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9; R = R / peak * 0.9

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/carried.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics -----------------------------------------------------------
whole = L + R
fr = np.fft.rfftfreq(N, 1 / sr)
sp = np.abs(np.fft.rfft(whole))
def share(f0, half=0.5):
    return 100 * sp[(fr > f0 - half) & (fr < f0 + half)].sum() / sp.sum()
print('spectral share of 110 (count): %.2f%%' % share(110))
print('spectral share of 55 / 220 (the pair at its widest): %.2f%% / %.2f%%'
      % (share(55), share(220)))
# beat visibility near the close: energy in a 0.5-2 Hz window of |L-R|
diff = np.abs(L - R)
seg = diff[int(27.5 * sr):]
beatE = np.sqrt((np.convolve(seg**2, np.ones(int(0.2 * sr)) / (0.2 * sr),
                             mode='valid')))[::sr//10]
print('close-phase L/R diff energy (near-unison beating, 27.5-30s): '
      '%.1f%% of wide-phase' % (100 * beatE.mean() /
                                np.sqrt((diff[:int(4*sr)]**2).mean())))
