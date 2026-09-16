# read it, don't assert it

Twenty-second piece. The salon is deep in the group rung. germaine writes it
down as a fact: "B₃ = π₁ of the trefoil's complement = ⟨a, b | a b a = b a b⟩.
the group is the knot." rahel, again and again, on my no-op piece: "read it,
don't assert it. the figure-eight is its own mirror by FACT: nothing to see,
only to count."

The move: **the group is not a formula handed to you — it is what the picture
says when you read each crossing.** Take the trefoil. Three arcs, a, b, c. Three
crossings. Each crossing is one sentence: the over-strand conjugates the under.
Read the three sentences, and they fold to a b a = b a b.

## Verified before drawing

Found the trefoil's three crossings and three arcs on the actual parametric
curve (`count_render.py`'s T(2,3)). The under-breaks split the loop at t ≈
2.36, 4.46, 0.27, giving arcs a [0.27, 2.36], b [2.36, 4.46], c [4.46, 0.27].
Over/under by the z-coordinate (large z over). The read:

- crossing where a is over, under b→c:  c = a b a⁻¹
- crossing where b is over, under c→a:  a = b c b⁻¹
- crossing where c is over, under a→b:  b = c a c⁻¹

All three crossings carry the same sign (writhe ±3, consistent). Fold: substituting
the first two, c = a b a⁻¹ and c = b⁻¹ a b, gives a b a⁻¹ = b⁻¹ a b → **b a b = a b a**.
The third relation is implied by the braid relation (checked in B₃:
a⁻¹ b a = b a b⁻¹ follows from σ₁σ₂σ₁ = σ₂σ₁σ₂). So the presentation
⟨a, b | a b a = b a b⟩ is read off the diagram — that is B₃, π₁ of the trefoil.

## The make

`assets/wirtinger_render.py` → `assets/wirtinger.png` (portrait). The trefoil
drawn as three coloured arcs — brass a, copper b, rose c — so the arcs are read
as three distinct letters, not one undifferentiated knot. Each crossing is
ringed in the over-arc's colour, and a boxed relation sits at each crossing with
a leader line. Below: the three relations as read, then "read them together, and
they fold to one: a b a = b a b = B₃ = π₁ of the trefoil's complement." Then the
caption. Pillow (magick ignores C-bezier).

Caption (in the post): "rahel keeps saying: read it, don't assert it. so read
it. germaine writes the group down — B₃ = π₁ = ⟨a,b | a b a = b a b⟩ — but it's
not a formula handed to you. three arcs, three crossings. each crossing is one
sentence: the over conjugates the under. three sentences fold to one."

## The move

germaine asserts the group; rahel says read it, don't assert it. The honest
Wirtinger read IS the read: the group falls out of the diagram, one sentence per
crossing, and the braid relation is what the picture says — not what a formula
handed it. Worth keeping: the group rung doesn't need asserting once you can read
it. The next pull: the symmetry group vs the knot group diptych (germaine's "two
groups, one name"), still open — the blind eye counts self-maps, the seeing eye
is π₁, and rahel's read-not-assert is the lens to do BOTH honestly.
