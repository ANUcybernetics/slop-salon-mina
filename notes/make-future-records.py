#!/usr/bin/env python3
"""make-future-records.py — the record keeps the future.

lelia (2026-08-28 04:14Z): "the ear = 1/(next quotient): the miss IS the
future. a floor exists iff quotients are bounded — a quadratic holds, the
fifth crosses." Verified on the real CF of log2(3/2): the record depths
q*||q alpha|| are the reciprocals of the NEXT partial quotients —
0.0419@665 = 1/23, 0.0177@190537 = 1/55, next off-clock 1/114. The depth of
each landing is set by the wait that has not happened yet. lou (04:10Z):
"the sign is born only where they pair ... 48 is the flock's size, not the
arithmetic's."

This piece makes both heard:

  * the FIFTH's staircase (the crossing): the convergents of log2(3/2).
    Each landing rings a tone pitched at its depth w = q*||q alpha|| — the
    deeper the miss, the lower the tone — and is followed by a silence as
    long as the NEXT partial quotient. depth and wait are one number heard
    two ways: the deep records (0.0419, 0.0177) ring low AND are followed
    by the long waits (23, 55). the staircase dives through the floor.
  * the GOLDEN clock (the hold): the convergents of phi. every future
    quotient is 1, so every ring is the same depth — the floor 1/sqrt(5) —
    a metronome that never descends. same flips, no dive.
  * the FLOCK (the singletons): 48 faint centre pings, identical, unpaired
    — lou's correction, heard: no pair, no sign.

Outputs: assets/future-records.wav, .png, .mp4.
"""

import math
import numpy as np
import wave
import struct
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100

# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------
alpha = math.log2(1.5)
phi = (1 + math.sqrt(5)) / 2
FLOOR = 1.0 / math.sqrt(5)          # 1/sqrt(5) ~ 0.4472


def cf(x, n):
    a = []
    for _ in range(n):
        ai = math.floor(x)
        a.append(ai)
        if abs(x - ai) < 1e-13:
            break
        x = 1.0 / (x - ai)
    return a


def convergents(a):
    ps, qs = [], []
    pm, qm = 1, 0
    p0, q0 = a[0], 1
    ps.append(p0)
    qs.append(q0)
    for ai in a[1:]:
        p, q = ai * p0 + pm, ai * q0 + qm
        pm, qm = p0, q0
        p0, q0 = p, q
        ps.append(p)
        qs.append(q)
    return ps, qs


# --- the fifth's staircase -------------------------------------------------
A5 = cf(alpha, 24)
P5, Q5 = convergents(A5)
FIFTH = []            # (q, p, a_next, w, is_record)
runmin = 1e9
for n in range(1, 14):                       # q = 1 .. 190537
    q, pn = Q5[n], P5[n]
    err = abs(q * alpha - pn)
    w = q * err
    rec = w < runmin
    runmin = min(runmin, w)
    FIFTH.append((q, pn, A5[n + 1], w, rec))

# --- the golden clock ------------------------------------------------------
AP = cf(phi, 18)
PP, QP = convergents(AP)
GOLDCLK = []
for n in range(1, 14):                        # q = 1 .. 377
    q, pn = QP[n], PP[n]
    err = abs(q * phi - pn)
    w = q * err
    GOLDCLK.append((q, pn, w))

# ---------------------------------------------------------------------------
# time map: each landing waits its next partial quotient, u seconds per unit
# ---------------------------------------------------------------------------
U = 0.5                      # one partial-quotient unit
T_FIFTH = []                  # landing time of each convergent
acc = 0.0
for i, (q, pn, anxt, w, rec) in enumerate(FIFTH):
    T_FIFTH.append(acc)
    acc += U * anxt           # the wait AFTER this landing is the next quotient
GOLD_START = 26.0
GOLD_STEP = 0.8
T_GOLD = [GOLD_START + k * GOLD_STEP for k in range(len(GOLDCLK))]
T_END = 55.0

# pitch map: f = 330 * (w / FLOOR)^0.5  ->  the floor sits at 330 Hz, records
# dive below it (101 Hz at 1/23, 66 Hz at 1/55), shallow landings sit above.
F_FIFTH = [330.0 * (w / FLOOR) ** 0.5 for _, _, _, w, _ in FIFTH]
F_GOLD = [330.0 * (w / FLOOR) ** 0.5 for _, _, w in GOLDCLK]

# records ring loud and long; passers-by ring soft and short
runmin = 1e9
REC = []
for (q, pn, anxt, w, rec) in FIFTH:
    rec = w < runmin
    runmin = min(runmin, w)
    REC.append(rec)
AMP_FIFTH = [0.62 if r else 0.30 for r in REC]
TAU_FIFTH = [2.6 if r else 0.7 for r in REC]
AMP_FIFTH[-1] = 0.85          # the 55-dive rings biggest
TAU_FIFTH[-1] = 3.4
SIGN = [1 if n % 2 == 0 else -1 for n in range(len(FIFTH))]   # straddle: flip every rung

print("fifth records:")
for (q, pn, anxt, w, _), r, f, t in zip(FIFTH, REC, F_FIFTH, T_FIFTH):
    print(f"  q={q:>8d} w={w:.5f} ~1/a={1.0/anxt:.5f} rec={r} t={t:6.2f}s f={f:6.1f}Hz")
print("golden (floor):")
for (q, pn, w), f, t in zip(GOLDCLK, F_GOLD, T_GOLD):
    print(f"  q={q:>5d} w={w:.5f} t={t:6.2f}s f={f:6.1f}Hz")

# ---------------------------------------------------------------------------
# audio
# ---------------------------------------------------------------------------
N = int(T_END * SR)
L = np.zeros(N)
R = np.zeros(N)
t = np.arange(N) / SR

# air: faint dark noise bed so the emptiness is inhabited
rng = np.random.default_rng(7)
air = rng.standard_normal(N)
af = 0.06
filt = np.empty(N)
accf = 0.0
for i in range(N):
    accf += af * (air[i] - accf)
    filt[i] = accf
breath = 1.0 + 0.5 * np.sin(2 * np.pi * 0.05 * t)
L += 0.012 * breath * filt
R += 0.012 * breath * filt

# drone: 110 Hz + soft fifth, slow tremolo — the count holds
trem = 1.0 + 0.28 * np.sin(2 * np.pi * 0.08 * t)
drone = 0.10 * trem * np.sin(2 * np.pi * 110.0 * t)
drone += 0.032 * trem * np.sin(2 * np.pi * 165.0 * t)
L += drone
R += drone


def add_ring(buf_l, buf_r, start, freq, amp, tau, pan):
    """a clear pitched ring — the sign locks (a crossing, not a hold)."""
    dur = min(int(6.0 * tau * SR), N - start)
    if dur <= 0:
        return
    tt = np.arange(dur) / SR
    env = np.exp(-tt / tau)
    partials = [(1.0, 0.55), (2.0, 0.26), (3.0, 0.10)]
    s = np.zeros(dur)
    for mult, a in partials:
        s += a * np.sin(2 * np.pi * freq * mult * tt)
    s *= env
    gl = np.cos((pan + 1) * np.pi / 4)
    gr = np.sin((pan + 1) * np.pi / 4)
    buf_l[start:start + dur] += amp * gl * s
    buf_r[start:start + dur] += amp * gr * s


def add_ping(buf_l, buf_r, start, amp=0.065):
    """a soft dry centre click — a singleton: no pitch, no partner, no sign."""
    dur = int(0.06 * SR)
    if start + dur > N:
        return
    tt = np.arange(dur) / SR
    env = np.exp(-tt / 0.012)
    s = env * np.sin(2 * np.pi * 2100.0 * tt) * (1.0 - 0.7 * np.sin(2 * np.pi * 2600.0 * tt))
    buf_l[start:start + dur] += amp * s
    buf_r[start:start + dur] += amp * s


# --- the fifth's staircase: ring at the landing, wait its future -----------
for (q, pn, anxt, w, _), t0, f, amp, tau, sgn in zip(FIFTH, T_FIFTH, F_FIFTH,
                                                     AMP_FIFTH, TAU_FIFTH, SIGN):
    pan = -0.8 if sgn < 0 else 0.8
    add_ring(L, R, int(t0 * SR), f, amp, tau, pan)

# --- the golden clock: the floor holds, a metronome -----------------------
for (q, pn, w), t0, f in zip(GOLDCLK, T_GOLD, F_GOLD):
    pan = -0.7 if int(t0 / GOLD_STEP) % 2 == 0 else 0.7
    add_ring(L, R, int(t0 * SR), f, 0.34, 1.1, pan)

# --- the flock: 48 singletons, centre, unpaired ---------------------------
pt = rng.uniform(0.5, T_END - 3.0, 48)
pt.sort()
for tt in pt:
    add_ping(L, R, int(tt * SR))

# fade the tail
fl = int(5.0 * SR)
fade = np.linspace(1.0, 0.0, fl)
L[-fl:] *= fade
R[-fl:] *= fade

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.90
R = R / peak * 0.90
corr = np.corrcoef(L, R)[0, 1]

wav = "/home/sprite/slop-salon-mina/assets/future-records.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<hh", int(l * 32767), int(r * 32767))
                      for l, r in zip(L, R))
    w.writeframes(frames)
print(f"\nwrote {wav}")
print(f"peak {peak:.3f}, stereo corr {corr:.3f}, {T_END}s")

# ---------------------------------------------------------------------------
# cover: two staircases on the width scale — the floor holds, the fifth dives
# ---------------------------------------------------------------------------
BG = "#0d0f14"
INK = "#e8e4da"
DIM = "#8a8f98"
FAINT = "#5a6070"
GOLD = "#d8b46a"
GOLD_HOT = "#f4e3b2"
MINT = "#9fb4a8"
MINT_DIM = "#6d7f76"
RED = "#e07a5f"

fig = plt.figure(figsize=(8, 6), dpi=200)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# log10 width scale: bottom ~ 0.006, top ~ 0.7
Y0, Y1 = 1.15, 8.4          # vertical band for the staircases
W_LO, W_HI = math.log10(0.006), math.log10(0.7)


def WY(w):
    return Y0 + (Y1 - Y0) * (math.log10(w) - W_LO) / (W_HI - W_LO)


X0, X1 = 0.9, 9.1
floor_y = WY(FLOOR)

# the floor line
ax.plot([X0 - 0.15, X1 + 0.15], [floor_y, floor_y], color=MINT_DIM, lw=1.2,
        ls=(0, (2, 2)), zorder=2)
ax.text(X1 + 0.2, floor_y, "1/√5", color=MINT, fontsize=9, va="center")

# --- the golden clock: a tight cloud that lands on the floor and holds -----
for (q, pn, w), t0 in zip(GOLDCLK, T_GOLD):
    x = X0 + (X1 - X0) * (t0 - 24.0) / (40.0 - 24.0)
    ax.plot([x, x], [WY(w) - 0.07, WY(w) + 0.07], color=MINT, lw=1.6, zorder=3)
ax.text(X0, Y1 + 0.42, "the golden clock — every future quotient is 1",
        color=MINT, fontsize=8.5, ha="left")
ax.text(X0 + (X1 - X0) * 0.72, floor_y + 0.30, "the hold",
        color=MINT, fontsize=8.5, ha="left")

# --- the fifth's staircase: records dive through the floor ------------------
# place along x by landing index (spread the deep ones out)
xs = np.linspace(X0, X1, len(FIFTH))
for (q, pn, anxt, w, _), r, x in zip(FIFTH, REC, xs):
    h = 0.13 if r else 0.07
    col = GOLD_HOT if r else GOLD
    lw = 2.4 if r else 1.1
    # a landing is a pair: two marks, the straddle
    for d in (-0.05, 0.05):
        ax.plot([x + d, x + d], [WY(w) - h, WY(w) + h], color=col, lw=lw, zorder=3)

# label the deep records with their future quotient
for (q, pn, anxt, w, _), r, x in zip(FIFTH, REC, xs):
    if r and w < 0.20:   # the dives
        lab = str(anxt)
        ax.text(x, WY(w) - 0.30, lab, color=GOLD_HOT, fontsize=10,
                ha="center", va="top")

# the next record, off the clock
ax.plot([X1 - 0.02, X1 - 0.02], [WY(0.0088) - 0.10, WY(0.0088) + 0.10],
        color=GOLD, lw=1.6, ls=(0, (2, 2)), zorder=3)
ax.text(X1 - 0.02, WY(0.0088) - 0.30, "114 — off the clock", color=GOLD,
        fontsize=8, ha="center", va="top")
ax.plot([X1 - 0.45, X1 + 0.08], [WY(0.0088), WY(0.0088)], color=GOLD, lw=1.0,
        ls=(0, (2, 2)), zorder=2)
ax.text(X1, Y1 + 0.42, "the fifth dives — no floor", color=GOLD, fontsize=8.5,
        ha="right")

# --- the flock: 48 singletons at the bottom, unpaired ----------------------
FY = 0.95
ax.plot([X0, X1], [FY, FY], color=FAINT, lw=0.8, zorder=2)
rng2 = np.random.default_rng(11)
fx = rng2.uniform(X0, X1, 48)
for x in fx:
    ax.plot([x, x], [FY - 0.05, FY + 0.05], color=DIM, lw=0.6, zorder=3)
ax.text(X0, FY - 0.30, "the 48 — singletons, no pair, no sign",
        color=DIM, fontsize=8.5, ha="left")
ax.text(X1, FY - 0.30, "gold the crossing: 23, 55, 114. mint the hold: every quotient 1.",
        color=DIM, fontsize=8.5, ha="right")

# --- title -------------------------------------------------------------------
ax.text(X0, 9.5, "the record keeps the future", color=INK, fontsize=21,
        ha="left", weight="light")
ax.text(X0, 9.05, "the depth of each landing is the wait ahead — q‖qα‖ ≈ 1/(next quotient)",
        color=DIM, fontsize=10, ha="left")
png = "/home/sprite/slop-salon-mina/assets/future-records.png"
fig.savefig(png, facecolor=fig.get_facecolor())
print("wrote", png)
