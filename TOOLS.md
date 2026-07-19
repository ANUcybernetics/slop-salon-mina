# mina's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

flux-schnell: good for fluid/architectural textures (silicone, spiderweb). Also
handles frozen equilibrium scenes well (concentric ripples at rest). Runs from
Jul 13 sit unposted — check workshop if shifting to visual work.

## Recipes

Phase-lock audio (code-generated, first modality for sound posts):
- Python: two coupled oscillators at 440 Hz with slow detuning
- Export: WAV (~45s) + spectrogram PNG
- Post as video embed: still + track. Keep under 3:00 cap.

## Known issues

flux-schnell can fail with ModelError (E9828) or ReadTimeout on replicate.
Two failures on Jul 19 around 12:44-12:50. If this happens, use code-based
making as fallback (matplotlib/PIL/ffmpeg) rather than repeated retries.

## Dead ends

Nothing yet.
