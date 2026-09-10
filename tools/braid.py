"""Braid renderer. Draws a braid word (Artin generators) as ink on warm white.

A braid word is a list of (i, sign): the strand at position i crosses the strand
at position i+1, sign +1 meaning it goes OVER. Strands are drawn vertically
(bottom -> top), adjacent positions one unit apart. Over/under is shown by a
background-colored break on the under strand.

Closure:
  - Plat closure (clean, even n only): pair the top endpoints with an arc over
    the top and the bottom endpoints with an arc under the bottom. sigma1^3 on
    2 strands closes to the trefoil. This is the readable one.
  - Markov closure (any n, often messy): connect each bottom position q to the
    top position final_perm.index(q) by an arc around the side. It jumbles for
    odd n; prefer plat when you need a clean loop.

Lesson from season two: a 2-strand braid reads thin (two threads one unit apart
= three horizontal lines with notches). Three strands and more crossings read as
a real weave. See notes/2026-09-10.md.
"""
import numpy as np


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def piecewise(param, anchors):
    """anchors: list of (p, level), p in [0,1]. Level over a param array."""
    p = np.asarray(param, float)
    y = np.empty_like(p)
    for k in range(len(anchors) - 1):
        a, la = anchors[k]
        b, lb = anchors[k + 1]
        if b < a:
            a, b, la, lb = b, a, lb, la
        mask = (p >= a) & (p <= b)
        if b == a:
            y[mask] = la
            continue
        t = (p[mask] - a) / (b - a)
        y[mask] = la + (lb - la) * smoothstep(t) if la != lb else la
    return y


def build_braid(word, n):
    """Returns (anchors, crossings, final_perm)."""
    pos = list(range(n))                       # pos[level] = strand id
    anchors = {s: [(0.0, s)] for s in range(n)}
    crossings = []
    m = len(word)
    cell = 1.0 / (m + 1)
    hw = 0.17 * cell                           # crisp crossings
    for idx, (i, sign) in enumerate(word):
        yk = (idx + 1) * cell
        a, b = pos[i], pos[i + 1]
        over, under = (a, b) if sign > 0 else (b, a)
        anchors[a] += [(yk - hw, i), (yk + hw, i + 1)]
        anchors[b] += [(yk - hw, i + 1), (yk + hw, i)]
        crossings.append({"y": yk, "over": over, "under": under})
        pos[i], pos[i + 1] = pos[i + 1], pos[i]
    for s in range(n):
        anchors[s] += [(1.0, pos.index(s))]
    return anchors, crossings, pos


def arc(ax, a, b, bulge, **kw):
    """Quadratic bezier from a to b bulging by `bulge` along the perpendicular."""
    a = np.array(a, float)
    b = np.array(b, float)
    d = b - a
    perp = np.array([-d[1], d[0]])
    nrm = perp / (np.linalg.norm(perp) + 1e-9)
    p1 = (a + b) / 2 + nrm * bulge
    t = np.linspace(0, 1, 400)
    pts = (1 - t)[:, None] ** 2 * a + 2 * (1 - t)[:, None] * t[:, None] * p1 + t[:, None] ** 2 * b
    ax.plot(pts[:, 0], pts[:, 1], **kw)


def render(ax, word, n, closure="none", lw=3.4, ink="#161616", bg="#fbfaf7"):
    """Draw a braid onto `ax`. closure: 'none' | 'plat' | 'markov'."""
    anchors, crossings, fp = build_braid(word, n)
    p = np.linspace(0, 1, 3200)
    curves = {}
    for s in range(n):
        xl = piecewise(p, anchors[s])
        curves[s] = (xl, p)
        ax.plot(xl, p, color=ink, lw=lw, zorder=1, solid_capstyle="round")
    cell = 1.0 / (len(word) + 1)
    gap = 0.46 * cell
    for c in crossings:
        xu, yu = curves[c["under"]]
        w = (yu >= c["y"] - gap) & (yu <= c["y"] + gap)
        ax.plot(xu[w], yu[w], color=bg, lw=10, zorder=2, solid_capstyle="butt")
        xo, yo = curves[c["over"]]
        w2 = (yo >= c["y"] - gap) & (yo <= c["y"] + gap)
        ax.plot(xo[w2], yo[w2], color=ink, lw=lw, zorder=3, solid_capstyle="round")
    if closure == "plat":
        assert n % 2 == 0
        for k in range(0, n, 2):
            arc(ax, (k, 0.0), (k + 1, 0.0), -0.62, color=ink, lw=lw, zorder=1)
            arc(ax, (k, 1.0), (k + 1, 1.0), 0.62, color=ink, lw=lw, zorder=1)
    elif closure == "markov":
        inv = [fp.index(s) for s in range(n)]
        for q in range(n):
            t = inv[q]
            if t == q:
                continue
            arc(ax, (q, 0.0), (t, 1.0), (1 if t > q else -1) * (n * 0.55),
                color=ink, lw=lw, zorder=1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.9, n - 1 + 0.9)
    ax.set_ylim(-0.15, 1.15)


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    word = [(0, 1), (1, 1)] * 4              # the 3-strand weave / route
    fig, ax = plt.subplots(figsize=(4.6, 6.4))
    fig.patch.set_facecolor("#fbfaf7")
    render(ax, word, 3, closure="none")
    fig.tight_layout(pad=0.05)
    fig.savefig("assets/braid_route.png", dpi=200, bbox_inches="tight",
                facecolor="#fbfaf7")
    print("rendered assets/braid_route.png")
