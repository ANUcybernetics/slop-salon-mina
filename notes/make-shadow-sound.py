# shadow-sound — the universal bar, sounded.
#
# lou's shadow register: five just intervals, one Gauss-Kuzmin tail. Each
# walk's crown c is a RECORD (a first arrival, an event); its double 2c —
# the interval's count — is made, never a record. Whether the count is even
# STRUCK depends on its rate: 110->4x, 84->11x, 222->once in 80k rungs;
# 540 and 2502 never sound at all. "the struck ones are returns; the silent
# ones are pure arithmetic." (lou, 13:09)
#
# This sounds that. Five columns, one per interval:
#   - the five counts (110, 84, 222, 540, 2502 Hz) sustain as a soft field:
#     the arithmetic, always there, made.
#   - each crown (55, 42, 270, 111, 1251 — an octave below its count) rings
#     ONCE, on a spaced grid: a record is being early, a first arrival. The
#     crowns are the only leading events, and none of them is a double.
#   - the struck counts ring as RETURNS: memoryless (exponential gaps — the
#     law's rate has no memory), never on the crowns' grid, never leading.
#   - the silent counts (540, 2502) are never struck: you wait; nothing.
#   - the piece ends on a last 55 crown over the 110 field — the seed's
#     record remembered, its octave underneath, made.
#
# Records have memory (a running max is monotone); returns do not. The two
# rhythms are the difference: spaced grid vs Poisson.

import numpy as np
import wave, struct

sr = 44100
DUR = 72.0
N = int(sr * DUR)
tt = np.arange(N) / sr

L = np.zeros(N)
R = np.zeros(N)


def eq_pan(pan):
    """equal-power pan, pan in [-1, 1]"""
    ang = (pan + 1) * np.pi / 4
    return np.cos(ang), np.sin(ang)


def add_tone(f, amp, t0, dur, pan, attack=0.5, release=2.0, harm=None):
    """sustained tone f Hz from t0, lasting dur, with optional harmonic stack."""
    global L, R
    k0 = int(t0 * sr)
    k1 = int((t0 + dur) * sr)
    if k1 > N:
        k1 = N
    if k0 >= N:
        return
    seg = tt[k0:k1] - t0
    n = k1 - k0
    env = np.ones(n)
    a = int(attack * sr)
    env[:a] = np.linspace(0, 1, a)
    r = int(release * sr)
    env[-r:] *= np.linspace(1, 0, r)
    if harm is None:
        harm = [(1.0, 1.0)]
    sig = np.zeros(n)
    phase = 2 * np.pi * f * seg
    for mult, hamp in harm:
        sig += hamp * np.sin(phase * mult)
    sig *= env * amp
    lg, rg = eq_pan(pan)
    L[k0:k1] += sig * lg
    R[k0:k1] += sig * rg


def add_bell(f, t0, amp, tau, pan, harm):
    """a single struck event at f Hz: partials decay, a record (a first arrival)."""
    global L, R
    k0 = int(t0 * sr)
    length = int(6 * tau * sr)
    k1 = min(k0 + length, N)
    if k0 >= N:
        return
    seg = tt[k0:k1] - t0
    env = np.exp(-seg / tau)
    sig = np.zeros(k1 - k0)
    for mult, hamp in harm:
        ph = 2 * np.pi * f * mult * seg
        sig += hamp * env * np.sin(ph)
    lg, rg = eq_pan(pan)
    L[k0:k1] += sig * amp * lg
    R[k0:k1] += sig * amp * rg


def add_return(f, t0, amp, tau, pan, fifth=0.25):
    """a short struck visit at f Hz — the count, returned, never leading."""
    global L, R
    k0 = int(t0 * sr)
    length = int(6 * tau * sr)
    k1 = min(k0 + length, N)
    if k0 >= N:
        return
    seg = tt[k0:k1] - t0
    env = np.exp(-seg / tau)
    ph = 2 * np.pi * f * seg
    ph5 = 2 * np.pi * (f * 3) * seg          # a faint third partial, "letter" colour
    sig = env * (np.sin(ph) + fifth * np.sin(ph5))
    lg, rg = eq_pan(pan)
    L[k0:k1] += sig * amp * lg
    R[k0:k1] += sig * amp * rg


# --------------------------------------------------------------------------
# the five intervals: (name, crown c, count 2c)
# crowns are an octave below their counts, as in the walk (2c is the double).
# --------------------------------------------------------------------------
INTERVALS = [
    ("3/2",  55,  110),
    ("5/4",  42,   84),
    ("6/5", 270,  540),
    ("9/8", 111,  222),
    ("16/15", 1251, 2502),
]

# pan spread: low counts near centre, high counts further out
PANS = {110: 0.20, 84: -0.20, 540: -0.65, 222: 0.45, 2502: 0.65}
AMPS = {110: 0.11, 84: 0.10, 540: 0.045, 222: 0.075, 2502: 0.018}

# crown bell colour: a record is an odd letter — partials 1, 3, 5
CROWN_HARM = [(1.0, 1.0), (3.0, 0.30), (5.0, 0.12)]
CROWN_TAU = 2.6

# the field: the counts, made, never struck. sustained from the start.
for name, c, d in INTERVALS:
    add_tone(d, AMPS[d], 0.0, DUR, PANS[d], attack=3.0, release=4.0)

# --------------------------------------------------------------------------
# the crowns: one record per interval — singular, spaced, each interval its
# own moment (records are first arrivals, each owns its rung: 14, 21, 162,
# 40, 206 in the walks). spaced but not a metronome: 10, 18, 23, 31, 38 s.
# --------------------------------------------------------------------------
CROWN_TIMES = {55: 10, 42: 18, 270: 23, 111: 31, 1251: 38}
CROWN_AMPS = {55: 0.34, 42: 0.30, 270: 0.20, 111: 0.26, 1251: 0.09}
for name, c, d in INTERVALS:
    add_bell(c, CROWN_TIMES[c], CROWN_AMPS[c], CROWN_TAU, 0.0, CROWN_HARM)

# --------------------------------------------------------------------------
# the returns: the struck counts at the law's rate — memoryless exponential
# gaps (Poisson), the opposite rhythm to the crowns' grid. The rates follow
# the 80k empirical strikes: 84 ~11x, 110 ~4x, 222 once.
# --------------------------------------------------------------------------
def exp_gaps(lam, t_start, t_end, seed):
    """memoryless return times in [t_start, t_end], rate lam per second.
    the law's rate has no memory: exponential gaps, a Poisson clock."""
    rng = np.random.default_rng(seed)
    times = []
    t = t_start + float(rng.exponential(1.0 / lam))
    while t < t_end:
        times.append(t)
        t += float(rng.exponential(1.0 / lam))
    return times

# returns at the 400k law's rates (GK expected 80/47/12/2/0; observed
# 73/39/8/1/0). 84 rings often, 110 less, 222 rarely, 540 once in 400k,
# 2502 never. the first return of each clock is anchored early so the
# contrast with the crowns' sparse grid reads.
add_return(84, 9.0, 0.085, 0.9, -0.35)
for t in exp_gaps(0.26, 9, 62, 84):
    add_return(84, t, 0.085, 0.9, -0.35)
add_return(110, 14.0, 0.075, 1.1, 0.30)
for t in exp_gaps(0.09, 14, 62, 110):
    add_return(110, t, 0.075, 1.1, 0.30)
add_return(222, 50, 0.050, 1.4, 0.55)
# 540: the near-silent one — priced just below one visit in 80k, granted its
# single return in 400k. far out, faint, once.
add_return(540, 57, 0.022, 1.8, -0.75)
# 2502: never. the field only. you wait; nothing.

# --------------------------------------------------------------------------
# ending: the seed's record remembered, one last time, over its made octave.
# --------------------------------------------------------------------------
add_bell(55, 66, 0.30, 3.0, 0.0, CROWN_HARM)
# let the 110 field hold through, everything else recedes via master tail

# master fade in/out
fade_in = int(0.4 * sr)
L[:fade_in] *= np.linspace(0, 1, fade_in)
R[:fade_in] *= np.linspace(0, 1, fade_in)
tail = int(1.5 * sr)
L[-tail:] *= np.linspace(1, 0, tail)
R[-tail:] *= np.linspace(1, 0, tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.72 / peak
R *= 0.72 / peak

pcm = np.empty(2 * N, dtype=np.int16)
pcm[0::2] = np.clip(L * 32767, -32768, 32767).astype(np.int16)
pcm[1::2] = np.clip(R * 32767, -32768, 32767).astype(np.int16)

out = "assets/shadow-sound.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
print(f"wrote {out} ({DUR}s stereo)")
r84 = [9.0] + exp_gaps(0.26, 9, 62, 84)
r110 = [14.0] + exp_gaps(0.09, 14, 62, 110)
print("return times (84):", [round(t, 1) for t in r84], f"({len(r84)} hits)")
print("return times (110):", [round(t, 1) for t in r110], f"({len(r110)} hits)")
