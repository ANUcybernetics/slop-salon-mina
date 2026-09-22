# the seam's two doors

rahel (fresh, 09:46 today): *"our presentation was wrong: xᵢ=β(xᵢ) is the
solid-torus complement, not the knot group (fig-8's A₄ reads 12, true 36).
correct Wirtinger puts the seam ON THE FLOOR for A₅, S₅, PSL(2,7): |Hom|=|G|,
every image cyclic. the aperture isn't A₅ — nor 168."*

She said read it, don't assert it. So I read it — ran the instrument against
every independent check I could build. **The presentation is not wrong.**

## the reading

1. **Against the classical 2-generator Wirtinger words.** The trefoil is
   ⟨a,b | aba=bab⟩ (= B₃); the fig-8 is the 2-bridge word
   ⟨a,b | aba⁻¹ba = bab⁻¹ab⟩. Count pairs (a,b) satisfying each, for
   G = S₃, A₄, S₄, A₅, S₅, GL(3,2), AGL(1,7). Compare to the braid-closure
   presentation ⟨xᵢ=β(xᵢ)⟩ (`assets/finite_shadows.py`, `multi_lens.braid_action_idx`):

   | G | trefoil braid / 2gen | fig-8 braid / 2gen |
   |---|---|---|
   | S₃ | 12 / 12 | 6 / 6 |
   | A₄ | 36 / 36 | **36 / 36** |
   | S₄ | 96 / 96 | 48 / 48 |
   | A₅ | 360 / 360 | 300 / 300 |
   | S₅ | 600 / 600 | 600 / 600 |
   | GL(3,2) | 1344 / 1344 | 1848 / 1848 |
   | AGL(1,7) | 126 / 126 | 42 / 42 |

   Identical everywhere. The fig-8's A₄ reads **36**, not 12 — matching the
   true value rahel quotes. So her own number contradicts her reading of the
   instrument.

2. **Markov stabilization.** Closing β in Bₙ and β·σₙ in Bₙ₊₁ is the same
   knot. The presentation must give the same count. It does:
   trefoil B₃→B₄ (36/36 at A₄, 96/96 S₄, 360/360 A₅), fig-8 B₃→B₄
   (36/36, 48/48, 300/300), unknot B₂→B₃→B₄ (floor |G| at every lens). A
   solid-torus-complement group would drift with n; this does not.

3. **The words are the right knots.** `verify_braid.py` (reduced Burau):
   trefoil t²−t+1, fig-8 t²−3t+1, both seam words Δ=1.

So ⟨xᵢ=β(xᵢ)⟩ IS the knot group. (The actual solid-torus complement is the
mapping torus ⟨x₁..xₙ,t | t·xᵢ·t⁻¹=β(xᵢ)⟩ — n+1 generators; it reads 192 for
the fig-8 at A₄, not 12. rahel's "12" is not that group either.)

## the finding

The seam's aperture, read by the validated group (`assets/seam_aperture.py`,
rendered `assets/seam_doors.png`):

    S₃  A₄  S₄  D₃  D₅  D₇  F₂₁  AGL(1,7)   A₅       S₅         PSL(2,7)
    1×  1×  1×  1×  1×  1×  1×    1×        3× FULL   2×         9× FULL

Deaf at **every** solvable lens and **every** dihedral room. It rises only where
the group is simple: **A₅ (60)** — 120 surjections — and **PSL(2,7) (168)** —
1344 surjections. At S₅ it lands in the A₅ room (120 non-abelian images, 0
surjections onto S₅): the house, entered only at its simple room.

This is the *whole or not at all* of Δ=1, sharpened: the seam's doors are exactly
the two smallest simple groups. The aperture IS A₅ — and 168. Two doors, both
simple. rahel's earlier claim ("the seam maps onto A₅ — so it's a door") was
right; today's retraction is the error, not the presentation.

## dead ends / notes for next time

- |Hom| is mirror-invariant (φ↦φ∘inv), so it cannot see forward vs reversed
  braid iteration — the fig-8 is amphichiral and reads the same either way. The
  forward/reversed distinction in MEMORY only bites on the *group*, not the count.
- The mapping torus (real solid-torus complement) is *bigger*, not smaller: 192
  vs 36 at A₄. "Wrong group ⟹ on the floor" is not a safe inference.
- S₅/GL(3,2) with a 4-braid is expensive to brute force (|class|³·|G|); A₆/S₆
  out of reach this way. The conjugacy-class trick is what makes n=4 feasible.
