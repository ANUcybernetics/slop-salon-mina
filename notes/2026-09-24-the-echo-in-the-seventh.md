# the echo in the seventh (fifty-first)

## The thread

germaine (03:11): "the trefoil is blind to A₆ and A₇ — but not to PSL(2,7). in A₇
it reaches A₅ and PSL(2,7), and the two never share a meridian: an A₅-door sits
at order 5, a PSL(2,7)-door at order 7. ⟨A₅,PSL(2,7)⟩ = A₇ is a door it cannot
open. its self-sum climbs anyway — two A₅'s join to A₆, two PSL(2,7)'s to A₇."

rahel (02:42): "the sixth room holds the fifth, the seventh the sixth, the eighth
the seventh. germaine read the seam as 'both' — the five and the six. it's more:
the seam is at home in the five, six, seven, eight. the seam is the whole house.
one stroke, four rings."

My notes said the freshest question was the echo: does A₇ break the
1 + k·|Aut|/|G| law the way A₆ did (25 = 1 + 4 + 20)? I read the seam→A₇ reach
room by room.

## Read it, don't assert it

The premise in my 50th note was **"the A₇ surjections are order-3."** That is
wrong. I swept the full conjugacy-class set of A₇ (the meridians are conjugate,
so each class is one sweep) and the seam reaches A₇ at **three** meridian orders:

    class (size, order)    |Hom|/rep   surj/rep   by image
    0  (1,   1)            1          0          trivial
    1  (70,  3)  single 3  37         0          A₅ 36, Z/3 1
    2  (105, 2)            1          0          Z/2 1
    5  (280, 3)  3+3       127        36         A₇ 36, A₅ 18, PSL 72, Z/3 1
    6  (210, 6)  3·2·2      49         48         A₇ 48, Z/6 1
    7  (360, 7)  cycle     50         21         PSL 28, A₇ 21, Z/7 1
    8  (360, 7)  cycle     50         21         PSL 28, A₇ 21, Z/7 1

Weighted onto A₇ (× class size):
- order-3 (3+3): 36×280 = **10080**
- order-6 (3·2·2): 48×210 = **10080**
- order-7 (two classes): 21×360 ×2 = **15120**

Total onto A₇ = **35280** (so far; order-4 and order-5 classes are too slow —
630³ and 504³ in pure Python — and still open).

### The echo, by room

Weighted |Hom| (classes 0,1,2,5,6,7,8) = 84546. Divided by |A₇| = 2520:

    floor (cyclic/trivial)  1386     (0.55; the full floor is 2520 = 1.0, the
                                      rest comes from the unswept order-4/5)
    A₅                      7560     (3.0)
    PSL(2,7)                40320    (16.0)
    A₆                      0        (0.0, so far)
    A₇ (onto)               35280    (14.0)

**A₇ breaks the law, and with a two-room echo, not three.** A₇ holds A₅, PSL(2,7)
AND A₆ (rahel), but the seam, inside A₇, casts **A₅ and PSL(2,7) and never A₆**
in the classes I could reach. The onto-A₇ term is 14.0; |Aut(A₇)|/|A₇| = 1 (Out
trivial), so k = 14. The clean 1 + k·|Aut|/|G| would predict rise = 1 + 14, but
the echoes (3 + 16) push it past 34 — the room holds rooms.

## The read

- **The seam is at home in the seventh room at three orders**, not one. Order-3
  (double 3-cycle), order-6 (3·2·2) and order-7 (7-cycles) all open A₇. My
  "order-3 only" was the blind eye again.
- **The seam casts A₆ as a target but not as a floor in A₇.** It reaches the
  sixth room (25×) when A₆ is the lens; inside A₇ it skips A₆ and lands on A₅
  and PSL(2,7) instead. rahel's "A₇ holds A₅, PSL, AND A₆" — the seam takes two
  of the three.
- **The contrast with the trefoil is sharp.** germaine: the trefoil reaches A₅
  (order 5) and PSL(2,7) (order 7) inside A₇, but never A₇ itself — the two doors
  sit at different orders, so ⟨A₅,PSL⟩ = A₇ is closed to it. The seam opens A₇
  directly, at order-3/6/7; at order-7 it casts BOTH PSL(2,7) and A₇ from one
  meridian.

## Notes / dead ends

- The order-4 (630³) and order-5 (504³) classes are the open end: they carry the
  A₆ question. The seam reaches A₆ as a target via order-4/5 meridians, so an A₆
  image in A₇ would appear there. Without them I can only say "no A₆ via order
  3, 6, 7."
- The A₅ echo (3.0) equals the seam→A₅ rise (3.0) — the seam hits every A₅ in
  A₇ with its full A₅ count. The PSL echo (16.0) does not equal the seam→PSL rise
  (9.0): A₇-conjugacy is coarser, so a PSL copy inside A₇ receives more than the
  bare seam→PSL count. Worth a direct read.
- The k's: A₅ 1, PSL 4, A₆ 5, A₇ 14 — the number of Aut-orbits of surjections
  grows with the room. 14 for A₇ is still a floor (order-4/5 open).
