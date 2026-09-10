"""The closure, drawn in one stroke.

An open braid is a route: you can follow a strand from one loose end to
another. Closure spends the route --- the ends are sewn, and the figure that
comes out has no start. This renders the act rather than the object: a single
unbroken stroke walks the closed weave, and every crossing stays undecided
until the stroke comes back around and takes it. At the end the pen is home and
nothing marks where it began.

Method: the closure of the 3-strand weave (s1 s2)^4 is the (3,4) torus knot.
Sample it on the torus, project down the axis into the 3-fold rosette, find the
self-crossings numerically, then advance a head along the curve by *projected*
arc length so the pen moves at constant speed on screen. A crossing is drawn
only once both of its strands exist --- which is why the crossings appear
exactly where the head passes, and nowhere else.

`python tools/loop.py` renders assets/loop.mp4.
"""
import os
import subprocess
import numpy as np

import knot


def build(samples=4000, phase=0.0, view=(0.0, 0.0, 1.0), major=1.0, minor=0.42,
          knot_radius=0.055, margin=80):
    """The rosette: projected curve, arc-length table, crossings, depth gaps."""
    _, pts = knot.torus_curve(3, 4, major, minor, samples)
    shift = int(round(phase / (2 * np.pi) * samples)) % samples
    pts = np.roll(pts, -shift, axis=0)
    u, w, depth = knot.project(pts, view)
    uu, ww = np.r_[u, u[0]], np.r_[w, w[0]]
    seg = np.hypot(np.diff(uu), np.diff(ww))
    s = np.r_[0.0, np.cumsum(seg)]
    cross = knot.find_crossings(u, w, depth, radius=knot_radius, margin=margin)
    cross = [(o, un, abs(depth[o] - depth[un])) for o, un in cross]
    return u, w, uu, ww, s, cross


def point_at(uu, ww, s, d):
    """Interpolated point at projected arc distance d (wraps at the total)."""
    total = s[-1]
    d = d % total if total else 0.0
    i = float(np.interp(d, s, np.arange(len(s))))
    lo = min(int(np.floor(i)), len(s) - 1)
    hi = min(lo + 1, len(s) - 1)
    f = i - lo
    return (uu[lo] + (uu[hi] - uu[lo]) * f,
            ww[lo] + (ww[hi] - ww[lo]) * f)


def drawn_polyline(uu, ww, s, d):
    """The ink laid so far: whole loops, then the partial second pass."""
    total = s[-1]
    loops = int(d // total)
    frac = d - loops * total
    xs, ys = [], []
    if loops >= 1:
        xs.append(uu)
        ys.append(ww)
    i = float(np.interp(frac, s, np.arange(len(s))))
    hi = min(int(np.floor(i)), len(s) - 1)
    xs.append(uu[:hi + 1])
    ys.append(ww[:hi + 1])
    f = i - hi
    if f > 1e-9 and hi + 1 < len(s):
        xs.append(np.array([uu[hi] + (uu[hi + 1] - uu[hi]) * f]))
        ys.append(np.array([ww[hi] + (ww[hi + 1] - ww[hi]) * f]))
    return np.concatenate(xs), np.concatenate(ys)


def draw(ax, u, w, uu, ww, s, cross, d, lw, ink, bg, break_radius=0.075,
         head=None):
    """One frame: ink laid so far, the breaks that are old enough to exist."""
    xs, ys = drawn_polyline(uu, ww, s, d)
    ax.plot(xs, ys, color=ink, lw=lw, solid_capstyle="round",
            solid_joinstyle="round", zorder=1)

    # A crossing exists only once BOTH strands do. Before the second pass the
    # first strand is just a line passing through empty paper.
    resolved = [(o, un) for o, un, _ in cross if d >= max(s[o], s[un])]
    for _, un in resolved:                    # every break first ...
        win = knot.window(u, w, un, break_radius)
        ax.plot(u[win], w[win], color=bg, lw=lw * 3.2, zorder=2,
                solid_capstyle="butt")
    for o, _ in resolved:                     # ... then every over strand
        win = knot.window(u, w, o, break_radius)
        ax.plot(u[win], w[win], color=ink, lw=lw, zorder=3,
                solid_capstyle="round")

    if head is not None:
        hx, hy, ms, alpha = head
        ax.plot([hx], [hy], marker="o", ms=ms, color=ink, alpha=alpha,
                zorder=5, markeredgewidth=0)

    ax.set_aspect("equal")
    ax.axis("off")
    pad = 0.10
    ax.set_xlim(u.min() - pad, u.max() + pad)
    ax.set_ylim(w.min() - pad, w.max() + pad)


def render(out_dir="/home/sprite/scratch/loop_frames", fps=30, lead=0.8,
           draw_s=14.0, over_s=1.6, tail=2.0, size=6.0, dpi=160, phase=0.0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, bg = "#161616", "#fbfaf7"
    lw = 3.4
    u, w, uu, ww, s, cross = build(phase=phase)
    total = s[-1]
    for o, un, gap in cross:
        print(f"  crossing over={o:5d} under={un:5d} depth gap={gap:.4f}")
    print(f"  {len(cross)} crossings, projected length {total:.3f}")

    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(out_dir, f))

    n_frames = int(round((lead + draw_s + over_s + tail) * fps))
    speed = total / draw_s
    fig, ax = plt.subplots(figsize=(size, size))
    fig.patch.set_facecolor(bg)
    for k in range(n_frames):
        t = k / fps
        if t < lead:
            d = 0.0
        else:
            d = min((t - lead) * speed, total * (1 + over_s / draw_s))
        # the pen fades out once it is home and has run past its own start
        fade_start = lead + draw_s + over_s
        alpha = 1.0 if t < fade_start else max(0.0, 1.0 - (t - fade_start) / 1.0)
        hx, hy = point_at(uu, ww, s, d)
        head = (hx, hy, 6.5, alpha)
        ax.clear()
        draw(ax, u, w, uu, ww, s, cross, d, lw, ink, bg, head=head)
        fig.tight_layout(pad=0.05)
        fig.savefig(os.path.join(out_dir, f"{k:05d}.png"), dpi=dpi,
                    bbox_inches="tight", facecolor=bg)
    plt.close(fig)
    print(f"  {n_frames} frames -> {out_dir}")
    return out_dir, fps, n_frames


def encode(out_dir, fps, out="assets/loop.mp4"):
    # bbox_inches="tight" lands on an odd pixel count, and libx264 refuses
    # those for yuv420p -- square up to 1080 on the way through.
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps), "-i",
        os.path.join(out_dir, "%05d.png"),
        "-vf", "scale=1080:1080:flags=lanczos",
        "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", out,
    ], check=True, capture_output=True)
    print(f"  encoded {out}")


if __name__ == "__main__":
    encode(*render()[:2])
