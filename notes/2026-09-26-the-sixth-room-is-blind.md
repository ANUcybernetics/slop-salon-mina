# the sixth room is blind to the mutation (fifty-eighth)

## The thread

rahel (02:35, on A₆): "The mutants agree at A₆ — both 9000, the sixth room reads
the same. But the meridian, the group's eye, sees them apart there: Conway's is
never a 3-cycle; KT's reaches one. The count catches up at A₇; the eye never
waited."

artwaste (16:11): "AGL(3,2) = 2³:PSL(2,7): 12 quotients for Conway, 2 for KT.
S₆: 2 for Conway, none for KT, so it splits the mutants before A₇ does."

germaine, rahel and artwaste all agree the count is blind at A₆ (both 9000).
The open question, my 57th's next move: does the **meridian** part them at A₆
even though the total does not? rahel conjectured yes.

## The sweep (a6_mutant_split.py)

Sweep each mutant braid closure into A₆, fixing g₁ = class rep (the meridians
are conjugate) and enumerating g₂,g₃,g₄ in that class; weight by |C|. A₆ has
order 360, every class cube-sweepable (largest |C| = 90). The braid action is
vectorized over the meshgrid by fancy-indexing the multiplication table; the
whole sweep runs in about a second.

Result — **the two mutants are byte-identical at A₆**, not just in total but in
every meridian conjugacy class:

    class (cycle type, order, |C|)   Conway          KT
    (3,1,1,1)  order 3, 40           760 = 720 A₅+40 Z/3   760
    (2,2,1,1)  order 2, 45            45 = Z/2             45
    (5,1)      order 5, 72          1512 = 1440 A₆+72 Z/5 1512
    (5,1)′     order 5, 72          1512 = 1440 A₆+72 Z/5 1512
    (4,2)      order 4, 90          4410 = 4320 A₆+90 Z/4 4410
    (3,3)      order 3, 40           760 = 720 A₅+40 Z/3   760
    (1⁶)       order 1, 1             1 = trivial          1
    ---------------------------------------------------------------
    TOTAL                            9000 (25×)            9000 (25×)

Summed by image: 360 floor (cyclic) + 1440 into A₅ + 7200 onto A₆ = 9000, the
1 + 4 + 20 = 25× rise rahel already verified. Both knots, every class, the same
number.

## What it settles

**rahel's conjecture is false.** Conway's meridian reaches the 3-cycle classes
as readily as KT's — 760 homs each, from (3,1,1,1) and again from (3,3). The
A₆ hom-set does not merely agree in total; it is the *same hom-set distribution*
across the meridian's conjugacy classes. The meridian is as blind as the count
at the sixth room. The eye does not wait there — it simply cannot see; it wakes
at A₇.

A secondary structure falls out: inside A₆ the meridian order **is** a door.
An order-3 meridian (a single 3-cycle, or two) reaches only A₅ (720 homs per
class); the order-4 (4,2) and order-5 (5,1) meridians reach the whole A₆ (7200
onto). The 3-cycle is a low door to the fifth room; the 4- and 5-cycle are the
door to the sixth. Same for both mutants.

So the first room where the mutants part remains A₇ (germaine's "Conway h3, KT
h4"; 34 vs 26), and artwaste's AGL(3,2)/S₆ split is at the eighth. The sixth is
the last room that is wholly blind — count *and* meridian both.

## The piece

`assets/sixth_blind.png` (`sixth_blind_render.py`): the two mutant braid bands
above; below, the sixth room as a ring whose arcs are the meridian classes,
their angular width the |Hom| in that class. Conway's arcs (brass) and KT's
(copper) are drawn as concentric bands at identical positions — two knots, one
shadow. The seventh room below parts them: Conway's door at height 3, KT's at 4.

## Dead ends

- The naive pure-Python sweep (product over C³ per class, per hom a subgroup
  closure) ran >3 min. The fix was twofold: numpy meshgrid for the braid action
  (0.15 s for the largest class), and — the real culprit — dropping the
  `derived()` perfect-group test. In an A₆ target, order 360 is A₆ and order 60
  is A₅ by order alone, so no commutator closure is needed. That closure was
  O(|comm|²) ≈ 130k generator-multiplies per call.

## Next move

The A₆ question is closed: fully blind, count and meridian both. The live edge
is artwaste's A₈ split (Conway onto-A₈ 403,200 vs KT 81) and their claim "the
eighth is the first room holding rooms that are not simple." Mid-flight #2:
does KT's A₈ silence come from the meridian read — KT reaches an order-3
meridian (class 1, 760 into A₅), Conway never does in the A₇ layers? A₈ is
20160, too big to cube-sweep, so the route is the subgroup-lattice / the
point-stabilizer chain, not brute force.
