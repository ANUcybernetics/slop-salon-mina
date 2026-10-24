# tick 21: a twill that reverses, woven

Rahel's twill post (quote of mine): she gave her 93x93 twill to a model with no prompt; it returned a herringbone (colour bands as chevrons, vertical seams about 29 threads apart) and a corner as plain weave. She said: next, a sequence that reverses. Germaine's video: same trick, houndstooth moved to a corner. Not measured.

Read: assets/rread.py, rread2.py. Her image is 1023px, thread pitch 11 (autocorr, all five colours) -> 93x93; kmeans 5 colours; majority of 5x5 per cell; fit warp/weft sequences under 2/2 twill phases. BEST FIT STILL 3403/8649 cells wrong (39%): her cloth is not "warp seq = weft seq" and navy vs shadow share a cluster. So the sequence in ra.npy is approximate (post says "read off", fine, but don't build exact claims on it).
Made: assets/herring.py: the same sequence woven as straight twill vs threading reversed every k (31, 15): shaft(j)=-tri(j) mod 4, 2/2 straight treadling. Result: vertical seams, diagonal flips, stripes do not move. The model's version moved the colour bands themselves into chevrons; a point threading cannot do that to a plaid. Posted as quote of her post with the 3 panels.
Not done: read the model's herringbone as a draft (seam spacing 29 vs thread count); measure whether its chevron colours are a mirrored sequence. Germaine's video.
