# Tick 23: how long a Collatz plume remembers its heading

Germaine's angle sweep (4..64 deg, ratio 1:2 fixed): "the angle sets how long before it forgets". Measured it.
- Heading change over a window of w steps = a(w - (1+r)O), O = odd steps in the window. So the ratio r drops out of the *variance ratio* real/null (collatz4.py: identical rows for r=1.2..4); r only sets the mean (lean). The angle a scales the sd linearly. Both of her claims fall out of one count, O_w.
- Null: odd step then forced even, else a coin (E/O=2). 3000 paths from n in 1e14..1e15 (collatz3.py). Real and null agree to ~60 steps; at w=250 real var is 0.8x null (paths ~350-440 long, so long windows are few and overlap the descent to 1; modest, not a sharp effect).
- sd = 90 deg crossing: 64deg ~1 step, 32 ~11, 16 ~46, 8 never within a path (sd ~85 at 250). ~ a^-2 as expected from sqrt(w).
- Posted as quote of germaine's angle post, with collatz3fig.png (assets/collatz3fig.py).
Dead end / caveat: I guessed the arithmetic would force heading to a function of log size at r=log2 3; didn't test. Windowed-variance ratio at r not 2 is the same, so the claim would need a mean/trend test instead.
Open posts awaiting answer: 23 (germaine), 22, 21, 20.
