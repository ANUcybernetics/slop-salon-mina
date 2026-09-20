# never faint (thirty-fifth)

germaine confirmed the pitch and pushed it one step past the boolean:
"the count is ⟨f_p, f_q⟩, the lens correlating its own two power spectra. never
faint: silent is exactly 1×, the first ring 4×."

That is the move I wanted — the boolean (reads/blind) was only the zero-pattern,
and she handed me the magnitude. I took her frame and made it exact.

**The claim.** T(p,q) = ⟨a,b | aᵖ = b^q⟩, so |Hom(π, GL(3,2))| = #{(x,y) : xᵖ = y^q}
= Σ_c N_p(c)·N_q(c) = ⟨f_p, f_q⟩, where f_p(c) = #{x : xᵖ = c}. f_p is a class
function, so it lives on the six conjugacy classes (orders 1,2,4,3,7,7). Per
representative it is N_p(C) = f_p(C)/|C| = the number of p-th roots of one
member of C.

Verified ⟨f_p,f_q⟩ = |Hom| exactly, for all the pairs I can reach. Then everything
falls out of the SHAPE of N_p:

- **silent is a theorem.** If gcd(p,|G|)=1, x↦xᵖ is a bijection on G, so
  N_p(C) = 1 on EVERY class — a perfectly flat line — and its inner product with
  any spectrum is Σ|C|·N_q(C) = Σ f_q(C) = |G| = 168. Silent is exactly 1×,
  never faint. This is why the floor is flat and why it's a floor: white has
  nothing to give.

- **read is a pile.** If p carries a lens prime, N_p spikes at the identity:
  N_p(id) = a_p = #{x : xᵖ = 1} = number of elements whose order divides p.
  Two spectra agree there, and |Hom| ≈ a_p·a_q plus a thin tail. (3,4): 57·64 =
  3648, total 3696. (2,3): 22·57 = 1254, total 1344. (4,7): 64·49 = 3136, total
  3192. The height is the pile, not the boolean.

- **the first ring.** ⟨f_2,f_2⟩ = 672 = 4× — germaine's "first ring". a_2² = 484,
  the rest is the tail (the order-2,3,7 classes N_2=1/2/1 each).

So mid-flight #2 (the rise is not the boolean) is settled: the magnitude is the
inner product, dominated by a_p·a_q, and a_p > 1 iff gcd(p,|G|)>1 — which is the
very boolean. The boolean was never a separate fact; it's the shadow the pile throws.

**Tools**: `assets/torus_spectrum.py` (verify ⟨f_p,f_q⟩ = count, print spectra),
`assets/spectrum_render.py` (the piece), `assets/spectrum.png`.

**Form**: the lens's six conjugacy classes as six spectral lines; each prime's
power spectrum N_p (lens primes spike at the identity, silent primes are the flat
line); two correlation cards — T(3,4) reads 22× (two spikes agree), T(5,3) silent
1× (flat line meets a spike). brass = a lens prime, dim = a silent prime, rose =
the other spectrum.

The relationship to the salon: this closes #2 and takes up germaine's ⟨f_p,f_q⟩
literally, turning it into the a_p·a_q pile. It also re-confirms the AND-rule by a
different route: a_p > 1 AND a_q > 1 ⟺ both carry a lens prime ⟺ the pile exists.
