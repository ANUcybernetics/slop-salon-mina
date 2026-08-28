#!/usr/bin/env python3
"""Zeno ladder — a ladder descending away, its rungs crowding and dissolving.

Camera above, looking down a ladder that descends away into fog. The near
rungs (bottom) are dark and distinct; the rungs crowd toward the vanishing
point (upper frame) and dissolve into weather. The rung depths are log-spaced,
so the ladder recedes naturally; the fog hides the tail — you cannot say where
the rungs stop being rungs. The count gives out in weather.

Second step in the weather register. Portrait frame, matches staircase-fog.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- frame ---
W, H = 864, 1056
cx = W / 2
cy_near = 0.89 * H          # near rung sits low in the frame
vp_y = 0.14 * H             # vanishing point (fog heart) high in the frame
f = 950.0
fs = cy_near - vp_y         # = f*s, the descent's projected drop

# --- world: log-spaced rungs ---
Z0 = 1.0
r = 1.037
nmax = 160
Z = Z0 * r ** np.arange(nmax + 1)

# projected rung geometry (camera looking down the descent, away)
pxL = cx - f * 0.32 / Z
pxR = cx + f * 0.32 / Z
py = cy_near - fs * (1.0 - Z0 / Z)     # rises toward vp_y as Z grows

t = np.clip((cy_near - py) / (cy_near - vp_y), 0.0, 1.0)
fog = t ** 1.6

# --- palette (dark stone structure, pale weather) ---
sky = np.array([238, 240, 243]) / 255.0        # pale fog air
ground = np.array([150, 155, 163]) / 255.0     # the slope the ladder lies on
stone = np.array([104, 111, 128]) / 255.0      # near ladder, lit slate
fogc = np.array([245, 246, 248]) / 255.0       # weather white
abyss = np.array([42, 47, 58]) / 255.0         # deep bottom

fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")

# --- background: fog white at top, mid ground, darkening to abyss at bottom ---
yy = np.linspace(0, H, 512)
p = np.clip((yy - vp_y) / (cy_near - vp_y), 0, 1)   # 0 at vp, 1 at near
bg = np.zeros((len(yy), 3))
for i, q in enumerate(p):
    # top: sky/fog -> ground -> abyss near the bottom
    if q < 0.55:
        bg[i] = sky * (1 - q / 0.55) + ground * (q / 0.55)
    else:
        u = (q - 0.55) / 0.45
        bg[i] = ground * (1 - u) + abyss * u
ax.imshow(np.tile(bg[:, None, :], (1, W, 1)), origin="upper",
          aspect="auto", extent=[0, W, H, 0], zorder=0)

# --- a soft light rising from the fog (the vanishing point glow) ---
yyg, xxg = np.mgrid[0:H, 0:W]
glow = np.zeros((H, W, 4))
for c in range(3):
    glow[..., c] = fogc[c]
rad2 = ((xxg - cx) ** 2 + (yyg - vp_y) ** 2)
glow[..., 3] = 0.75 * np.exp(-rad2 / (2 * (0.16 * H) ** 2))
ax.imshow(glow, origin="upper", zorder=1)

# --- ground slope: a slightly darker wedge under the ladder ---
ax.fill([0, W, W, 0], [cy_near, cy_near, H, H], color=abyss, alpha=0.35, zorder=2)

def mix(g):
    g = np.clip(g, 0, 1)
    return stone * (1 - g) + fogc * g

# --- rails ---
for side in (-1, 1):
    xs = cx + side * f * 0.32 / Z
    for i in range(len(Z) - 1):
        g = fog[i]
        if g > 0.995:
            break
        col = mix(g)
        lw = 4.0 * (1 - g) + 0.6
        ax.plot([xs[i], xs[i + 1]], [py[i], py[i + 1]], color=col, lw=lw,
                solid_capstyle="round", zorder=4, alpha=1 - 0.92 * g)

# --- rungs ---
dpy = np.abs(np.diff(py))
keep = np.where(dpy > 0.35)[0]
for i in keep:
    g = fog[i]
    if g > 0.99:
        continue
    col = mix(g)
    lw = 3.0 * (1 - g) + 0.4
    ax.plot([pxL[i], pxR[i]], [py[i], py[i]], color=col, lw=lw,
            solid_capstyle="round", zorder=5, alpha=1 - 0.92 * g)

# --- fog haze: white, densest at the vanishing point, per-pixel alpha ---
low = np.clip((vp_y - yyg) / (vp_y), 0, 1) ** 1.6 + np.exp(-rad2 / (2 * (0.2 * H) ** 2))
haze = np.zeros((H, W, 4))
for c in range(3):
    haze[..., c] = fogc[c]
haze[..., 3] = np.clip(0.62 * low, 0, 1)
ax.imshow(haze, origin="upper", zorder=6)

# --- vignette: gently darken the frame edges ---
vig = np.clip(1 - 1.1 * ((xxg - cx) ** 2 / (0.5 * W) ** 2 +
                         (yyg - 0.45 * H) ** 2 / (0.55 * H) ** 2), 0, 1)
vig_img = np.zeros((H, W, 4))
vig_img[..., 3] = (1 - vig) * 0.20
ax.imshow(vig_img, origin="upper", zorder=7)

fig.savefig("assets/zeno-ladder-0.png", dpi=100)
print("wrote assets/zeno-ladder-0.png")
