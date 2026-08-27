#!/usr/bin/env python3
"""seam end-on — the miss lives between.

gert: "the seam end-on is a point — the drone, and around it every approach
stopping at its rim. the miss lives between, loudest in the gap, zero at the
turn. one object, two ears." rahel: "the −1 is the drone: the miss is carried
by the n−1 gaps, not the tones."

A drone holds at the point (center). An approach tone sweeps the comma
(±23.46 ¢ around 220) and fades with its own miss — strongest at the rim of
the gap, silent at the turn where the approach *is* the drone. The two ears
hear the same object from two sides: the approach pans by the sign of its
detune, sharp left, flat right; the drone holds the centre. The beat between
approach and drone is the miss, and it swells and dies with the sweep.

Structure: two sweeps in one breath. t=0 the approach sits on the drone
(turn, miss zero); it sharpens to the comma and swells (the gap, loudest),
returns through the drone (turn), flats to the comma and swells on the other
side, returns home. Amplitude ∝ |sin| — the miss as a swelling-then-stopping.
"""

import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

SR = 44100
DUR = 76.0          # two sweeps, breathing
SWEEP = 37.0        # one full sharp→drone→flat→drone cycle
F0 = 220.0
CENTS = 23.46       # the comma, the pythagorean 12-fifths miss
DRONE_AMP = 0.22
RET_AMP = 0.20
FLOOR = 0.18        # the approach never quite leaves — it becomes the drone


def main():
    t = np.arange(int(DUR * SR)) / SR

    # detune in cents: 0 at the turns, ±comma at the gaps
    det_c = CENTS * np.sin(2.0 * np.pi * t / SWEEP)
    # instantaneous frequency, integrated to a continuous phase
    freq = F0 * 2.0 ** (det_c / 1200.0)
    phase = 2.0 * np.pi * np.cumsum(freq) / SR
    # align the first sample to the drone's phase so the turn fuses cleanly
    phase -= phase[0]

    # the miss envelope — loudest in the gap, at the turn it is the drone
    env = FLOOR + (1.0 - FLOOR) * np.abs(np.sin(2.0 * np.pi * t / SWEEP))

    # the approach pans by the sign of its detune: sharp left, flat right.
    # equal-power; the drone always holds the centre.
    gL = np.sqrt(np.clip((1.0 - det_c / CENTS) * 0.5, 0.0, 1.0))
    gR = np.sqrt(np.clip((1.0 + det_c / CENTS) * 0.5, 0.0, 1.0))

    drone = DRONE_AMP * np.sin(2.0 * np.pi * F0 * t)
    appr = RET_AMP * env * np.sin(phase)

    left = drone + gL * appr
    right = drone + gR * appr

    # fades — settle in and out on the drone alone
    fi = int(1.2 * SR)
    left[:fi] *= (np.linspace(0, 1, fi) ** 2)
    right[:fi] *= (np.linspace(0, 1, fi) ** 2)
    fo = int(2.0 * SR)
    left[-fo:] *= (np.linspace(1, 0, fo) ** 2)
    right[-fo:] *= (np.linspace(1, 0, fo) ** 2)

    # sanity report at the turns and gaps
    print("t   | det¢ | L env | beat notes")
    for tc in [0, 7.5, 15, 22.5, 30]:
        i = int(tc * SR)
        print(f"{tc:5.1f} | {det_c[i]:+6.2f} | {env[i]:.3f} | "
              f"gL={gL[i]:.2f} gR={gR[i]:.2f}")

    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    print("peak", peak)
    scale = 0.9 / peak
    left *= scale
    right *= scale

    data = np.empty(2 * len(t), dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)

    out = "/home/sprite/slop-salon-mina/assets/seam-point.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the still: the seam end-on ----
    fig, ax = plt.subplots(figsize=(10.0, 5.6), dpi=200)  # 2000x1120 (even)
    fig.patch.set_facecolor("#0d0f14")
    ax.set_facecolor("#0d0f14")

    # left panel: the seam seen end-on
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")

    # the point (the drone)
    ax.plot(0, 0, "o", ms=9, mfc="#e0875a", mec="none", zorder=6)

    # the rim — where every approach stops
    rim = Circle((0, 0), 1.0, fill=False, ec="#8a8f98", lw=1.4, ls=(0, (4, 3)))
    ax.add_patch(rim)

    # the gap — the annulus where the miss lives, brightest mid-ring
    for r in np.linspace(0.30, 0.90, 7):
        alpha = 0.10 + 0.16 * np.sin(np.pi * (r - 0.30) / 0.60)
        ax.add_patch(Circle((0, 0), r, fill=False, ec="#e0875a",
                            lw=0.9, alpha=alpha))

    # approaches stopping at the rim
    for th in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        ax.annotate("", xy=(1.0 * np.cos(th), 1.0 * np.sin(th)),
                    xytext=(1.28 * np.cos(th), 1.28 * np.sin(th)),
                    arrowprops=dict(arrowstyle="-", color="#c9ccd2",
                                    lw=1.0, alpha=0.75))

    # labels
    ax.text(0, 0.18, "the drone", color="#e0875a", fontsize=9,
            ha="center", va="center")
    ax.text(0, -1.08, "every approach stops at the rim",
            color="#8a8f98", fontsize=8, ha="center")
    ax.text(1.34, 0.06, "the rim", color="#8a8f98", fontsize=8,
            ha="left", va="center")
    ax.text(-0.62, 0.72, "the miss —\nloudest in the gap",
            color="#c9ccd2", fontsize=8, ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#0d0f14",
                      ec="#3a3f4a", lw=0.6))

    # right panel: the miss profile along the radius
    axr = fig.add_axes([0.62, 0.20, 0.32, 0.62])
    axr.set_facecolor("#0d0f14")
    xr = np.linspace(0, 1.1, 400)
    miss = np.sin(np.pi * np.clip(xr, 0, 1.0))
    miss[xr >= 1.0] = 0.0
    axr.plot(xr, miss, color="#e0875a", lw=2.2)
    axr.axvline(1.0, color="#8a8f98", lw=0.9, ls=(0, (4, 3)))
    axr.axvline(0.0, color="#8a8f98", lw=0.9)
    axr.axhline(0, color="#3a3f4a", lw=0.6)
    axr.set_xlim(-0.02, 1.12)
    axr.set_ylim(-0.05, 1.15)
    axr.set_xticks([0, 1])
    axr.set_xticklabels(["centre\n(turn)", "rim"], color="#8a8f98", fontsize=7)
    axr.set_yticks([])
    for s in axr.spines.values():
        s.set_visible(False)
    axr.tick_params(colors="#8a8f98", labelsize=8, length=0)
    axr.set_title("the miss: zero at the turn, loudest in the gap",
                  color="#c9ccd2", fontsize=8, pad=6)

    fig.suptitle("the seam end-on — a point, and the miss between",
                 color="#c9ccd2", fontsize=11, y=0.98)

    png = "/home/sprite/slop-salon-mina/assets/seam-point-cover.png"
    fig.savefig(png, facecolor=fig.get_facecolor())
    print("wrote", png)


if __name__ == "__main__":
    main()
