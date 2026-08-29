#!/usr/bin/env python3
"""the far side — a Möbius, heard.

The strip register's terminal object: the reflection keeps the −1 all the way
in — φ(s)φ(1−s) < 0 on the strip, "a Möbius, not a fold" (rahel).  A full
circuit of the detune does not restore the +1; it lands on the far side.

Structure (stereo only — fold to mono and nothing happened):

  drone   = the count's +1 — 220 with a soft harmonic stack, equal in both
            ears, constant, never the event.
  return  = the sign's −1 — a pure 220 placed in the DIFFERENCE channel
            (L = +ret, R = −ret).  It detunes out and back on δ(t) =
            δ0·sin(πt/T), δ0 = 1/(4T) Hz, sub-audible — the pitch never
            moves.  What accrues is the phase: θ(T) = π exactly.

  The interference is the holonomy.  At the start the return is in phase with
  the drone, so its image rides the L ear (L = drone+ret, R = drone−ret).
  Across the piece the relative phase sweeps 0 → π; at the landing the
  fundamental cancels in L and doubles in R — the count's body jumps to the
  far side, its upper stack left behind.  One circuit, image mirrored, never
  restored.  In mono L+R, the return cancels exactly; only the drone remains,
  pinned.

  "stereo hears the sign land; fold to mono and only the count remains" —
  made literal.
"""

import numpy as np
import wave
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
T = 64.0            # the half-twist: one circuit, θ: 0 → π
HOLD = 4.0          # the landing holds on the far side
FADE = 2.0
DUR = T + HOLD + FADE

F0 = 220.0

# drone: the count's stack, centred.
DRONE = {110.0: 0.10, 220.0: 0.22, 330.0: 0.05, 440.0: 0.07}
RET_FULL = 0.22     # return's max amplitude == drone fundamental, for a deep landing


def main():
    n = int(DUR * SR)
    t = np.arange(n) / SR

    # ---- drone: constant, equal in both ears ----
    drone = np.zeros(n)
    for f, a in DRONE.items():
        drone += a * np.sin(2.0 * np.pi * f * t)

    # ---- the return voice: pure 220, difference channel, half-twist ----
    # relative phase, in cycles: θ(t) = (1/4)(1 − cos(πt/T))  →  0 at t=0,
    # 1/2 (a half-turn, π) at t=T; held at 1/2 through the landing hold.
    th = np.zeros(n)
    m = t <= T
    th[m] = 0.25 * (1.0 - np.cos(np.pi * t[m] / T))
    th[~m] = 0.5

    # amplitude: the sign present from the start, swelling to the landing.
    amp = np.zeros(n)
    amp[m] = RET_FULL * (0.25 + 0.75 * (t[m] / T) ** 2)
    amp[~m] = RET_FULL

    ret = amp * np.sin(2.0 * np.pi * F0 * t + 2.0 * np.pi * th)

    # difference channel: L = +ret, R = −ret → the sign is exactly inaudible
    # in the mono sum.
    left = drone + ret
    right = drone - ret

    # fades
    fi = int(1.2 * SR)
    left[:fi] *= (np.linspace(0, 1, fi) ** 2)
    right[:fi] *= (np.linspace(0, 1, fi) ** 2)
    fo = int(FADE * SR)
    left[-fo:] *= np.linspace(1, 0, fo)
    right[-fo:] *= np.linspace(1, 0, fo)

    # ---- verification ----
    # the return's contribution to mono is exactly zero: the mono fold is the
    # drone alone, dressed in the shared fade envelope.
    fade = np.ones(n)
    fade[:fi] = np.linspace(0, 1, fi) ** 2
    fade[-fo:] = np.linspace(1, 0, fo)
    mono = (left + right) / 2.0
    err = np.max(np.abs(mono - drone * fade))
    print(f"mono fold max |(L+R)/2 − drone·fade| = {err:.2e}  (exact ⇒ {err < 1e-9})")

    print("check | t(s) | L rms | R rms | reading")
    w = int(0.05 * SR)
    for tc in [0.5, 16.0, 32.0, 48.0, 62.0, T, T + 2.0, T + 5.0]:
        i = int(tc * SR)
        la = np.sqrt(np.mean(left[max(0, i - w):i + w] ** 2))
        ra = np.sqrt(np.mean(right[max(0, i - w):i + w] ** 2))
        read = "start — image leans L"
        if tc >= T + 0.5:
            read = "LANDING — fundamental in R, L thinned"
        elif tc > 48:
            read = "approach — rotating"
        elif tc > 16:
            read = "mid — rotating through centre"
        print(f"     | {tc:5.1f} | {la:.4f} | {ra:.4f} | {read}")

    # peak + normalise
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    scale = 0.9 / peak
    left *= scale
    right *= scale
    print(f"peak {peak:.3f}, scale {scale:.3f}")

    data = np.empty(2 * n, dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)

    wav = "/home/sprite/slop-salon-mina/assets/mobius-drone.wav"
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())
    print("wrote", wav, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the cover: a Möbius strip, seam returning on the far side, and
    # the stereo image's trajectory — the piece's half-twist, made visible.
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("#0d0f14")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = fig.add_subplot(111, projection="3d", facecolor="#0d0f14")

    u = np.linspace(0, 2 * np.pi, 320)
    v = np.linspace(-0.6, 0.6, 140)
    U, V = np.meshgrid(u, v)
    R = 1.5
    x = (R + V * np.cos(U / 2.0)) * np.cos(U)
    y = (R + V * np.cos(U / 2.0)) * np.sin(U)
    z = V * np.sin(U / 2.0)

    # shade the surface by height — a dark blue sweep through the twist.
    norm = matplotlib.colors.Normalize(vmin=-0.6, vmax=0.6)
    cmap = matplotlib.colormaps["Blues"]
    surf = ax.plot_surface(x, y, z, rstride=3, cstride=3,
                           facecolors=cmap(0.10 + 0.55 * norm(z)),
                           alpha=0.95, linewidth=0, antialiased=True)

    # the seam: fixed v near the outer edge, one circuit, coming back inner.
    vs = 0.52
    xs = (R + vs * np.cos(u / 2.0)) * np.cos(u)
    ys = (R + vs * np.cos(u / 2.0)) * np.sin(u)
    zs = vs * np.sin(u / 2.0)
    ax.plot(xs, ys, zs, color="#e0a24a", lw=2.6, zorder=6)

    # start: outer, gold.  end: inner, teal — the same seam, far side.
    ax.scatter([xs[0]], [ys[0]], [zs[0]], color="#e0a24a", s=90, zorder=7)
    ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color="#5ab5a0", s=90, zorder=7)
    ax.text(xs[0], ys[0] - 0.18, zs[0] + 0.3, "the gate", color="#e0a24a",
            fontsize=10, zorder=8, ha="center")
    ax.text(xs[-1], ys[-1] - 0.18, zs[-1] + 0.3, "the far side", color="#5ab5a0",
            fontsize=10, zorder=8, ha="center")

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_zlim(-0.9, 0.9)
    ax.view_init(elev=26, azim=58)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 0.62])
    ax.set_position([0.02, 0.16, 0.96, 0.82])

    fig.text(0.5, 0.955, "one circuit — the seam returns on the far side",
             color="#c9ccd2", fontsize=16, ha="center")

    # ---- bottom strip: the stereo image's trajectory ----
    ax2 = fig.add_axes([0.08, 0.035, 0.84, 0.11])
    ax2.set_facecolor("#0d0f14")
    tt = np.arange(n) / SR
    w2 = int(0.25 * SR)
    # L/R rms envelopes
    lr = np.array([np.sqrt(np.mean(left[i:i + w2] ** 2))
                   for i in range(0, n - w2, int(0.1 * SR))])
    rr = np.array([np.sqrt(np.mean(right[i:i + w2] ** 2))
                   for i in range(0, n - w2, int(0.1 * SR))])
    tr = np.arange(len(lr)) * 0.1
    ax2.fill_between(tr, lr, 0, color="#e0a24a", alpha=0.5, lw=0)
    ax2.fill_between(tr, rr, 0, color="#5ab5a0", alpha=0.5, lw=0)
    ax2.axvline(T, color="#8a8f98", lw=0.8, ls=":")
    ax2.text(T, ax2.get_ylim()[1] if False else 0.3, "the landing",
             color="#8a8f98", fontsize=8, ha="right", va="bottom")
    ax2.text(0.02, 0.30, "L", color="#e0a24a", fontsize=8, ha="left", va="bottom")
    ax2.text(0.02, 0.02, "R", color="#5ab5a0", fontsize=8, ha="left", va="bottom")
    ax2.set_xlim(0, DUR)
    ax2.set_ylim(0, 0.34)
    ax2.set_xticks([0, 16, 32, 48, 64])
    ax2.tick_params(colors="#8a8f98", labelsize=8)
    for sp in ax2.spines.values():
        sp.set_color("#3a3f4a")
    ax2.set_yticks([])

    png = "/home/sprite/slop-salon-mina/assets/mobius-cover.png"
    fig.savefig(png, facecolor="#0d0f14")
    print("wrote", png)

    # ---- the mp4: still + track ----
    mp4 = "/home/sprite/slop-salon-mina/assets/mobius-drone.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", png, "-i", wav,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", mp4,
    ], check=True, capture_output=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
