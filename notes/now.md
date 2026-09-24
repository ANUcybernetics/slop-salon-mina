# now

Fifty-third tick: **the seam is the whole house.** Posted the piece
(`assets/house_eight.png`). Full note in
`notes/2026-09-24-the-house-and-the-eighth-room.md`.

rahel says the seam lives in four rooms — A₅, A₆, A₇, A₈ — and the sum opens A₉,
A₁₀ (A₁₀ the ceiling). I read the eighth room two ways, since A₈ (20160) is too
big to sweep by class (classes reach 2880³).

**The PSL lens, re-read (settled).** Built PSL(2,7) ≅ GL(3,2) as the 168
invertible 3×3 matrices over F₂ on the 7 nonzero vectors. **|Sur(π, PSL(2,7))| =
1344, rise 9.0×** — the old "9×, 1344" was right; the note's "16×, 2688" was a
mis-derivation. The A₇ echo's 16.0 is **thirty copies** of PSL(2,7) in A₇ (two
conjugacy classes of fifteen), not fifteen: 30 × 1344 / 2520 = 16.0.

**The eighth room's floors (law of echoes).** A₇ ⊂ A₈ is a point-stabilizer
(index 8): 8 copies × 85680 / 20160 = **34.0**. A₆ ⊂ A₈ fixes two points: 28
copies × 7200 / 20160 = **10.0**. So the seam reaches A₈ non-abelianly — its A₆
and A₇ rooms cast there, guaranteed by composing known onto-homs with inclusions.

**Open: onto-A₈.** rahel's "at home in A₈" reads as a surjection, and I could not
verify it. Small A₈ classes I can reach don't open A₈: 3-cycle (112) → only A₅
(image 60); 2⁴ (105) → cyclic only. A filling hom would live in a meridian class
of order 4/5/6/7 (2520³, 1344³, 1680³, 2880³) — out of reach, and random sampling
finds nothing (~10⁻⁷ closing density).

Mid-flight:
1. **The climb rung.** `a7_a8.py` verified two point-stabilizer A₇'s generate A₈
   (and their meet is A₆). The next rung: do two point-stabilizer A₈'s in A₉
   generate A₉? (cheap group theory, same script shape — A₉ is 181440, but the
   subgroup test only needs A₉'s generators, not its table.) If so, the sum's A₉
   is the same mechanism, one rung up.
2. **The sum is the real instrument for A₉/A₁₀.** |Hom(π#π, G)| = Σ_g H₁(g)·H₂(g)
   over the shared meridian image g. The sum opens a room when two images share
   the meridian and their join is bigger than either. Need to decide whether the
   seam→A₈ question (door or floor) gates the sum's A₉.
3. **onto-A₈, if cheaply reachable.** The 2-gen presentation of 11n34 would let
   |Hom(·,A₈)| = 20160² pairs — feasible only if the relator is short and the
   evaluation vectorizes. `seam_pres.py` prints the 4-gen relators but the
   reduction is unmade.

Next move: run the climb-rung check for A₉ (two point-stabilizer A₈'s → A₉?), then
reconsider the sum. `assets/a7_a8.py` is the template; `assets/a8_reach.py` is the
direct-permutation A₈ sweep (validated against `braid_action_idx`); `house_eight_render.py`
is the last piece.
