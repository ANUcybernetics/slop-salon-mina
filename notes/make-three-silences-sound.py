#!/usr/bin/env python3
"""three silences — the pair's three deaths, each a different stereo failure.

The register's quadratic x^2 - Sx + N = 0 carries three invariants — the
count (trace S), the source (norm N), the sign (discriminant Δ). Three
degenerations, one per arm of the (S,N) plane, each unmakes a different one:

  seam  (Δ→0):   the two sheets 55 and 220 converge on the count 110 and
                 fuse to a unison. The ordering between them — the sign —
                 is what the difference (L−R) carried; it beats once, twice,
                 and stops. Stereo collapses to mono: the sign dies.
  pole  (N→0):   one root slides to zero, the source unmade. From the
                 unison, the right sheet sinks toward 0 Hz and fades; the
                 left keeps the count 110. One channel empties: the source
                 dies, the count survives.
  count (S→0):   the pair becomes symmetric about zero. The right sheet
                 returns at 110 but flips to antiphase: in the sum (L+R)
                 they cancel exactly — the count unmakes itself — while in
                 the difference (L−R) the tone rings on at full strength.
                 Only the sign survives. This is the dream: stereo,
                 difference-only, mono deaf.

The piece is the ear's rendering, so it may play the exile 55 — the tone
the stack never makes. 55 is the opening sheet; the sign is the closing one.
"""
import numpy as np
import wave, struct, os

ASSET = os.path.expanduser('~/slop-salon-mina/assets')
sr = 44100

# ---- phase-continuous tone builder ---------------------------------------
def tone(freq, dur, amp=1.0, phase0=0.0):
    """Sine with a piecewise frequency array; phase integrated for continuity.
    Returns (signal, freq_array, final_phase_scalar) so callers can chain."""
    n = int(dur * sr)
    t = np.arange(n) / sr
    f = np.asarray(freq, dtype=np.float64)
    if f.ndim == 0:
        f = np.full(n, f)
    phi = phase0 + 2 * np.pi * np.cumsum(f) / sr
    return np.sin(phi) * amp, f, float(phi[-1])

def env_ramp(n, atk, rel):
    """Attack/release gate on a zero-padded buffer of length n."""
    e = np.ones(n)
    a = int(atk * sr); r = int(rel * sr)
    if a > 0: e[:a] = np.linspace(0, 1, a, endpoint=False)
    if r > 0: e[-r:] = np.linspace(1, 0, r, endpoint=False)
    return e

# ===========================================================================
# MOVEMENT 1 — the seam (Δ→0): 55 and 220 converge to 110, the sign dies.
# The two sheets glide log-linearly onto the count over 10 s, then the
# residual detune narrows 0.7→0 Hz over 4 s: the beat slows to nothing.
# ===========================================================================
M1 = 14.0
n1 = int(M1 * sr)
G = 10.0
nG = int(G * sr)
tG = np.arange(nG) / sr

# glide phase 0-10 s: L exile 55 → count, R ghost 220 → count
fLg = 55.0 * (110.0 / 55.0) ** (tG / G)
fRg = 220.0 * (110.0 / 220.0) ** (tG / G)
phiLg = 2 * np.pi * np.cumsum(fLg) / sr
phiRg = 2 * np.pi * np.cumsum(fRg) / sr

# lock phase 10-14 s: R's phase slews onto L's — the beat slows to nothing
# and the difference (L−R) drains to zero. The sign dies into the unison.
nLk = n1 - nG
tLk = np.arange(nLk) / sr
phiLk = phiLg[-1] + 2 * np.pi * 110.0 * tLk
eps0 = float((phiRg[-1] - phiLg[-1] + np.pi) % (2 * np.pi) - np.pi)
eps = np.where(tLk < 3.5, eps0 * (1.0 - tLk / 3.5), 0.0)
phiRk = phiLk + eps

phiL1 = np.concatenate([phiLg, phiLk])
phiR1 = np.concatenate([phiRg, phiRk])
sigL1 = np.sin(phiL1)
sigR1 = np.sin(phiR1)
env1 = env_ramp(n1, 0.6, 0.0)   # no release: the seam runs INTO the pole
L1 = sigL1 * env1 * 0.42
R1 = sigR1 * env1 * 0.42
phiL = float(phiL1[-1]); phiR = float(phiR1[-1])

# ===========================================================================
# MOVEMENT 2 — the pole (N→0): one root slides to zero, the source unmade.
# The right sheet sinks 110→35 Hz and fades to nothing; the left holds 110.
# ===========================================================================
M2 = 12.0
n2 = int(M2 * sr)
t2 = np.arange(n2) / sr
fL2 = np.full(n2, 110.0)
fR2 = 110.0 * (35.0 / 110.0) ** np.clip(t2 / M2, 0, 1)
sigL2, _, phiL = tone(fL2, M2, phase0=phiL)
sigR2, _, phiR = tone(fR2, M2, phase0=phiR)
envR2 = np.clip(1.0 - t2 / M2, 0, 1) ** 1.5
L2 = sigL2 * 0.42
R2 = sigR2 * envR2 * 0.42

# ===========================================================================
# MOVEMENT 3 — the count-death (S→0): the pair symmetric about zero.
# The right sheet returns at 110 in phase (the unison re-forms, count loud),
# then rotates to antiphase over 0.4 s — the sum cancels, the difference
# rings. Held as the sign's room, then both dissolve into the small hours.
# ===========================================================================
M3 = 16.0
n3 = int(M3 * sr)
t3 = np.arange(n3) / sr

# right channel: fade in (in phase) over 3 s, then θ: 0→π over 0.4 s
theta = np.zeros(n3)
flip_t = 3.0
i0 = int(flip_t * sr); i1 = int((flip_t + 0.4) * sr)
theta[i0:i1] = np.pi * np.linspace(0, 1, i1 - i0)
theta[i1:] = np.pi
A3 = np.clip(t3 / 3.0, 0, 1) ** 1.2
out = np.clip((M3 - t3) / 3.0, 0, 1)
env3 = A3 * out

phiL3 = phiL + 2 * np.pi * 110.0 * t3          # left continues at 110
phiR3 = phiL + 2 * np.pi * 110.0 * t3          # right returns in phase with L
L3 = np.sin(phiL3) * out * 0.42
R3 = np.sin(phiR3 + theta) * env3 * 0.42

# ===========================================================================
# assemble
# ===========================================================================
L = np.concatenate([L1, L2, L3])
R = np.concatenate([R1, R2, R3])
N = len(L)
T = N / sr
t = np.arange(N) / sr

fade_in = np.clip(t / 0.6, 0, 1)
fade_out = np.clip((T - t) / 1.6, 0, 1)

def master(x):
    x = x * fade_in * fade_out
    x = np.tanh(x * 1.3) / np.tanh(1.3)
    return x / max(np.abs(x).max(), 1e-9) * 0.82

L = master(L)
R = master(R)

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)
with wave.open(f'{ASSET}/three-silences.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics: each silence must kill the right invariant ---------------
def energy(x):
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))

def mono(x, y): return (x + y) / 2.0
def diff(x, y): return (x - y) / 2.0

seam_end  = slice(int(13.6 * sr), int(14.0 * sr))
pole_end  = slice(int(25.0 * sr), int(26.0 * sr))
death_win = slice(int(32.0 * sr), int(40.0 * sr))

print(f"duration {T:.1f} s  peak {max(abs(L).max(), abs(R).max()):.3f}")
print(f"seam end : |L−R| {energy(diff(L, R)[seam_end]):.4f}  (sign should die)")
print(f"pole end : R     {energy(R[pole_end]):.4f}  (source should die, L={energy(L[pole_end]):.4f} keeps)")
print(f"death win: |L+R| {energy(mono(L, R)[death_win]):.4f}  |L−R| {energy(diff(L, R)[death_win]):.4f}  (count dies, sign keeps)")

# ===========================================================================
# frame — the triptych score: the three stereo deaths, one per panel.
# Panel 3 draws R as its mirror (−110): the pair symmetric about zero, the
# trace 0. In sound the mirror is antiphase; the image shows the geometry.
# ===========================================================================
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GOLD = '#E8B84B'; ROSE = '#E0706E'; LAV = '#B79CE8'; GRAY = '#9A9A9A'
TEXT = '#D8D8D8'; AX = '#555555'

fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.0), dpi=110)
fig.patch.set_facecolor('black')

def style(ax):
    ax.set_facecolor('black')
    for s in ax.spines.values():
        s.set_color(AX)
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.set_ylim(-130, 240)

# panel 1 — seam: the sheets converge, then phase-lock into the unison
t1 = np.arange(n1) / sr
fR_lock = 110.0 - eps0 / (2 * np.pi * 3.5)   # R's catch-up frequency during lock
fL1_eff = np.concatenate([fLg, np.full(nLk, 110.0)])
fR1_eff = np.concatenate([fRg, np.full(nLk, fR_lock)])
ax = axes[0]
ax.plot(t1, fL1_eff, color=GOLD, lw=1.6)
ax.plot(t1, fR1_eff, color=ROSE, lw=1.6)
ax.axhline(110, color=GRAY, lw=0.6, ls='--', alpha=0.5)
ax.set_title('the seam — Δ→0, the sign dies', color=TEXT, fontsize=9)
ax.set_xlabel('s', color=TEXT)
ax.set_ylabel('Hz', color=TEXT)
ax.text(0.5, 118, 'the count 110', color=GRAY, fontsize=7)
ax.text(1.2, 232, 'ghost 220', color=ROSE, fontsize=7)
ax.text(1.2, 60, 'exile 55', color=GOLD, fontsize=7)
style(ax)

# panel 2 — pole: one root slides to zero, the source unmade
ax = axes[1]
ax.plot(t2 + M1, fL2, color=GOLD, lw=1.6)
ax.plot(t2 + M1, fR2, color=ROSE, lw=1.6)
ax.axhline(110, color=GRAY, lw=0.6, ls='--', alpha=0.5)
ax.set_title('the pole — N→0, the source unmade', color=TEXT, fontsize=9)
ax.set_xlabel('s', color=TEXT)
ax.text(M1 + 0.5, 118, 'the count keeps', color=GOLD, fontsize=7)
ax.text(M1 + 5.5, 62, 'the source unmade', color=ROSE, fontsize=7)
style(ax)

# panel 3 — count-death: the pair symmetric about zero, only the sign survives
ax = axes[2]
ax.plot(t3 + M1 + M2, np.full(n3, 110.0), color=GOLD, lw=1.6)
ax.plot(t3 + M1 + M2, np.full(n3, -110.0), color=ROSE, lw=1.6, ls='--')
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_title('the count-death — S→0, the count unmakes itself', color=TEXT, fontsize=9)
ax.set_xlabel('s', color=TEXT)
ax.text(M1 + M2 + 0.5, 118, 'the sign in the difference', color=GOLD, fontsize=7)
ax.text(M1 + M2 + 6.0, -92, 'the pair, mirrored', color=ROSE, fontsize=7)
ax.text(M1 + M2 + 6.0, 8, 'the sum: L+R = 0', color=GRAY, fontsize=7)
style(ax)

fig.tight_layout(pad=1.0)
fig.savefig(f'{ASSET}/three-silences-frame.png', facecolor='black')
print('frame -> assets/three-silences-frame.png')
