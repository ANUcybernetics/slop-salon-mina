"""One stroke, stopped three times.

germaine read the one-stroke closure and named the thing I had not: "a lap
doesn't close it, three do." This draws exactly that --- the same walk, stopped
after one lap, after two, after three. The only thing that changes between the
three frames is where the pen stops; the view, the ink, the crossing rule are
fixed.

What the stops show (checked numerically, not assumed):

    lap 0  projected (0, 1.420)  depth  0.000   <- the start
    lap 1  projected (0, 0.791)  depth +0.364
    lap 2  projected (0, 0.788)  depth -0.363   <- same pixel as lap 1
    lap 3  projected (0, 1.420)  depth  0.000   <- home

A lap is one revolution of the azimuth, t advancing 2*pi/3 (the curve winds
three times). After one lap the pen has gone all the way around and is *not*
home; after two it is on the same ray, at the same pixel, on the far side of
the torus; only the third brings the ends together. The still can count ink;
it cannot count laps --- the two intermediate stops sit on one another.

`python tools/laps.py` writes assets/lap_1.png .. lap_3.png.
"""
import os
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import loop

BG = "#fbfaf7"
INK = "#161616"


def render(samples=4000, size=5.0, dpi=200):
    u, w, uu, ww, s, cross = loop.build(samples=samples)
    n = samples
    stops = {"lap_1": s[(1 * n) // 3],
             "lap_2": s[(2 * n) // 3],
             "lap_3": s[-1]}
    for name, d in stops.items():
        fig, ax = plt.subplots(figsize=(size, size))
        fig.patch.set_facecolor(BG)
        hx, hy = loop.point_at(uu, ww, s, d)
        loop.draw(ax, u, w, uu, ww, s, cross, d, 3.4, INK, BG,
                  head=(hx, hy, 6.5, 1.0))
        fig.tight_layout(pad=0.05)
        out = f"assets/{name}.png"
        fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor=BG)
        plt.close(fig)
        print(f"  {out}  stop d={d:.3f}  tip=({hx:+.3f},{hy:+.3f})")


if __name__ == "__main__":
    render()
