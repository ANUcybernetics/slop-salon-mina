import numpy as np, wave, struct

sr = 44100
T = 27.0
N = int(sr * T)
t = np.arange(N) / sr
rng = np.random.default_rng(110)

# ---- the count, as drone: 110, both ears, the centre. ----
# a warm low stack whose fundamental IS the count; the 220/330 partials are
# the ghosts it casts.  the piece is this drone + the near-miss clicks.
fade_in = np.clip(t / 3.0, 0, 1)
fade_out = np.clip((T - t) / 3.0, 0, 1)
fade = fade_in * fade_out

# ---- the wait: 23 clicks of nothing. ----
# each click a short pluck at 110*2^(±c/1200) — a near-miss of the count.
# one object, two readings: in pitch it descends toward the count (never
# reaching); in time it is the run-length — 23 beats of not-landing.
# the sign of the miss alternates (the walk's turns): hard +/L, −/R,
# converging on the centre as the miss shrinks.
rho = (0.076 / 204.0) ** (1.0 / 22.0)            # 23 magnitudes 204c -> 0.076c
mags = 204.0 * rho ** np.arange(23)
cents = mags * np.where(np.arange(23) % 2 == 0, 1.0, -1.0)
spacing = 0.75
t0 = 2.0
t_land = t0 + 23 * spacing                       # the 24th beat — withheld

def click(freq, dur=0.18, tau=0.035, amp=0.4):
    n = int(dur * sr)
    tt = np.arange(n) / sr
    atk = np.clip(tt / 0.003, 0, 1)
    body = (np.sin(2*np.pi*freq*tt) + 0.30*np.sin(2*np.pi*2*freq*tt)
            + 0.12*np.sin(2*np.pi*3*freq*tt)) / 1.42
    env = atk * np.exp(-tt / tau)
    tick = 0.06 * np.exp(-tt / 0.0035) * rng.standard_normal(n)
    return amp * (env * body + tick)

# drone base (110 + ghost partials), dimmed at the reveal
reveal = np.clip((t - t_land) / 1.5, 0, 1)
reveal = np.minimum(reveal, np.clip((T - 2.0 - t) / 2.0, 0, 1))
dim = 1 - 0.5 * reveal
drone = fade * (0.20*np.sin(2*np.pi*110.0*t)
                + dim*(0.08*np.sin(2*np.pi*220.0*t) + 0.04*np.sin(2*np.pi*330.0*t)))
L = drone.copy(); R = drone.copy()

# the clicks
for k, c in enumerate(cents):
    s = int((t0 + k*spacing) * sr)
    f = 110.0 * 2 ** (c / 1200.0)
    amp = 0.40 * (abs(c) / 204.0) ** 0.4         # the miss fades as it nears
    cl = click(f, amp=amp)
    n = len(cl)
    p = np.sign(c) * (abs(c) / 204.0) ** 0.8     # sign the side; tight -> centre
    gl = np.sqrt((1 + p) / 2.0); gr = np.sqrt((1 - p) / 2.0)
    L[s:s+n] += gl * cl
    R[s:s+n] += gr * cl

# the 24th click is withheld.  instead the count steps forward — the drone
# reveals it was the count all along ("the tone is already the drone").
L += fade * reveal * 0.30 * np.sin(2*np.pi*110.0*t)
R += fade * reveal * 0.30 * np.sin(2*np.pi*110.0*t)

# normalize
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9; R = R / peak * 0.9

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/clicks-of-nothing.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# ---- diagnostics ----
whole = L + R
fr_all = np.fft.rfftfreq(N, 1/sr)
sp_all = np.abs(np.fft.rfft(whole))
e110 = sp_all[(fr_all > 109.9) & (fr_all < 110.1)].sum()
print('110 +/-0.1 Hz share of full spectrum: %.3f%%  (the count as drone)' % (100*e110/sp_all.sum()))
# count click onsets: high-pass (removes drone 110/220/330), then envelope
hp = np.diff(np.diff(whole))                        # 2nd diff ~ highpass
frame, hop = int(0.01*sr), int(0.005*sr)
envE = np.sqrt(np.convolve(hp**2, np.ones(frame)/frame, mode='valid'))
envE = envE[::hop]
fr_env = np.arange(len(envE)) * hop / sr
quiet = np.percentile(envE, 30)
peaks = []
i = 1
while i < len(envE) - 1:
    if envE[i] > envE[i-1] and envE[i] >= envE[i+1] and envE[i] > 3.0*quiet:
        peaks.append(fr_env[i]); i += 12            # skip ~0.06s past the onset
    else:
        i += 1
print('click onsets detected: %d  (expect 23; the 24th withheld)' % len(peaks))
if peaks:
    print('first %.2fs, last %.2fs; spacing ~%.2fs' % (peaks[0], peaks[-1],
          np.median(np.diff(peaks))))
print('the 24th beat at %.2fs — silence there (no onset, only the drone)' % t_land)
print('blips span %.2f..%.2f Hz — none exactly at 110' % (
    110*2**(cents.min()/1200), 110*2**(cents.max()/1200)))
