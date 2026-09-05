#!/usr/bin/env python3
"""A closed projection can forget an unclosed lift."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

n = 1800
t = np.linspace(0, 2*np.pi, n)
x, y, z = np.cos(t), np.sin(t), t/(2*np.pi)
pts = np.stack([x, y, z], axis=1).reshape(-1, 1, 3)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

fig = plt.figure(figsize=(11, 5.8), facecolor="#10131b")
ax = fig.add_subplot(121, projection="3d", facecolor="#10131b")
bx = fig.add_subplot(122, facecolor="#10131b")
for a in (ax, bx):
    a.set_facecolor("#10131b")

lc = Line3DCollection(segs, cmap="magma", linewidth=2.4)
lc.set_array(t[:-1])
ax.add_collection3d(lc)
ax.scatter([x[0], x[-1]], [y[0], y[-1]], [z[0], z[-1]],
           c=["#77b7d7", "#f0a45b"], s=36, depthshade=False)
ax.text2D(0.03, 0.95, "the lift does not close", transform=ax.transAxes,
          color="#f4e9d8", fontsize=15)
ax.text2D(0.03, 0.89, "one turn higher", transform=ax.transAxes,
          color="#9da8b5", fontsize=10)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, 1)
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([0, 1])
ax.set_zticklabels(["0", "1"], color="#9da8b5")
ax.view_init(elev=20, azim=35)
ax.grid(False)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.set_facecolor((0.06, 0.075, 0.105, 1))
    axis.pane.set_edgecolor("#303745")

bx.plot(x, y, color="#f0a45b", lw=3)
bx.scatter([x[0]], [y[0]], s=55, c="#77b7d7", zorder=3)
bx.scatter([x[-1]], [y[-1]], s=55, c="#f0a45b", zorder=3)
bx.annotate("same shadow", (x[0], y[0]), xytext=(12, 12),
            textcoords="offset points", color="#f4e9d8", fontsize=11)
bx.text(-1.12, 1.18, "the shadow closes", color="#f4e9d8", fontsize=15)
bx.text(-1.12, 1.04, "height is not visible here", color="#9da8b5", fontsize=10)
bx.set_aspect("equal"); bx.set_xlim(-1.35, 1.35); bx.set_ylim(-1.35, 1.35)
bx.set_xticks([]); bx.set_yticks([])
for spine in bx.spines.values(): spine.set_color("#303745")
plt.tight_layout(pad=1.5)
plt.savefig("assets/helix-shadow.png", dpi=190, facecolor=fig.get_facecolor())
print("projection endpoints:", np.linalg.norm([x[-1]-x[0], y[-1]-y[0]]))
