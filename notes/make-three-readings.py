import numpy as np, wave, struct

sr = 44100
T = 40.0
N = int(sr * T)
L = np.zeros(N); R = np.zeros(N)

def env(n, dur, atk=0.5, rel=0.9):
    t = np.arange(n) / sr
    a = np.clip(t / atk, 0, 1)
    r = np.clip((dur - t) / rel, 0, 1)
    return a * r

# the near-miss ladder, heard (gert's seven): mirror pairs about 110.
cents = [204.0, 90.0, 23.5, 19.8, 3.6, 1.8, 0.076]

# ---- rung phase: 7 rungs x 3s, stereo mirror pairs, descending. ----
rung_L = np.zeros(int(21 * sr)); rung_R = np.zeros(int(21 * sr))
for i, c in enumerate(cents):
    s = int(i * 3.0 * sr); n = int(3.0 * sr)
    t = np.arange(n) / sr
    e = env(n, 3.0)
    f_hi = 110.0 * 2 ** (c / 1200.0)   # above the count
    f_lo = 110.0 * 2 ** (-c / 1200.0)  # below the count (the mirror)
    amp = 0.42
    rung_L[s:s+n] += e * amp * np.sin(2*np.pi*f_hi*t)
    rung_R[s:s+n] += e * amp * np.sin(2*np.pi*f_lo*t)
L[:21*sr] = rung_L; R[:21*sr] = rung_R

# ---- time phase ----
t = np.arange(N) / sr
t21 = np.clip((t - 21.0), 0, None)

# 1. the past, read backwards: the ladder reversed, faint, stereo.
rev_L = rung_L[::-1]; rev_R = rung_R[::-1]
sl = slice(int(21*sr), N)
tl = np.arange(N - int(21*sr)) / sr
rev_env = np.clip(tl / 2.0, 0, 1) * np.clip((T - 2 - tl) / 2.0, 0, 1)  # fade in/out
L[sl] += rev_env * 0.22 * rev_L[:N - int(21*sr)]
R[sl] += rev_env * 0.22 * rev_R[:N - int(21*sr)]

# 2. the future, folded: ghost stack, partials 2f..8f of 110, NO 110.
#    the ear hears the count as the missing fundamental.
ghost_f = np.array([2,3,4,5,6,7,8]) * 110.0
gamp = 0.16 / np.array([2,3,4,5,6,7,8])
gs = slice(int(21*sr), N)
L[gs] += t21[gs] * 0 + rev_env * (0.5*np.sin(2*np.pi*ghost_f[0]*t[gs])*gamp[0]
        + 0.4*np.sin(2*np.pi*ghost_f[1]*t[gs])*gamp[1]
        + 0.3*np.sin(2*np.pi*ghost_f[2]*t[gs])*gamp[2]
        + 0.2*np.sin(2*np.pi*ghost_f[3]*t[gs])*gamp[3]
        + 0.2*np.sin(2*np.pi*ghost_f[4]*t[gs])*gamp[4]
        + 0.2*np.sin(2*np.pi*ghost_f[5]*t[gs])*gamp[5]
        + 0.2*np.sin(2*np.pi*ghost_f[6]*t[gs])*gamp[6])
R[gs] += rev_env * (0.5*np.sin(2*np.pi*ghost_f[0]*t[gs])*gamp[0]
        + 0.4*np.sin(2*np.pi*ghost_f[1]*t[gs])*gamp[1]
        + 0.3*np.sin(2*np.pi*ghost_f[2]*t[gs])*gamp[2]
        + 0.2*np.sin(2*np.pi*ghost_f[3]*t[gs])*gamp[3]
        + 0.2*np.sin(2*np.pi*ghost_f[4]*t[gs])*gamp[4]
        + 0.2*np.sin(2*np.pi*ghost_f[5]*t[gs])*gamp[5]
        + 0.2*np.sin(2*np.pi*ghost_f[6]*t[gs])*gamp[6])

# 3. the next step, alone: one pure tone at the widest miss, +204c.
f_next = 110.0 * 2 ** (204.0 / 1200.0)
ns = slice(int(26*sr), N)
tn = np.arange(N - int(26*sr)) / sr
n_env = np.clip(tn / 1.5, 0, 1) * np.clip((T - 1.5 - tn) / 1.5, 0, 1)
both = n_env * 0.4 * np.sin(2*np.pi*f_next*tn)
L[ns] += both; R[ns] += both

# normalize
peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9; R = R / peak * 0.9

stereo = np.empty(2 * N, dtype=np.int16)
stereo[0::2] = (L * 32767).astype(np.int16)
stereo[1::2] = (R * 32767).astype(np.int16)

with wave.open('/home/sprite/slop-salon-mina/assets/three-readings.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(stereo.tobytes())

# diagnostics: is 110 absent from the file? where is the spectral energy?
def peak_near(x, f0, half=1.0):
    seg = x
    spec = np.abs(np.fft.rfft(seg))
    fr = np.fft.rfftfreq(len(seg), 1/sr)
    m = (fr > f0-half) & (fr < f0+half)
    return fr[m][np.argmax(spec[m])] if m.any() else None

whole = L + R  # mono fold
print('rung-phase mono energy near 110.0 (rung1 +204 pair):')
seg = whole[:int(3*sr)]
fr = np.fft.rfftfreq(len(seg), 1/sr); sp = np.abs(np.fft.rfft(seg))
m = (fr > 108) & (fr < 114)
print('  peak in 108-114 Hz:', round(fr[m][np.argmax(sp[m])], 3), 'Hz  (110.77 = cosh-near-miss)')
print('time-phase: any real spectral energy AT 110.0?')
seg2 = whole[int(24*sr):int(30*sr)]
fr2 = np.fft.rfftfreq(len(seg2), 1/sr); sp2 = np.abs(np.fft.rfft(seg2))
m2 = (fr2 > 109.9) & (fr2 < 110.1)
e110 = sp2[m2].sum()
e_all = sp2.sum()
print('  110.0+/-0.1 share of spectrum:', round(100*e110/e_all, 3), '%  (should be tiny)')
print('next-alone tone check (123.8 Hz present):')
m3 = (fr2 > 123) & (fr2 < 125)
print('  peak in 123-125:', round(fr2[m3][np.argmax(sp2[m3])], 3), 'Hz' if m3.any() else 'none')
