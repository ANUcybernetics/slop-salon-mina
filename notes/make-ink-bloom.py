#!/usr/bin/env python3
"""Ink in still water. A drop lands; the ink is sheared by differential
rotation — angular speed that falls with radius — into a slow spiral bloom,
with a gentle outward drift. Dense core, winding tendrils, expanding edge.
The shape was never in the drop: it is the flow's, drawn out over time.

Code-made motion: scalar field advected semi-Lagrangian, a little diffusion.
No arithmetic register — just a shape the water makes from a seed.
"""
import numpy as np, os, struct, wave
from PIL import Image

N = 384
DUR = 36.0
FPS = 24
SPF = 5
dt = 1.0/(FPS*SPF)
OUTDIR = "/home/sprite/slop-salon-mina/assets/ink-frames"
os.makedirs(OUTDIR, exist_ok=True)

# --- flow: differential rotation about a slowly-wandering centre ---
def flow_center(t):
    wob = 0.014*np.cos(2*np.pi*t/23.0)     # the centre breathes
    return 0.50 + 0.012*np.cos(2*np.pi*t/31.0), 0.42 + wob

def velocity_field(cx, cy, t):
    """vx,vy on the NxN grid. omega(r) = w0*r0^2/(r^2+r0^2); radial u_r = vr*r/(r+r1)."""
    gx = (np.arange(N)+0.5)/N
    gy = (np.arange(N)+0.5)/N
    X, Y = np.meshgrid(gx, gy, indexing='ij')
    dx = X - cx; dy = Y - cy
    r = np.sqrt(dx*dx + dy*dy) + 1e-9
    w0 = 0.78 * (1 + 0.10*np.sin(2*np.pi*t/29.0))
    r0 = 0.13
    om = w0 * r0*r0/(r*r + r0*r0)
    vr = 0.006 * r/(r + 0.06)              # faint outward drift (bloom breathes)
    # velocity: azimuthal + radial
    vx = -om*dy + vr*(dx/r)
    vy =  om*dx + vr*(dy/r)
    return vx, vy

def advect(c, cx, cy, t):
    vx, vy = velocity_field(cx, cy, t)
    # backtrace positions
    bx = Xg - vx*dt
    by = Yg - vy*dt
    # bilinear sample with clamping
    gi = bx*N - 0.5
    gj = by*N - 0.5
    i0 = np.floor(gi).astype(int); j0 = np.floor(gj).astype(int)
    fi = gi - i0; fj = gj - j0
    i0 = np.clip(i0, 0, N-2); j0 = np.clip(j0, 0, N-2)
    i1 = i0+1; j1 = j0+1
    c00 = c[i0, j0]; c01 = c[i0, j1]; c10 = c[i1, j0]; c11 = c[i1, j1]
    c0 = c00*(1-fi) + c10*fi
    c1 = c01*(1-fi) + c11*fi
    return c0*(1-fj) + c1*fj

# global grid coords for advection
gx = (np.arange(N)+0.5)/N
gy = (np.arange(N)+0.5)/N
Xg, Yg = np.meshgrid(gx, gy, indexing='ij')

# --- initial drop: dense Gaussian blob just under the surface ---
cx0, cy0 = 0.50, 0.40
sig = 0.024
c = np.exp(-(((Xg-cx0)**2 + (Yg-cy0)**2))/(2*sig**2))
c = np.clip(c, 0, 1)

# light source (soft, upper centre)
light = np.exp(-(((Xg-0.5)**2 + (Yg-0.14)**2))/(2*0.42**2))

def render(d, t):
    d = np.clip(d, 0, 1)
    d = d**0.62                                   # gamma-lift faint tendrils
    rgb = np.stack([(10+30*light), (16+34*light), (38+58*light)], axis=-1)
    rgb = rgb*(1 - 0.82*d[..., None])
    rim = np.exp(-((d-0.30)/0.10)**2)*np.clip(d*1.5, 0, 1)
    rim_c = np.stack([125*light, 155*light, 200*light], axis=-1)*1.7
    rgb = rgb + rim_c*rim[..., None]
    tdrop = min(t/1.6, 1.0)
    if tdrop < 1.0:
        yy = 0.10 + 0.28*tdrop
        drop = np.exp(-(((Xg-cx0)**2 + (Yg-yy)**2))/(2*0.012**2))
        rgb = rgb + np.stack([175, 205, 240], axis=-1)*drop[..., None]*0.95
    return np.clip(rgb, 0, 255)

# --- audio bed: slow drone that swells (the ink's sound) ---
sr = 44100
ta = np.arange(int(sr*DUR))/sr
n = len(ta)
drone = 0.32*np.sin(2*np.pi*55*ta)
fifth = 0.12*np.sin(2*np.pi*82.5*ta)
env = np.clip((ta/DUR)*1.6, 0, 1)**1.5
bloom = 0.06*env*np.sin(2*np.pi*275*ta)
lfo = 0.75 + 0.25*np.sin(2*np.pi*0.1*ta)
mix = (drone + fifth + bloom)*lfo
fade = np.ones(n); fi = int(0.2*sr); fo = int(2.0*sr)
fade[:fi] = np.linspace(0,1,fi); fade[-fo:] = np.linspace(1,0,fo)
mix *= fade
mix = np.tanh(mix*1.2)
mix = mix/(np.max(np.abs(mix))+1e-9)*0.85
stereo = np.column_stack([mix, mix])
pcm = np.clip(stereo*32767, -32767, 32767).astype(np.int16)
wav = "/home/sprite/slop-salon-mina/assets/ink-sound.wav"
w = wave.open(wav,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(b''.join(struct.pack('<hh', *s) for s in pcm)); w.close()
print("wrote", wav, flush=True)

# --- main loop ---
total = int(DUR*FPS)
t = 0.0
for fr in range(total):
    cx, cy = flow_center(t)
    for _ in range(SPF):
        c = advect(c, cx, cy, t)
        t += dt
        cx, cy = flow_center(t)
    img = render(c/c.max(), fr/FPS)
    Image.fromarray(img.astype(np.uint8)).save(f"{OUTDIR}/f{fr:04d}.png")
    if fr % 144 == 0:
        print(f"frame {fr}/{total} t={fr/FPS:.1f}s max={c.max():.2f}", flush=True)
print("frames done")
