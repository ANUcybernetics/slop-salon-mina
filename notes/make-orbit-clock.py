#!/usr/bin/env python3
"""The orbit clock — two clocks, one miss.

Every bound orbit carries two clocks that never agree. The MEAN clock moves
uniformly on the circle: the drone, the tone that never misses. The TRUE clock
moves on the ellipse: the return that grazes the near ring every lap and never
reaches the centre. The gap between them is the equation of centre — the beat,
one per orbit, amplitude the eccentricity.

The sweep walks the eccentricity out from the drone (e -> 0, both clocks agree,
the miss absent) toward the fall (e -> 1, the ellipse thins, the apastron
crawl stretches past the room, the return is cut before it comes home).

Composition: main panel = the two clocks + the miss between them, morphing as e
sweeps; lower strip = the miss written out over the last orbit, its zero line
the drone. The video ends at apoapsis — mid-crawl, before the return.
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation, FFMpegWriter

# --- validated dark-surface palette (dataviz reference) ---
SURFACE = "#1a1a19"
INK     = "#ffffff"
SEC     = "#c3c2b7"
MUT     = "#898781"
GRID    = "#2c2c2a"
WARM    = "#e66767"   # the landed clock / periapsis (the always-touched)
COOL    = "#3987e5"   # the uniform clock / drone (the never-missed)

A = 1.0                     # semi-major axis == the drone circle radius
E0, E1 = 0.03, 0.90         # eccentricity sweep bounds
SWEEP_T = 24.0              # seconds the sweep takes; then it holds at E1
T_ORB = 6.0                 # seconds per orbit (mean anomaly goes 2pi)
DUR = 36.0                  # total seconds; ends at apoapsis, mid-crawl
FPS = 24
NFRAMES = int(DUR * FPS)


def kepler_E(M, e, iters=7):
    """Solve E - e sin E = M by Newton from E = M (fine for e <= 0.92)."""
    E = M.copy()
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def sweep_e(t):
    """Eccentricity as a function of time: eased ramp, then hold at E1."""
    u = np.clip(t / SWEEP_T, 0.0, 1.0)
    s = u * u * (3.0 - 2.0 * u)          # smoothstep — slow out of the drone
    return E0 + (E1 - E0) * s


def room_alpha(e):
    """The room fades in with the miss: at the drone the two rings coincide
    with the reference circle and are invisible; they appear as e grows."""
    return float(np.clip((e - 0.03) / 0.13, 0.0, 1.0))


def ellipse_curve(e, n=800):
    """Points of the ellipse (focus at origin, periapsis on +x)."""
    E = np.linspace(0.0, 2.0 * np.pi, n)
    b = np.sqrt(1.0 - e * e)
    return A * (np.cos(E) - e), A * b * np.sin(E)


def true_from_E(E, e):
    """(r, theta) of the landed point given eccentric anomaly."""
    b = np.sqrt(1.0 - e * e)
    x = A * (np.cos(E) - e)
    y = A * b * np.sin(E)
    r = A * (1.0 - e * np.cos(E))
    th = np.arctan2(y, x) % (2.0 * np.pi)
    return r, th


def wrap_pi(x):
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", action="store_true", help="render a few PNG frames and exit")
    ap.add_argument("--out", default="/home/sprite/slop-salon-mina/assets/orbit-clock.mp4")
    args = ap.parse_args()

    times = np.arange(NFRAMES) / FPS
    e_t = np.array([sweep_e(t) for t in times])
    M_t = 2.0 * np.pi * (times / T_ORB) - 11.0 * np.pi    # M=pi (apoapsis) at both ends
    M_w = M_t % (2.0 * np.pi)

    # precompute the landed points for every frame
    E_all = kepler_E(M_t, e_t)
    th_all = true_from_E(E_all, e_t)[1]

    if args.stills:
        for fi in [0, 180, 360, 600, 800, NFRAMES - 1]:
            draw_frame(fi, times, e_t, M_w, th_all,
                       f"/tmp/orbit-clock-still-{fi:04d}.png")
        return

    fig = plt.figure(figsize=(7.2, 7.8), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 1.0], hspace=0.16,
                          left=0.03, right=0.97, top=0.97, bottom=0.04)

    ax = fig.add_subplot(gs[0])
    ax.set_facecolor(SURFACE)
    ax.set_aspect("equal")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.15, 2.15)
    ax.set_axis_off()

    # --- static references ---
    circ_phi = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(circ_phi), np.sin(circ_phi), color=INK, lw=0.8,
            ls=(0, (3, 5)), alpha=0.30)                    # the drone circle
    ax.plot([], [], color=SEC, lw=1.1, alpha=0.55)         # the ellipse (morphs)
    ax.add_patch(Circle((0, 0), 0.05, fill=True, color=MUT, alpha=0.4))      # the empty focus
    ax.add_patch(Circle((0, 0), 0.085, fill=False, lw=0.8, color=MUT, alpha=0.7))
    c_p = ax.add_patch(Circle((0, 0), 0.97, fill=False, lw=1.2,
                              ls=(0, (5, 3)), color=WARM, alpha=0.9))   # near ring
    c_a = ax.add_patch(Circle((0, 0), 1.03, fill=False, lw=1.2,
                              ls=(0, (5, 3)), color=COOL, alpha=0.8))   # far ring

    # --- the two clocks + the miss ---
    line_ell, = ax.plot([], [], color=SEC, lw=1.1, alpha=0.55)
    dot_mean, = ax.plot([], [], "o", ms=7, color=COOL, mec="none", alpha=0.95)
    dot_true, = ax.plot([], [], "o", ms=7, color=WARM, mec="none", alpha=0.95)
    miss_line, = ax.plot([], [], color=INK, lw=0.8, alpha=0.35, ls=(0, (2, 2)))

    txt_e = ax.text(0.025, 0.955, "", transform=ax.transAxes, fontsize=11,
                    color=SEC, va="top", family="DejaVu Sans")
    txt_m = ax.text(0.025, 0.045, "", transform=ax.transAxes, fontsize=9,
                    color=MUT, va="bottom", family="DejaVu Sans")

    # --- lower strip: the miss written out over the last orbit ---
    axs = fig.add_subplot(gs[1])
    axs.set_facecolor(SURFACE)
    axs.set_ylim(-2.6, 2.6)
    axs.set_xlim(0, 1)
    axs.set_axis_off()
    axs.plot([0, 1], [0, 0], color=MUT, lw=0.8, alpha=0.5)   # the drone (delta=0)
    wave, = axs.plot([], [], color=INK, lw=1.3, alpha=0.9)
    wave_pt, = axs.plot([], [], "o", ms=4.5, color=WARM, mec="none", alpha=1.0)
    axs.text(0.985, 1.03, "the miss", transform=axs.transAxes, fontsize=8,
             color=MUT, ha="right", va="bottom", family="DejaVu Sans")

    WINSZ = int(T_ORB * FPS)          # one orbit of delta history
    buf = np.full(WINSZ, np.nan)

    def frame(i):
        e = e_t[i]
        M = M_w[i]
        th = th_all[i]

        # ellipse path for current e
        ex, ey = ellipse_curve(e)
        line_ell.set_data(ex, ey)

        # turning circles follow the room; the room appears with the miss
        ra = room_alpha(e)
        c_p.set_radius(A * (1 - e))
        c_a.set_radius(A * (1 + e))
        c_p.set_alpha(0.9 * ra)
        c_a.set_alpha(0.8 * ra)

        # the two clocks
        dot_mean.set_data([np.cos(M)], [np.sin(M)])
        rp = float(A * (1.0 - e * np.cos(kepler_E(np.array([M]), e)[0])))
        xl, yl = rp * np.cos(th), rp * np.sin(th)
        dot_true.set_data([float(xl)], [float(yl)])
        miss_line.set_data([float(np.cos(M)), float(xl)], [float(np.sin(M)), float(yl)])

        txt_e.set_text(f"e = {e:.2f}")

        # the miss, wrapped, current value in degrees
        d = wrap_pi(th - M)
        txt_m.set_text(f"miss {np.degrees(d):+.0f}°")

        # lower strip — scroll one orbit of the miss
        buf[:-1] = buf[1:]
        buf[-1] = d
        xs = np.linspace(0, 1, WINSZ)
        wave.set_data(xs, buf)
        wave_pt.set_data([1.0], [d])

        return (line_ell, c_p, c_a, dot_mean, dot_true, miss_line,
                txt_e, txt_m, wave, wave_pt)

    anim = FuncAnimation(fig, frame, frames=NFRAMES, interval=1000 / FPS,
                         blit=False, repeat=False)
    writer = FFMpegWriter(fps=FPS, codec="libx264", bitrate=-1,
                          extra_args=["-pix_fmt", "yuv420p",
                                      "-crf", "20", "-preset", "medium"])
    anim.save(args.out, writer=writer)
    print("wrote", args.out)


def draw_frame(i, times, e_t, M_w, th_all, out):
    """Render one still frame (used for --stills previews)."""
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(7.2, 7.8), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 1.0], hspace=0.16,
                          left=0.03, right=0.97, top=0.97, bottom=0.04)
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor(SURFACE)
    ax.set_aspect("equal")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.15, 2.15)
    ax.set_axis_off()

    e = e_t[i]
    M = M_w[i]
    th = th_all[i]
    circ_phi = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(circ_phi), np.sin(circ_phi), color=INK, lw=0.8,
            ls=(0, (3, 5)), alpha=0.30)
    ex, ey = ellipse_curve(e)
    ax.plot(ex, ey, color=SEC, lw=1.1, alpha=0.55)
    ax.add_patch(Circle((0, 0), 0.05, fill=True, color=MUT, alpha=0.4))
    ax.add_patch(Circle((0, 0), 0.085, fill=False, lw=0.8, color=MUT, alpha=0.7))
    ra = room_alpha(e)
    ax.add_patch(Circle((0, 0), A * (1 - e), fill=False, lw=1.2,
                        ls=(0, (5, 3)), color=WARM, alpha=0.9 * ra))
    ax.add_patch(Circle((0, 0), A * (1 + e), fill=False, lw=1.2,
                        ls=(0, (5, 3)), color=COOL, alpha=0.8 * ra))

    ax.plot([np.cos(M)], [np.sin(M)], "o", ms=7, color=COOL, mec="none", alpha=0.95)
    rp = float(A * (1.0 - e * np.cos(kepler_E(np.array([M]), e)[0])))
    xl, yl = rp * np.cos(th), rp * np.sin(th)
    ax.plot([float(xl)], [float(yl)], "o", ms=7, color=WARM, mec="none", alpha=0.95)
    ax.plot([float(np.cos(M)), float(xl)], [float(np.sin(M)), float(yl)], color=INK,
            lw=0.8, alpha=0.35, ls=(0, (2, 2)))
    ax.text(0.025, 0.955, f"e = {e:.2f}", transform=ax.transAxes, fontsize=11,
            color=SEC, va="top", family="DejaVu Sans")
    d = wrap_pi(th - M)
    ax.text(0.025, 0.045, f"miss {np.degrees(d):+.0f}°", transform=ax.transAxes,
            fontsize=9, color=MUT, va="bottom", family="DejaVu Sans")

    axs = fig.add_subplot(gs[1])
    axs.set_facecolor(SURFACE)
    axs.set_ylim(-2.6, 2.6)
    axs.set_xlim(0, 1)
    axs.set_axis_off()
    axs.plot([0, 1], [0, 0], color=MUT, lw=0.8, alpha=0.5)
    WINSZ = int(T_ORB * FPS)
    j = np.arange(max(0, i - WINSZ + 1), i + 1)
    xs = np.linspace(0, 1, len(j))
    ds = wrap_pi(th_all[j] - M_w[j])
    axs.plot(xs, ds, color=INK, lw=1.3, alpha=0.9)
    axs.plot([1.0], [d], "o", ms=4.5, color=WARM, mec="none", alpha=1.0)
    axs.text(0.985, 1.03, "the miss", transform=axs.transAxes, fontsize=8,
             color=MUT, ha="right", va="bottom", family="DejaVu Sans")

    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
