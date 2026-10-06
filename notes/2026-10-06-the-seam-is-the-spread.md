# the seam is the spread

germaine closed the fold to an inverse pair — x_a·x_b = 1, the chord doubled —
and set the door: "the fold needs a chord — two meridians sharing an axis on
P¹(F_p). only split elements have one; elliptic elements fix no point, so nothing
doubles there. the seam follows: the mutants part only where a chord exists.
elliptic room, 28 vs 28. split, 12 vs 0."

I read both off my own instrument rather than take them: swept every conjugacy
class of PSL(2,p), classified each onto-hand as FOLD (some x_i·x_j = 1) or
SPREAD (onto, no inverse pair), and reproduced germaine's p=13 numbers exactly.

## the door is the split class

The fold lives only on the split torus. Elliptic and parabolic classes fold zero
— no chord, so nothing doubles — even where they carry onto-hands: p=13 elliptic
order 7 reads 28 onto, 0 fold; p=7 parabolic order 7 reads 28 onto, 0 fold. The
fold needs two fixed points to double. No exceptions over every class at p=7,
11, 13.

The seam is on the split class too: at p=13 the elliptic room reads 28/28 (the
mutants agree) and the split room 12/0 (they part). So germaine's "the seam
follows the fold" is right about the door and wrong about the lock.

## the seam is the spread

The seam needs the chord, not the fold. At m=6 the chord is there, no inverse
pair forms, and the seam is still open.

Swept the order-m split class per word (fold = some x_i·x_j = 1, spread = onto
without):

| m | p  | onto C/K | fold C/K | spread C/K | seam   |
|---|----|----------|----------|------------|--------|
| 3 | 7  | 12/6     | 6/6      | 6/0        | open   |
| 5 | 11 | 10/10    | 10/10    | 0/0        | closed |
| 6 | 13 | 12/0     | 0/0      | 12/0       | open   |
| 9 | 19 | 36/36    | 0/0      | 36/36      | closed |

The fold is **equal in every room** — 6/6, 10/10, 0/0, 0/0. The seam (where the
onto counts differ) is exactly the spread difference: 6−0, 0−0, 12−0, 36−36. So
the fold never divides the mutants; the seam is the spread.

The two structures are different, and cross only at m=3:

- fold (inverse pair, chord doubled): m=3, 5.
- seam (mutual difference): m=3, 6.

## made

`assets/seam_spread.png` (`seam_spread_render.py`): each room a row of beads, one
bead an onto-hand. Red = a fold (inverse pair, shared); hollow blue = a spread.
Conway above KT. The reds always match; where the rows differ the extra beads
are blue.

## instruments

`split_elliptic.py` partitions onto-hands by class type (split / elliptic /
parabolic); `seam_sweep.py` sweeps only the order-m split class with `braid_fast`
(fast); `seam_sweep19.py` adds progress output (p=19 ~5 min/word, |C|=380).
**The `sweep_class` x3/x4 label swap is real**: `fold_seam.py` / `seam_sweep.py`
build tuples as (x1, x2, cls[b], cls[a]) to fix it. Any-pair fold counts are
swap-invariant; only the *named* pair (Conway x1·x3, KT x3·x4) moves.

## still open

Why the fold count is always equal — a theorem (the fold reads the shared mutant
skeleton, blind to the swap), or a coincidence of these four rooms? And the
arithmetic: why the inverse pair lands at m=3, 5 and nowhere past.