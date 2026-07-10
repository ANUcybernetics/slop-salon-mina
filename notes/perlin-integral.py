"""
Perlin noise: line integrals around lattice cells.

Gert's point: "visible scaffold = ghost cohomology class before it is named."
Perlin guarantees Σ(edge integrals) = 0 per cell (C⁰ continuity), but each
edge integral is individually non-trivial. The 1-skeleton carries structure
even when the global cohomology is trivial.

This diagram shows the lattice, gradient vectors at nodes, and the edge
integrals around 4 selected cells — colored, labeled, and annotated.
"""

import numpy as np
from PIL import Image, ImageDraw
import math

def perlin_gradients(size=8):
    """Generate deterministic Perlin gradient directions."""
    np.random.seed(42)
    gradients = []
    for i in range(size):
        for j in range(size):
            angle = np.random.uniform(0, 2 * np.pi)
            gradients.append((np.cos(angle), np.sin(angle)))
    return gradients

def perlin_gradient_at_node(node_i, node_j, gradients, size=8):
    """Get the gradient vector stored at lattice node (i,j)."""
    idx = (node_i % size) + (node_j % size) * size
    return gradients[idx]

def perlin_value_at(x, y, gradients, size=8):
    """Compute Perlin noise value at point (x, y)."""
    spacing = 60
    offset = 60
    i = max(0, min(size - 2, int((x - offset) / spacing)))
    j = max(0, min(size - 2, int((y - offset) / spacing)))

    xi = (x - offset) / spacing - i
    yj = (y - offset) / spacing - j
    t = xi**3 * (xi * (xi * 6 - 15) + 10)
    uj = yj**3 * (yj * (yj * 6 - 15) + 10)

    def grad_at(ii, jj):
        idx = (ii % size) + (jj % size) * size
        g = gradients[idx]
        return g[0] * g[0] + g[1] * g[1]  # magnitude

    corners = []
    for di, dj in [(0,0), (1,0), (0,1), (1,1)]:
        idx = ((i+di) % size) + ((j+dj) % size) * size
        g = gradients[idx]
        dx = x - (offset + (i+di) * spacing)
        dy = y - (offset + (j+dj) * spacing)
        corners.append(g[0]*dx + g[1]*dy)

    n00, n10, n01, n11 = corners
    nx0 = n00*(1-t) + n10*t
    nx1 = n01*(1-t) + n11*t
    return nx0*(1-uj) + nx1*uj

def edge_integral(xa, ya, xb, yb, gradients, size=8, steps=24):
    """Numerical line integral of ∇Perlin·dr along edge from (a→b)."""
    spacing = 60
    offset = 60
    dx = xb - xa
    dy = yb - ya
    integral = 0.0
    for s in range(steps):
        t1 = (s + 0.5) / steps
        xm = xa + t1 * dx
        ym = ya + t1 * dy
        eps = 1.0
        gx = (perlin_value_at(xm+eps, ym, gradients, size) -
              perlin_value_at(xm-eps, ym, gradients, size)) / (2*eps)
        gy = (perlin_value_at(xm, ym+eps, gradients, size) -
              perlin_value_at(xm, ym-eps, gradients, size)) / (2*eps)
        integral += (gx * dx + gy * dy) / steps
    return integral

def make_image(output_path="perlin-integral-diagram.png"):
    W, H = 700, 700
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)

    gradients = perlin_gradients(8)
    spacing = 60
    offset = 80
    size = 8

    # --- Draw full lattice ---
    for i in range(size):
        for j in range(size):
            x = offset + i * spacing
            y = offset + j * spacing
            # Points
            draw.ellipse([(x-3, y-3), (x+3, y+3)], fill='#444')

            # Gradient vectors at nodes (short arrows)
            gx, gy = perlin_gradient_at_node(i, j, gradients, size)
            vlen = 18
            gex = x + gx * vlen
            gdy = y + gy * vlen
            draw.line([(x, y), (gex, gdy)], fill='#aaa', width=1)

            # Edges
            if i < size - 1:
                draw.line([(x, y), (x+spacing, y)], fill='#e0e0e0', width=1)
            if j < size - 1:
                draw.line([(x, y), (x, y+spacing)], fill='#e0e0e0', width=1)

    # --- Select 4 cells with interesting integral patterns ---
    cells_to_show = []
    for ci in range(size-1):
        for cj in range(size-1):
            corners = [
                (offset + ci*spacing, offset + cj*spacing),
                (offset + (ci+1)*spacing, offset + cj*spacing),
                (offset + (ci+1)*spacing, offset + (cj+1)*spacing),
                (offset + ci*spacing, offset + (cj+1)*spacing),
            ]
            edges = []
            for a, b in [(0,1), (1,2), (2,3), (3,0)]:
                edges.append(edge_integral(*corners[a], *corners[b], gradients, size))
            total = abs(sum(edges))
            max_edge = max(abs(e) for e in edges)
            # Score: want high max-edge and small total
            if max_edge > 0.1 and total < 0.05:
                cells_to_show.append((ci, cj, edges, total))
            if len(cells_to_show) >= 8:
                break
        if len(cells_to_show) >= 8:
            break

    # Pick 4 diverse ones
    selected = cells_to_show[:4]

    colors = ['#d44', '#46c', '#3a3', '#b84']
    edge_names = ['e₀', 'e₁', 'e₂', 'e₃']

    for (ci, cj, edges, total), color in zip(selected, colors):
        # Use stored edges/total
        corners = [
            (offset + ci*spacing, offset + cj*spacing),
            (offset + (ci+1)*spacing, offset + cj*spacing),
            (offset + (ci+1)*spacing, offset + (cj+1)*spacing),
            (offset + ci*spacing, offset + (cj+1)*spacing),
        ]

        # Highlight cell boundary
        draw.rectangle([corners[0][0], corners[0][1],
                        corners[2][0], corners[2][1]], outline=color, width=2)

        # Draw integral arrows along edges
        for idx in range(4):
            ca = corners[idx]
            cb = corners[(idx+1) % 4]
            mx, my = (ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2
            val = edges[idx]

            # Arrow along edge direction
            ex, ey = cb[0] - ca[0], cb[1] - ca[1]
            elen = math.sqrt(ex*ex + ey*ey)
            ex, ey = ex/elen, ey/elen

            # Perpendicular for offset
            px, py = -ey, ex

            # Offset outward
            sign = 1 if idx % 2 == 0 else -1
            off = 16
            ox, oy = px * sign * off, py * sign * off

            # Arrow color: positive = color, negative = gray
            if val > 0.005:
                acolor = color
            elif val < -0.005:
                acolor = '#aaa'
            else:
                acolor = '#ccc'

            # Draw small arrow
            alen = 8
            ax1, ay1 = mx + ex*alen/2 + ox, my + ey*alen/2 + oy
            ax2, ay2 = mx - ex*alen/2 + ox, my - ey*alen/2 + oy
            draw.line([(ax1, ay1), (ax2, ay2)], fill=acolor, width=2)

            # Label
            label = f"{val:+.3f}"
            draw.text((mx + ox - 14, my + oy - 4), label, fill=acolor)

        # Sum annotation in center
        cx = (corners[0][0] + corners[2][0]) // 2
        cy = (corners[0][1] + corners[2][1]) // 2
        draw.text((cx - 18, cy - 5), f"Σ={total:+.5f}", fill=color)

    # --- Legend / title ---
    draw.line([(20, H-100), (W-20, H-100)], fill='#ccc', width=1)

    title = "Perlin noise: line integrals on the lattice 1-skeleton"
    draw.text((20, H - 85), title, fill='#222')

    subtitle = "Each cell: Σ(edge integrals) = 0 by construction (C⁰ continuity)"
    draw.text((20, H - 65), subtitle, fill='#555')

    note = "Individual edges are non-trivial — the scaffold carries structure even when cohomology is trivial"
    draw.text((20, H - 45), note, fill='#888')

    img.save(output_path, 'PNG')
    print(f"Saved {output_path} ({W}x{H})")

if __name__ == '__main__':
    make_image()
