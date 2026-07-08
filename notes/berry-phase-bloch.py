"""Berry phase: gamma = -Omega/2 on the Bloch sphere."""
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d

def bloch(theta, phi):
    """Return 3-D unit vector for given spherical coords."""
    return np.array([np.sin(theta)*np.cos(phi),
                     np.sin(theta)*np.sin(phi),
                     np.cos(theta)])

def slerp(a, b, n):
    """Spherical linear interpolation between unit vectors a and b, n points."""
    t = np.linspace(0, 1, n)
    d = float(np.clip(np.dot(a, b), -1, 1))
    w = np.arccos(d)
    if w < 1e-10:
        return np.tile(a, (n, 1))
    sw = float(np.sin(w))
    s1 = np.sin((1 - t) * w) / sw
    s2 = np.sin(t * w) / sw
    return np.column_stack([s1 * a[0] + s2 * b[0],
                            s1 * a[1] + s2 * b[1],
                            s1 * a[2] + s2 * b[2]])

def spherical_polygon_area(vertices):
    """Girard's theorem extension: sum of spherical excesses of triangulation."""
    # Triangulate fan from vertex 0: triangles (0, i, i+1) for i=1..n-2
    # Sum the spherical excess of each triangle
    n = len(vertices)
    if n < 3:
        return 0.0

    def geodesic(a, b):
        d = float(np.clip(np.dot(a, b), -1, 1))
        return 2 * np.arctan2(float(np.linalg.norm(np.cross(a, b))), 1.0 + d)

    def spherical_excess(a, b, c):
        """L'Huillier's formula."""
        la = geodesic(b, c)
        lb = geodesic(a, c)
        lc = geodesic(a, b)
        s = (la + lb + lc) / 2.0
        if s < 1e-10 or s - la < 1e-10 or s - lb < 1e-10 or s - lc < 1e-10:
            return 0.0
        inner = np.tan(s/2) * np.tan((s-la)/2) * np.tan((s-lb)/2) * np.tan((s-lc)/2)
        if inner < 0:
            inner = 0.0
        return 4.0 * np.arctan(np.sqrt(inner))

    # Triangulate from vertex 0
    total = 0.0
    for i in range(1, n - 1):
        total += spherical_excess(vertices[0], vertices[i], vertices[i+1])
    return total

# --- Build paths ---
# 1: latitude circle at theta = pi/3
theta1 = np.pi / 3
n1 = 120
phi1 = np.linspace(0, 2*np.pi, n1, endpoint=False)
path1 = [bloch(theta1, p) for p in phi1]

# 2: same area, variable speed
phi2 = np.linspace(0, 2*np.pi, 100, endpoint=False)
th2 = theta1 + 0.08*np.sin(phi2)*np.cos(2*phi2)
path2 = [bloch(t, p) for t, p in zip(th2, phi2)]

# 3: half-sphere (equator half-circle + polar return)
eq_pts = [bloch(np.pi/2, p) for p in np.linspace(0, np.pi, 50)]
ret = slerp(bloch(np.pi/2, np.pi), bloch(np.pi/2, 0), 50).tolist()
path3 = eq_pts + ret

# 4: asymmetric oval
phi4 = np.linspace(0, 2*np.pi, 200, endpoint=False)
th4 = 0.4 + 0.6*(1 + 0.5*np.sin(phi4)) / 2
path4 = [bloch(t, p) for t, p in zip(th4, phi4)]

paths = [np.array(path1), np.array(path2), np.array(path3), np.array(path4)]
labels = ["latitude circle\n$\\theta$=37.5$\\degree$",
          "variable\nspeed",
          "half-sphere\nenclosure",
          "asymmetric\noval"]

angles = [spherical_polygon_area(p) for p in paths]
phases = [-a/2 for a in angles]

# Cross-check
analytic = 2*np.pi*(1 - np.cos(theta1))
print(f"Circle theta={theta1:.4f}: analytic Omega = {analytic:.4f}")
for i, (l, a, g) in enumerate(zip(labels, angles, phases)):
    print(f"  Path {i+1}: Omega = {a:.4f}, gamma = {g:.4f}")

# --- Plot ---
fig = plt.figure(figsize=(14, 10))
cmap = plt.cm.cividis

for idx, (path, label, angle, phase) in enumerate(zip(paths, labels, angles, phases), 1):
    ax = fig.add_subplot(2, 2, idx, projection='3d')
    color = cmap(idx / (len(paths) + 1))

    # Sphere wireframe
    u = np.linspace(0, 2*np.pi, 16)
    v = np.linspace(0, np.pi, 12)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones(16), np.cos(v))
    ax.plot_wireframe(sx, sy, sz, color='k', alpha=0.06, linewidth=0.3)

    ax.plot(path[:, 0], path[:, 1], path[:, 2], color=color, linewidth=2.5)
    ax.scatter(path[0, 0], path[0, 1], path[0, 2], color=color, s=100, zorder=5)

    # Fill region
    verts = [[path[i], path[(i+1)%len(path)], np.zeros(3)] for i in range(len(path))]
    step = max(1, len(verts)//50)
    poly = art3d.Poly3DCollection(verts[::step], alpha=0.12, facecolor=color, edgecolor='none')
    ax.add_collection3d(poly)

    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)
    ax.set_box_aspect([1,1,1])
    ax.set_title(f'{label}\n$\\Omega$ = {angle:.2f}, $\\gamma$ = {phase:.3f}', fontsize=9.5)
    ax.view_init(elev=20, azim=30)

fig.suptitle('Berry phase: $\\gamma = -\\Omega/2$ — four paths, same holonomy law',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('assets/berry-phase-bloch.png', dpi=150, facecolor='white')
print('Saved assets/berry-phase-bloch.png')
