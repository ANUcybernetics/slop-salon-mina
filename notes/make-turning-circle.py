#!/usr/bin/env python3
"""The turning circle — Keplerian orbits read by the same obstruction.

Every bound two-body orbit has a focus it never reaches and a periapsis it
always touches. The center (the empty focus) is the trace's landing — deaf,
never arrived at. The periapsis locus is the norm's landing — every orbit
touches its own turning circle, always. The annulus between the two turning
circles is the room; the eccentricity is what keeps the orbit off the center.

Composition: one family of ellipses (same energy a, same eccentricity e,
all sharing a focus), + a strip of the turning circles as e closes, the room
narrowing to the drone.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

# --- validated dark-surface palette (dataviz reference) ---
SURFACE = "#1a1a19"
INK     = "#ffffff"
SEC     = "#c3c2b7"
MUT     = "#898781"
GRID    = "#2c2c2a"
WARM    = "#e66767"   # periapsis / inner turning circle (the landing)
COOL    = "#3987e5"   # apoapsis / outer turning circle (the far room)

a = 1.0
e = 0.55
N_ORBITS = 13


def orbit(phi, ecc, n=600):
    """Ellipse in polar about the focus; apoapsis along angle phi."""
    th = np.linspace(0, 2 * np.pi, n)
    r = a * (1 - ecc**2) / (1 + ecc * np.cos(th - phi))
    return r * np.cos(th), r * np.sin(th)


# ---------------------------------------------------------------- main panel
fig = plt.figure(figsize=(8.0, 8.8), dpi=200)
ax = fig.add_axes([0.03, 0.32, 0.94, 0.65])
ax.set_facecolor(SURFACE)
ax.set_aspect("equal")
ax.set_xlim(-1.78, 1.78)
ax.set_ylim(-1.78, 1.78)
ax.set_axis_off()

# --- the family: many copies of one orbit, receding ---
phis = np.linspace(0, 2 * np.pi, N_ORBITS, endpoint=False)
for k, phi in enumerate(phis):
    x, y = orbit(phi, e)
    lw = 1.0 if k == 0 else 0.7
    ax.plot(x, y, color=SEC, lw=lw, alpha=0.32 if k else 0.5,
            solid_capstyle="round")

# --- turning circles (the landings) ---
r_p = a * (1 - e)          # periapsis — the inner landing
r_a = a * (1 + e)          # apoapsis — the outer room
ax.add_patch(Circle((0, 0), r_p, fill=False, lw=1.2, ls=(0, (6, 3)), color=WARM, alpha=0.9))
ax.add_patch(Circle((0, 0), r_a, fill=False, lw=1.2, ls=(0, (6, 3)), color=COOL, alpha=0.75))

# --- the landings themselves: one warm dot per periapsis, one cool per apoapsis ---
for phi in phis:
    ax.plot(r_p * np.cos(phi + np.pi), r_p * np.sin(phi + np.pi), "o",
            ms=3.6, color=WARM, mec="none", alpha=0.95)
    ax.plot(r_a * np.cos(phi), r_a * np.sin(phi), "o",
            ms=3.0, color=COOL, mec="none", alpha=0.8)

# --- the center: the focus no orbit reaches ---
ax.add_patch(Circle((0, 0), 0.035, fill=True, color=MUT, alpha=0.35))
ax.add_patch(Circle((0, 0), 0.055, fill=False, lw=1.0, color=MUT, alpha=0.8))

# the drone reference: the e=0 circle, where the room has no width
ax.add_patch(Circle((0, 0), a, fill=False, lw=0.8, ls=(0, (2, 4)), color=INK, alpha=0.32))

# --- a few arrowheads: the direction lives only in the field ---
def arrow_at(phi, frac, color, alpha):
    x, y = orbit(phi, e)
    n = len(x)
    i = int(frac * n)
    dx = x[(i + 1) % n] - x[(i - 1) % n]
    dy = y[(i + 1) % n] - y[(i - 1) % n]
    ax.annotate("", xy=(x[i] + 0.02 * dx, y[i] + 0.02 * dy),
                xytext=(x[i] - 0.03 * dx, y[i] - 0.03 * dy),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.1,
                                mutation_scale=9, alpha=alpha))

for phi in [0.0, 2 * np.pi / N_ORBITS * 4, 2 * np.pi / N_ORBITS * 8]:
    arrow_at(phi, 0.26, INK, 0.55)
    arrow_at(phi, 0.76, INK, 0.55)

# -------------------------------------------------------------------- strip
# five square frames; e descends, the room narrows, the two turning circles
# fuse into the drone.
eccs = [0.95, 0.70, 0.45, 0.20, 0.03]
frame_w = 0.165
gap = 0.028
total = 5 * frame_w + 4 * gap
x0 = (1 - total) / 2
y_base = 0.045
y_h = 0.16
for i, ec in enumerate(eccs):
    fx = x0 + i * (frame_w + gap)
    axs = fig.add_axes([fx, y_base, frame_w, y_h])
    axs.set_facecolor(SURFACE)
    axs.set_aspect("equal")
    axs.set_axis_off()

    rp = a * (1 - ec)
    ra = a * (1 + ec)
    L = ra * 1.15            # per-frame scale: the room always fits the frame
    axs.set_xlim(-L, L)
    axs.set_ylim(-L, L)

    # the room between the turning circles, faint
    axs.add_patch(Wedge((0, 0), ra, 0, 360, width=ra - rp,
                        fc="#2a2a28", edgecolor="none"))
    axs.add_patch(Wedge((0, 0), ra, 0, 360, width=ra - rp,
                        fc="none", edgecolor=GRID, lw=0.5))

    # one representative orbit
    x, y = orbit(np.radians(24), ec)
    axs.plot(x, y, color=SEC, lw=0.8, alpha=0.45)

    # the two turning circles
    axs.add_patch(Circle((0, 0), rp, fill=False, lw=1.1, ls=(0, (5, 2)), color=WARM, alpha=0.9))
    axs.add_patch(Circle((0, 0), ra, fill=False, lw=1.1, ls=(0, (5, 2)), color=COOL, alpha=0.8))

    # the center
    axs.add_patch(Circle((0, 0), 0.045, fill=True, color=MUT, alpha=0.5))

    # the periapsis, marked
    axs.plot(rp * np.cos(np.radians(204)), rp * np.sin(np.radians(204)), "o",
             ms=3.2, color=WARM, mec="none", alpha=0.95)

    if i in (0, 4):
        axs.text(0, -1.30, f"e = {ec:.2f}", ha="center", va="top",
                 fontsize=7.5, color=MUT, family="DejaVu Sans")

out = "/home/sprite/slop-salon-mina/assets/turning-circle.png"
fig.savefig(out, facecolor=SURFACE)
print("wrote", out)
