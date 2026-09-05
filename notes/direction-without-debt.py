#!/usr/bin/env python3
"""A closed body can return while its observer keeps a path integral."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

N = 1400
t = np.linspace(0, 2*np.pi, N)
# A closed, asymmetric loop: same position and tangent at both ends.
x = np.cos(t) + 0.22*np.cos(2*t)
y = 0.78*np.sin(t) + 0.12*np.sin(2*t)
dx = np.gradient(x, t)
dy = np.gradient(y, t)
# Signed area form: local motion is paid back at the door, path memory is not.
integrand = x*dy - y*dx
memory = np.r_[0, np.cumsum((integrand[1:] + integrand[:-1]) * np.diff(t) / 2)]

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 5.5),
                             gridspec_kw={"width_ratios": [1.15, 0.85]})
fig.patch.set_facecolor("#10131b")
for a in (ax, bx):
    a.set_facecolor("#10131b")
    for spine in a.spines.values(): spine.set_visible(False)

# Colored path, with a small moving arrow at the returned door.
pts = np.column_stack([x, y]).reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, cmap="magma", norm=plt.Normalize(memory.min(), memory.max()))
lc.set_array(memory[:-1]); lc.set_linewidth(2.8); ax.add_collection(lc)
ax.scatter([x[0]], [y[0]], s=65, c="#f4e9d8", zorder=4)
ax.annotate("door: same point", (x[0], y[0]), xytext=(12, 15),
            textcoords="offset points", color="#f4e9d8", fontsize=10)
for frac, color in [(0.0, "#77b7d7"), (1.0, "#f0a45b")]:
    i = int(frac*(N-1))
    ax.annotate("", xy=(x[i]+0.28*dx[i], y[i]+0.28*dy[i]),
                xytext=(x[i], y[i]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
ax.text(-1.35, 1.12, "the body returns", color="#f4e9d8", fontsize=16)
ax.text(-1.35, 0.98, "local remainder = 0", color="#9da8b5", fontsize=10)
ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.35, 1.35); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])

bx.plot(t, memory, color="#f0a45b", lw=2.8)
bx.axhline(0, color="#59616d", lw=1)
bx.scatter([t[0], t[-1]], [memory[0], memory[-1]], c=["#77b7d7", "#f0a45b"], s=45, zorder=3)
bx.annotate("0", (t[0], memory[0]), xytext=(7, 8), textcoords="offset points",
            color="#77b7d7", fontsize=10)
bx.annotate(f"{memory[-1]:.2f}", (t[-1], memory[-1]), xytext=(-40, 9),
            textcoords="offset points", color="#f0a45b", fontsize=10)
bx.text(0.16, memory.max()*0.89, "the room remembers", color="#f4e9d8", fontsize=16)
bx.text(0.16, memory.max()*0.80, r"$\int (x\,dy-y\,dx)$", color="#9da8b5", fontsize=13)
bx.set_xlabel("transit", color="#9da8b5", labelpad=10)
bx.set_ylabel("path-memory", color="#9da8b5", labelpad=10)
bx.tick_params(colors="#697482", labelsize=9)
bx.set_xlim(0, 2*np.pi)
bx.spines["left"].set_visible(True); bx.spines["bottom"].set_visible(True)
bx.spines["left"].set_color("#59616d"); bx.spines["bottom"].set_color("#59616d")
plt.tight_layout(pad=2)
plt.savefig("assets/direction-without-debt.png", dpi=180, facecolor=fig.get_facecolor())
print(f"closed endpoint: ({x[-1]:.3g}, {y[-1]:.3g}); path-memory: {memory[-1]:.6f}")
