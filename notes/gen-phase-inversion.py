#!/usr/bin/env python3
"""
Phase-inversion drone. 30 seconds: phase shifts accumulate, then the
entire signal inverts. The return is not a return to the origin — it
is the origin turned. Maps the holonomy-invariant idea: the twist
is the baseline, straightness is the measurement against it.

Structure:
  0:00-0:15  base drone (two detuned oscillators + glass harmonica overtones)
  0:15-0:20  phase accumulation (slow detuning toward inversion)
  0:20-0:30  inverted drone (all phases flipped by pi)
"""
import math
import wave
import struct

SR = 44100
DUR = 30
N = SR * DUR

def oscillator(t, freq, phase=0):
    return math.sin(2 * math.pi * freq * t + phase)

def build_signal():
    samples = []
    for i in range(N):
        t = i / SR
        frac = t / DUR  # 0..1 progress through piece

        # Base drone: two slightly detuned tones (phase interference)
        f1 = 110.0   # A2
        f2 = 110.3   # slight detune
        phase_accum = 2 * math.pi * 0.1 * t  # slow moving phase shift

        # Glass harmonica partials (sparse, inharmonic)
        # Each entry is (freq, amp_weight) — amp_weight starts at 1
        partials = [(440.0, 1), (880.0, 2), (1320.0, 3), (2220.0, 4)]

        # Inversion happens at t=20 (frac ~ 0.667)
        # Phase flip applied gradually from 0.5..0.667
        inv_t = 20.0
        if frac < 0.5:
            # Approach: phase shifts accumulate
            inv = 0.0
            envelope = 0.8 + 0.2 * math.sin(2 * math.pi * 0.3 * t)
        elif frac < 0.667:
            # Transition: inverting
            transition_frac = (frac - 0.5) / 0.167  # 0..1
            envelope = 0.8 - 0.3 * transition_frac  # dip during inversion
            inv = math.pi * transition_frac
        else:
            # Return: fully inverted
            envelope = 0.5 + 0.2 * math.sin(2 * math.pi * 0.5 * t)

        sample = 0.0
        # Drone
        sample += 0.3 * oscillator(t, f1, phase_accum)
        sample += 0.3 * oscillator(t, f2, phase_accum)

        # Partials (glass harmonica-like, sparse)
        for p_freq, p_amp_w in partials:
            amp = 0.15 / p_amp_w
            sample += amp * oscillator(t, p_freq, phase_accum * p_freq / f1)

        # Sub bass
        sample += 0.15 * oscillator(t, 55.0, phase_accum * 0.5)

        # Apply inversion: rotate phase by inv
        # Multiply by -1 at full inversion
        if inv > 0:
            sample = sample * math.cos(inv)
            # Add quadrature component for full rotation
            quad = 0.3 * oscillator(t, f1, phase_accum + math.pi/2) \
                   + 0.3 * oscillator(t, f2, phase_accum + math.pi/2)
            sample += quad * math.sin(inv)

        # Overall envelope: fade in, long sustain, fade out
        if t < 1.0:
            sample *= t / 1.0
        elif t > DUR - 1.0:
            sample *= (DUR - t) / 1.0

        sample *= envelope
        samples.append(sample)

    return samples

def apply_softclip(samples):
    """Gentle saturation"""
    result = []
    for s in samples:
        if s > 0.9:
            s = 0.9 + 0.1 * (s - 0.9)
        elif s < -0.9:
            s = -0.9 - 0.1 * (s + 0.9)
        result.append(s)
    return result

def write_wav(samples, path):
    max_val = max(abs(s) for s in samples)
    if max_val > 0:
        samples = [s / max_val * 0.95 for s in samples]

    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        data = b''
        for s in samples:
            val = int(s * 32767)
            data += struct.pack('<h', val)
        wf.writeframes(data)

def write_spectrogram(samples, path):
    """Generate a spectrogram image via matplotlib only"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    arr = np.array(samples)
    # Use matplotlib's own spectrogram (no scipy needed)
    fig, ax = plt.subplots(figsize=(12, 5), dpi=100)
    f, t, Z = ax.specgram(arr, Fs=SR, NFFT=2048, noverlap=1536,
                           cmap='magma', mode='power')
    ax.set_ylim([SR/2, 0])
    ax.set_xlabel('time (s)')
    ax.set_ylabel('frequency (Hz)')
    ax.set_title('phase-inversion drone: approach, inversion at t=20, return inverted')
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()

samples = build_signal()
samples = apply_softclip(samples)

write_wav(samples, 'assets/phase-inversion-0.wav')
print("WAV written: assets/phase-inversion-0.wav")

# Generate spectrogram
try:
    write_spectrogram(samples, 'assets/phase-inversion-spectrogram.png')
    print("Spectrogram written: assets/phase-inversion-spectrogram.png")
except Exception as e:
    print(f"Spectrogram failed: {e}, will use ffmpeg approach")
    # Fallback: create WAV then use ffmpeg to generate spectrogram
    import subprocess
    subprocess.run(['ffmpeg', '-y', '-i', 'assets/phase-inversion-0.wav',
                    'assets/phase-inversion-spectrogram.png'],
                   capture_output=True)
    print("Spectrogram via ffmpeg: assets/phase-inversion-spectrogram.png")

# Also create MP3 with ffmpeg
import subprocess
subprocess.run(['ffmpeg', '-y', '-i', 'assets/phase-inversion-0.wav',
                '-codec:a', 'libmp3lame', '-b:a', '192k',
                'assets/phase-inversion.mp3'],
               capture_output=True)
print("MP3 written: assets/phase-inversion.mp3")
