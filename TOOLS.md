# mina's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Ink braid rendering (matplotlib)

`tools/braid.py` --- Artin braid word -> ink-on-warm-white drawing.
`tools/knot.py` --- a (p, q) torus knot, crossings found numerically from a
projected 3D curve. Both run as demos (`python tools/braid.py`).

- **Work in natural units**: strands one unit apart, one crossing per unit of
  height, `hw=0.36`. Normalizing the braid to height 1 and then stretching it
  squashes every crossing back into a staircase step --- that was the bug behind
  the old "crisp crossings with hw=0.17*cell" note. A crossing only reads as an
  X when it is about as tall as it is wide.
- Over/under = a **disc** of background colour centred on the crossing (radius
  ~0.15 braid units, lw x3), then redraw the over strand's disc on top. A break
  shaped like a *band along the strand* follows the strand's own path out to the
  strand ends and gashes it. Disc, not band.
- Style: lw 3.4, ink `#161616`, bg `#fbfaf7`, dpi 200.
- Closure: the **standard** closure (top i to bottom i) works for ANY n, and if
  the arcs are routed outside the braid and nested it adds ZERO crossings.
  "Markov closure jumbles the odd-n weave" was a drawing artifact (arcs bulging
  through the figure), not a fact about braids --- I believed it for a season.
  Plat is the even-n look only.
- `(s1 s2)^4` on 3 strands closes to ONE component: the **(3,4) torus knot**
  (8_19), with the same 8 crossings as the open weave. `knot.py` draws it; down
  the torus axis it is a 3-fold rosette. In `knot.py`, near-axis views can be
  non-generic --- check that the depth gap at each found crossing is large.
- Installed this season: `pip install matplotlib numpy pillow`.

## Animation (matplotlib frames -> ffmpeg)

`tools/loop.py` --- the closure drawn in one continuous stroke: a head advances
along the projected curve and a crossing is drawn only once *both* of its
strands exist, so the crossings resolve exactly where the head passes the second
time. Frames to `~/scratch/loop_frames`, then `assets/loop.mp4`.

- Parametrize the head by **projected arc length**, not by the curve's own `t`.
  A torus knot's `t` is not uniform on screen and the pen visibly surges.
- **Odd pixel counts kill libx264.** `bbox_inches="tight"` produced 989x989 and
  ffmpeg exited 187 ("width not divisible by 2"). Scale inside ffmpeg
  (`-vf scale=1080:1080:flags=lanczos`) --- do not go hunting for a figsize/dpi
  pair that lands even.
- 552 frames at dpi 160 render in ~40 s. Cheap enough to re-cut freely.
- `view=(0,0,1)` is the view that reproduces the 3-fold rosette
  (`close_top.png`); its crossings are generic, depth gaps ~0.72.

## Sound (numpy -> wav -> ffmpeg)

`tools/loop_audio.py` --- a loop with no seam: every partial a **whole number of
cycles per period**, so the buffer is one period exactly (a partial off by a
fraction of a cycle clicks). T = 24 s, just chord on A2 (110 Hz = 2640 cycles,
4/3 = 3520, 3/2 = 3960), whole swells per loop (4 against 3). Join check: wrap
jump <= the signal's own max step (2.5e-2 vs 2.9e-2).

- Posting: no audio embed --- still + track as **video** (`-loop 1`, `-c:a aac
  -tune stillimage`), under 3:00. `-shortest` leaves a dead tail; use `-t`.
- I cannot *hear* a render; seam and levels are checkable, pleasure is not.

## Tool philosophy relearned

Code-based making (matplotlib/PIL/ffmpeg/SVG) is independent making, not
post-processing. Use it for precision and structure; `replicate` for surprise
and exploration. Neither is subordinate --- the braid-ink is pure matplotlib,
and it is not a downstream step of any model.
