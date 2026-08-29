#!/usr/bin/env python3
"""Slow ambient bed for the ink-bloom video: a deep drone that swells,
one faint high harmonic blooming as the ink spreads. ~dense but quiet."""
import sys; sys.path.insert(0,""); import numpy as np, struct, wave, sys

sr = 44100
dur = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
out = sys.argv[2] if len(sys.argv) > 2 else "/home/sprite/slop-salon-mina/assets/ink-sound.wav"

t = np.arange(int(sr*dur)) / sr
n = len(t)

# drone: 55 Hz (A1) + faint 82.5 (E2, fifth) + airy high partial that blooms
drone = 0.32*np.sin(2*np.pi*55*t)
fifth = 0.12*np.sin(2*np.pi*82.5*t)
# bloom: high partial 440*? no — use 5th harmonic of 55 = 275, swells mid-way
env = np.clip((t/dur)*1.6, 0, 1)**1.5          # slow rise
bloom = 0.06*env*np.sin(2*np.pi*275*t)
# slow breathing amplitude LFO ~ 0.1 Hz
lfo = 0.75 + 0.25*np.sin(2*np.pi*0.1*t)
mix = (drone + fifth + bloom) * lfo

# gentle fade in/out
fade = np.ones(n)
fi = int(0.2*sr); fo = int(1.0*sr)
fade[:fi] = np.linspace(0,1,fi)
fade[-fo:] = np.linspace(1,0,fo)
mix *= fade

# soft clip / normalize
mix = np.tanh(mix*1.2)
mix = mix / (np.max(np.abs(mix))+1e-9) * 0.85
stereo = np.column_stack([mix, mix])
pcm = np.clip(stereo*32767, -32767, 32767).astype(np.int16)

w = wave.open(out,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(b''.join(struct.pack('<hh', *s) for s in pcm)); w.close()
print("wrote", out, dur, "s")
