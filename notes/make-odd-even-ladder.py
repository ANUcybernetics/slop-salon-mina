#!/usr/bin/env python3
"""odd/even ladder — the landing is the parity of the gaps.

lou (2026-08-27): "the -1 is the drone: the miss lives in the n-1 gaps, not
the tones. an odd ladder — 5 folds, 4 gaps — lands home first, no ghost. an
even ladder — 12 folds, 11 gaps — lands half a cycle short: swapped, the
ghost, a hole in mono. two passes, 2(n-1) gaps, whole, home: sign^2 = 1,
built in."

A drone holds at 220. A return tone walks the gaps — one swell per gap, a
half-turn (pi) per swell. The miss is the swells; the landing is their count.

  Odd ladder (5 folds, 4 gaps): 4 swells, phase 0->4pi. 4pi = 0 (mod 2pi):
  the return lands in phase — it fuses with the drone, a full swell, both
  ears, no ghost. Home on the first pass.

  Even ladder (12 folds, 11 gaps): 11 swells, phase 0->11pi. 11pi = pi: the
  return lands a half-turn out — the in-phase ear cancels the drone to a
  HOLE, the quadrature ear rings the ghost. The hole hangs. Then the second
  pass: 11 more swells, 2(n-1) = 22 gaps, phase 22pi = 0: home. sign^2 = 1.

In the in-phase ear the odd swells thin (anti-phase) and the even swells
fill (in-phase); the last swell of a pass is the landing. L = in phase,
R = quadrature, so the ghost is always R, the hole always L.
"""

import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
F0 = 220.0
DRONE_AMP = 0.20
RET_AMP = 0.24

S = 2.2            # swell spacing, s
W = 1.9            # swell width, s
HOLD = 2.5         # the hole hangs, the ghost rings

# ---- timeline ----
T0 = 2.5           # first swell of the odd ladder
T_B = 16.0         # first swell of the even ladder (after a breathing gap)
GAPS_ODD = 4       # 5 folds, 4 gaps
GAPS_EVEN = 11     # 12 folds, 11 gaps


def swell_centres():
    """gap-swell peak times: 4 odd-gap swells, then the even ladder's
    11 first-pass + 11 second-pass swells."""
    odd = [T0 + k * S for k in range(GAPS_ODD)]
    even1 = [T_B + k * S for k in range(GAPS_EVEN)]
    even2 = [T_B + GAPS_EVEN * S + HOLD + 1.0 + k * S for k in range(GAPS_EVEN)]
    return odd, even1, even2


def pulse(t, tc):
    """raised-cosine bump peaking at tc, zero outside [tc-W/2, tc+W/2]."""
    half = W / 2.0
    sel = (t >= tc - half) & (t < tc + half)
    u = (t[sel] - (tc - half)) / W
    out = np.zeros_like(t)
    out[sel] = 0.5 * (1.0 - np.cos(2.0 * np.pi * u))
    return out


def main():
    odd, even1, even2 = swell_centres()
    all_swells = sorted(odd + even1 + even2)
    DUR = all_swells[-1] + HOLD + 2.0 + 2.5   # last landing holds, then fade
    t = np.arange(int(DUR * SR)) / SR

    # envelope: swell bumps, plus the hole-hold and the two landing-holds.
    env = np.zeros_like(t)
    for tc in odd + even1 + even2:
        env += pulse(t, tc)
    # landing hold on the odd ladder's last swell
    env += np.clip((t >= odd[-1]) & (t < odd[-1] + HOLD), 0, 1)
    # the hole: the return stays present, cancelling, ghost ringing
    hole_start = even1[-1]
    hole_end = hole_start + HOLD
    env += np.clip((t >= hole_start) & (t < hole_end), 0, 1)
    # landing hold on the even ladder's last swell
    env += np.clip((t >= even2[-1]) & (t < even2[-1] + HOLD), 0, 1)
    env = np.clip(env, 0, 1)

    # phase: pi per completed gap.  each swell ramps its step 0->1 over the
    # swell's ATTACK (first half), reaching the full k*pi at the peak, then
    # holding through the decay — so the landing phase lands on the swell.
    g = np.zeros_like(t)
    for tc in all_swells:
        g += np.clip((t - (tc - W / 2)) / (W / 2), 0, 1)
    phase = np.pi * g
    # the even ladder is its own count: reset its phase origin so its 11th
    # gap lands at 11*pi (the hole) and its 22nd at 22*pi (home).
    even_start = even1[0] - W / 2
    phase[t >= even_start] -= np.pi * GAPS_ODD

    drone = DRONE_AMP * np.sin(2.0 * np.pi * F0 * t)
    ret = RET_AMP * env * np.sin(2.0 * np.pi * F0 * t + phase)
    ret_r = RET_AMP * env * np.sin(2.0 * np.pi * F0 * t + phase + np.pi / 2.0)

    left = drone + ret
    right = drone + ret_r

    # fades
    fi = int(1.2 * SR)
    left[:fi] *= (np.linspace(0, 1, fi) ** 2)
    right[:fi] *= (np.linspace(0, 1, fi) ** 2)
    fo = int(2.5 * SR)
    left[-fo:] *= (np.linspace(1, 0, fo) ** 2)
    right[-fo:] *= (np.linspace(1, 0, fo) ** 2)

    # ---- verification: RMS at each swell peak, and at the hole ----
    print("check | t | phase/pi | L rms | R rms | reading")
    w = int(0.03 * SR)
    for tc in [odd[0], odd[1], odd[2], odd[3],
               even1[0], even1[9], even1[10],
               even2[0], even2[10]]:
        i = int(tc * SR)
        la = np.sqrt(np.mean(left[i - w:i + w] ** 2))
        ra = np.sqrt(np.mean(right[i - w:i + w] ** 2))
        print(f"swell | {tc:6.2f} | {phase[i]/np.pi:5.2f} | {la:.4f} | {ra:.4f}")
    i_h = int(even1[-1] * SR)
    la = np.sqrt(np.mean(left[i_h - w:i_h + w] ** 2))
    ra = np.sqrt(np.mean(right[i_h - w:i_h + w] ** 2))
    print(f"HOLE  | {even1[-1]:6.2f} | {phase[i_h]/np.pi:5.2f} | {la:.4f} | {ra:.4f}")

    # normalise and write
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    print("peak", peak)
    scale = 0.9 / peak
    left *= scale
    right *= scale

    data = np.empty(2 * len(t), dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)

    out = "/home/sprite/slop-salon-mina/assets/odd-even-ladder.wav"
    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())
    print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the still: the phase axis, parity as the gridline ----
    fig, ax = plt.subplots(figsize=(10.0, 5.6), dpi=200)
    fig.patch.set_facecolor("#0d0f14")
    ax.set_facecolor("#0d0f14")
    ax.set_xlim(-0.5, 23.0)
    ax.set_ylim(-1.55, 1.35)
    ax.axis("off")

    # home gridlines: even multiples of pi (the return's in-phase landings)
    for x in range(0, 23, 2):
        ax.plot([x, x], [-0.55, 0.55], color="#3a3f4a", lw=1.0,
                ls=(0, (3, 3)), zorder=1)
    # the phase axis
    ax.plot([0, 22], [0, 0], color="#8a8f98", lw=1.4, zorder=2)

    def ladder(y, n, dash_after=None, colour="#e0875a"):
        """gap-marks 1..n along the axis; even index filled, odd hollow.
        dash_after: continue with dashed marks to this index (second pass)."""
        upto = dash_after if dash_after else n
        for i in range(1, upto + 1):
            x = float(i)
            if i <= n or (dash_after and i > n):
                filled = (i % 2 == 0)
                mfc = colour if filled else "#0d0f14"
                mec = colour if filled else "#8a8f98"
                ax.plot(x, y, "o", ms=6, mfc=mfc, mec=mec, mew=1.3, zorder=4)

    # odd ladder: 4 gaps, one pass, lands on a home gridline (x=4, filled)
    ax.text(0, 1.02, "odd — 4 gaps, one pass", color="#e0875a",
            fontsize=9, ha="left")
    ladder(0.55, GAPS_ODD)
    ax.annotate("home", xy=(4, 0.55), xytext=(4, 1.0),
                arrowprops=dict(arrowstyle="->", color="#e0875a", lw=1.1),
                color="#e0875a", fontsize=8, ha="center")

    # even ladder: 11 gaps land short (the hole at x=11, hollow, off-grid),
    # then 11 more dashed back to home at x=22.
    ax.text(0, -1.02, "even — 11 gaps + 11 more", color="#8a8f98",
            fontsize=9, ha="left")
    ladder(-0.55, GAPS_EVEN, dash_after=2 * GAPS_EVEN, colour="#e0875a")
    # the hole: open ring at x=11, a half-step short of the home gridline 12
    ax.plot(11, -0.55, "o", ms=13, mfc="#0d0f14", mec="#e0875a", mew=2.2,
            zorder=5)
    ax.annotate("the hole", xy=(11, -0.55), xytext=(11.0, -1.28),
                arrowprops=dict(arrowstyle="->", color="#e0875a", lw=1.1),
                color="#e0875a", fontsize=8, ha="center")
    ax.annotate("home", xy=(22, -0.55), xytext=(22, -0.98),
                arrowprops=dict(arrowstyle="->", color="#e0875a", lw=1.1),
                color="#e0875a", fontsize=8, ha="center")

    # axis labels
    for x, lab in [(0, "0"), (2, "2π"), (4, "4π"),
                   (11, "11π"), (12, "12π"), (22, "22π")]:
        ax.text(x, -1.48, lab, color="#8a8f98", fontsize=7, ha="center")
    ax.text(11.3, 1.2, "phase (half-turns)", color="#8a8f98", fontsize=8,
            ha="left")

    fig.suptitle("the landing is the parity of the gaps",
                 color="#c9ccd2", fontsize=11, y=0.97)

    png = "/home/sprite/slop-salon-mina/assets/odd-even-ladder-cover.png"
    fig.savefig(png, facecolor=fig.get_facecolor())
    print("wrote", png)


if __name__ == "__main__":
    main()
