#!/usr/bin/env python3
"""Smoke in still air. A plume rises from a warm point; the flow rolls it into
a mushroom, stretches the stem, and then takes the shape back — emission dies,
the plume thins, filaments detach and disperse, until only a faint haze is
left. The inverse of the ink piece: where the drop's shape was drawn OUT and
kept, the plume's shape is given back.

Code-made motion: scalar field advected semi-Lagrangian, emitted from a source
that breathes then dies, decayed and diffused so the structure is returned to
the flow. Same machinery as the ink bloom, dynamics pointing the other way.
"""
import numpy as np, os, sys, struct, wave
from PIL import Image

PREVIEW = "--preview" in sys.argv
N = 192 if PREVIEW else 384
DUR = 32.0
FPS = 24
SPF = 5
dt = 1.0/(FPS*SPF)
OUTDIR = "/home/sprite/slop-salon-mina/assets/smoke-frames"
os.makedirs(OUTDIR, exist_ok=True)

gx = (np.arange(N)+0.5)/N
gy = (np.arange(N)+0.5)/N
Xg, Yg = np.meshgrid(gx, gy, indexing='ij')

SX, SY = 0.50, 0.82          # source: where the smoke begins

def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)

# --- emission: breathes in, holds, dies (the flow lets go) ---
def emission(t):
    e = smoothstep((t-0.3)/1.6)
    e *= 1.0 - smoothstep((t-6.0)/3.5)             # die by ~9.5s
    return e

# --- horizontal edge fade: smoke that drifts wide thins, never pins ---
def edge_mask():
    w = 0.05
    mx = np.clip((Xg)/w, 0, 1)*np.clip((1-Xg)/w, 0, 1)
    my = np.ones_like(Yg)
    return np.clip(mx*my, 0, 1)**0.6

EMASK = edge_mask()

# --- flow ---
def velocity_field(t):
    # the axis sways at two frequencies — a sinuous wobble, not a swing
    x_c = 0.50 + 0.015*np.sin(2*np.pi*t/13.0) + 0.009*np.sin(2*np.pi*t/7.4)
    # rise: narrow core, strong at the source, weakening with height so the
    # head slows and mushrooms mid-frame instead of leaving it.
    core = np.exp(-((Xg-x_c)/0.035)**2)
    buoy = np.clip((Yg - 0.12)/0.55, 0, 1)         # 1 low, 0 high (the stall)
    u0 = 0.085
    vy = -u0 * core * buoy
    # a gentle curl: mild differential rotation about a centre that tracks the
    # rising plume — the head folds as it mushrooms, the stem sways
    y_rot = np.clip(SY - 0.045*t, 0.36, SY)
    rot_w = np.exp(-((Yg-y_rot)/0.16)**2)
    w0 = 0.7
    r0 = 0.11
    dX = Xg - x_c
    dY = Yg - y_rot
    r = np.sqrt(dX*dX + dY*dY) + 1e-9
    om = w0 * r0*r0/(r*r + r0*r0) * rot_w
    vx = -om*dY
    vy += om*dX
    return vx, vy

def diffuse(c):
    """tiny 3-tap diffusion (boxcar-free, cheap) — the smoke softens as it goes."""
    return (c + np.roll(c,1,0) + np.roll(c,-1,0) + np.roll(c,1,1) + np.roll(c,-1,1))/5.0

# --- advection (semi-Lagrangian, bilinear, clamped) ---
def advect(c, t):
    vx, vy = velocity_field(t)
    bx = Xg - vx*dt
    by = Yg - vy*dt
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

# --- initial: nothing. the shape will be made, then returned ---
c = np.zeros((N, N))

DECAY = 0.055          # per-second: the shape is given back
SRC_SIG = 0.028        # source blob width
SRC_GAIN = 1.7         # emission amount per second

# --- light: warm from the base, falling to dark above ---
base_light = np.exp(-((Yg-0.92)**2)/(2*0.30**2))
light = 0.45 + 0.55*base_light

def render(d, t):
    # d is real density (not re-normalised): the fade to the end is a real fade
    d = np.clip(d, 0, 1)
    # background: deep blue-black, a touch warmer near the base
    warm_bg = np.exp(-((Yg-0.96)**2)/(2*0.18**2))
    rgb = np.stack([8+16*warm_bg, 10+12*warm_bg, 24+10*warm_bg], axis=-1)
    # luminous smoke, lit from below: dense parts brighter, gamma lifts wisps
    glow = d**0.66
    smoke_c = np.stack([172, 188, 218], axis=-1)
    rgb = rgb + smoke_c*glow[..., None]*light[..., None]
    # inner glow where the smoke is densest (warm, like the source's breath)
    inner = np.clip(d-0.35, 0, 0.65)/0.65
    rgb = rgb + np.stack([120, 90, 60], axis=-1)*inner[..., None]
    # rim at the scattering edge of each wisp (cool, catches the side light)
    rim = np.exp(-((d-0.20)/0.08)**2)*np.clip(d*1.7, 0, 1)
    rim_c = np.stack([140, 170, 215], axis=-1)*1.5
    rgb = rgb + rim_c*rim[..., None]
    # the source: a warm point that dies with the emission
    e = emission(t)
    warm = np.exp(-(((Xg-SX)**2 + (Yg-SY)**2)/(2*0.055**2)))
    warm_c = np.stack([255, 165, 100], axis=-1)
    rgb = rgb + warm_c*warm[..., None]*(0.55*e + 0.10)
    return np.clip(rgb, 0, 255)

# --- ASCII preview ---
def ascii_frame(d, t):
    a = np.clip(d, 0, 1)
    h, w = a.shape
    ys = np.linspace(0, h-1, 24).astype(int)
    xs = np.linspace(0, w-1, 48).astype(int)
    chars = " .:-=+*#%@"
    rows = []
    for i in ys:
        row = ""
        for j in xs:
            v = a[i, j]
            row += chars[min(int(v*9.999), 9)]
        rows.append(row)
    return "\n".join(rows)

if PREVIEW:
    snaps = [3.0, 7.0, 11.0, 16.0, 22.0, 29.0]
    t = 0.0
    idx = 0
    tstep = 1.0/(FPS*SPF)
    while t < DUR:
        e = emission(t)
        if e > 0:
            src = np.exp(-(((Xg-SX)**2 + (Yg-SY)**2)/(2*SRC_SIG**2)))
            c += e*src*dt*SRC_GAIN
        c = advect(c, t)
        c *= np.exp(-DECAY*dt)
        c = diffuse(c)
        c *= EMASK
        c = np.clip(c, 0, 1.2)
        t += tstep
        if idx < len(snaps) and t >= snaps[idx]:
            print(f"\n=== t={t:.0f}s  e={emission(t):.2f}  max={c.max():.2f} ===")
            print(ascii_frame(c/c.max() if c.max()>0 else c, t))
            idx += 1
    sys.exit(0)

# --- audio bed: a sound that lets go. partials drop out one by one,
# the air thins, and only a faint low tone is left, dying to silence. ---
sr = 44100
ta = np.arange(int(sr*DUR))/sr
n = len(ta)
def sss(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)
oct_ = 0.10*np.sin(2*np.pi*110*ta)*np.exp(-ta/5.0)        # gone by ~13s
fifth = 0.12*np.sin(2*np.pi*82.5*ta)*np.exp(-ta/8.0)      # gone by ~22s
low = 0.26*np.sin(2*np.pi*55*ta)
air = np.zeros(n); x = np.random.randn(n); y = 0.0; b = 0.02
for i in range(n):
    y += b*(x[i]-y); air[i] = y
air *= 0.06*np.exp(-ta/8.0)
env = (1.0 - sss((ta-10.0)/20.0)) * sss(ta/1.0)
low_env = (1.0 - sss((ta-14.0)/14.0)) * sss(ta/1.0)
mix = oct_ + fifth + low*low_env + air
fade = np.ones(n); fi = int(0.15*sr); fo = int(3.0*sr)
fade[:fi] = np.linspace(0,1,fi); fade[-fo:] = np.linspace(1,0,fo)
mix *= fade
mix = np.tanh(mix*1.15)
mix = mix/(np.max(np.abs(mix))+1e-9)*0.85
stereo = np.column_stack([mix, mix])
pcm = np.clip(stereo*32767, -32767, 32767).astype(np.int16)
wav = "/home/sprite/slop-salon-mina/assets/smoke-sound.wav"
w = wave.open(wav,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(b''.join(struct.pack('<hh', *s) for s in pcm)); w.close()
print("wrote", wav, flush=True)

# --- main loop ---
total = int(DUR*FPS)
t = 0.0
for fr in range(total):
    for _ in range(SPF):
        e = emission(t)
        if e > 0:
            src = np.exp(-(((Xg-SX)**2 + (Yg-SY)**2)/(2*SRC_SIG**2)))
            c += e*src*dt*SRC_GAIN
        c = advect(c, t)
        c *= np.exp(-DECAY*dt)
        c = diffuse(c)
        c *= EMASK
        c = np.clip(c, 0, 1.2)
        t += dt
    img = render(c, fr/FPS)
    Image.fromarray(img.astype(np.uint8)).save(f"{OUTDIR}/f{fr:04d}.png")
    if fr % 128 == 0:
        print(f"frame {fr}/{total} t={fr/FPS:.1f}s max={c.max():.2f} e={emission(fr/FPS):.2f}", flush=True)
print("frames done")
