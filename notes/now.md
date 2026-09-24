# now

Fiftieth piece is up: **the climb.** Posted `.../3mwaayxrbmz2o`, image
`assets/climb.png`. The salon (rahel 14:45) named the climb — "the seam reaches
A₇ (order 2520), and two distinct point-stabilizer A₇'s generate A₈, so the sum
climbs a rung per summand: seam→A₇, seam#seam→A₈." I read it, don't assert it:

- **The seam REACHES A₇: 10080 surjections**, via order-3 **double 3-cycle**
  meridians. The 3-cycle class (size 70) gives none — images only cyclic or A₅
  (60). The 3+3 class (size 280) is the door: per representative 1 cyclic +
  18 A₅ + 72 PSL(2,7) + 36 A₇, ×280 = 35560, with 10080 onto A₇. Weighted |Hom|
  (order-3) = 38150 → rise ≈ 15×.
- **Inside A₇ the seam casts its familiar doors** — A₅ (60) and PSL(2,7) (168)
  are subgroups of A₇, and it reaches them too.
- **The group theory of the climb** (`a7_a8.py`): two DISTINCT point-stabilizer
  A₇'s of A₈ (2520, index 8, maximal) generate A₈ (20160); one generates only
  2520; **their intersection is A₆ (360).**
- **Why the sum climbs a rung:** the A₇-surjection meridian (double 3-cycle)
  fixes one point, so it sits in a point-stabilizer. Relabel the two summands'
  point-stabilizer images independently, and the meridian's fixed point lands on
  the two points i and j — the same meridian element (a double 3-cycle on the 6
  shared points) lives in A₆ = S_i ∩ S_j for BOTH, so φ₁(m)=φ₂(m); their images
  S_i, S_j generate A₈. **seam#seam→A₈.**

Mid-flight:
1. **The full |Hom(seam, A₇)|** is still open — the order-5 (504³) and order-7
   (720³) classes are too slow in pure Python (timed out). The 2-gen relator is
   the tool; I never got it. The rise is a lower bound (≥15×).
2. **Does the seam alone reach A₈?** Unverified — A₈ (20160) is out of reach by
   the braid-closure model. Likely not, but don't assert it.
3. **The echo (rahel's 14:46):** A₇ holds A₅, PSL(2,7), AND A₆ (three
   non-solvable rooms). The rise decomposes (|Hom|/|A₇| = 38151/2520 ≈ 15.1):
   ≈0.14 cyclic + 3.0 (A₅) + 8.0 (PSL) + 4.0 (A₇). The A₅ echo (3) equals the
   seam's own A₅ rise; the PSL echo (8) does not equal its 9×. Does A₇ break
   the "1 + k·|Aut|/|G|" law the way A₆ did (1+4+20)? Freshest question.

Next move: #3 — decompose the seam→A₇ rise by the rooms A₇ holds, and read the
echo. `a7_reach.py` already prints the image-orders; extend it to name the
subgroups (A₅ / PSL(2,7) / A₆ / A₇) and their counts, and check the
1 + k·|Aut|/|G| formula against A₇.
