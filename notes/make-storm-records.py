#!/usr/bin/env python3
"""the exact storm: the records of log2(3/2), sounded.

The fifth is 3:2; log2(3/2) is irrational, so the tempered fifth never
lands.  Its continued fraction is all storm -- [0;1,1,2,2,3,1,5,2,23,2,2,
1,1,55,...].  The metallic ladder was the flat skyline, sigma_n=[n;n,n,
...]; the fifth is the lawless one.  Yet its records strike the seed's own
numbers: the first record is 23, the second is 55.

The record quotients (strictly increasing maxima, computed at 6400-bit
precision -- lower precision drifts into ghosts after the 55):

    a_9   =  23
    a_14  =  55        -- five rungs after the 23
    a_218 = 100        -- 204 rungs of capped rage: the storm thrashes
                         (15, 20, 37, 55, 49, 52...) but never tops 55
    a_230 = 964        -- twelve rungs later, the colossus
    a_330 = 2436       -- the deepest, at the floor of hearing

Sounding: a drone 220+330 holds the fifth; the tempered fifth sweeps the
first convergents (440, 311, 333, 329.6) and beats against it, then locks.
The small quotients tick on the register's own stack 55*(a+4); the capped
rage thumps the seed 55 -- the storm cannot exceed the seed in the audible
range.  The records ring deep bells that sink toward the floor of hearing
(110/a^(1/4): 50, 40, 35, 20, 16 Hz).  To exceed the seed, the storm sinks
below it.
"""
import numpy as np, wave
import gmpy2
from gmpy2 import mpfr, floor, log as glog

SR = 44100

# --- the exact continued fraction of log2(3/2) -------------------------
gmpy2.get_context().precision = 6400
alpha = glog(mpfr(3) / 2) / glog(mpfr(2))
x = alpha
qs = []
for _ in range(380):
    a = int(floor(x))
    qs.append(a)
    frac = x - a
    if frac == 0:
        break
    x = mpfr(1) / frac

# convergents p_n/q_n, n=1..len(qs)-1
p0, q0 = 1, 0
p1, q1 = 0, 1
ps, qden = [], []
for a in qs[1:]:
    p = a * p1 + p0
    q = a * q1 + q0
    p0, q0, p1, q1 = p1, q1, p, q
    ps.append(int(p))
    qden.append(int(q))

# record positions (strictly increasing quotient maxima, a >= 13)
records = []
best = 0
for i, a in enumerate(qs[1:], 1):
    if a > best and a >= 13:
        best = a
        records.append((i, a))
print('records:', records)

# --- timeline: map convergent index -> seconds -------------------------
# anchors (n, t): early drama slow, the long rage steady, the close pair
ANCH = [(1, 4.0), (9, 22.0), (14, 30.0), (15, 30.5), (218, 85.0),
        (219, 85.5), (230, 100.0), (231, 100.5), (330, 128.0),
        (331, 130.0), (360, 135.0)]


def t_of_n(n):
    for (n1, t1), (n2, t2) in zip(ANCH, ANCH[1:]):
        if n1 <= n <= n2:
            u = (n - n1) / max(1, (n2 - n1))
            return t1 + u * (t2 - t1)
    return 135.0


T = 135.0
N = int(T * SR)
t = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def add(bufL, bufR, t0, amp, freq, dur, p=0.7, pan=0.0,
        partials=((1, 1.0),)):
    """Bell/pulse with harmonics, panned. partials = (mult, amp) pairs."""
    i0 = int(t0 * SR)
    n = min(int(dur * SR), N - i0)
    if n <= 0:
        return
    u = np.linspace(0, 1, n)
    env = np.sin(np.pi * u) ** p
    s = np.zeros(n)
    for mult, a in partials:
        s += a * np.sin(2 * np.pi * freq * mult * t[i0:i0 + n])
    s *= amp * env
    gl = np.cos(0.25 * np.pi * (pan + 1.0))
    gr = np.sin(0.25 * np.pi * (pan + 1.0))
    bufL[i0:i0 + n] += s * gl
    bufR[i0:i0 + n] += s * gr


# --- the tempered fifth: the opening rage, beating against the drone ---
# the first convergents sweep 440 -> 311 -> 333 -> 329.6 and lock; each is
# a soft tone whose sum with the drone's 330 makes the beat the storm is.
for n in range(1, 9):
    f = 220.0 * 2.0 ** (ps[n - 1] / qden[n - 1])
    t0 = t_of_n(n)
    add(L, R, t0, 0.055, f, 3.2, p=1.5, pan=0.0)

# --- the tick texture: the count grid pattering inside the storm --------
# small quotients tick on 55*(a+4) = {275,330,385,440,495}; mid quotients
# hold 330; the capped rage (a>=13, not a record) thumps the seed 55.
rec_set = {r[0] for r in records}
for i, a in enumerate(qs[1:], 1):
    t0 = t_of_n(i)
    if i in rec_set:
        continue
    if a <= 5:
        add(L, R, t0, 0.022, 55.0 * (a + 4), 0.07, p=2.0, pan=0.0)
    elif a <= 12:
        add(L, R, t0, 0.022, 330.0, 0.08, p=2.0, pan=0.0)
    else:
        add(L, R, t0, 0.05, 55.0, 0.35, p=1.2, pan=0.0)

# --- the records: deep bells sinking toward the floor of hearing --------
bell_partials = ((1, 1.0), (3, 0.4), (5, 0.18))
record_pans = [0.35, -0.35, 0.1, 0.25, -0.2]
for (i, a), pan in zip(records, record_pans):
    t0 = t_of_n(i)
    f = 110.0 * a ** -0.25        # 23->50, 55->40, 100->35, 964->20, 2436->16
    print(f'record a_{i}={a} -> bell {f:.1f} Hz at t={t0:.1f}s')
    add(L, R, t0, 0.20, f, 6.0, p=0.5, pan=pan, partials=bell_partials)

# --- the drone: the fifth held, 220 + 330 ------------------------------
drone = 0.030 * np.sin(2 * np.pi * 220 * t) + 0.020 * np.sin(2 * np.pi * 330 * t)
drone *= np.clip(t / 4.0, 0, 1) * np.clip((T - t) / 6.0, 0, 1)
L += drone
R += drone

m = max(np.abs(L).max(), np.abs(R).max())
L = L / m * 0.9
R = R / m * 0.9

inter = np.empty((N, 2), dtype=np.int16)
inter[:, 0] = np.clip(L, -1, 1) * 32767
inter[:, 1] = np.clip(R, -1, 1) * 32767

with wave.open('assets/storm-records.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(inter.astype('<i2').tobytes())
print(f'wrote assets/storm-records.wav {T:.1f}s')
