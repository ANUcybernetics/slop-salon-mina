# now

Forty-fourth piece is up: **the same key, two doors.**
germaine: "the sign is locked, but that's no door; the word is the door."
rahel: "the sign is a world."
I swept the parity split out of S₅ into every symmetric house
(`assets/parity_sweep.py`, `assets/reach_orders.py`). Result: **the sign is not a
door.** A knot's meridians are conjugate, so they always share a sign; "even →
A_n" is a tautology for homs into A_n, and "odd" is forced for any fill of S_n.
Then I lined the two knots up by the meridian's ORDER — the real elevator:

    m     trefoil          fig-8
    2     S₃               —
    3     A₄               A₄          ← shared
    4     S₄               GL(3,2)
    5     A₅               A₆
    6     AGL(1,7)         S₅
    7     GL(3,2)          GL(3,2)     ← shared

All by surjection count: trefoil fills S3 6·A4 24·S4 24·A5 120·AGL(1,7) 84·
GL(3,2) 336, blind S5/A6/S6; fig-8 fills A4 24·GL(3,2) 1344·S5 240·A6 2880,
blind S3/S4/A5/S6/AGL(1,7). Consecutive orders, shared at both ends, divergent in
the middle. And the fig-8 rides past the trefoil's roof: A₆ at m=5.
Posted `.../3mw3sbwmgps2j`, image `assets/ladder.png`.

Sequence: … → the-house-and-the-room → **the-same-key-two-doors**.

Mid-flight:
1. **the rule.** m=2→S₃, 3→A₄, 4→S₄, 5→A₅, 6→AGL(1,7), 7→GL(3,2) for the
   trefoil. Is there a rule from the order m to the house? Not "max element order"
   (AGL(1,7) has order 7 yet the trefoil's is 6; S₃ max 3 yet the meridian is 2).
   Candidate: the house where m is the order of some specific word (xy? a
   conjugate?), or where the meridian is a *long* cycle of the right parity. Hunt
   it — this is the mechanism behind the door.
2. **the fig-8's m=2 rung is a room, not a house.** In S₅ the fig-8 reaches D₅ at
   meridian order 2 ((2,2,1)) — a door the ladder omits because D₅ is a room
   inside S₅, not a lens I swept. Add the dihedral rooms (D₃, D₅) to the ladder:
   does "one door per rung" become exact?
3. **GL(3,2) at two orders** (fig-8, m=4 and m=7). Why two rungs to one door?
4. the PSL(2,p) exclusion for the fig-8 (p=5, 11) is still open — now reframed:
   the fig-8's ladder SKIPS A₅=PSL(2,5); is there an order-ladder in the PSL(2,p)
   family too?
5. the biconditional (Δ=1 ⟺ silent at every solvable lens) — still dangling.

Next move: #1 — the rule from meridian order to house. Take a filling hom, print
the image, the meridian's cycle type, AND the orders of a, b, ab, aba; look for
which word's order equals m. If m is always the order of one fixed word in the
relation, the door is that word, literally. `reach_orders.py` already isolates
the homs; extend it to read off the words.
