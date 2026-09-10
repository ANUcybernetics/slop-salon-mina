"""Braid renderer. Draws a braid word (Artin generators) as ink on warm white.

A braid word is a list of (i, sign): the strand at position i crosses the strand
at position i+1, sign +1 meaning it goes OVER. Strands are drawn vertically
(bottom -> top), adjacent positions one unit apart. Over/under is shown by a
background-colored break on the under strand.

Closure:
  - Standard closure (any n): connect top position i to bottom position i.
    Correctly drawn it adds ZERO crossings -- the arcs go around the outside of
    the braid, nested, and never cross a strand. This is the one that keeps an
    odd-n weave legible: (s1 s2)^4 on 3 strands closes to a single knot.
  - Plat closure (even n only): pair the endpoints over the top and under the
    bottom. sigma1^3 on 2 strands closes to the trefoil.
  - Markov closure: the standard closure but with the arcs bulging *through* the
    figure -- it jumbles for odd n. Kept for comparison; that jumble is a
    drawing artifact, not a fact about the braid.

Lesson from season two: work in natural units -- strands one unit apart, one
crossing per unit of height. A braid normalized to height 1 and then stretched
reads as stacked horizontals with steps, not as crossings; the crossings are
only X's when they are about as tall as they are wide. Three strands and more
crossings read as a real weave; two read thin. See notes/2026-09-10.md.
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


def build_braid(word, n, hw=0.36):
    """Returns (anchors, crossings, final_perm, hw).

    Natural units: strands one unit apart, one crossing per unit of height,
    each crossing taking 2*hw of it. So an m-crossing braid is m units tall --
    `hw=0.36` leaves 0.14 of flat run between crossings, which is what makes a
    crossing read as an X with vertical runs rather than a staircase step.
    Do NOT normalize the braid to height 1 and then stretch it: the stretch
    flattens the crossings back into steps.
    """
    pos = list(range(n))                       # pos[level] = strand id
    anchors = {s: [(0.0, s)] for s in range(n)}
    crossings = []
    for idx, (i, sign) in enumerate(word):
        yk = idx + 0.5
        a, b = pos[i], pos[i + 1]
        over, under = (a, b) if sign > 0 else (b, a)
        anchors[a] += [(yk - hw, i), (yk + hw, i + 1)]
        anchors[b] += [(yk - hw, i + 1), (yk + hw, i)]
        crossings.append({"x": i + 0.5, "y": yk, "over": over, "under": under})
        pos[i], pos[i + 1] = pos[i + 1], pos[i]
    for s in range(n):
        anchors[s] += [(float(len(word)), pos.index(s))]
    return anchors, crossings, pos, hw


def disc(curve, xc, yc, radius):
    """Indices of a strand within `radius` of (xc, yc). The strand is monotone
    in y, so this is one contiguous run -- the notch for an over/under break."""
    x, y = curve
    return (x - xc) ** 2 + (y - yc) ** 2 <= radius * radius


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


def catmull_rom(points, per_seg=48):
    """Smooth a polyline through `points` (Catmull-Rom; no scipy needed)."""
    pts = np.asarray(points, float)
    ext = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]])
    t = np.linspace(0, 1, per_seg, endpoint=False)[:, None]
    out = []
    for k in range(len(pts) - 1):
        p0, p1, p2, p3 = ext[k], ext[k + 1], ext[k + 2], ext[k + 3]
        out.append(0.5 * (2 * p1 + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1][None, :])
    return np.vstack(out)


def closure_arcs(n, height):
    """The standard closure, routed around the outside of the braid.

    Connects top position i to bottom position i with an arc that lives outside
    x in [0, n-1] and outside y in [0, height], nested so no two arcs cross and
    no arc crosses a strand. Returns [(position, polyline), ...]. Left-hand
    positions nest outward; the right half runs on the right.
    """
    arcs = []
    for i in range(n):
        k = min(i, n - 1 - i)                       # nesting depth
        right = i >= n / 2.0                        # right half runs right
        H = 0.55 + k * 0.60                         # clearance above/below
        Rx = 0.75 + k * 1.45                        # lateral reach
        sign = 1.0 if right else -1.0
        pts = [(i, height), (i, height + H * 0.55), (i + sign * Rx * 0.45, height + H),
               (i + sign * (Rx + 0.55), height + H - 0.6),
               (i + sign * (Rx + 0.55), H - 0.6),
               (i + sign * Rx * 0.45, -H), (i, -H * 0.55), (i, 0.0)]
        arcs.append((i, catmull_rom(pts)))
    return arcs


def render(ax, word, n, closure="none", lw=3.4, ink="#161616", bg="#fbfaf7",
           zorder=1, break_r=0.075):
    """Draw a braid onto `ax`. closure: 'none' | 'standard' | 'plat' | 'markov'."""
    anchors, crossings, fp, hw = build_braid(word, n)
    height = float(len(word))
    p = np.linspace(0.0, height, 4000)
    curves = {}
    for s in range(n):
        curves[s] = (piecewise(p, anchors[s]), p)
        ax.plot(curves[s][0], curves[s][1], color=ink, lw=lw, zorder=zorder,
                solid_capstyle="round")
    for c in crossings:
        # The over/under break is a DISC around the crossing point, not a band
        # along the strand: a band as long as the crossing window follows the
        # strand's own path and gashes it open far past the ink it must hide.
        # `break_r` is in braid units -- keep it a little above the ink width
        # (lw in points, converted by the saved figure's scale).
        wu = disc(curves[c["under"]], c["x"], c["y"], break_r)
        ax.plot(curves[c["under"]][0][wu], curves[c["under"]][1][wu], color=bg,
                lw=lw * 3, zorder=zorder + 1, solid_capstyle="butt")
        wo = disc(curves[c["over"]], c["x"], c["y"], break_r)
        ax.plot(curves[c["over"]][0][wo], curves[c["over"]][1][wo], color=ink,
                lw=lw, zorder=zorder + 2, solid_capstyle="round")
    extent = [np.array([[0.0, 0.0], [n - 1.0, height]])]
    if closure == "standard":
        for _, pts in closure_arcs(n, height):
            extent.append(pts)
            ax.plot(pts[:, 0], pts[:, 1], color=ink, lw=lw, zorder=zorder,
                    solid_capstyle="round")
    elif closure == "plat":
        assert n % 2 == 0
        for k in range(0, n, 2):
            arc(ax, (k, 0.0), (k + 1, 0.0), -0.62, color=ink, lw=lw,
                zorder=zorder)
            arc(ax, (k, height), (k + 1, height), 0.62, color=ink, lw=lw,
                zorder=zorder)
    elif closure == "markov":
        inv = [fp.index(s) for s in range(n)]
        for q in range(n):
            t = inv[q]
            if t == q:
                continue
            arc(ax, (q, 0.0), (t, height), (1 if t > q else -1) * (n * 0.55),
                color=ink, lw=lw, zorder=zorder)
    allpt = np.vstack(extent)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(allpt[:, 0].min() - 0.5, allpt[:, 0].max() + 0.5)
    ax.set_ylim(allpt[:, 1].min() - 0.4, allpt[:, 1].max() + 0.4)


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    word = [(0, 1), (1, 1)] * 4              # the 3-strand weave / route
    for name, cl in [("braid_route", "none"), ("braid_closed", "standard")]:
        fig, ax = plt.subplots(figsize=(5.2, 7.4))
        fig.patch.set_facecolor("#fbfaf7")
        render(ax, word, 3, closure=cl)
        fig.tight_layout(pad=0.05)
        fig.savefig(f"assets/{name}.png", dpi=200, bbox_inches="tight",
                    facecolor="#fbfaf7")
        print(f"rendered assets/{name}.png")
