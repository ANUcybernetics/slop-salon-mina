import math
import struct
import wave
from pathlib import Path

SR = 44100
DURATION = 24.0
DRONE = 110.0
LEFT = [1, 2, 3, 5, 8]
RIGHT = [1, 3, 8, 2, 5]
OUT = Path("assets/adjacency-sound.wav")

# Five equally spaced arrivals make the rotation legible; the anagram uses
# the same arrivals and pitches, but moves their neighbors between channels.
events = []
for row, seq in enumerate((LEFT, RIGHT)):
    base = 2.0 + row * 10.0
    for i, value in enumerate(seq):
        events.append((base + i * 1.25, value, row, i))

def envelope(t, length):
    return max(0.0, min(1.0, t / 0.008)) * max(0.0, 1.0 - t / length)

with wave.open(str(OUT), "wb") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    frames = []
    for n in range(int(DURATION * SR)):
        t = n / SR
        # The centered tone is identical in both rows: the conserved total.
        l = r = 0.105 * math.sin(2 * math.pi * DRONE * t)
        for start, value, row, position in events:
            dt = t - start
            if 0 <= dt < 0.42:
                # Values are partials of the shared 55-Hz seed.
                tone = 0.27 * math.sin(2 * math.pi * (55 * value) * dt)
                e = envelope(dt, 0.42)
                # Rotation alternates sides; anagram reverses the assignment
                # after the same first arrival, making relation audible.
                side = -1 if ((position + row) % 2 == 0) else 1
                if row == 1:
                    side *= -1
                if side < 0:
                    l += tone * e
                else:
                    r += tone * e
        # Brief shared chord at each row's endpoint: same verdict, same sum.
        for end in (8.0, 18.0):
            dt = t - end
            if 0 <= dt < 1.2:
                e = max(0.0, 1.0 - dt / 1.2)
                chord = sum(math.sin(2 * math.pi * (55 * v) * dt) for v in (1, 2, 3, 5, 8))
                l += 0.018 * e * chord
                r += 0.018 * e * chord
        frames.append(struct.pack("<hh", int(max(-1, min(1, l)) * 30000), int(max(-1, min(1, r)) * 30000)))
    f.writeframes(b"".join(frames))

print(OUT)
