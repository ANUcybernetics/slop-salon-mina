"""Torus knot renderer: a (p, q) curve on a torus, drawn as ink on warm white.

Why this exists: the closure of a braid is a knot. The closure of the 3-strand
weave (s1 s2)^4 is the (3, 4) torus knot -- the same eight crossings as the open
weave, with the ends spent. A torus knot is the *right* body for that object: it
is the closed braid drawn where it actually lives (on the torus), so it needs no
closure arcs and cannot jumble.

Method: sample the curve in 3D, project orthographically, find the self-
intersections numerically, and break the under-strand at each one -- the same
over/under trick as tools/braid.py, but the crossings are found rather than
built in.

`python tools/knot.py` renders assets/knot_34.png as a demo.
"""
import numpy as np


def torus_curve(p, q, major=1.0, minor=0.42, samples=3000):
    """The (p, q) curve on a torus. gcd(p, q) == 1 gives a knot."""
    t = np.linspace(0.0, 2 * np.pi, samples, endpoint=False)
    a = major + minor * np.cos(q * t)
    pts = np.stack([a * np.cos(p * t), a * np.sin(p * t),
                    minor * np.sin(q * t)], axis=1)
    return t, pts


def project(pts, view, up=(0.0, 0.0, 1.0)):
    """Orthographic projection. Returns (u, w, depth); depth grows toward view."""
    v = np.asarray(view, float)
    v = v / np.linalg.norm(v)
    right = np.cross(v, np.asarray(up, float))
    if np.linalg.norm(right) < 1e-6:
        right = np.cross(v, (1.0, 0.0, 0.0))
    right = right / np.linalg.norm(right)
    up2 = np.cross(right, v)
    return pts @ right, pts @ up2, pts @ v


def find_crossings(u, w, depth, radius, margin=80, chunk=256):
    """Parameter pairs (i, j) where the projected curve crosses itself.

    Two parameters closer than `radius` in the projection are one crossing
    unless they are within `margin` samples along the curve (then they are just
    the curve being near itself locally). Returns one (i, j) per crossing, with
    i the nearer point (larger depth).
    """
    n = len(u)

    def near(a, b):
        d = abs(a - b)
        return min(d, n - d) < margin

    seen = []
    for start in range(0, n, chunk):
        sl = slice(start, min(start + chunk, n))
        du = u[sl][:, None] - u[None, :]
        dw = w[sl][:, None] - w[None, :]
        for a, b in np.argwhere(du * du + dw * dw < radius * radius):
            i = start + int(a)
            j = int(b)
            sep = min((j - i) % n, (i - j) % n)
            if sep <= margin:
                continue
            if any((near(i, s) and near(j, t)) or (near(i, t) and near(j, s))
                   for s, t in seen):
                continue
            seen.append((i, j))
    out = []
    for i, j in seen:
        out.append((i, j) if depth[i] >= depth[j] else (j, i))
    return out


def window(u, w, k, radius):
    """Indices around k whose projected distance from k stays under `radius`."""
    n = len(u)
    lo, hi = k, k
    while True:
        nxt = (lo - 1) % n
        if nxt == hi or np.hypot(u[nxt] - u[k], w[nxt] - w[k]) > radius:
            break
        lo = nxt
    while True:
        nxt = (hi + 1) % n
        if nxt == lo or np.hypot(u[nxt] - u[k], w[nxt] - w[k]) > radius:
            break
        hi = nxt
    return np.arange(lo, hi + 1) % n


def render(ax, p, q, view, lw=2.8, ink="#161616", bg="#fbfaf7",
           major=1.0, minor=0.42, samples=3000, knot_radius=0.055,
           break_radius=0.075, margin=80):
    """Draw the (p, q) torus knot onto `ax` with correct over/under breaks."""
    _, pts = torus_curve(p, q, major, minor, samples)
    u, w, depth = project(pts, view)
    ax.plot(u, w, color=ink, lw=lw, solid_capstyle="round", zorder=1)

    cross = find_crossings(u, w, depth, radius=knot_radius, margin=margin)
    spans = []
    for over, under in cross:
        uo = window(u, w, over, break_radius)
        un = window(u, w, under, break_radius)
        spans.append((uo, un))
    for _, un in spans:                                   # every break first ...
        ax.plot(u[un], w[un], color=bg, lw=lw * 3.2, zorder=2,
                solid_capstyle="butt")
    for uo, _ in spans:                                   # ... then every over
        ax.plot(u[uo], w[uo], color=ink, lw=lw, zorder=3,
                solid_capstyle="round")

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(u.min() - 0.12, u.max() + 0.12)
    ax.set_ylim(w.min() - 0.12, w.max() + 0.12)
    return len(cross)


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bg = "#fbfaf7"
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    fig.patch.set_facecolor(bg)
    n = render(ax, 3, 4, view=(0.42, -0.78, 0.46))
    fig.tight_layout(pad=0.05)
    fig.savefig("assets/knot_34.png", dpi=200, bbox_inches="tight", facecolor=bg)
    print(f"rendered assets/knot_34.png ({n} crossings)")
