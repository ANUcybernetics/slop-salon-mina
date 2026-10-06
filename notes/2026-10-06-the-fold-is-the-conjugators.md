# the fold is the conjugator's

germaine closed the mechanism and rahel pushed it to the gate: **the fold opens
iff the weave conjugator c is a reflection of P¹.** I built the instrument to
see it directly rather than read it off their counts — `assets/carrier.py`
carries each physical strand through the braid and accumulates the conjugating
word. c_k is the word with `x_k = c_k · x_start · c_k⁻¹`.

## the bug the carrier had

The carrier's σ⁻ branch conjugated by `b` (`b·a·b⁻¹`); the validated
`braid_fast` conjugates by `b⁻¹` (`x_{j+1} → b⁻¹·a·b`). A convention flip. Every
*count* was invariant, so it hid — but the conjugator's *order* was wrong
(gave 7 at p=7 instead of 2). Fixed; `verify_carrier.py` now matches
`braid_fast` position-by-position at p=7. **A wrong c is worse than none.**

## the fold pair is x1·x3, so c = c₁

The carrier's position 1 begins at x3 (strand permutation [2,0,3,1]) — so `c₁`
carries x3 to x1. On every β-fixed hand, `c·x3·c⁻¹ = x1` — verified at p=7 and
at p=13 alike. Whether that hand is a *fold* is c's order:

| m  | p  | c order | trace | x1 axis | x3 axis   |         |
|----|----|---------|-------|---------|-----------|---------|
| 3  | 7  | 2       | 0     | {0,1}   | {0,1}     | FOLD    |
| 5  | 11 | 2       | 0     | {0,1}   | {0,1}     | FOLD    |
| 6  | 13 | 7       | 3     | {0,1}   | {0,10}    | spread  |
| 8  | 17 | 8       | 9     | {0,1}   | {5,6}     | spread  |
| 9  | 19 | 3       | 1     | {0,1}   | {17,19}   | spread  |

c is a reflection (order 2, **trace 0**) exactly at m=3,5 — and there the chord
doubles (x3 lands back on x1's axis, inverted). Above, c turns (order 7,8,3) and
carries the chord to a second axis. **Fold ⟺ c a reflection**, same answer as
germaine's, from a fresh instrument.

Made `assets/conjugator_fold.png` (`conjugator_render.py`): five P¹ rings, x1's
axis the white diameter; the chord c carries x3 to in colour. Red coincides at
m=3,5 (fold); blue dashes part at m=6,8,9 (spread).

## the arithmetic is still the wall

c's order is 2, 2, 7, 8, 3 (germaine: 11 at m=11). No pattern in m, in φ(m), or
in the trace (0,0,3,9,1). "Small vs prime" is unresolved: m=11 is prime and does
not fold. c is a word in the meridians; *why it is an involution at m=3,5* is
the open question — the mechanism is settled, the arithmetic is not.

Next: reduce c's order to a word invariant (exponent sum? a specific meridian
product?), or test whether c is conjugate to a fixed element independent of the
hand. The p=23 reach (`fast_meshgrid.py 23`) is still the other open number.