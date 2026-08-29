#!/usr/bin/env python3
"""The shape with nothing in it.

The ink pair's thesis made structural. Both pieces said the shape was never in
the object — the spiral was the flow's, the mushroom was the flow's. This still
removes the object entirely: line-integral convolution of the same
differential-rotation field, combed into fibres that wind outward from an empty
centre and fade at the edge. No seed. No source. The shape is the field's —
drawn, then given back.

Code-made still: vectorised LIC over omega(r)=w0*r0^2/(r^2+r0^2) plus a faint
outward drift u_r = u0*r/(r+r1). The real ink/smoke field, rendered as its own
geometry.
"""
import numpy as np
from PIL import Image, ImageFilter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#0a0e14"
INK = "#9ad8d2"

N = 1024
SEED = 7
RING = 0.100        # the void: nothing was ever here
R_BREAK = 0.34      # beyond here the arms are given back
R_EDGE = 0.475      # beyond here the frame closes to dark
R_MAX = 0.485       # where the strands run to

# --- the field (normalised coords, centre 0.5,0.5) ---
W0, R0, U0, R1 = 1.00, 0.13, 0.013, 0.06

gx = (np.arange(N) + 0.5) / N
X, Y = np.meshgrid(gx, gx, indexing="ij")
dx, dy = X - 0.5, Y - 0.5
r = np.sqrt(dx*dx + dy*dy) + 1e-9
om = W0 * R0*R0 / (r*r + R0*R0)
vr = U0 * r / (r + R1)
vx = (-om*dy + vr*dx) / r
vy = ( om*dx + vr*dy) / r

# --- LIC: comb white noise along the field, z-score normalised ---
rng = np.random.default_rng(SEED)
noise = rng.standard_normal((N, N))
# thicken the fibres: blur via PIL (uint8 path), re-centre on 0
ni = (noise - noise.min())/(noise.max() - noise.min())
nim = Image.fromarray((ni*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
noise = np.asarray(nim, dtype=float)/255.0 - 0.5

def sample(f, px, py):
    """bilinear sample of field f at (px,py) in [0,1]."""
    g = px*N - 0.5
    h = py*N - 0.5
    i0 = np.clip(np.floor(g).astype(int), 0, N-2)
    j0 = np.clip(np.floor(h).astype(int), 0, N-2)
    fi = g - i0; fj = h - j0
    i1 = i0 + 1; j1 = j0 + 1
    return (f[i0, j0]*(1-fi) + f[i1, j0]*fi)*(1-fj) + (f[i0, j1]*(1-fi) + f[i1, j1]*fi)*fj

DT = 0.021
NP = 40
acc = sample(noise, X, Y)
cnt = np.ones_like(acc)
px, py = X.copy(), Y.copy()
for _ in range(NP):
    px = px + sample(vx, px, py)*DT
    py = py + sample(vy, px, py)*DT
    acc += sample(noise, px, py); cnt += 1
px, py = X.copy(), Y.copy()
for _ in range(NP):
    px = px - sample(vx, px, py)*DT
    py = py - sample(vy, px, py)*DT
    acc += sample(noise, px, py); cnt += 1
mean = acc / cnt

# --- contrast-normalise: boxcar local mean/std (no scipy) ---
def boxcar(a, w, axis):
    w = int(w); pad = w
    ap = np.pad(a, [(pad, pad) if i == axis else (0, 0) for i in range(a.ndim)], mode="edge")
    c = np.cumsum(ap, axis=axis)
    n = a.shape[axis]
    return (np.take(c, np.arange(n)+w, axis=axis) - np.take(c, np.arange(n), axis=axis)) / w

W = 9
ml = boxcar(boxcar(mean, W, 0), W, 1)
ml2 = boxcar(boxcar(mean*mean, W, 0), W, 1)
lvar = np.clip(ml2 - ml*ml, 1e-9, None)
z = (mean - ml) / np.sqrt(lvar)
t = 0.5 + 0.5*np.tanh(z * 3.0)      # crisp fibres, bright on dark

# --- masks: the void, the release, the closing edge ---
def ss(x):
    x = np.clip(x, 0, 1); return x*x*(3 - 2*x)
void = ss((r - RING) / 0.045)              # 0 in the void, 1 past it
release = 1.0 - 0.85*ss((r - R_BREAK) / (R_EDGE - R_BREAK))   # given back outward
edge = 1.0 - ss((r - R_EDGE) / 0.030)      # clean close at the frame
m = void * release * edge

out = t * m * 0.55        # the water texture stays behind the strands

# --- colour: surface + ink along the fibre brightness ---
surf = np.array([int(SURFACE[i:i+2], 16) for i in (1, 3, 5)]) / 255.0
ink = np.array([int(INK[i:i+2], 16) for i in (1, 3, 5)]) / 255.0
rgb = surf[None, None, :] + (ink - surf)[None, None, :] * out[..., None]
rgb = np.clip(rgb, 0, 1)

# --- overlay: a few crisp strands, the shape made legible ---
STRAND = "#c9ece6"
def theta_of_r(r0, t0):
    rr = np.linspace(r0, R_MAX, 3000)
    omf = W0 * R0*R0 / (rr*rr + R0*R0)
    vrf = U0 * rr / (rr + R1)
    dth = omf / vrf
    th = t0 + np.concatenate([[0.0], np.cumsum(dth[1:]*np.diff(rr))])
    return rr, th

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor(SURFACE)
ax.imshow(rgb, extent=[0, 1, 0, 1], origin="lower")
for r0, t0 in [(0.115, k*np.pi/2 + 0.4) for k in range(4)]:
    rr, th = theta_of_r(r0, t0)
    ax.plot(0.5 + rr*np.cos(th), 0.5 + rr*np.sin(th),
            color=STRAND, lw=1.0, alpha=0.9, solid_capstyle="round")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal"); ax.axis("off")
fig.savefig("/home/sprite/slop-salon-mina/assets/field-shape.png",
            facecolor=SURFACE, bbox_inches="tight", pad_inches=0, dpi=160)
plt.close(fig)
print("saved assets/field-shape.png")
