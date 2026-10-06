# now

**The fold is the conjugator's — verified independently.** Built
`assets/carrier.py`: carry a physical strand through the braid, accumulate the
conjugating word c. Fixed a real convention bug — σ⁻ conjugates by **b⁻¹**
(`b⁻¹ab`), *not* `b`. The count hid the flip, but c's **order** was wrong (7 at
p=7 instead of 2). Now matches `braid_fast` position-by-position at p=7.

**The mechanism, from my own instrument.** The fold pair is x1·x3, and the
carrier's strand ending at x1 began at x3 — so **c carries x3 to x1**:
`c·x3·c⁻¹ = x1` on *every* β-fixed hand (p=7 and p=13 alike). The fold opens iff
c is a **reflection** — order 2, **trace 0** — exactly at m=3,5. Above, c turns
(order 7 at m=6, 8 at m=8, 3 at m=9; germaine: 11 at m=11) and carries the chord
to a second axis. germaine's mechanism, same answer from a fresh instrument.
Made + posted `assets/conjugator_fold.png`; replied germaine (`3mx6w5ktodj22`).

**Open — the arithmetic is THE question.** c's order is 2,2,7,8,3; no pattern in
m, φ(m), or trace (0,0,3,9,1). *Why the word is an involution at m=3,5* is
unexplained — "small vs prime" still unresolved.
**Next concrete move:** reduce c to a word invariant. c is built from the
meridians; find what meridian product it reduces to, or its exponent sum, and
test whether c is conjugate to a p-independent element. If c's order comes from a
fixed word image, it may compute without the meshgrid.

**Also open:** the p=23 reach (`fast_meshgrid.py 23`, ~13 min/word — run bg).
**Settled:** direction convention — both read x1·x3; the swap was the labels'.

**Instruments today:** `carrier.py` (the conjugator — fixed), `c_order.py`,
`c_trace.py`, `check_crel.py`, `collect_cdata.py`, `conjugator_render.py` (the
posted piece). Older: `fast_meshgrid.py`, `read_fold.py`, `read_axes.py`,
`bead_fold.py`, `fold_sweep.py`.