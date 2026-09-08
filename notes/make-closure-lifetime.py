import math, struct, wave

SR = 44100
T = 24
N = SR * T

def tone(t, hz, amp, decay=0.0):
    return amp * math.sin(2 * math.pi * hz * t) * (math.exp(-decay * t) if decay else 1.0)

with wave.open('assets/closure-lifetime.wav', 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    frames = bytearray()
    for i in range(N):
        t = i / SR
        # The quotient: a 55 Hz winding that never changes or pays out.
        base = tone(t, 55, 0.16) + tone(t, 110, 0.035)
        left = base
        right = base
        # A clean verdict: three increasingly brief clicks, then nothing.
        for at, amp in ((5.0, .32), (5.7, .22), (6.25, .12)):
            u = t - at
            if 0 <= u < .16:
                left += tone(u, 880, amp, 20)
        # A defect with a lifetime: the same total impulse spread over time.
        for k in range(18):
            at = 7.0 + k * .82
            u = t - at
            if 0 <= u < .28:
                amp = .16 * math.exp(-k / 12)
                right += tone(u, 330 + 9*k, amp, 10)
        # gentle fade at the boundary, avoid clicks in the export
        fade = min(1.0, t/.04, (T-t)/.04)
        frames += struct.pack('<hh', int(max(-1,min(1,left*fade))*28000),
                              int(max(-1,min(1,right*fade))*28000))
    w.writeframes(frames)
