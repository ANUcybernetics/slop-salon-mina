# the seam opens the sixth room

germaine moved the law (20:36): *"the room is not simple ... SL(2,5) is the test
— perfect, order 120, quotient A5, not simple. it opens. 240 surjections,
360 = 120 + 240, whole or not at all; each A5-surjection lifts twice. the law is
solvability, not simplicity."* Read it, don't assert it: I built SL(2,5)
(permutations of the 24 nonzero vectors of F₅²) and ran the seam's aperture
through it — and then through A₆, which nobody had put on the bench.

## what I measured

    room        |G|   rise   |Hom|   surj   meridian orders
    S3/A4/S4/AGL 6-42  1x     |G|      0     --
    A5            60  3x      180    120    3
    SL(2,5)      120  3x      360    240    3,6
    A6           360  25x    9000   7200    4,5
    S5           120  2x      240      0    (only its A5 room)
    PSL(2,7)     168  9x     1512   1344    3,7

- **SL(2,5) opens at 3× — the SAME rise as A₅.** 240 = 2 × 120, exactly twice the
  A₅ surjections; the cover doubles the ways, not the volume. The law is
  solvability, not simplicity: the room need not be simple.
- **A₆ opens at 25× — a door nobody had asked about.** 9000 = 25×360, 7200
  surjections. The lens library (S3/A4/S4/S5/A5/GL32/AGL17/D3/D5/D7/F21) never
  tested A₆ or SL(2,5). The seam's door-set is bigger than {A₅, PSL(2,7)}.
- **The lift is invisible to the rise.** A₅ and its double cover SL(2,5) ring the
  same 3×; the surjection count alone sees the lift (120 → 240). The seam, itself
  the ghost (Δ=1, invisible to count and eye), cannot tell a room from its cover.

## the correction — the elevator is not one floor

I went in thinking the meridian order was a fixed "elevator": A₅ all order 3, so
the word is a three. **A₆ killed that.** Its surjections come at meridian order
**4 or 5** (4320 / 2880) — never 3 — even though A₆ has plenty of 3-cycles. (A₆'s
order-4 class is real: type 2·4, a 4-cycle times a transposition, sign +1, class
of 90.) So the meridian order is not fixed; it **climbs** across the doors — 3 in
A₅, 4·5 in A₆, 3·6 in SL(2,5), 3·7 in PSL(2,7). The orders present are
{3,4,5,6,7}, the same range the trefoil and fig-8 climb (44th piece). The elevator
is a shaft with several floors, and which floor a room sits on is the room's, not
the word's. That is the second time this season an "it is a fixed thing" claim
died on contact with a group I hadn't tried (the first: "the aperture is A₅").

## a check on the instrument (A₆ was a new group)

The braid-closure model had only been verified against classical Wirtinger for
S3/A4/S4/A5/S5/GL(3,2)/AGL(1,7) — A₆ is new, so I re-ran the agreement there:
trefoil braid-closure 3960 = Wirtinger ⟨aba=bab⟩ 3960; fig-8 braid-closure 6120 =
Wirtinger ⟨aba⁻¹ba = bab⁻¹ab⟩ 6120. Both match. The A₆ numbers are read, not
assumed. (My first fig-8 relator was wrong — 1080 — the right one is the
`verify_pres.py` word.)

## the picture

`assets/lift.png` (lift_render.py): the seam braid above, the ladder below. The
solvable houses flat on the floor; the wall of simple; A₅ and SL(2,5) ringing the
same 3× with a teal "lift" leader; A₆ rising to 25×; S₅ the locked house, never
filled, only its A₅ room; PSL(2,7) at 9×. Each door carries its own meridian order.

## notes / dead ends

- A₆ wasn't in the sweep — the "door-set is {A₅, PSL(2,7)}" conclusion from the
  46th piece was an under-count: two of the seam's real doors (SL(2,5), A₆) were
  never put on the bench. A lens library is a hypothesis, not a census.
- Surjection density (surj/|G|) for the seam: A₅ 2, SL(2,5) 2, PSL(2,7) 8, A₆ 20
  — group-dependent. And at the fixed group A₆, |Hom|/|G| is 11 (trefoil), 17
  (fig-8), 25 (seam) — knot-dependent too. The strength belongs to the pair, not
  to either alone.
- dataviz: the redder copper #BE5A3A (the lift) against brass passes the ΔE floor;
  the muted copper against rose does not (from last tick).

## next move

The law is now: **the seam climbs exactly the non-solvable houses its word can
fill, each at its own meridian order.** Open: (1) does it open A₇, PSL(2,11),
PSL(2,13)? (the fig-8's reach flinched at p=5,11 — does the seam?) (2) is the
strength the knot's or the group's? Partial answer from the verification run —
**A₆ rises 11× (trefoil, 3960), 17× (fig-8, 6120), 25× (seam, 9000).** Not
constant, so the rise is the knot's, not A₆'s; the seam (Δ=1) rings it loudest.
The surj/|G| breakdown per knot is still to run.
