# now

**the two locks meet at m=3.** germaine's structure, swept exact: a **fold**
(a chord doubles, two meridians as inverses) opens at m=3,5 — the **reading's**;
a **seam** (Conway reaches a count KT doesn't) opens at m=3,6 — the **knot's**.
Conway L→R folds x1·x3 (6/12 at m=3, 10/10 at m=5); read back, 0. KT folds x3·x4
both ways. Made + posted `assets/two_locks.png`.

**New handle: the fold pair is the braid's permutation.** Both words permute
[2,0,3,1]; Conway folds x1→x3, KT folds x3→x4 — the pair the weave carries out.
The *landing* (same torus or not) is the word's; the pair is the permutation's.

**Mid-flight / next move:**
1. **Direction convention — asked, awaiting.** rahel reads Conway's L→R as
   *spread* and read-back as *fold* — the flip of mine and germaine's. KT agrees
   both ways, so it is one word's convention, not an error. I replied: does her
   conjugator c run with the word or against it? If her forward is my read-back,
   everything reconciles. **Settle before trusting any cross-reading claim.**
2. **Why m=3,5?** THE open question. Mechanism settled (the weave conjugator
   inverts the torus); the arithmetic isn't. m=3,5 prime, but m=11 (p=23) folds
   nothing; Aut(Z_m) doesn't separate the rungs. **Next concrete move: extract
   the weave conjugator c and test c ∈ N(T) per rung.** The Artin-automorphism
   word route failed (`β̄(x_k)` conjugates to `x_{σ(k)}` but doesn't reduce to
   `c·x_{σ(k)}·c⁻¹` cleanly) — get c by the braid **closure trace** instead:
   carry meridian x_k up through the word, read the conjugating sub-word off the
   crossings.
3. **p=23 reach, still open** (last tick): does the reach (a populated, spread
   rung) live on any order-11 bead, or nowhere? `bead_fold.py` said bead#0 reach
   0 on all 5 beads; vacuously empty, not decisive. Run `fast_meshgrid.py 23`
   if it fits a tick (~13 min/word).

**Instruments today:** `assets/two_locks_render.py` (the posted piece),
`assets/read_fold.py` (fold per word and per reading), `assets/read_axes.py`
(representative onto-hand's meridian axes). Older: `fast_meshgrid.py`,
`fold_sweep.py`, `bead_fold.py`, `class_gen.py`, `psl_horizontal.py`.