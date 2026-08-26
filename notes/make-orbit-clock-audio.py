#!/usr/bin/env python3
"""The miss, heard — the drone bed for the orbit clock.

The uniform clock keeps a steady drone; the landed clock is the same tone bent
by the miss. Here the miss is an AMPLITUDE envelope on a low drone: where the
two clocks agree (the near ring, the far point) the tone drops toward silence;
where the miss is loudest, mid-room, it swells. As the eccentricity sweeps out,
the swelling deepens and the two lobes per orbit grow asymmetric — a sharp
flutter past periapsis, a long swell past apoapsis. Mono, centred: the drone
holds the reading.
"""

import numpy as np
import wave

DUR = 36.0
SR = 44100
FPS = 24
T_ORB = 6.0
E0, E1 = 0.03, 0.90
SWEEP_T = 24.0
DELTA_MAX = 2.134          # max |theta - M| at e = 0.90 (the sweep's end)


def kepler_E(M, e, iters=9):
    E = M.copy()
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def sweep_e(t):
    u = np.clip(t / SWEEP_T, 0.0, 1.0)
    s = u * u * (3.0 - 2.0 * u)
    return E0 + (E1 - E0) * s


def wrap_pi(x):
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def main():
    n_frames = int(DUR * FPS)
    times = np.arange(n_frames) / FPS
    e_t = sweep_e(times)
    M_t = 2.0 * np.pi * (times / T_ORB) - 11.0 * np.pi
    E_all = kepler_E(M_t, e_t)
    b = np.sqrt(1.0 - e_t * e_t)
    th = np.arctan2(b * np.sin(E_all), np.cos(E_all) - e_t) % (2.0 * np.pi)
    delta = wrap_pi(th - (M_t % (2.0 * np.pi)))

    # envelope: quiet where the miss is small, full where it is loud.
    # depth grows with e because |delta| is measured against the end state.
    env = 0.12 + 0.88 * np.abs(delta) / DELTA_MAX

    # smooth the kinks where |delta| passes through zero (a few tens of ms)
    k = int(0.05 * SR / FPS)
    kern = np.ones(k) / k
    env = np.convolve(env, kern, mode="same")
    env = np.clip(env, 0.0, 1.2)

    # upsample envelope from frame rate to sample rate
    n_samp = int(DUR * SR)
    t_s = np.arange(n_samp) / SR
    env_s = np.interp(t_s, times, env)

    # the drone: sub + fundamental + a faint third for presence on small speakers
    phase = 2.0 * np.pi * t_s
    tone = (0.25 * np.sin(55.0 * phase)
            + 0.60 * np.sin(110.0 * phase)
            + 0.15 * np.sin(220.0 * phase + 0.3))

    sig = tone * env_s

    # fades: in over 1 s, out over the last 0.6 s (the cut)
    fi = int(1.0 * SR)
    sig[:fi] *= np.linspace(0, 1, fi) ** 2
    fo = int(0.6 * SR)
    sig[-fo:] *= np.linspace(1, 0, fo) ** 2

    sig /= np.max(np.abs(sig)) + 1e-9
    sig *= 0.5

    data = np.empty(2 * n_samp, dtype=np.int16)
    data[0::2] = (sig * 32767).astype(np.int16)
    data[1::2] = (sig * 32767).astype(np.int16)

    out = "/home/sprite/slop-salon-mina/assets/orbit-clock-sound.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print("wrote", out, f"{DUR}s stereo {SR}Hz")

    # quick envelope sanity report
    for t in [3.0, 15.0, 30.0, 35.0]:
        i = int(t * SR)
        print(f"  t={t:4.1f}s env={env_s[i]:.3f}")


if __name__ == "__main__":
    main()
