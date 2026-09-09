from pathlib import Path

W, H = 1600, 1000
bg = "#f4efe5"
ink = "#242321"
muted = "#736e64"
blue = "#287d87"
red = "#bd5547"
gold = "#c7993d"

def pt(cx, cy, r, a):
    import math
    return cx + r * math.cos(a), cy + r * math.sin(a)

def circle_word(cx, cy, perm, color, label, note):
    import math
    out = [f'<circle cx="{cx}" cy="{cy}" r="205" fill="none" stroke="#cfc7b8" stroke-width="3"/>']
    pts = [pt(cx, cy, 205, -math.pi/2 + i*2*math.pi/5) for i in range(5)]
    for i in range(5):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%5]
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="8" stroke-linecap="round"/>')
    for i, val in enumerate(perm):
        x,y = pts[i]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="31" fill="{bg}" stroke="{color}" stroke-width="5"/>')
        out.append(f'<text x="{x:.1f}" y="{y+12:.1f}" text-anchor="middle" font-size="30" font-family="sans-serif" fill="{ink}">{val}</text>')
    out.append(f'<text x="{cx}" y="{cy+285}" text-anchor="middle" font-size="30" font-family="sans-serif" letter-spacing="4" fill="{color}">{label}</text>')
    out.append(f'<text x="{cx}" y="{cy+325}" text-anchor="middle" font-size="22" font-family="sans-serif" fill="{muted}">{note}</text>')
    return "\n".join(out)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" fill="{bg}"/>
<text x="90" y="105" font-family="sans-serif" font-size="42" letter-spacing="5" fill="{ink}">ENDPOINT FORGETS SENTENCE</text>
<text x="92" y="155" font-family="sans-serif" font-size="24" fill="{muted}">same letters · different relation · one surviving verdict</text>
{circle_word(400, 475, [1,2,3,5,8], blue, "ROTATION  /  C₅", "adjacency retained")}
{circle_word(1200, 475, [1,3,8,2,5], red, "ANAGRAM  /  S₅", "adjacency spent")}
<path d="M650 475 C760 410 840 410 950 475" fill="none" stroke="{gold}" stroke-width="5" stroke-dasharray="12 15"/>
<text x="800" y="390" text-anchor="middle" font-family="sans-serif" font-size="25" fill="{gold}">the side remembers</text>
<line x1="170" y1="860" x2="1430" y2="860" stroke="#cfc7b8" stroke-width="3"/>
<text x="800" y="925" text-anchor="middle" font-family="sans-serif" font-size="30" fill="{ink}">TOTAL  →  SIGN  →  ORDER</text>
<text x="800" y="962" text-anchor="middle" font-family="sans-serif" font-size="22" fill="{muted}">what dies · whether it flips · who stood next to whom</text>
</svg>'''

Path("notes/adjacency-verdict.svg").write_text(svg)
