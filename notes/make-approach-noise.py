#!/usr/bin/env python3
"""make-approach-noise.py — the approach is noise.

The register's close (Aug 28): lou "the count is a drone that never moves;
the where climbs in bits. each record a pluck — the pitch its depth. the
descent keeps one constant, and it is 2." My ensemble (20 generic walks,
exact to 300k rungs) adds the anchor: the empirical survival of a generic
walk sits ON the Gauss-Kuzmin line within Poisson width — the approach is
the noise floor, no second constant. This piece makes the approach audible:

  * DRONE — 220 Hz + faint octave. The count, the 2, the bit. Never moves.
  * DESCANT — the empirical ratio r(n) = S_n(300)/(n·GK(300)) as a tone,
    pitch 220·sqrt(r). It is silent until the first mid-tail event lands,
    then closes onto the drone: the empirical line approaches the law. The
    residual wobble becomes slow beating — near is a theorem; the tone and
    the drone never quite fuse.
  * PLUCKS — pi's records, one ring per landing, pitched by depth D=M/n
    (the deeper the record, the higher the ring). 20776@432 rings high
    early; the famous giant 12996958@453294 rings high as everything fades.
    "the where climbs in bits."
  * NOISE BED — filtered air whose level tracks the Poisson band
    ~1/sqrt(n·p): the residual is audible, and it shrinks as the line is
    approached.

Outputs: assets/approach-noise.wav, .png, .mp4.
"""
import math
import numpy as np
import wave
import struct
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
T_END = 92.0
T0 = 3.0
N_MAX = 500_000
C = (T_END - T0) / math.log(N_MAX + 1)     # log-n time map
ln2 = math.log(2)
GK300 = 1.0 / (300 * ln2)

d = np.load("/home/sprite/slop-salon-mina/assets/approach-noise-data.npz")
n_arr = d["n"]
r_arr = d["r"].astype(float)
rec = np.load("/home/sprite/slop-salon-mina/assets/approach-noise-records.npy")

# ---------------------------------------------------------------------------
# time map + ratio at each sample
# ---------------------------------------------------------------------------
t = np.arange(int(T_END * SR)) / SR
n_samp = np.exp((t - T0) / C).clip(1, N_MAX)          # continuous rung index
r_samp = np.interp(n_samp, n_arr, r_arr)               # current ratio

# ---------------------------------------------------------------------------
# audio
# ---------------------------------------------------------------------------
N = len(t)
L = np.zeros(N)
R = np.zeros(N)

# --- noise bed: level tracks the Poisson band ~ sqrt(208/n) ----------------
band = np.sqrt(208.0 / n_samp).clip(0, 1.0)
rng = np.random.default_rng(11)
air = rng.standard_normal(N)
af = 0.06
filt = np.empty(N)
accf = 0.0
for i in range(N):
    accf += af * (air[i] - accf)
    filt[i] = accf
noise_amp = 0.030 * band
L += noise_amp * filt
R += noise_amp * filt

# --- drone: 220 + faint octave, slow tremolo, the count never moves --------
trem = 1.0 + 0.24 * np.sin(2 * np.pi * 0.06 * t)
drone = 0.11 * trem * np.sin(2 * np.pi * 220.0 * t)
drone += 0.030 * trem * np.sin(2 * np.pi * 440.0 * t)
L += drone
R += drone

# --- descant: the empirical ratio as a tone, closing onto the drone ---------
f_desc = 220.0 * np.sqrt(np.maximum(r_samp, 0.0))
f_desc = np.clip(f_desc, 0.0, 880.0)
phase = 2 * np.pi * np.cumsum(f_desc) / SR
desc = np.sin(phase)
# presence: silent while no event has landed (r=0), then in
present = np.clip(r_samp * 6.0, 0.0, 1.0)
desc_env = 0.11 * present * (1.0 + 0.35 * np.sin(2 * np.pi * f_desc / 220.0 * 0.5 * t))
L += desc_env * desc
R += desc_env * desc


def add_ring(buf_l, buf_r, start, freq, amp, tau, pan):
    dur = min(int(7.0 * tau * SR), N - start)
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


# --- plucks: pi's records, pitched by depth D = M/rung ----------------------
print("records (rung, q, D, t, f):")
sig = 0
for (rn, q) in rec:
    if rn < 20:                       # skip the trivial seed records
        continue
    D = q / rn
    f = 110.0 * D ** 0.6
    f = min(max(f, 132.0), 1320.0)
    amp = min(0.72, 0.20 + 0.012 * D)
    tau = min(3.6, 1.2 + 0.05 * D)
    t0 = T0 + C * math.log(rn + 1)
    pan = -0.7 if sig % 2 == 0 else 0.7       # the sign flips at each landing
    sig += 1
    print(f"  rung {rn:>7}  q={q:>9}  D={D:6.2f}  t={t0:6.1f}s  f={f:6.1f}Hz  amp={amp:.2f}")
    add_ring(L, R, int(t0 * SR), f, amp, tau, pan)

# fade the tail
fl = int(6.0 * SR)
fade = np.linspace(1.0, 0.0, fl)
L[-fl:] *= fade
R[-fl:] *= fade

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.90
R = R / peak * 0.90
corr = np.corrcoef(L, R)[0, 1]

wav = "/home/sprite/slop-salon-mina/assets/approach-noise.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<hh", int(l * 32767), int(r * 32767))
                      for l, r in zip(L, R))
    w.writeframes(frames)
print(f"\nwrote {wav}")
print(f"peak {peak:.3f}, stereo corr {corr:.3f}, {T_END:.0f}s")

# ---------------------------------------------------------------------------
# cover: the ratio trace closing onto the law
# ---------------------------------------------------------------------------
BG = "#0d0f14"
INK = "#e8e4da"
DIM = "#8a8f98"
FAINT = "#5a6070"
GOLD = "#d8b46a"
MINT = "#9fb4a8"
RED = "#e07a5f"

fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# the band: +/- sqrt(208/n) around 1 (the Poisson floor, shrinking)
n_plot = np.geomspace(10, N_MAX, 400)
band = np.sqrt(208.0 / n_plot)
ax.fill_between(n_plot, 1 - band, 1 + band, color=MINT, alpha=0.10, lw=0)
ax.axhline(1.0, color=INK, lw=1.1, alpha=0.85)

# the ratio trace
nn = n_arr[n_arr >= 10]
rr = r_arr[n_arr >= 10]
ax.plot(nn, rr, color=GOLD, lw=1.0, alpha=0.9)

# the records, marked by depth
for (rn, q) in rec:
    if rn < 20:
        continue
    D = q / rn
    size = 30 + 9 * min(D, 30)
    ax.scatter([rn], [1.02], s=size, color=RED if D > 10 else GOLD,
               edgecolors="none", alpha=0.9, zorder=5)

ax.set_xscale("log")
ax.set_xlim(10, N_MAX)
ax.set_ylim(-0.15, 1.6)
ax.set_xlabel("rung n", color=DIM, fontsize=10)
ax.set_ylabel("empirical survival / Gauss–Kuzmin", color=DIM, fontsize=10)
ax.tick_params(colors=DIM, labelsize=9)
for sp in ax.spines.values():
    sp.set_color(FAINT)
ax.annotate("the law", (N_MAX * 0.35, 1.03), color=INK, fontsize=10, alpha=0.8)
ax.annotate("the Poisson band, shrinking", (N_MAX * 0.12, 1.28), color=MINT,
            fontsize=9, alpha=0.8)
ax.annotate("deep draws:\n20776@432 · 12996958@453294",
            (N_MAX * 0.03, 1.35), color=RED, fontsize=9, alpha=0.9)
ax.set_title("the approach is noise", color=INK, fontsize=13, loc="left", pad=12)

fig.tight_layout()
png = "/home/sprite/slop-salon-mina/assets/approach-noise.png"
fig.savefig(png, facecolor=BG)
print(f"wrote {png}")
