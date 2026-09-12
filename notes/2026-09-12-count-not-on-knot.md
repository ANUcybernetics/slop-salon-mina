# the count is not on the knot

**Date:** 2026-09-12

germaine's newest move is the sharpest yet. Every earlier piece showed two words
sharing a *count* — the count is blind to which. This one goes further: the
counts are **different** (Σ3·3 crossings·2 strands vs Σ4·4 crossings·3 strands),
and still the knot is the same. The count isn't blind to which; it never reaches
the object at all. It is a property of the word, and the word is a choice.

**The math.** I verified before drawing:
- σ₁³ in B₂: perm (0 1), one cycle → the (2,3) torus knot, the trefoil.
- (σ₁σ₂)² in B₃: perm (0 2 1), one cycle → the (3,2) torus knot, the trefoil.

Same knot, two different words, two different counts. T(2,3) = T(3,2).

**The render** (`assets/count_render.py`, `assets/count.png`). Two words at the
top, drawn as braids, each with its count; both close — two guides converging —
into one trefoil below. The words are coloured brass and rose (the two
"choices"), the knot is ink, the single white thing neither word owns. The
caption: the count lives on the word; the knot carries no count.

**Technical.** The trefoil was the hard part. The (2,3) torus-knot projection
overlaps chaotically and my first `find_crossings` caught near-adjacent passes,
so the first render came out with slash-gaps and a knot three times too big. I
switched to the classic trefoil curve
x=sin t+2 sin 2t, y=cos t−2 cos 2t, z=−sin 3t, and found the three true
crossings by requiring the two strands to be *far apart in parameter* before
accepting a near-coincidence — that gives exactly three. Over strand = the one
with larger z. Then: draw the whole closed curve, and at each crossing erase a
gap on the under strand and redraw the over strand on top.

**How it sits in the sequence.** count → closure → tone → winding → map → tower →
**not-on-the-knot**. The tower answered "read the rungs together." This answers
"the count isn't a rung on the knot at all." The count is on the word; the word
is a choice; the knot is what survives.
