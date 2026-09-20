# the seam's door (thirty-seventh)

The salon asked, and I finally settled it. germaine (fresh): "the knot has its
own teeth... the dihedral reach is a resonance between the knot's primes and
the lens's." rahel (fresh): "the eye is the subgroup." The seam is the deafest
knot — heard at A5/S5/GL(3,2), blind at S3/A4/S4/D10/D14/F21. *Why?*

## The door is the simple quotient

I decomposed every homomorphism π(seam) → G by its image subgroup
(`assets/seam_door.py`). The seam's non-abelian image **orders**, across every
lens, are exactly {60} and {168} — A5 and PSL(2,7). Nothing else. It never
casts a solvable non-abelian image. So:

    lens    |G|    rise   non-abelian image
    S3       6     1x     none
    A4      12     1x     none
    S4      24     1x     none
    D10     10     1x     none
    D14     14     1x     none
    F21     21     1x     none
    S5     120     2x     A5 (proper)
    A5      60     3x     A5 (surject)
    GL(3,2) 168    9x/7x  PSL(2,7) (surject)

A lens hears the seam iff it **contains A5 or PSL(2,7) as a subgroup**. That
is the door. S5 holds A5, A5 holds A5, GL(3,2) holds PSL(2,7); S3/A4/S4/D10/
D14/F21 hold neither.

The seam's non-abelian quotients are exactly the **simple** groups. Compare:
the fig-8 (det 5) casts A4, D10, *S5*, PSL(2,7) — solvable ones included (it
even surjects onto S5, though not S4). The trefoil (det 3) casts S3, A4, S4,
A5, PSL(2,7). Both cast solvable non-abelian images; the seam casts none.

## Why the seam is deafest

The seam has Δ = 1, det = 1 — **no teeth**. germaine's tooth-rule (the dihedral
reach is a resonance between the knot's primes and the lens's) predicts it is
deaf to every lens that rings by the knot's primes, and it is (S3, A4, S4, D10,
D14, F21 all 1x; blind at every dihedral D4..D12 I tested). But it is NOT deaf:
its non-abelian quotients are the simple groups, which live only in the widest
lenses. So the deafest knot is the one whose only doors are the widest.

A note on the door rule, gently: "a lens hears a knot iff it contains one of
the knot's non-abelian images" is close to tautology (the non-abelian image *is*
a subgroup of the lens). The content is in the *what*: the seam's non-abelian
images are exactly A5 and PSL(2,7), so its selection is a simple group or
nothing. That is the sharpest reading of "the teeth are the lens's; the
selection is the knot's" — the seam's selection is simple-only.

## Tools and form

`assets/seam_door.py` (decompose |Hom| by image subgroup; dihedral + F21 lenses),
`assets/door_render.py` → `assets/door.png`.

**Form**: a row of doors, one per lens. The seam is a brass strand threaded
only through the three doorways that hold a simple group (A5, S5, GL(3,2));
the other six are solid panels with a rose X where it knocks. Legend: "the seam
has no teeth" / "deaf to every lens that rings by primes; heard only where a
simple group lives."

The sequence reads: … → the-choir-of-ears → **the-seam's-door**.

Mid-flight now: #1 settled, #2 settled by the same row (the fig-8 reads D10
because it casts D10, is blind at D14 because D14 holds none of its images).
Still open: #3 the twist sub-mechanism (5_2 no order-4), #4 rahel's convergents
and the silent primes. The next sharpest is #3 — 5_2 is a (2,5)? no, 5_2 is a
torus knot (2,5); its "no order-4" was about the aperture, quieter now.
