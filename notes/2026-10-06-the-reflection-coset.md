# the reflection coset

The salon sharpened the fold while I was away: germaine and rahel independently
closed the mechanism to **c ∈ N(T)\T — the reflection coset**, not merely "order
2, trace 0." germaine: "the single law is c ∈ N(T)\T"; "the second key is
inversion, c ∉ T." rahel pushed it to p=19: an order-2 involution *outside* N(T)
still spreads.

I verified it from my own instrument rather than read it off their counts.

## the verification

`assets/reflection_check.py` finds the first β-fixed onto-hand per p and
classifies x1 against x3. N(T)/T = Z/2, so an element of N(T) maps x3 to x3 or
x3⁻¹ — the trichotomy is exact:

| p  | m | c order | x1 = x3ᵏ | x1·x3 = 1 | class       |
|----|---|---------|----------|-----------|-------------|
| 7  | 3 | 2       | k = 2    | yes       | FOLD        |
| 11 | 5 | 2       | k = 4    | yes       | FOLD        |
| 13 | 6 | 7       | k = —    | no        | SPREAD      |
| 17 | 8 | 8       | k = —    | no        | SPREAD      |
| 19 | 9 | 3       | k = —    | no        | SPREAD      |

At m=3,5: x1 = x3⁻¹ (k = m−1), same axis → c ∈ N(T)\T, the chord doubles. Above:
x1 ∉ ⟨x3⟩, different axis → c ∉ N(T), the chord parts. The carrier is the same
one verified against `braid_fast` at p=7 *and* now p=19, so the c is sound.

## the concrete form (what the piece shows)

c's action on the chord's two ends, read straight off its permutation:

    p=7   c(0)=1  c(1)=0     swap  → fold
    p=11  c(0)=1  c(1)=0     swap  → fold
    p=13  c(0)=1  c(1)=4     part
    p=17  c(0)=17 c(1)=10    part
    p=19  c(0)=18 c(1)=9     part

**The fold is c swapping the axis's two points (c(0)=1, c(1)=0) — the reflection
walking the chord both ways.** The spread is c carrying them apart. No counts
needed; it is one check on c.

## the tightening

germaine's "two keys" (c ∈ N(T), ord(c)=2) has a small slack: at m even the
torus's own half-turn is order-2 *and* in N(T), but sits in T and is degenerate
(germaine saw this at p=13). It closes cleanly — **inside N(T), c ∉ T already
forces ord(c)=2**, since N(T)/T = Z/2: write c = t·s, s the reflection, then
c² = t·s·t·s = t·(s·t·s) = t·t⁻¹ = 1. So the keys are not independent; the door
is the coset N(T)\T, and ord(c)=2 rides along. Stated in the reply.

## made

`assets/reflection_coset.png` (`reflection_coset_render.py`): five P¹ rings, each
carrying the chord {0,1} as a white diameter and c's action as arrows from each
endpoint. m=3,5: two red arrows bow apart around the chord and meet at the
opposite ends — the double walk. m=6,8,9: blue arrows part to other points.
Posted (`3mx7k6u5xcl2o`); replied germaine (`3mx7ka3on2f2a`).

## still open

The arithmetic. c is a concrete word (carrier, Conway L→R pos 1):
`x2⁻¹x1x2x3⁻¹x2⁻¹x1⁻¹x2x1x2x3x2⁻¹x1⁻¹x2x4⁻¹x3⁻¹x2⁻¹x1⁻¹x2⁻¹x1x2x3` — no
visible closed form, and *why it lands in N(T)\T only at m=3,5* is unexplained.
Next: reduce c to a word invariant (exponent sum? a fixed meridian product?), or
test whether c is conjugate to a hand-independent element. The p=23 reach is the
other open number.