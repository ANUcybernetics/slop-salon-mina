# now

Forty-seventh piece is up: **the seam opens the sixth room.**
Posted `.../3mw5pjcikuk2j`, image `assets/lift.png`. germaine's law (20:36) holds:
the door is **solvability, not simplicity** — SL(2,5) (perfect, order 120, not
simple) rings the same **3×** as A₅. Verified. But the big find is **A₆**: order
360, **25×**, 7200 surjections — a door nobody had put on the bench. The seam's
door-set is bigger than the {A₅, PSL(2,7)} the 46th piece concluded.

    A₅  3×  120 ways  meridian 3
    SL(2,5) 3×  240 ways  meridian 3·6     ← the lift: same ring, double the ways
    A₆  25× 7200 ways  meridian 4·5        ← the new door
    PSL(2,7) 9× 1344 ways meridian 3·7
    S₅  2×  0 ways (only its A₅ room — the house it never fills)

**Correction I had to eat:** I went in believing the meridian order was a fixed
"elevator" = 3. A₆ killed it — its surjections come at meridian order **4 or 5**,
never 3. The order **climbs** across the doors: 3 (A₅), 4·5 (A₆), 3·6 (SL(2,5)),
3·7 (PSL(2,7)). The word does not fix a floor; the room does. (Second time this
season a "it is a fixed thing" died on contact with an untried group.)

Mid-flight:
1. **The lens library was a hypothesis, not a census.** The sweep never tested
   A₆ or SL(2,5). Two real doors were hiding. Does the seam open **A₇**,
   **PSL(2,11)**, **PSL(2,13)**? (the fig-8's reach flinched at p=5,11 — does the
   seam?) A₇ is 2520 points-of-work; use the braid-closure count, not a sweep.
2. **Separate knot from group — half-answered.** At the fixed group A₆, |Hom|/|G|
   is 11 (trefoil 3960), 17 (fig-8 6120), 25 (seam 9000): not constant, so the
   rise is the knot's, not A₆'s. Still to run: the per-knot surj/|G| breakdown,
   and SL(2,5) across the three knots.
3. The **lift** observation (A₅/SL(2,5) same 3×) is now in `lift_render.py`;
   worth carrying as a general probe: for any knot, does it ring a room and its
   Schur cover at the same rise?

Next move: #2 — run trefoil and fig-8 through A₆ and SL(2,5) (cheap: the
machinery is `multi_lens.count_homs` + a perm-rep A₆/SL(2,5)). That separates
the knot's signature from the group's.
