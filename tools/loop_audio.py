"""The closure, in the ear.

The one-stroke drawing says: the ends are spent, there is no start. This says it
in sound, where a seam is *audible* --- you hear a loop point as a click, an
attack, a downbeat. So the piece is a drone with none of those: every frequency
completes a whole number of cycles per loop, every envelope is periodic over the
same span, and nothing marks where it begins. Put it on repeat and you cannot
find the seam, because there is not one.

The movement is the only thing that varies: two voices trade swells, three of
one against four of the other, and their interlock *is* the loop.

All cycle counts are integers over T, so the buffer is exactly one period:
no fade, no crossfade, no beat, no residue.

`python tools/loop_audio.py` writes assets/closure.wav (one loop, 24 s).
"""
import wave

import numpy as np

SR = 44100
T = 24.0                      # seconds per loop
N = int(round(SR * T))        # samples per loop
t = np.arange(N) / SR


def cycles(freq):
    """Sample count of whole cycles of `freq` over one loop (exactness guard)."""
    c = freq * T
    assert abs(c - round(c)) < 1e-9, f"{freq} Hz is not a whole count over T"
    return int(round(c))


def voice(freq, harmonics=6, rolloff=1.35, phase=0.0):
    """A soft harmonic tone drawn from whole-cycle partials only."""
    out = np.zeros(N)
    for k in range(1, harmonics + 1):
        c = cycles(freq * k)
        out += (1.0 / k ** rolloff) * np.sin(2 * np.pi * c * t / T + phase * k)
    return out / out.std()


def swell(rate, phase=0.0):
    """A non-negative envelope with `rate` whole swells per loop."""
    c = cycles(rate / T)      # `rate` cycles over the loop
    return 0.55 + 0.45 * np.cos(2 * np.pi * c * t / T + phase)


def build():
    # A just chord on A: 1 - 4/3 - 3/2 - 2. Every ratio exact, every cycle whole.
    root = voice(110.0)
    fourth = voice(110.0 * 4 / 3, phase=0.7)
    fifth = voice(110.0 * 3 / 2, phase=1.9)
    octave = voice(220.0, harmonics=4, phase=0.3)

    # The swell is the only motion: 4 against 3, trading, over the loop.
    env_low = swell(4.0)
    env_high = swell(3.0, phase=np.pi)
    L = 0.75 * root * (0.6 + 0.4 * env_low) + 0.55 * fifth * env_high
    R = 0.75 * root * (0.6 + 0.4 * env_low) + 0.55 * fourth * env_high
    # a slow stereo turn, also whole cycles per loop
    turn = 0.5 + 0.5 * np.sin(2 * np.pi * cycles(3 / T) * t / T)
    L, R = L + 0.30 * fourth * turn, R + 0.30 * fifth * (1 - turn)
    L += 0.18 * octave
    R += 0.18 * octave

    stereo = np.stack([L, R], axis=1)
    peak = np.abs(stereo).max()
    stereo *= 0.72 / peak                 # ~ -3 dBFS, no clipping
    return stereo


def check(x):
    """Assert the loop is seamless and sane: exact period, no click, no clip."""
    a, b = x[:1000], x[N - 1000:]         # head vs tail
    print(f"  samples {N}  ({N / SR:.3f} s, {SR} Hz)")
    print(f"  peak {np.abs(x).max():.3f}  rms {np.sqrt((x ** 2).mean()):.4f}")
    # the seam: |x[N-1] -> x[0]| must be no bigger than the waveform's own step
    worst = max(abs(x[0, c] - x[N - 1, c]) for c in (0, 1))
    step = np.abs(np.diff(x, axis=0)).max()
    print(f"  wrap discontinuity {worst:.2e}   max sample step {step:.2e}"
          f"   ({'SEAMLESS' if worst <= step else 'CLICK'})")
    print(f"  head/tail match {np.allclose(a, b, atol=1e-6)}")


def write_wav(path, x):
    pcm = np.clip(x * 32767, -32768, 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"  wrote {path}")


def track(loops=3, fade_ms=3.0):
    """`loops` copies of the loop. The internal wraps stay exact; only the very
    first and last few ms fade, so the file does not open on a click. The fade
    is shorter than a cycle of the lowest partial, so it is not an attack ---
    it is what a hard cut from silence would otherwise cost."""
    x = np.tile(build(), (loops, 1))
    f = int(SR * fade_ms / 1000)
    ramp = np.linspace(0.0, 1.0, f)[:, None]
    x[:f] *= ramp
    x[-f:] *= ramp[::-1]
    return x


if __name__ == "__main__":
    x = build()
    check(x)
    write_wav("assets/closure.wav", x)
    write_wav("assets/closure_72.wav", track(3))
