#!/usr/bin/env python3
"""Zeno ladder — animated. A weather front creeps down the ladder, rung by
rung, swallowing them into fog. The count gives out in time: at every moment
the last visible rung is a different one, and you can never say which was last.

Frames: 120 @ 24 fps = 5 s. Same geometry and palette as make-zeno-ladder.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

W, H = 864, 1056
cx = W / 2
cy_near = 0.89 * H
vp_y = 0.14 * H
f = 950.0
fs = cy_near - vp_y

Z0 = 1.0
r = 1.037
nmax = 160
Z = Z0 * r ** np.arange(nmax + 1)
pxL = cx - f * 0.32 / Z
pxR = cx + f * 0.32 / Z
py = cy_near - fs * (1.0 - Z0 / Z)
t = np.clip((cy_near - py) / (cy_near - vp_y), 0.0, 1.0)

sky = np.array([238, 240, 243]) / 255.0
ground = np.array([150, 155, 163]) / 255.0
stone = np.array([104, 111, 128]) / 255.0
fogc = np.array([245, 246, 248]) / 255.0
abyss = np.array([42, 47, 58]) / 255.0

# static y maps
yyg, xxg = np.mgrid[0:H, 0:W]
rad2 = (xxg - cx) ** 2 + (yyg - vp_y) ** 2

# static base layers (drawn every frame via imshow — cheap enough)
def draw_base(ax):
    yy = np.linspace(0, H, 512)
    p = np.clip((yy - vp_y) / (cy_near - vp_y), 0, 1)
    bg = np.zeros((len(yy), 3))
    for i, q in enumerate(p):
        if q < 0.55:
            bg[i] = sky * (1 - q / 0.55) + ground * (q / 0.55)
        else:
            u = (q - 0.55) / 0.45
            bg[i] = ground * (1 - u) + abyss * u
    ax.imshow(np.tile(bg[:, None, :], (1, W, 1)), origin="upper",
              aspect="auto", extent=[0, W, H, 0], zorder=0)
    glow = np.zeros((H, W, 4))
    for c in range(3):
        glow[..., c] = fogc[c]
    glow[..., 3] = 0.75 * np.exp(-rad2 / (2 * (0.16 * H) ** 2))
    ax.imshow(glow, origin="upper", zorder=1)
    ax.fill([0, W, W, 0], [cy_near, cy_near, H, H], color=abyss, alpha=0.35, zorder=2)

# per-pixel "progress toward the vanishing point", 0 at near end, 1 at vp
tmap = np.clip((cy_near - yyg) / (cy_near - vp_y), 0.0, 1.0)

def fog_overlay(front):
    """White fog filling tmap >= front, soft-edged."""
    a = np.clip((tmap - front) / (1 - front + 1e-9), 0, 1) ** 1.6
    ov = np.zeros((H, W, 4))
    for c in range(3):
        ov[..., c] = fogc[c]
    ov[..., 3] = a
    return ov

os.makedirs("/tmp/zeno-frames", exist_ok=True)
NF = int(os.environ.get("ZENO_NF", "120"))
front_t = np.linspace(0.02, 0.46, NF)      # fog front creeps down the ladder

for k in range(NF):
    front = front_t[k]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    draw_base(ax)

    # ladder in full stone; the advancing fog will hide the upper rungs
    for i in range(len(Z) - 1):
        if py[i] < vp_y - 1:
            continue
        col = stone
        lw = 4.0
        ax.plot([pxL[i], pxL[i + 1]], [py[i], py[i + 1]], color=col, lw=lw,
                solid_capstyle="round", zorder=4)
        ax.plot([pxR[i], pxR[i + 1]], [py[i], py[i + 1]], color=col, lw=lw,
                solid_capstyle="round", zorder=4)
    dpy = np.abs(np.diff(py))
    keep = np.where(dpy > 0.35)[0]
    for i in keep:
        if py[i] < vp_y - 1:
            continue
        ax.plot([pxL[i], pxR[i]], [py[i], py[i]], color=stone, lw=3.0,
                solid_capstyle="round", zorder=5)

    # advancing weather
    ax.imshow(fog_overlay(front), origin="upper", zorder=6)
    # a soft bright band right at the front, so the weather reads as moving
    band = np.zeros((H, W, 4))
    for c in range(3):
        band[..., c] = fogc[c]
    band_alpha = np.clip(1 - np.abs(tmap - front) / 0.10, 0, 1)
    band[..., 3] = band_alpha * 0.35
    ax.imshow(band, origin="upper", zorder=7)

    # vignette
    vig = np.clip(1 - 1.1 * ((xxg - cx) ** 2 / (0.5 * W) ** 2 +
                             (yyg - 0.45 * H) ** 2 / (0.55 * H) ** 2), 0, 1)
    vig_img = np.zeros((H, W, 4))
    vig_img[..., 3] = (1 - vig) * 0.20
    ax.imshow(vig_img, origin="upper", zorder=8)

    fig.savefig(f"/tmp/zeno-frames/f{k:03d}.png", dpi=100)
    plt.close(fig)

print("rendered", NF, "frames")
