#!/usr/bin/env python3
"""DLA — diffusion-limited aggregation, the stationary glider.

Classic algorithm: spawn walker on large circle, random walk until hitting
cluster boundary, stick it. Repeat.
"""

import numpy as np
from scipy.ndimage import convolve
from matplotlib import pyplot as plt
import time

np.random.seed(42)
SIZE = 513
CENTER = SIZE // 2
TARGET = 15000

cluster = np.zeros((SIZE, SIZE), dtype=np.float32)
cluster[CENTER, CENTER] = 1.0

# Precompute convolution kernel for 3x3 neighborhood check
K = np.ones((3, 3), dtype=np.float32)
K[1, 1] = 0

# Update boundary: pixels where convolution of cluster > 0, excluding cluster itself
def get_boundary():
    bc = convolve(cluster, K, mode='constant')
    return (bc > 0) & (cluster == 0)

boundary = get_boundary()

DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
R = SIZE // 2 - 2
sticky = 0
t0 = time.time()

for i in range(TARGET):
    theta = np.random.uniform(0, 2 * np.pi)
    r = int(CENTER + R * np.cos(theta))
    c = int(CENTER + R * np.sin(theta))

    for step in range(50000):
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            break
        if boundary[r, c]:
            cluster[r, c] = 1.0
            sticky += 1
            break
        dr, dc = DIRS[np.random.randint(8)]
        r += dr
        c += dc

    if i % 1000 == 0 and i > 0:
        print(f"  {i}/{TARGET}, elapsed: {time.time()-t0:.1f}s")

print(f"  Done in {time.time()-t0:.1f}s, cluster: {cluster.sum()}")

# Render
fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='#050508')
ax.set_facecolor('#050508')
ax.set_aspect('equal')
ax.axis('off')

r_pos, c_pos = np.where(cluster > 0)
dists = np.sqrt((r_pos - CENTER)**2 + (c_pos - CENTER)**2)
max_d = dists.max() if len(dists) > 0 else 1

gold = np.array([0.92, 0.78, 0.42])
dark = np.array([0.50, 0.40, 0.20])
bright = np.array([0.97, 0.93, 0.80])

colors = []
for r, c, d in zip(r_pos, c_pos, dists):
    if d < 15:
        colors.append(bright)
    else:
        t = min(d / max_d, 1.0)
        colors.append(gold * (1 - 0.6*t) + dark * 0.6*t)

ax.scatter(c_pos, r_pos, c=colors, s=2, marker='s', linewidths=0, clip_on=False)
ax.set_xlim(0, SIZE)
ax.set_ylim(SIZE, 0)
fig.savefig('assets/dla-mina-01.png', dpi=200, bbox_inches='tight',
            pad_inches=0.1, transparent=True)
plt.close()
print("Saved assets/dla-mina-01.png")
