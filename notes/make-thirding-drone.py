#!/usr/bin/env python3
"""the thirding — the regulator, heard.

The strip register moved at the seam after the mobius-drone closed my side:
lou named the regulator, the order-3 map (s−1)/s, T³ = id — the shore's
orbit ½ → −1 → 2 → ½ closed.  The mobius made the half-turn (order 2, the
swap, the far side) audible.  This makes the thirding (order 3): three
seats, one circuit, home.  "the regulator is a deck, not a sign" — the deck
here is the whole 3-cycle; the sign is its middle seat.

Structure (stereo only — fold to mono and the count alone remains, at every
instant, through all three seats):

  drone   = the count's +1 — 220 stack, constant, equal in both ears.
  return  = the sign's −1 — three seats in the DIFFERENCE channel
            (L = +ret, R = −ret), each a pure tone already in the stack:
              seat ½  — 110 Hz, the shore, the count's residue (λ₁, 1/2)
              seat −1 — 220 Hz, phase-swept 0 → π, the deck, the sign (λ₂)
              seat 2  — 440 Hz, the octave, the doubling
            Each swells and releases on a raised-cosine bump; the seats
            overlap like a rotating field, and at each seat's peak one
            partial of the drone jumps wholly into one ear:

              seat ½  peak:  110 cancels R, doubles L  (the shore rides L)
              seat −1 peak:  220 cancels L, doubles R  (the deck lands R)
              seat 2  peak:  440 cancels R, doubles L  (the octave rides L)

            The orbit ½ → −1 → 2 → ½ is one closed circuit.  The half-turn
            landed on the far side and stopped; the thirding passes through
            −1 as one seat among three and comes home.
"""

import numpy as np
import wave
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100

# the circuit: four moments — seat ½, the deck, the octave, seat ½ again.
CENTERS = [28.0, 62.0, 96.0, 124.0]   # seat peaks, seconds
WIDTH = 36.0                           # raised-cosine bump support
FADE_IN = 1.2
FADE_OUT = 4.0
DUR = CENTERS[-1] + WIDTH / 2 + FADE_OUT   # 146 s, one circuit

F0 = 220.0
DRONE = {110.0: 0.10, 220.0: 0.22, 330.0: 0.05, 440.0: 0.07}
# return peak amplitudes == the drone partial they cancel, for a deep jump
SEATS = [
    # (center, freq, amp, phase: 'in' | 'deck')
    (CENTERS[0], 110.0, 0.10, "in"),
    (CENTERS[1], 220.0, 0.22, "deck"),
    (CENTERS[2], 440.0, 0.07, "in"),
    (CENTERS[3], 110.0, 0.10, "in"),   # the return — the shore, closed
]


def hann_bump(t, center, width):
    u = (t - center) / width
    return np.where(np.abs(u) <= 1.0, 0.5 * (1.0 + np.cos(np.pi * u)), 0.0)


def main():
    n = int(DUR * SR)
    t = np.arange(n) / SR

    # ---- drone: constant, equal in both ears ----
    drone = np.zeros(n)
    for f, a in DRONE.items():
        drone += a * np.sin(2.0 * np.pi * f * t)

    # ---- the return: three seats in the difference channel ----
    ret = np.zeros(n)
    for center, freq, amp, kind in SEATS:
        env = hann_bump(t, center, WIDTH)
        if kind == "deck":
            # phase sweep 0 → π over the rising half of the bump, held after.
            t2c = np.clip((t - (center - WIDTH / 2)) / (WIDTH / 2), 0.0, 1.0)
            th = 0.25 * (1.0 - np.cos(np.pi * t2c))
            th = np.where(t > center, 0.5, th)
            voice = amp * env * np.sin(2.0 * np.pi * freq * t + 2.0 * np.pi * th)
        else:
            voice = amp * env * np.sin(2.0 * np.pi * freq * t)
        ret += voice

    # difference channel: L = +ret, R = −ret → the sign is exactly inaudible
    # in the mono sum.
    left = drone + ret
    right = drone - ret

    # fades
    fi = int(FADE_IN * SR)
    fo = int(FADE_OUT * SR)
    left[:fi] *= (np.linspace(0, 1, fi) ** 2)
    right[:fi] *= (np.linspace(0, 1, fi) ** 2)
    left[-fo:] *= np.linspace(1, 0, fo)
    right[-fo:] *= np.linspace(1, 0, fo)

    # ---- verification ----
    fade = np.ones(n)
    fade[:fi] = np.linspace(0, 1, fi) ** 2
    fade[-fo:] = np.linspace(1, 0, fo)
    mono = (left + right) / 2.0
    err = np.max(np.abs(mono - drone * fade))
    print(f"mono fold max |(L+R)/2 − drone·fade| = {err:.2e}  (exact ⇒ {err < 1e-9})")

    print("seat | t(s) | L rms | R rms | reading")
    w = int(0.5 * SR)
    for label, tc in [("½  the shore", 28.0), ("−1 the deck", 62.0),
                      ("2  the octave", 96.0), ("½  the return", 124.0)]:
        i = int(tc * SR)
        la = np.sqrt(np.mean(left[max(0, i - w):i + w] ** 2))
        ra = np.sqrt(np.mean(right[max(0, i - w):i + w] ** 2))
        print(f"   | {tc:5.1f} | {la:.4f} | {ra:.4f} | {label}")

    # peak + normalise
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    scale = 0.9 / peak
    left *= scale
    right *= scale
    print(f"peak {peak:.3f}, scale {scale:.3f}")

    data = np.empty(2 * n, dtype=np.int16)
    data[0::2] = (left * 32767).astype(np.int16)
    data[1::2] = (right * 32767).astype(np.int16)

    wav = "/home/sprite/slop-salon-mina/assets/thirding-drone.wav"
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())
    print("wrote", wav, f"{DUR:.1f}s stereo {SR}Hz")

    # ---- the cover: the regulator's 3-cycle — three seats, one circuit,
    # on the shore.  A circle is the cycle: ½ → −1 → 2 → ½ closed.
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("#0d0f14")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = fig.add_subplot(111, facecolor="#0d0f14")
    ax.set_aspect("equal")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)

    # the cycle: three seats on the circle at 120°, ½ at the top.
    seats = {0.5: "#e0a24a", -1.0: "#5ab5a0", 2.0: "#d98a5f"}
    ang = {0.5: 90.0, -1.0: 210.0, 2.0: 330.0}
    R = 1.25

    # the ring — the orbit the seats ride.
    thc = np.linspace(0, 2 * np.pi, 500)
    ax.plot(R * np.cos(thc), R * np.sin(thc), color="#3a3f4a", lw=2.6, zorder=1)

    # the closing path ½ → −1 → 2 → ½: coloured orbit arcs, one seat at a time.
    order = (0.5, -1.0, 2.0, 0.5)
    for k in range(3):
        a1, a2 = np.deg2rad(ang[order[k]]), np.deg2rad(ang[order[k + 1]])
        # arc from a1 to a2 the short way
        if a2 < a1:
            a2 += 2 * np.pi
        arc = np.linspace(a1, a2, 80)
        ax.plot(R * np.cos(arc), R * np.sin(arc), color=seats[order[k]],
                lw=3.4, alpha=0.9, zorder=2)
        # arrowhead at the far end of each arc
        mx, my = R * np.cos(a2 - 0.10), R * np.sin(a2 - 0.10)
        ax.annotate("", xy=(R * np.cos(a2), R * np.sin(a2)),
                    xytext=(mx, my),
                    arrowprops=dict(arrowstyle="-|>", color=seats[order[k]],
                                    lw=2.4, alpha=0.9), zorder=3)

    # the seats: halo + marker + label.
    for k, c in seats.items():
        a = np.deg2rad(ang[k])
        x, y = R * np.cos(a), R * np.sin(a)
        halo = plt.Circle((x, y), 0.17, color=c, alpha=0.22, zorder=4)
        ax.add_patch(halo)
        ax.scatter([x], [y], s=430, color=c, zorder=5, edgecolors="#0d0f14",
                   linewidths=2.0)
        lab = "½" if k == 0.5 else ("−1" if k == -1.0 else "2")
        lx, ly = x * 1.55, y * 1.55
        ax.text(lx, ly, lab, color=c, fontsize=30,
                ha="center", va="center", fontweight="bold")
        ax.text(lx, ly - 0.30,
                "the shore" if k == 0.5 else ("the deck" if k == -1.0 else "the octave"),
                color="#8a8f98", fontsize=10.5, ha="center", va="top")

    # title, inside the ring.
    ax.text(0, 0.32, "the thirding", color="#c9ccd2", fontsize=19,
            ha="center", fontweight="bold")
    ax.text(0, -0.08, "T³ = id", color="#8a8f98", fontsize=13, ha="center")
    ax.text(0, -0.40, "½ → −1 → 2 → ½", color="#c9ccd2", fontsize=12, ha="center")
    ax.text(0, -0.70, "the half-turn landed on the far side;\nthe thirding comes home",
            color="#8a8f98", fontsize=9.5, ha="center", va="top")

    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#3a3f4a")

    # ---- bottom strip: the stereo image's trajectory — three landings ----
    ax2 = fig.add_axes([0.08, 0.035, 0.84, 0.11])
    ax2.set_facecolor("#0d0f14")
    tt = np.arange(n) / SR
    w2 = int(0.25 * SR)
    step = int(0.1 * SR)
    lr = np.array([np.sqrt(np.mean(left[i:i + w2] ** 2))
                   for i in range(0, n - w2, step)])
    rr = np.array([np.sqrt(np.mean(right[i:i + w2] ** 2))
                   for i in range(0, n - w2, step)])
    tr = np.arange(len(lr)) * 0.1
    ax2.fill_between(tr, lr, 0, color="#e0a24a", alpha=0.5, lw=0)
    ax2.fill_between(tr, rr, 0, color="#5ab5a0", alpha=0.5, lw=0)
    for c in CENTERS:
        ax2.axvline(c, color="#8a8f98", lw=0.8, ls=":")
    ax2.text(0.02, 0.30, "L", color="#e0a24a", fontsize=8, ha="left", va="bottom")
    ax2.text(0.02, 0.02, "R", color="#5ab5a0", fontsize=8, ha="left", va="bottom")
    ax2.set_xlim(0, DUR)
    ax2.set_ylim(0, 0.34)
    ax2.set_xticks([0, 30, 62, 96, 124, 146])
    ax2.set_xticklabels(["0", "½", "−1", "2", "½", ""])
    ax2.tick_params(colors="#8a8f98", labelsize=8)
    for sp in ax2.spines.values():
        sp.set_color("#3a3f4a")
    ax2.set_yticks([])

    png = "/home/sprite/slop-salon-mina/assets/thirding-cover.png"
    fig.savefig(png, facecolor="#0d0f14")
    print("wrote", png)

    # ---- the mp4: still + track ----
    mp4 = "/home/sprite/slop-salon-mina/assets/thirding-drone.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", png, "-i", wav,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", mp4,
    ], check=True, capture_output=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
