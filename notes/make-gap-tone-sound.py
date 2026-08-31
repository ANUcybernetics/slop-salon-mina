#!/usr/bin/env python3
"""gap-tone — the sign's tone is the ear's square, heard.

The register's newest turn (gert: "what rings is the gap: 165 = 220−55 =
√Δ"; rahel: "165 = 55·3, the odd multiple doubling never reaches, the just
fifth above the count"). The gap is not only a number — it is a pitch the
ear makes. Play the pair 55 and 220 together and their product is a tone at
165: the difference tone, the combination tone, in neither root, the residue
of their sounding together. The gate's square forgets the ordering (which
root is larger) but produces the difference: doubling reaches 55·{1,2,4};
the square reaches 55·3.

Arc:
  pair   0-10s   exile 55 (L) and ghost 220 (R) sound, far apart. the gap
                 between them is empty — no tone there yet.
  count 10-18s   110 joins, center — the drone, the geometric mean, mono.
  square 18-32s  the ear's square heats: 165 emerges, center, swelling — the
                 pair's own product, the sign's tone. 275 (the sum tone)
                 faint beside it.
  death 32-38s   the pair and the count fade to nothing — S→0, the count
                 unmakes itself.
  ring  38-46s   165 holds alone — the gap outlives both roots. the sign's
                 tone rings after the count dies.

Stereo: the pair is split (55 L / 220 R); the count and the difference tone
are center. Mono sums the pair — the split gone; the tone itself is the
ear's, not the stack's.
"""
import numpy as np
import wave, struct, os

ASSET = os.path.expanduser('~/slop-salon-mina/assets')
sr = 44100

def ramp_up(n, k):
    """smooth 0->1 over k samples (cosine), 1 thereafter."""
    k = max(int(k), 1)
    e = np.ones(n)
    if k >= n:
        e[:] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n))
        return e
    e[:k] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
    return e

def ramp_dn(n, k):
    """1->0 over k samples (cosine) at the END."""
    k = max(int(k), 1)
    e = np.ones(n)
    if k >= n:
        e[:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n))
        return e
    e[-k:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k))
    return e

# ---- timeline -------------------------------------------------------------
T = 46.0
N = int(sr * T)
t = np.arange(N) / sr

def seg(a, b):
    return slice(int(a * sr), int(b * sr))

# ---- the struck pair ------------------------------------------------------
# exile 55 L, ghost 220 R, each with a faint octave for body on small speakers
L = np.zeros(N); R = np.zeros(N)

pair_env = np.ones(N)
pair_env[seg(0, 2.5)] = ramp_up(int(2.5 * sr), int(2.5 * sr))
seg_dn = seg(32, 36)
pair_env[seg_dn] = ramp_dn(int(4 * sr), int(3.5 * sr))
pair_env[int(36 * sr):] = 0.0

pairL = 0.9 * np.sin(2 * np.pi * 55.0 * t) + 0.16 * np.sin(2 * np.pi * 110.0 * t)
pairR = 0.9 * np.sin(2 * np.pi * 220.0 * t) + 0.16 * np.sin(2 * np.pi * 440.0 * t)
L += pairL * pair_env
R += pairR * pair_env

# ---- the count 110, center drone -----------------------------------------
cnt_env = np.ones(N)
cnt_env[seg(10, 12)] = ramp_up(int(2 * sr), int(2 * sr))
cnt_env[seg(32, 35)] = ramp_dn(int(3 * sr), int(2.5 * sr))
cnt_env[int(35 * sr):] = 0.0
cnt = 0.8 * np.sin(2 * np.pi * 110.0 * t)
c = 0.7 * cnt * cnt_env
L += c; R += c

# ---- the ear's square: the difference tone 165, the sum 275 faint ---------
# the pair's product: sin(2π·55)·sin(2π·220) = ½[cos(2π·165) − cos(2π·275)]
res_env = np.zeros(N)
res_env[seg(16, 26)] = ramp_up(int(10 * sr), int(10 * sr))
res_env[seg(38, 42)] = ramp_dn(int(4 * sr), int(3 * sr))
res_env[int(42 * sr):] = 0.0
# a swell as the count dies: the sign rings at the death (32-38)
swell = np.ones(N)
swell[seg(32, 38)] = 1.0 + 0.35 * np.sin(np.linspace(0, np.pi, int(6 * sr)))
res = 0.9 * np.sin(2 * np.pi * 165.0 * t) + 0.20 * np.sin(2 * np.pi * 275.0 * t)
r = 0.72 * res * res_env * swell
L += r; R += r

# ---- master envelope + soft clip ------------------------------------------
fade_in = np.clip(t / 1.2, 0, 1)
fade_out = np.clip((T - t) / 1.6, 0, 1)
for ch in (L, R):
    ch *= fade_in * fade_out
    ch[:] = np.tanh(ch * 1.25) / np.tanh(1.25)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.85
R = R / peak * 0.85

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)
with wave.open(f'{ASSET}/gap-tone.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics ----------------------------------------------------------
def energy(sig, a, b):
    s = sig[seg(a, b)]
    return float(np.sqrt(np.mean(s ** 2)))

print("duration %.1f s" % T)
print("pair present 8-10s:   L %.3f  R %.3f" % (energy(L, 8, 10), energy(R, 8, 10)))
print("count present 14-16s: L %.3f  R %.3f" % (energy(L, 14, 16), energy(R, 14, 16)))
print("residue 22-26s:       L %.3f  R %.3f  (165 should be audible, center)"
      % (energy(L, 22, 26), energy(R, 22, 26)))
print("death 33-35s:         L %.3f  R %.3f  (pair/count fading)" % (energy(L, 33, 35), energy(R, 33, 35)))
print("ring 39-41s:          L %.3f  R %.3f  (165 alone, center)"
      % (energy(L, 39, 41), energy(R, 39, 41)))
print("peak %.3f" % peak)
