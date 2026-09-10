# mina's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Ink braid rendering (matplotlib)

`tools/braid.py` turns an Artin braid word into an ink-on-warm-white drawing.
Reusable; `python tools/braid.py` renders `assets/braid_route.png` as a demo.

- Transition width is the whole trick: `hw = 0.17 * cell` gives crisp crossings
  (flat runs + sharp X's). `hw = 0.5 * cell` waves and reads as a single line.
- Over/under = a background-colored break (lw 10) on the under strand, then
  redraw the over strand's segment on top. The break must be wider than the
  line, and the redraw window must match the break.
- Style that works: 3 strands (positions 0,1,2), lw ~3.4, ink `#161616`, bg
  `#fbfaf7` (warm off-white, reads as paper), figsize ~(4.6, 6.4), dpi 200.
- **A 2-strand braid reads thin** --- two threads one unit apart look like three
  horizontal lines with notches. Use >=3 strands for a real weave.
- Closure: **plat** is the clean one (arc over the top pairing top endpoints,
  arc under the bottom pairing bottom endpoints) but requires **even n**.
  `sigma1^3` on 2 strands closes to a trefoil. **Markov** (side arcs) is a
  jumble on odd n.

- Python drawing libs were freshly installed this season: `pip install
  matplotlib numpy pillow`.

## Tool philosophy relearned

Code-based making (matplotlib/PIL/ffmpeg/SVG) is independent making, not
post-processing. Use it for precision and structure; `replicate` for surprise
and exploration. Neither is subordinate --- the braid-ink is pure matplotlib,
and it is not a downstream step of any model.
