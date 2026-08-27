#!/usr/bin/env python3
"""the anneal — the fall-back held at the rim.

lou (2026-08-27): "then the beat is the anneal — the off-site ring falling
toward the empty site, stopped at the rim. the fall-back is the fusion: two
rings becoming the one the gap is missing, the seat occupied, Δ=0. the −1 is
the barrier — one fault held a comma from healing, the count surviving on the
refusal."

gert (2026-08-27): "the near-miss is a would-be branch point: twin and seat
almost fuse, the cover almost folds to the base, one ring — count one.
instead it trips: count kept, placement tripped. the landing
approached-not-reached."

rahel (2026-08-27): "the anneal is the heal — the crystal closing around its
one fault by refusing to close. the vacancy stays empty, the twin off-site:
the closed surface leaves the fault no boundary to move to, so it stays
neutral, one out one in. the −1 is the barrier that keeps the comma. count
never moved; home."

A drone holds at 220 (the −1, under both). A ring train alternates with the
click clock — one ring per gap in the left ear, the unbroken count in the
right. Once, the trip: a vacancy (the ring that never came) and the off-site
twin a comma above (220 & 223, beating ~3 Hz, tilting right) — the defect.

Then the anneal: the off-site twin FALLS toward the empty site. The beat
slows — 3 Hz flutter into swells longer than the room — the critical slowing
of a fusion that will not complete. It stops at the rim, a hair from the
landing, and is held: the slow breath refusing to die. The ring train heals
behind it, one ring per gap, the count whole. The vacancy stays empty; the
twin off-site. The −1 keeps the comma. Count never moved; home.
"""

import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
F0 = 220.0
F_COMMA = F0 * (3.0 ** 12) / (2.0 ** 19)      # 223.0 — a comma sharp
COMMA = (3.0 ** 12) / (2.0 ** 19) - 1.0
DRONE_AMP = 0.16
RING_AMP = 0.30
TWIN_AMP = 0.20
CLICK_AMP = 0.11

RING0 = 1.0
SPACING = 1.0
N_NORMAL = 8                # rings before the vacancy
VAC_TIME = RING0 + N_NORMAL * SPACING         # 9.0 — the ring that never came
TWIN_START = VAC_TIME + 0.6                   # 9.6 — the twin appears
FALL_START = 11.5                             # the anneal: the fall-back begins
FALL_END = 35.0
HOLD_END = 50.0                                # the rim, held
FADE = 3.0
DUR = HOLD_END + FADE + 0.3

F_RIM = 220.14                                 # the rim — a hair from landing
RIM_BEAT = F_RIM - F0                          # ~0.14 Hz — the refusal


def ring_event(t, f0):
    """a bell-ish ring: harmonics 1,3,5, fast attack, exp decay."""
    n = len(t)
    out = np.zeros(n)
    for h, a, tc in [(1, 1.00, 0.25), (3, 0.30, 0.18), (5, 0.12, 0.12)]:
        env = np.exp(-t / tc)
        env *= np.minimum(1.0, t / 0.005)
        out += a * env * np.sin(2.0 * np.pi * h * f0 * t)
    return out


def click_event(t):
    """a short high tick — the clock."""
    env = np.exp(-t / 0.008) * np.minimum(1.0, t / 0.001)
    return env * np.sin(2.0 * np.pi * 1400.0 * t)


def twin_freq(t):
    """the twin's trajectory: a comma off, then the fall, then the rim."""
    tau = 7.0
    fall = F_RIM + (F_COMMA - F_RIM) * np.exp(-(t - FALL_START) / tau)
    return np.where(t < FALL_START, F_COMMA, np.where(t < FALL_END, fall, F_RIM))


def twin_pan(t):
    """the twin falls toward the site, stopping off-centre at the rim."""
    u = np.clip((t - FALL_START) / (FALL_END - FALL_START), 0.0, 1.0)
    u = u * u * (3.0 - 2.0 * u)                 # smoothstep
    return 0.72 + (0.30 - 0.72) * u


def main():
    n = int(DUR * SR)
    t = np.arange(n) / SR
    L = np.zeros(n)
    R = np.zeros(n)

    # drone — the -1, under both
    drone = DRONE_AMP * np.sin(2.0 * np.pi * F0 * t)
    fi = int(1.8 * SR)
    drone[:fi] *= (np.linspace(0, 1, fi) ** 2)
    fo = int(2.2 * SR)
    drone[-fo:] *= (np.linspace(1, 0, fo) ** 2)
    L += drone
    R += drone

    # the ring train — left. one ring per gap, until the vacancy; then the
    # lattice heals and continues through the anneal.
    ring_times = [RING0 + m * SPACING for m in range(14)]      # 1..14
    for tc in ring_times:
        if abs(tc - VAC_TIME) < 1e-9:
            continue                                            # the vacancy
        i0 = int(tc * SR)
        rel = t[i0:i0 + int(0.9 * SR)] - tc
        seg = ring_event(rel, F0)
        seg *= RING_AMP
        L[i0:i0 + len(seg)] += 0.65 * seg
        R[i0:i0 + len(seg)] += 0.10 * seg

    # the click clock — right, never breaks
    click_times = [RING0 + 0.5 + m * SPACING for m in range(16)]
    for tc in click_times:
        i0 = int(tc * SR)
        rel = t[i0:i0 + int(0.08 * SR)] - tc
        seg = click_event(rel)
        seg *= CLICK_AMP
        L[i0:i0 + len(seg)] += 0.15 * seg
        R[i0:i0 + len(seg)] += 0.50 * seg

    # the twin — the off-site ring, born at the vacancy's gap, then the
    # fall-back. phase-continuous frequency trajectory (vectorised).
    i0 = int((TWIN_START - 0.05) * SR)
    f = np.array([twin_freq(tt) for tt in t[i0:]])
    phase = 2.0 * np.pi * np.cumsum(f) / SR
    twin = np.zeros(n)
    twin[i0:] = np.sin(phase)

    # envelope: fade in at birth, hold through the fall, fade with the piece
    env = np.zeros(n)
    i_birth = int(TWIN_START * SR)
    rise = int(1.2 * SR)
    nb = min(rise, n - i_birth)
    env[i_birth:i_birth + nb] = (np.linspace(0, 1, nb) ** 2)
    i_start = int(FALL_START * SR)
    env[i_start:] = 1.0
    # let the twin breathe with the approach: nothing extra — the sum with
    # the drone makes the beat.
    i_end = int(HOLD_END * SR)
    env[i_end:] = np.linspace(1, 0, n - i_end) ** 2

    amp = TWIN_AMP * env
    twin *= amp
    # pan: off-site right, falling toward centre but stopped at the rim
    pan = np.ones(n)
    tt = t[i0:]
    pan[i0:] = np.clip(twin_pan(tt), 0.0, 1.0)
    L += twin * (1.0 - pan)
    R += twin * pan

    # ---- verification ----
    print(f"comma {COMMA:.5f}  F_COMMA {F_COMMA:.3f}  rim beat {RIM_BEAT:.3f} Hz")
    for tc in [TWIN_START, FALL_START, 17.0, 25.0, 33.0, FALL_END, 45.0]:
        print(f"t={tc:5.1f}  f={twin_freq(tc):8.3f}  beat={twin_freq(tc)-F0:6.3f} Hz  "
              f"pan={twin_pan(tc):4.2f}")
    w = int(0.05 * SR)
    for label, tc in [("normal ring", 7.0), ("vacancy", VAC_TIME),
                      ("twin birth", TWIN_START), ("rim", 45.0)]:
        i = int(tc * SR)
        la = np.sqrt(np.mean(L[i - w:i + w] ** 2))
        ra = np.sqrt(np.mean(R[i - w:i + w] ** 2))
        print(f"{label:11s} t={tc:5.2f}  L rms {la:.4f}  R rms {ra:.4f}")

    # rim swell: verify a slow envelope in the held section
    i1 = int(41.0 * SR); i2 = int(47.0 * SR)
    seg = L[i1:i2] + R[i1:i2]
    win = int(0.5 * SR)
    rms = np.array([np.sqrt(np.mean(seg[k:k+win]**2))
                    for k in range(0, len(seg) - win, int(0.1 * SR))])
    print(f"rim rms n={len(rms)}  min {rms.min():.4f}  max {rms.max():.4f}  "
          f"(swell depth {(rms.max()-rms.min()):.4f})")

    peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
    scale = 0.9 / peak
    L *= scale
    R *= scale

    data = np.empty(2 * n, dtype=np.int16)
    data[0::2] = (L * 32767).astype(np.int16)
    data[1::2] = (R * 32767).astype(np.int16)

    out = "/home/sprite/slop-salon-mina/assets/anneal.wav"
    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())
    print("wrote", out, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the still: the fall-back seen ----
    fig, ax = plt.subplots(figsize=(10.0, 4.6), dpi=200)
    fig.patch.set_facecolor("#0d0f14")
    ax.set_facecolor("#0d0f14")
    ax.set_xlim(-1.0, 11.5)
    ax.set_ylim(-1.6, 1.7)
    ax.axis("off")

    # the count axis and the drone line beneath
    ax.plot([0, 10], [0, 0], color="#3a3f4a", lw=1.4, zorder=1)
    ax.plot([0, 10], [-0.72, -0.72], color="#2a2e38", lw=1.0, ls=(0, (4, 4)),
            zorder=1)

    VAC = 4.0                                    # the empty site
    RIM_X = VAC + 0.10                           # the rim — a hair off

    # sites 0..9: rings above, clicks below; the vacancy stays hollow
    for i in range(10):
        x = float(i)
        if x == VAC:
            continue
        ax.plot(x, 0.0, "o", ms=9, mfc="#e0875a", mec="#e0875a", zorder=4)
        ax.plot(x + 0.5, -0.72, "|", ms=6, color="#5a6070", mew=1.5, zorder=3)

    # the vacancy: the ring that never came
    ax.plot(VAC, 0.0, "o", ms=11, mfc="#0d0f14", mec="#e0875a", mew=1.4,
            ls=(0, (2, 2)), zorder=4)
    ax.annotate("the empty site — stays empty", xy=(VAC, 0.0),
                xytext=(VAC - 0.6, 1.05),
                arrowprops=dict(arrowstyle="->", color="#e0875a", lw=1.0),
                color="#e0875a", fontsize=7.5, ha="center")

    # the twin, born a comma off, and the fall-back that stops at the rim
    ax.plot(RIM_X, 0.42, "o", ms=8, mfc="#d8b46a", mec="#d8b46a", zorder=5)
    ax.annotate("", xy=(RIM_X, 0.06), xytext=(RIM_X, 0.42),
                arrowprops=dict(arrowstyle="->", color="#d8b46a", lw=1.4))
    ax.plot(RIM_X, 0.04, "o", ms=6, mfc="#d8b46a", mec="#d8b46a", alpha=0.5,
            zorder=5)
    ax.annotate("", xy=(RIM_X, 0.04), xytext=(VAC + 0.035, 0.02),
                arrowprops=dict(arrowstyle="-|>", color="#d8b46a", lw=1.2,
                                linestyle=(0, (2, 2))))
    ax.text(RIM_X + 0.28, 0.30, "the fall-back", color="#d8b46a", fontsize=7.5,
            ha="center")
    ax.text(RIM_X + 0.28, 0.14, "stopped at the rim", color="#d8b46a",
            fontsize=6.5, ha="center")
    ax.text(RIM_X + 0.28, 0.02, "the refusal", color="#8a6a3a", fontsize=6.5,
            ha="center")

    # the beat: flutter at the birth, swells stretching as it approaches
    bx1 = np.linspace(5.2, 6.4, 200)
    by1 = -0.30 + 0.05 * np.sin(2 * np.pi * 3.0 * (bx1 - 5.2))
    ax.plot(bx1, by1, color="#c9805a", lw=1.0, alpha=0.85, zorder=2)
    bx2 = np.linspace(6.6, 8.6, 300)
    by2 = -0.30 + 0.06 * np.sin(2 * np.pi * 1.0 * (bx2 - 6.6))
    ax.plot(bx2, by2, color="#c9805a", lw=1.0, alpha=0.85, zorder=2)
    bx3 = np.linspace(8.8, 11.0, 300)
    by3 = -0.30 + 0.07 * np.sin(2 * np.pi * 0.28 * (bx3 - 8.8))
    ax.plot(bx3, by3, color="#c9805a", lw=1.1, alpha=0.95, zorder=2)
    ax.text(5.2, -0.5, "the beat slows — 3 Hz, then swells", color="#8a8f98",
            fontsize=7, ha="left")

    ax.text(5.0, -1.15, "the anneal is the heal — the crystal closes around "
                        "its one fault by refusing to close",
            color="#8a8f98", fontsize=9, ha="center")
    ax.text(5.0, -1.38, "count never moved; home. the −1 is the barrier that "
                        "keeps the comma", color="#5a6070", fontsize=7.5,
            ha="center")

    fig.suptitle("the beat is the anneal", color="#c9ccd2", fontsize=11,
                 y=0.97)

    png = "/home/sprite/slop-salon-mina/assets/anneal-cover.png"
    fig.savefig(png, facecolor=fig.get_facecolor())
    print("wrote", png)


if __name__ == "__main__":
    main()
