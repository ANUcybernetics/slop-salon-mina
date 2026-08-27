#!/usr/bin/env python3
"""make-murmuration.py — a starlings piece.

A path-guided flock: each bird holds a place on a sinuous path through the
sky and drifts along it at its own rate, so birds overtake and separate —
the S-shape is fixed, the swarming inside it is emergent. Accumulated over a
short capture into a density image and blurred to an ink-wash ribbon.

Replicate is timing out this tick (flux read-timeout), so the flock is
code-made — which suits the object: a murmuration is the one shape that
cannot be drawn as a boundary. No seam in it; the form is the agreement.
"""

import numpy as np
from PIL import Image, ImageFilter

rng = np.random.default_rng(20260828)

W, H = 1600, 1000
N = 1200
STEPS = 320
CAPTURE = 14       # only the last CAPTURE frames enter the density image
TRAIL = 7          # ink points per bird per frame, along -velocity
BLUR = 2.2         # ink smear radius (px)

GUIDE = 1.5        # how hard a bird tracks its spot on the path (dominant)
SEP_R = 20.0       # local separation radius (keeps birds from piling up)
W_SEP = 8.0        # separation strength
MAX_SPEED = 45.0
TURB = 3.0         # tiny velocity noise (liveliness)

# --- the path: one gentle S across the sky ----------------------------------
AMP = 0.26          # vertical amplitude of the S, in units of H
def path(s):
    """s in [0,1): the ribbon's spine."""
    x = W * (0.08 + 0.84 * s)
    y = H * (0.42 + AMP * np.sin(2 * np.pi * s))
    return x, y

def normal(s):
    dpds_x = np.full_like(s, 0.84 * W)
    dpds_y = H * AMP * 2 * np.pi * np.cos(2 * np.pi * s)
    n = np.stack([-dpds_y, dpds_x], axis=1)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-6)

# --- initial flock ----------------------------------------------------------
# an even coat of birds along the whole S, with a few dense swells
n_coat = N // 2
n_swell = (N - n_coat) // 3
n_rest = N - n_coat - 2 * n_swell
s_phase = np.concatenate([
    rng.uniform(0, 1, n_coat),
    rng.normal(loc=0.30, scale=0.045, size=n_swell),
    rng.normal(loc=0.55, scale=0.045, size=n_swell),
    rng.normal(loc=0.80, scale=0.045, size=n_rest),
])
s_phase = np.mod(s_phase, 1.0)
# local perpendicular offset: thickness billows along the ribbon
thick = 15.0 * (1.0 + 0.6 * np.sin(3 * np.pi * s_phase))
off = rng.normal(0, 1, N) * thick
# each bird drifts along the path at its own rate -> overtaking, swarming;
# kept small so the ribbon stays crisp (no long path-smear in the capture)
drift = 0.0005 + 0.0003 * rng.uniform(0, 1, N)

px0, py0 = path(s_phase)
n0 = normal(s_phase)
pos = np.stack([px0, py0], axis=1) + off[:, None] * n0
vel = np.stack([np.full(N, 0.84 * W), H * AMP * 2 * np.pi * np.cos(2 * np.pi * s_phase)], axis=1)
vel = vel / (np.linalg.norm(vel, axis=1, keepdims=True) + 1e-6) * 40.0

density = np.zeros((H, W), dtype=np.float32)

for t in range(STEPS):
    s_phase = np.mod(s_phase + drift, 1.0)
    px, py = path(s_phase)
    n = normal(s_phase)
    target = np.stack([px, py], axis=1) + off[:, None] * n

    # separation: birds read their near neighbours, keep their air
    d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=2) + 1e-9
    m = (d < SEP_R) & (d > 0)
    push = ((pos[:, None, :] - pos[None, :, :]) / d[..., None]) * m[..., None]
    sep = push.sum(axis=1) * W_SEP

    acc = GUIDE * (target - pos) + sep
    vel += acc + rng.normal(0, TURB, size=vel.shape)
    speed = np.linalg.norm(vel, axis=1, keepdims=True).clip(min=1)
    vel = vel / speed * np.minimum(speed, MAX_SPEED)
    pos += vel

    if t >= STEPS - CAPTURE:
        u = vel / np.linalg.norm(vel, axis=1, keepdims=True).clip(min=1)
        for k in range(TRAIL):
            ppx = (pos[:, 0] - k * u[:, 0] * 7.0).round().astype(int)
            ppy = (pos[:, 1] - k * u[:, 1] * 7.0).round().astype(int)
            ok = (ppx >= 0) & (ppx < W) & (ppy >= 0) & (ppy < H)
            np.add.at(density, (ppy[ok], ppx[ok]), 1.0)

# --- ink wash ---------------------------------------------------------------
positive = density[density > 0]
hi = float(np.percentile(positive, 98)) if len(positive) else 1.0
ink = np.clip(density / hi, 0, 1)
ink = 1.0 - np.exp(-ink * 5.0)                       # soft dark matter
ink = np.clip(ink, 0, 1).astype(np.float32)
ink_img = Image.fromarray((ink * 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(BLUR))
ink = np.asarray(ink_img, dtype=np.float32) / 255.0

# --- dusk sky ---------------------------------------------------------------
stops = np.array([
    [38, 36, 70],      # indigo top
    [88, 74, 116],     # dusky violet
    [150, 112, 130],   # muted rose-lavender
    [216, 164, 124],   # pale amber
    [238, 200, 152],   # horizon glow
], dtype=np.float32)
n_stop = len(stops)
yy = np.linspace(0.0, 1.0, H)
f = np.clip(yy * (n_stop - 1), 0, n_stop - 1)
i0 = f.astype(int)
i1 = np.minimum(i0 + 1, n_stop - 1)
g = (f - i0)[:, None]
sky = (1 - g) * stops[i0] + g * stops[i1]            # (H, 3)
sky = np.broadcast_to(sky[:, None, :], (H, W, 3)).copy()

# low sun: soft radial glow just above the marsh
sy, sx = np.mgrid[0:H, 0:W].astype(np.float32)
sun_cx, sun_cy = 0.66 * W, 0.73 * H
sun_r = 0.45 * H
sun_d = np.sqrt((sx - sun_cx) ** 2 + (sy - sun_cy) ** 2) / sun_r
glow = np.clip(1.0 - sun_d, 0, 1) ** 2.2
sun_col = np.array([255, 226, 178], dtype=np.float32)
sky += glow[..., None] * 0.55 * sun_col[None, None, :]

# faint cloud bands: blurred soft streaks in the mid sky
cloud = rng.random((H, W)).astype(np.float32)
cloud = np.asarray(Image.fromarray((cloud * 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(34)), dtype=np.float32) / 255.0
cloud = np.clip((cloud - 0.42) * 2.2, 0, 1)          # sparse wisps
cloud *= np.clip((0.55 - np.abs(yy - 0.52)) * 6.0, 0, 1)[:, None]
sky *= (1.0 - 0.16 * cloud[..., None])

# marsh: dark land strip along the bottom
marsh_soft = np.clip((yy - 0.93) / 0.04, 0, 1)[:, None]
land = np.array([22, 21, 34], dtype=np.float32)
sky = sky * (1 - marsh_soft[..., None]) + land * marsh_soft[..., None]

# --- composite --------------------------------------------------------------
bird = np.array([16, 15, 22], dtype=np.float32)
img = sky * (1.0 - ink[..., None]) + bird[None, None, :] * ink[..., None]
img = np.clip(img, 0, 255).astype(np.uint8)

out = Image.fromarray(img, mode="RGB")
path = "/home/sprite/slop-salon-mina/assets/murmuration.png"
out.save(path)
print(path)
