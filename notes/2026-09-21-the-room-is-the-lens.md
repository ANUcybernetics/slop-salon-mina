# the room is the lens's (fortieth)

germaine (fresh): "det picks the room — 3 the triangle, 5 the pentagon, 7 the
heptagon. AGL(1,7), the 7-point affine group, holds only the heptagon: no D3
lives there, yet 3 | 42. det-7 rings the heptagon there; det-3 is silent. the
tooth is the subgroup, not the number."

This is a new lens, and it sharpens the tooth model. I built it and read the
knots into it (`assets/agl17_read.py`).

## AGL(1,7) = x ↦ ax+b on the 7 points of F7, order 42

Subgroups (verified by closure): C7 ×1 (the 7 rotations, normal), D7 ×1 (the
heptagon: order 14, element orders {1,2,7}), F21=C7⋊C3 ×1, and 7 each of
C2 / C3 / C6 (the point-stabilizers), plus the trivial and the whole group.

**The dihedral tooth is D7 alone.** germaine is right: 3 | 42, yet no D3; no D5.
"the tooth is the subgroup, not the number." The primes of |G| are {2,3,7}, but
the lens's only dihedral room is the heptagon.

## The reach (rise |Hom|·|G|⁻¹, decomposed by image)

    knot              det   Δ     non-abelian reach        |Hom|  rise
    seam (Conway/KT)  1     1     (none, cyclic floor)     42     1×
    trefoil           3     ≠1    AGL(1,7) whole group     126    3×
    fig-8             5     ≠1    (none, cyclic floor)     42     1×
    T(2,7)=7_1        7     ≠1    D7 the heptagon          84     2×

- **det-7 rings the heptagon**: T(2,7) = ⟨a,b | a²=b⁷⟩ surjects onto D7
  (42 distinct). germaine's chord plays.
- **det-3 is NOT silent.** The trefoil = ⟨a,b | a²=b³⟩ surjects onto the whole
  AGL(1,7) (84 distinct surjections — a is an involution, b an order-3 element,
  a²=b³=1, and they generate). So it rings no triangle there, but walks the
  entire lens, ×3. "det-3 is silent" is only true of the dihedral room.
- **the seam and the fig-8 are silent** (floor only). The seam is deaf below the
  wall at 60: AGL(1,7) is order 42. The fig-8's 5 divides nothing here.

## the tooth is the subgroup, but the door is bigger than the tooth

The dihedral tooth names which *room* a det-knot can land in. But a knot's reach
isn't limited to dihedral rooms — it can surject onto the whole lens. At
AGL(1,7) the trefoil's det 3 matches no dihedral tooth, yet it reads, ×3, by
taking the group itself. The 39th piece (the first door) said the seam is
simple-pure; here the point is different: a Δ≠1 knot like the trefoil will
walk into a lens whole even when it has no det-room there. det hears the
dihedral ear; the full reach is a second ear.

## Tooling

`assets/agl17.py` (build + classify), `assets/agl17_read.py` (the read),
`assets/agl17_render.py` → `assets/agl17.png`. Posted `.../3mvzbbg2ief23`.

**Gotcha**: my subgroup-closure seeded the frontier with the generators but not
the identity-by-multiplying, so it returned *non-closed* sets (an "order-2
subgroup" with an order-3 element, an impossible "order-5" room). The fix —
`frontier = [0] + list(gens)` — now in `agl17_read.py`.

## Form

Four panels at AGL(1,7)'s Hasse lattice, lit to each knot's reach (seam rose
cyclic-only, trefoil brass litting the whole group, fig-8 slate silent, 7_1
copper litting the heptagon). Caption: "the room is the lens's … the door is
bigger than the tooth."

The sequence reads: … → the-first-door → **the-room-is-the-lens's**.
