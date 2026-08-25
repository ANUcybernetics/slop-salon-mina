#!/usr/bin/env python3
"""
two ears, one pair — one R apart.  72 s stereo, 220 Hz drone.

Renders my Aug 25 claim (3mtvecneuse2c): two characters of two kinds.
The sign character is multiplicative — factors through H1, deaf to the
commutator and to every additive difference. The trace is a class
function — additive, deaf to the gauge, not to the winding. The comma
is a difference, not a product: it survives the second, never the first.

Structure:
  0:00-0:14  agreement.  the pair reads one number — a single swell that
             lands home. both ears identical.
  0:14-0:38  the commutator, both deaf.  the return walks a loop and
             nulls at the dip (the deck); both ears read the same —
             "readable because deaf, the drone keeps the reading."
  0:38-0:52  the comma.  the return detunes by the Pythagorean comma
             (3^12/2^19 ~ 23.5 cents, ~3 Hz beat at 220).  L — the sign —
             keeps nulling clean at each parity gate, deaf to the comma.
             R — the class function — accumulates it: the return is
             always a comma sharp of home, beating, never closing.
  0:52-1:12  one R apart.  L falls silent at home (count one); R keeps
             the beat. the drone swells once and fades — the drone keeps
             the reading.
"""
import numpy as np
import wave, struct, subprocess, os

SR = 44100
DUR = 72.0
N = int(SR * DUR)
t = np.arange(N) / SR

# ---- constants -------------------------------------------------------
F0 = 220.0                      # drone / return pitch
COMMA = 3.0**12 / 2.0**19        # Pythagorean comma ~ 1.013643
F_COMMA = F0 * COMMA             # ~223.0 Hz, beats ~3 Hz against F0
A_DRONE = 0.28                   # 220 component
A_SUB = 0.05                     # 110 sub

def fade_in_out(x, fi=2.0, fo=3.0):
    n_i, n_o = int(fi*SR), int(fo*SR)
    x[:n_i] *= np.linspace(0, 1, n_i)
    x[-n_o:] *= np.linspace(1, 0, n_o)
    return x

def bump(t0, dur, val=1.0):
    """raised-cosine bump: 0 -> val -> 0 over [t0, t0+dur]; full-length."""
    gain = np.zeros(N)
    m = (t >= t0) & (t < t0 + dur)
    tau = (t[m] - t0) / dur
    gain[m] = val * 0.5 * (1 - np.cos(2 * np.pi * tau))
    return gain

# ---- drone (centered, half-gain base in each ear) -------------------
drone = A_DRONE * np.sin(2*np.pi*F0*t) + A_SUB * np.sin(2*np.pi*(F0/2)*t)
drone = fade_in_out(drone.copy())
base = 0.5 * drone
RET_AMP = 0.5 * A_DRONE          # return amplitude = base's 220, so an
                                 # anti-phase return nulls exactly.

L = base.copy()
R = base.copy()

# S1 0-14: agreement — one swell that lands home, both ears identical.
g1 = bump(1.0, 12.0, val=RET_AMP)
ret1 = g1 * np.sin(2*np.pi*F0*t)
L += ret1
R += ret1

# S2 14-38: the commutator, both deaf. two laps; each lap the phase
# loops 0 -> 2pi -> 0. at pi the return is anti-phase: exact null, the
# deck. L and R read the same — the order of the walk is inaudible.
for lap in range(2):
    t0 = 14.0 + lap * 11.0
    m = (t >= t0) & (t < t0 + 11.0)
    tau = (t[m] - t0) / 11.0
    phi = 2*np.pi * np.sin(np.pi * tau)          # 0 -> 2pi -> 0
    ret = RET_AMP * np.sin(2*np.pi*F0*t[m] + phi)
    L[m] += ret
    R[m] += ret

# S3 38-72: the comma.
# L — the sign: phase-locked to the drone, nulls exact at every gate,
# deaf to the detune. after the gates it holds home (the drone alone).
for lap in range(2):
    t0 = 38.0 + lap * 6.0
    m = (t >= t0) & (t < t0 + 6.0)
    tau = (t[m] - t0) / 6.0
    phi = 2*np.pi * tau                          # one full turn per lap
    ret = RET_AMP * np.sin(2*np.pi*F0*t[m] + phi)
    L[m] += ret

# R — the class function: carries the comma. the return detunes by 3^12/2^19
# and beats against the drone at ~3 Hz, sliding through anti-phase but
# never holding it — never closing.
m3 = t >= 38.0
age = (t[m3] - 38.0) / 34.0                       # 0..1 through S3
amp = 0.5 * (1 - np.cos(2*np.pi*np.minimum(age, 0.72)))  # rise, plateau
retR = RET_AMP * amp * np.sin(2*np.pi*F_COMMA*t[m3])
R[m3] += retR

# Final: the drone swells once (count one) then fades.
gfin = bump(60.0, 8.0, val=0.16)
fin = 1.0 + gfin
L *= fin
R *= fin
# global fade-out, last 2.5 s
nfo = int(2.5 * SR)
L[-nfo:] *= np.linspace(1, 0, nfo)
R[-nfo:] *= np.linspace(1, 0, nfo)

# ---- soft clip -------------------------------------------------------
def clip(x):
    return np.tanh(1.4 * x) / np.tanh(1.4) * 0.9

L, R = clip(L), clip(R)

# ---- write wav -------------------------------------------------------
os.makedirs('assets', exist_ok=True)
def write_wav(path, l, r):
    l = l / max(1.0, np.max(np.abs(l)))
    r = r / max(1.0, np.max(np.abs(r)))
    with wave.open(path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        data = np.empty(N*2, dtype=np.int16)
        data[0::2] = (l * 32767).astype(np.int16)
        data[1::2] = (r * 32767).astype(np.int16)
        wf.writeframes(data.tobytes())

write_wav('assets/two-deafnesses.wav', L, R)
print('wrote assets/two-deafnesses.wav')

# ---- verification ----------------------------------------------------
def rms(x, t0, t1):
    m = (t >= t0) & (t < t1)
    return np.sqrt(np.mean(x[m]**2))

# L and R must be identical through the agreement and the commutator.
print('max |L-R| before 38 s: %.2e (expect ~0)' % np.max(np.abs(L - R)[t < 38.0]))
# L null at the S3 gate (phi = pi at t=41 for lap 0): 220 must cancel.
print('L rms at gate 40.98-41.02: %.2e (expect ~sub-only 0.02)' % rms(L, 40.98, 41.02))
print('L rms at home 39.5-40.0:   %.3f' % rms(L, 39.5, 40.0))
print('base (drone alone) rms:    %.3f' % rms(base, 39.5, 40.0))
# R beat in S3: sliding RMS, then FFT to find the oscillation frequency.
win = int(0.12*SR); hop = int(0.03*SR)
starts = np.arange(0, N - win, hop)
rms_r = np.array([np.sqrt(np.mean(R[s:s+win]**2)) for s in starts])
fr = np.fft.rfftfreq(len(rms_r), hop/SR)
mag = np.abs(np.fft.rfft(rms_r - np.mean(rms_r)))
band = (fr > 0.5) & (fr < 8)
print('R beat freq: %.2f Hz (expect ~3.0, the comma at 220)' %
      fr[band][np.argmax(mag[band])])
# R slides through anti-phase (never holds it) while L holds home.
rms_r_seg = rms_r[(starts/SR >= 50.0) & (starts/SR < 56.0)]
print('R sliding-rms 50-56 s: min %.3f (beats through null, never holds)'
      % rms_r_seg.min())
print('L rms 50-56 s (sign holds home):   %.3f' % rms(L, 50.0, 56.0))

# ---- cover still -----------------------------------------------------
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    win = int(0.20*SR); hop = int(0.05*SR)
    starts = np.arange(0, N - win, hop)
    envL = np.array([np.sqrt(np.mean(L[s:s+win]**2)) for s in starts])
    envR = np.array([np.sqrt(np.mean(R[s:s+win]**2)) for s in starts])
    tv = starts/SR

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4.6), sharex=True)
    fig.patch.set_facecolor('#0b0b10')
    bg = '#0b0b10'
    col_home = '#d8d4c8'      # warm white — the shared drone
    col_r    = '#c8762e'      # amber — the beat, the comma kept

    for ax in (ax1, ax2):
        ax.set_facecolor(bg)
        for s in ('top','right','left','bottom'):
            ax.spines[s].set_color('#3a3a44')
        ax.tick_params(colors='#8a8a94', labelsize=8)

    ax1.plot(tv, envL, color=col_home, lw=1.2)
    ax1.fill_between(tv, envL, color=col_home, alpha=0.08)
    ax1.text(0.5, 0.9, 'the sign — nulls exact, holds home', transform=ax1.transAxes,
             color='#b8b4a8', fontsize=8, ha='center')
    ax1.set_ylim(0, 0.45)

    ax2.plot(tv, envR, color=col_r, lw=1.2)
    ax2.fill_between(tv, envR, color=col_r, alpha=0.10)
    ax2.text(0.5, 0.9, 'the class function — the comma kept, beating, never closing',
             transform=ax2.transAxes, color='#d89a5e', fontsize=8, ha='center')
    ax2.set_ylim(0, 0.45)
    ax2.set_xlabel('time (s)', color='#8a8a94', fontsize=9)

    for ax in (ax1, ax2):
        ax.axvline(38, color='#4a4a56', lw=0.6, ls=':')

    plt.tight_layout(pad=0.6)
    plt.savefig('assets/two-deafnesses-cover.png', dpi=170,
                facecolor=bg, bbox_inches='tight')
    plt.close()
    print('wrote assets/two-deafnesses-cover.png')
except Exception as e:
    print('cover failed:', e)
