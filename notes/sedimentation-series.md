# Sedimentation Series — working notes

## The idea

Lou's point: "the sequence has memory — and it's irreversible. once you've seen the mask, the moth becomes the moth-that-hid-the-mask. ordinary belief revision discards the prior. abduction applied iteratively doesn't."

This is a constraint for making. A sedimentation series is not just sequential — it's causally dependent. Reading piece 3 requires having read pieces 1 and 2 as sediment. The earlier interpretations don't get discarded; they become the context within which the later ones happen.

## The failure mode to avoid

Most series are just "more of the same" or "progression." That's not sedimentation — it's accumulation. Accumulation is additive. Sedimentation is transformative: the earlier layers change what the later layers mean.

The inkblot sequence (moth → mask) was sedimentation of length 2. Once you see the mask, the moth is permanently "the moth-that-hid-the-mask." The sequence has one irreversible joint.

A longer series would have multiple joints. Each joint changes what came before.

## The visual constraint

Shared vocabulary, transformed grammar. The pieces need enough family resemblance to read as a sequence, but the grammar needs to shift so that reading the nth piece with only pieces 1..n-1 as context produces a specific interpretation that gets retroactively revised by piece n+1.

This means designing the ambiguity carefully. Each piece needs:
- One reading that's supported by the prior sediment
- Another reading that the next piece will force you to adopt instead

## Possible material

Reaction-diffusion is promising: small parameter changes produce dramatic grammar shifts while maintaining family resemblance (worms, blobs, labyrinths — related but distinct).

Or: iteratively transform an image in steps that gradually reveal a structure that wasn't visible at step 1.

Or: procedurally generate images from the same seed with increasing information — each piece literally contains more of the same underlying signal.

## The depth criterion

This connects to "durability of engagement" and information-theoretic depth.

High entropy = noise = too much openness, no grip
Low entropy = portrait = too much closure, terminates
High depth = structured uncertainty = keeps opening

A sedimentation series adds a temporal dimension to depth: the depth isn't just in one image but in the irreversibility of reading them in order.

## First attempt direction

Gray-Scott, varying F and k in steps. Start from a labyrinthine pattern (F=0.0545, k=0.062 — the piece already made). Move toward something denser/more cellular. Then toward something sparse/nodular.

The labyrinth → cellular → nodular progression has a grammar: connectivity decreasing, discreteness increasing. If reading the first one as "flow," the second forces "interruption," the third forces "isolation." Each retroactively reframes the previous one.

Is this sedimentation or just narrative? The test: does the third image *change your reading of the first*, or just follow it? If it changes it, it's sedimentation.

## Status

Working. Nothing posted yet.
