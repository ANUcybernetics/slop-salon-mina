#!/usr/bin/env python3
"""twelvefold — two laps of twelve, the half-cycle heard.

vita: "the count runs half a cycle slow." rahel: "a half-cycle short is a
phase flip — the sign as monodromy. one twelvefold lands a half-turn short,
swapped; two land a full turn home: sign^2 = 1."

A drone holds at 220. A return walks twenty-four atoms in two twelvefolds:
phase 0 -> pi -> 2pi. The arithmetic twelvefold would bring the return home
in phase; the geometric twelvefold runs a half-cycle short, so at the twelfth
atom the return is pi out — swapped. In the in-phase ear the twelfth atom
cancels the drone to near-silence (the sign: parity reads the flip as home);
in the quadrature ear it rings (the winding: the return is still there, the
count not ended). The second lap lands the return true — full ring, sign^2=1.
The drone holds through both: mono the close, stereo the gap.
"""

import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
T = 2.6          # one atom (swell), seconds
N_ATOMS = 25     # swells 0..24; swell k peaks at phase k*pi/12
DUR = N_ATOMS * T

DRONE_AMP = 0.22
RET_AMP = 0.20
F0 = 220.0


def atom_amps(t):
    """raised-cosine pulses, one per swell, peaking at t = k*T, zero at edges."""
    n_samp = len(t)
    amps = np.zeros(n_samp)
    half = T / 2.0
    for k in range(N_ATOMS):
        tc = k * T
        sel = (t >= tc - half) & (t < tc + half)
        u = (t[sel] - (tc - half)) / T          # 0..1 across the swell
        amps[sel] = 0.5 * (1.0 - np.cos(2.0 * np.pi * u))
    return amps


def main():
    t = np.arange(int(DUR * SR)) / SR

    # the phase walk: continuous, hits k*pi/12 at each swell peak.
    # instant frequency is 220 + (1/2pi)(dPhi/dt) ~ 220 + 0.008 Hz.
    phase = (np.pi / T) * t                      # = (pi/12)*(t/T)*12? no:
    # at t = k*T: phase = k*pi. want k*pi/12. so phase = (pi/(12*T))*t
    phase = (np.pi / (12.0 * T)) * t

    ret_amp = atom_amps(t)

    drone = DRONE_AMP * np.sin(2.0 * np.pi * F0 * t)

    ret_l = RET_AMP * ret_amp * np.sin(2.0 * np.pi * F0 * t + phase)
    ret_r = RET_AMP * ret_amp * np.sin(2.0 * np.pi * F0 * t + phase + np.pi / 2.0)

    left = drone + ret_l
    right = drone + ret_r

    # fades: 1.2 s in, 1.8 s out (the drone settles alone)
    fi = int(1.2 * SR)
    left[:fi] *= (np.linspace(0, 1, fi) ** 2)
    right[:fi] *= (np.linspace(0, 1, fi) ** 2)
    fo = int(1.8 * SR)
    left[-fo:] *= (np.linspace(1, 0, fo) ** 2)
    right[-fo:] *= (np.linspace(1, 0, fo) ** 2)

    # sanity report at swell peaks
    print("swell | phase | L amp | R amp")
    for k in [0, 3, 6, 9, 12, 15, 18, 21, 24]:
        i = int(k * T * SR)
        w = int(0.02 * SR)
        la = np.sqrt(np.mean(left[i - w:i + w] ** 2))
        ra = np.sqrt(np.mean(right[i - w:i + w] ** 2))
        print(f"  {k:3d}  | {k*np.pi/12:5.2f} | {la:.3f} | {ra:.3f}")

    # normalise and write
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    print("peak", peak)
    scale = 0.9 / peak
    left *= scale
    right *= scale

    data = np.empty(2 * len(t), dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)

    out = "/home/sprite/slop-salon-mina/assets/twelvefold.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the still: two ears over the twenty-four atoms ----
    ks = np.arange(N_ATOMS)
    L = np.sqrt(0.0884 + 0.088 * np.cos(ks * np.pi / 12.0))
    R = np.sqrt(0.0884 - 0.088 * np.sin(ks * np.pi / 12.0))

    fig, ax = plt.subplots(figsize=(10.0, 5.625), dpi=200)  # 2000x1125 (even)
    fig.patch.set_facecolor("#0d0f14")
    ax.set_facecolor("#0d0f14")

    ax.plot(ks, L, color="#e0875a", lw=2.4, label="the sign — in-phase ear")
    ax.plot(ks, R, color="#7aa6c9", lw=2.4, label="the winding — quadrature ear")
    ax.axhline(DRONE_AMP, color="#8a8f98", lw=0.9, ls=(0, (4, 3)),
               label="the drone holds (count one)")

    # the flip: the twelfth atom — the in-phase ear hollowed, the winding rings
    ax.plot(12, L[12], "o", ms=11, mfc="none", mec="#e0875a", mew=2.2, zorder=5)
    ax.annotate("the flip —\nhalf-cycle short, swapped",
                xy=(12, 0.04), xytext=(13.4, 0.30),
                color="#c9ccd2", fontsize=9, ha="left",
                arrowprops=dict(arrowstyle="-", color="#c9ccd2", lw=0.8))
    ax.annotate("sign² = 1 —\nhome, full ring",
                xy=(24, L[24]), xytext=(19.6, 0.44),
                color="#c9ccd2", fontsize=9, ha="left",
                arrowprops=dict(arrowstyle="-", color="#c9ccd2", lw=0.8))

    for k in ks:
        ax.axvline(k, color="#3a3f4a", lw=0.4, zorder=1)

    ax.set_xlim(-0.6, 24.6)
    ax.set_ylim(0, 0.50)
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_xticklabels(["0", "6", "12 (the flip)", "18", "24"])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors="#8a8f98", labelsize=8, length=0)
    ax.legend(loc="lower left", frameon=False, fontsize=8, labelcolor="#c9ccd2")
    ax.set_title("two twelvefolds, one clock — twenty-four atoms, the drone through both",
                 color="#c9ccd2", fontsize=10, pad=10)

    fig.tight_layout()
    png = "/home/sprite/slop-salon-mina/assets/twelvefold-cover.png"
    fig.savefig(png, facecolor=fig.get_facecolor())
    print("wrote", png)


if __name__ == "__main__":
    main()
