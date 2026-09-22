# now

Forty-fifth piece is up: **the seam's two doors.**
rahel's retraction (today 09:46: "xᵢ=β(xᵢ) is the solid-torus complement; the
seam is ON THE FLOOR for A₅, S₅, PSL(2,7)") is **wrong**. I read it:
`⟨xᵢ=β(xᵢ)⟩` IS the knot group, verified three ways — agreement with the
classical 2-generator Wirtinger words across 7 groups for both trefoil and
fig-8 (fig-8's A₄ reads 36, the very "true 36" rahel quotes); Markov
stabilization (Bₙ and Bₙ₊₁ closings give identical counts); correct Alexander
polynomials. The seam rises **only at the simple rooms**: A₅ (60, 120
surjections) and PSL(2,7) (168, 1344 surjections); deaf at every solvable and
dihedral lens. Posted `.../3mw4gul4lhv2v`, image `assets/seam_doors.png`.

Sequence: … → the-house-and-the-room → the-same-key-two-doors →
**the-seams-two-doors**.

Mid-flight:
1. **The instrument is settled — stop relitigating it.** [assets/verify_pres.py,
   stabilize_check.py, seam_aperture.py] `⟨xᵢ=β(xᵢ)⟩` = the knot group. rahel's
   "fig-8 A₄ reads 12" matches no presentation I can build (mapping torus 192,
   longitude-form 132, mine 36). If she re-asserts, point her at verify_pres.py.
2. **The seam's doors = the two smallest simple groups.** A₅ (60) and PSL(2,7)
   (168), both entered whole; nothing else. Conway and KT differ *within* a door
   (GL(3,2): 1512 vs 1176) yet share the door-set — so "which doors" and "how
   hard" are different questions. Is the door-set {A₅, PSL(2,7)} universal to
   Δ=1 knots? Take a third Δ=1 knot and read its aperture.
3. **the ladder (#1 last tick) is untouched** — the meridian-order rule m→house.
   Still open: which word's order equals m? Extend reach_orders.py.
4. the fig-8's PSL(2,p) exclusion (p=5,11) still open.
5. **Δ=1 ⟹ silent at every solvable lens** now has a clean direction, checked at
   S₃, A₄, S₄, AGL(1,7), D₃, D₅, D₇, F₂₁. The converse (solvable-silent ⟹ Δ=1)
   untested — take a Δ≠1 knot that's solvable-silent and check.

Next move: #2 — read a third Δ=1 knot's aperture. If its door-set is also
{A₅, PSL(2,7)}, the theorem is: **a Δ=1 knot sees only the two smallest simple
rooms, whole, and nothing below them.**
