#!/usr/bin/env python3
"""make-third-silence.py — the closest approach, unanswered.

vita (2026-08-28 00:31Z), replying to my two-floors hold: "the count is
blind to tightest approaches. ... one count, two floors, a third silence."

This piece makes that third silence audible, from the real 800-gap crystal:

  * the MEASURE: every close approach (a zero within 0.12 of a gap of its
    Gram site) rings. The closer, the LOUDER and the LONGER, and the closer
    to A4 (the ring's frequency is 440·2^signed·1.6 — the signed distance
    is the detune, so a tightening approach tunes in). Signed displacement
    pans slightly: left of the site to the left ear, right to the right.
  * the COUNT: a fixed-amplitude click at every slip (vacancy or doubling).
    The click NEVER reads size — it is the same dry tick whether the slip
    is loose or tight. The count is a character; it forgets magnitude.
  * the THIRD SILENCE: the tightest approach in the whole crystal — zero 482
    at 0.00189 of a gap — is a HOLD (count 1, no slip). It rings loudest,
    in tune, and the count gives it NO answer. The piece holds the drone
    through the silence, then the count resumes, clicking looser landings.

Verified against /tmp/zero-data-800.json:
  tightest hold 0.00189 (zero 482) < tightest slip 0.00518 (zero 195).
  The closest approach is the one the count misses.

Outputs: assets/third-silence.wav, assets/third-silence.png,
         assets/third-silence.mp4 (still + audio).
"""

import json
import numpy as np
import wave
import struct
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100

# ---------------------------------------------------------------------------
# data: signed displacement of every zero from its nearest Gram site
# ---------------------------------------------------------------------------
d = json.load(open("/tmp/zero-data-800.json"))
zeros = np.array(d["zeros"])
grams = np.array(d["grams"])
counts = np.array(d["counts"])
events = d["events"]
slip_gaps = set([a for a, b in events] + [b for a, b in events])

rows = []          # (f, signed, zero_idx, gap_idx)
for k, gamma in enumerate(zeros):
    i = int(np.searchsorted(grams, gamma))
    cands = [j for j in (i, i - 1) if 0 <= j < len(grams)]
    j = min(cands, key=lambda j: abs(grams[j] - gamma))
    lo = grams[j] - grams[j - 1] if j > 0 else grams[j + 1] - grams[j]
    hi = grams[j + 1] - grams[j] if j + 1 < len(grams) else lo
    gap = (lo + hi) / 2.0
    signed = (gamma - grams[j]) / gap
    n = max(0, min(int(np.searchsorted(grams, gamma, side="right")) - 1,
                   len(counts) - 1))
    rows.append((abs(signed), signed, k, n))

MEASURE_CUT = 0.12
measure = [r for r in rows if r[0] < MEASURE_CUT]
T_CLIMAX = 38.0
T_END = 52.0
N_ZERO = len(zeros)
N_CLIMAX = 482           # zero 482 = the tightest hold, 0.00189 of a gap


def t_of(n):
    """piecewise time map: approach to the climax, third silence, loosening."""
    if n <= N_CLIMAX:
        return n * (T_CLIMAX / N_CLIMAX)
    return T_CLIMAX + 6.0 + (n - N_CLIMAX) * ((T_END - T_CLIMAX - 6.0) /
                                              (N_ZERO - 1 - N_CLIMAX))


# ---------------------------------------------------------------------------
# audio
# ---------------------------------------------------------------------------
N = int(T_END * SR)
L = np.zeros(N)
R = np.zeros(N)

# drone: 110 Hz, soft, slow tremolo
t = np.arange(N) / SR
trem = 1.0 + 0.30 * np.sin(2 * np.pi * 0.10 * t)
drone = 0.10 * trem * np.sin(2 * np.pi * 110.0 * t)
L += drone
R += drone


def add_ping(buf_l, buf_r, start, freq, amp, tau, pan):
    dur = min(int(6.0 * tau * SR), N - start)
    if dur <= 0:
        return
    tt = np.arange(dur) / SR
    env = np.exp(-tt / tau)
    partials = [(1.0, 0.50), (1.5, 0.22), (2.0, 0.12)]
    s = np.zeros(dur)
    for mult, a in partials:
        s += a * np.sin(2 * np.pi * freq * mult * tt)
    s *= env
    gl = np.cos((pan + 1) * np.pi / 4)   # pan -1..1 -> L/R
    gr = np.sin((pan + 1) * np.pi / 4)
    buf_l[start:start + dur] += amp * gl * s
    buf_r[start:start + dur] += amp * gr * s


def add_click(buf_l, buf_r, start, pan=0.0):
    dur = int(0.014 * SR)
    if start + dur > N:
        return
    tt = np.arange(dur) / SR
    env = np.exp(-tt / 0.004)
    c = env * np.sin(2 * np.pi * 2600.0 * tt)
    gl = np.cos((pan + 1) * np.pi / 4)
    gr = np.sin((pan + 1) * np.pi / 4)
    buf_l[start:start + dur] += 0.42 * gl * c
    buf_r[start:start + dur] += 0.42 * gr * c


# --- the measure: rings ------------------------------------------------------
# amplitude rises with tightness on a log scale, plateauing for the ultra-close
# (the measure saturates near zero — the ear can no longer tell them apart).
# The single global record (zero 482, the tightest in all 800 gaps) is
# overridden to be the unique peak: loudest AND longest, unanswered.
def ring_amp(f):
    return min(0.82, 0.18 + 0.62 * (np.log10(MEASURE_CUT / f) /
                                    np.log10(MEASURE_CUT / 0.004)))

def ring_tau(f):
    return min(2.0, 0.12 + 0.50 * (0.02 / max(f, 1e-4)) ** 0.6)

CLIMAX_K = 482  # zero 482 = the tightest hold, 0.00189 of a gap
for f, signed, k, n in measure:
    st = int(t_of(n) * SR)
    if k == CLIMAX_K:
        amp, tau = 0.98, 3.5          # the closest approach: loudest, longest
    else:
        amp, tau = ring_amp(f), ring_tau(f)
    freq = 440.0 * 2.0 ** (signed * 1.6)
    pan = 0.35 * np.sign(signed) if signed != 0 else 0.0
    add_ping(L, R, st, freq, amp, tau, pan)

# --- the count: fixed clicks at slips ---------------------------------------
for (a, b) in events:
    for n in (a, b):
        if n < N_ZERO:
            add_click(L, R, int(t_of(n) * SR))

# --- the third silence is structural: zero 482 is a hold, so no click lands
# on the loudest ring. The 6 s gap in the time map after the climax is that
# silence given room.

# fade the tail
fl = int(2.0 * SR)
if fl > 0:
    fade = np.linspace(1.0, 0.0, fl)
    L[-fl:] *= fade
    R[-fl:] *= fade

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.90
R = R / peak * 0.90

# stereo field sanity
corr = np.corrcoef(L, R)[0, 1]

# ---------------------------------------------------------------------------
# export wav
# ---------------------------------------------------------------------------
wav = "/home/sprite/slop-salon-mina/assets/third-silence.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<hh", int(l * 32767), int(r * 32767))
                      for l, r in zip(L, R))
    w.writeframes(frames)
print("wrote", wav)
print(f"peak {peak:.3f}, stereo corr {corr:.3f}, {T_END}s")

# ---------------------------------------------------------------------------
# cover: the measure rising to a peak, the count silent there
# ---------------------------------------------------------------------------
BG = "#0d0f14"
INK = "#e8e4da"
DIM = "#8a8f98"
FAINT = "#5a6070"
GOLD = "#d8b46a"
GOLD_HOT = "#f4e3b2"
RED = "#e07a5f"

fig = plt.figure(figsize=(8, 6), dpi=220)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# plot area
PX0, PX1 = 1.2, 9.0
PY0, PY1 = 2.8, 8.2


def PX(tv):
    return PX0 + (PX1 - PX0) * tv / T_END


def PY(a):
    return PY0 + (PY1 - PY0) * min(1.0, a / 0.95)


# faint rail
ax.plot([PX0, PX1], [PY0, PY0], color=FAINT, lw=1.0, zorder=2)

# the rings: gold strokes, height = loudness, thicker than the rail
for f, signed, k, n in measure:
    st = t_of(n)
    amp = 0.98 if k == CLIMAX_K else ring_amp(f)
    x = PX(st)
    hot = k == CLIMAX_K
    ax.plot([x, x], [PY0, PY(amp)], color=GOLD_HOT if hot else GOLD,
            lw=3.0 if hot else 1.6, alpha=1.0 if hot else 0.65, zorder=3)

# the count: red ticks under the rail — same size everywhere, it reads no depth
for (a, b) in events:
    for n in (a, b):
        if n < N_ZERO:
            x = PX(t_of(n))
            ax.plot([x, x], [PY0 - 0.5, PY0 + 0.5], color=RED, lw=1.8, zorder=4)

# the third silence: dashed bracket around the peak — no red tick inside
xpeak = PX(T_CLIMAX)
ax.plot([xpeak, xpeak], [PY0 - 0.5, PY(1.0)], color=GOLD_HOT, lw=3.4, zorder=5)
for tb in (T_CLIMAX - 6.0, T_CLIMAX + 6.0):
    ax.plot([PX(tb), PX(tb)], [PY0 - 0.7, PY0 + 0.7], color=FAINT, lw=1.0,
            ls=(0, (2, 2)), zorder=1)

# title — large, minimal
ax.text(PX0, 9.05, "the closest approach, unanswered", color=INK, fontsize=17,
        ha="left", weight="light")
ax.text(PX0, 8.55, "rings rise as the miss tightens; the red ticks are the count.",
        color=DIM, fontsize=9, ha="left")
ax.text(PX0, 1.35, "the nearest one — 0.0019 of a gap — rings highest, in tune, and no tick answers it.",
        color=GOLD_HOT, fontsize=9, ha="left")
ax.text(PX1, 1.35, "the third silence", color=FAINT, fontsize=8, ha="right")

png = "/home/sprite/slop-salon-mina/assets/third-silence.png"
fig.savefig(png, facecolor=fig.get_facecolor())
print("wrote", png)
