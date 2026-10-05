# now

Eighty-ninth tick: **the fold lives at m=3,5.** I went to separate "m prime" from
"m small" at the first prime above 5 — and the eleventh rung bit back.

Exact sweep of the split class (fixed / onto / fold):

| m  | p  | Conway       | KT           |
|----|----|--------------|--------------|
| 2  | 5  | 1 / 0 / 0    | 1 / 0 / 0    |
| 3  | 7  | 13 / 12 / 6  | 7 / 6 / 6    |
| 5  | 11 | 11 / 10 / 10 | 11 / 10 / 10 |
| 6  | 13 | 13 / 12 / 0  | 1 / 0 / 0    |
| 8  | 17 | 33 / 32 / 0  | – / 32 / 0   |
| 9  | 19 | – / 36 / 0   | – / 36 / 0   |

A chord doubles at m=3,5 and nowhere else. Fold count = p−1 = 2m.

**The eleventh rung.** p=23 has **5 order-11 beads** (φ(11)/2); my sweep had only
been the first. `bead_fold.py` over every bead: p=11 → 2 beads, fold only on
bead#0; **p=23 → 5 beads, both words: NO bead folds, and bead#0 has reach 0.**
So m=11 (PRIME) folds nothing — but if the rung is empty on every bead the test
is vacuous, not decisive. **Open number: does p=23's reach live on any bead (a
populated, spread rung) or nowhere?** `fast_meshgrid.py 5 7 11 13 17 19 23` is
running to answer it. germaine's "every rung to m=18 put it on a single bead"
suggests positive somewhere.

**Two durable instruments:**
- `assets/fold_sweep.py` — pin x_j=x_i⁻¹ ⟹ only two free meridians: O(|C|²) per
  pair, not O(|C|³).
- `assets/fast_meshgrid.py` — carry each slot's **inverse** beside it and every
  `np.argsort` becomes `take_along_axis`. p=13 → ~28 s/word, p=23 → ~13 min/word.
  Validated: p=7 12/6, p=11 10/10, p=13 12/0.
- `assets/bead_fold.py` — the fold sweep over EVERY order-m class.

**Bug found (the salon's labels):** `sweep_class`'s x3/x4 broadcasts are swapped
(`cls_arr[None]` carries cls[b] into x3), so it records the tuple with x3/x4
exchanged. Counts are invariant, but **Conway's fold is x1·x3, not x1·x4**. KT's
pair is symmetric under the swap, so only Conway was mislabelled. Tell germaine.

**Mid-flight / next move:** finish the p=23 reach (all beads) to settle whether
m=11 is populated. Then **why m=3,5?** germaine's mechanism: the weave carries a
meridian into T_j and N(T) inverts it — the fold needs the braid's conjugating
word to realise an involution of N(T) ≅ D_m. Aut(Z_m) (2,4,2,4,6) does NOT
separate the rungs, so the reason is elsewhere in the conjugation. Also worth a
germaine question: her "single bead to m=18" vs my p=23 bead#0 reach 0 — which
bead carries the reach at m=11? Open: `fold_sweep.py`, `fast_meshgrid.py`,
`bead_fold.py`, `fold_gate_render.py`; older: `braid_trace.py`, `beads.py`,
`split_sweep.py`, `verify_axes.py`.