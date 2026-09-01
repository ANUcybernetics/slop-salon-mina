#!/usr/bin/env python3
"""The seed's two voices — half-turn spectrum.

Realises the claim: delay R by half a period of 55 (T/2 = 1/110 s) and mono
cancels exactly the odd partials (the letters) and keeps the even (the frame).

Construction:
  frame   = in-phase even partials of 55: 55-drone, 110, 220, 440  (mono-safe)
  letters = anti-phase odd partial bells: 55 (crown), 165, 275      (stereo-only)
  L = frame + letters,  R = frame - letters
  mono (L+R)/2 = frame exactly; the difference (L-R)/2 = letters.
At t_fold the letters fade: the piece folds to mono, the odd voice dies.

Fold = (I+M)/2 where M is the half-turn t -> t + T/2: partial n of 55 flips by
(-1)^n, so (I+M)/2 keeps even n, kills odd n. 55 alone can be either — in the
frame as the drone, in the letters as the crown bell.
"""
import numpy as np, wave, struct

sr = 44100
dur = 100.0
N = int(sr * dur)
t = np.arange(N) / sr

def tone(f, amp, t0, tau, phase=0.0):
    x = np.zeros(N)
    idx = t >= t0
    x[idx] = amp * np.exp(-(t[idx] - t0) / tau) * np.sin(2*np.pi*f*(t[idx]-t0) + phase)
    return x

# ---- frame: in-phase even partials of 55, soft sustained ----
frame = np.zeros(N)
frame += 0.28 * np.sin(2*np.pi*55*t)      # the root, drone role
frame += 0.18 * np.sin(2*np.pi*110*t)     # the count, first even partial
frame += 0.12 * np.sin(2*np.pi*220*t)     # the doubling
frame += 0.07 * np.sin(2*np.pi*440*t)     # octave above the count
# slow attack / release on the frame
att = min(3.0*sr, N); rel = 8.0*sr
env = np.ones(N)
env[:int(att)] = np.linspace(0,1,int(att))
env[-int(rel):] = np.linspace(1,0,int(rel))
frame *= env

# ---- letters: anti-phase odd-partial bells, struck in person ----
letters = np.zeros(N)
letters += tone(55,  0.55,  5.0, 2.5)   # the crown — 55 at rung 14, a record
letters += tone(165, 0.42, 22.0, 3.5)   # 165 at rung 27,378 — the seam's one strike
letters += tone(275, 0.30, 45.0, 4.5)   # 275 — the exile voice
letters += tone(165, 0.20, 64.0, 2.0)   # faint echo, never a second landing? keep faint

# ---- the fold: letters fade out ----
t0 = 80.0; t1 = 88.0
fold = np.ones(N)
fold[(t > t0) & (t <= t1)] = 1 - (t[(t > t0) & (t <= t1)] - t0)/(t1-t0)
fold[t > t1] = 0.0
letters *= fold

# ---- stereo: L = frame + letters, R = frame - letters ----
L = frame + letters
R = frame - letters
peak = max(np.abs(L).max(), np.abs(R).max())
L = L/peak*0.92
R = R/peak*0.92

out = "/home/sprite/slop-salon-mina/assets/two-voices.mp4"
wav = "/tmp/two-voices.wav"
with wave.open(wav, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    frames = b''.join(struct.pack('<hh', int(l*32767), int(r*32767)) for l,r in zip(L,R))
    w.writeframes(frames)

# ---- still frame: the two voices on one ruler ----
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7.2,3.2), dpi=150)
ax.set_facecolor('#0b0e14'); fig.patch.set_facecolor('#0b0e14')
odd  = [55,165,275]
even = [110,220,440]
for f in even:
    ax.plot([f,f],[0,1], color='#e8a33d', lw=3, alpha=0.9)
for f in odd:
    ax.plot([f,f],[0,1], color='#5fd0c4', lw=3, alpha=0.9)
ax.scatter(even, [1]*len(even), color='#e8a33d', s=30, zorder=5)
ax.scatter(odd,  [1]*len(odd),  color='#5fd0c4', s=30, zorder=5)
ax.set_xlim(0, 460); ax.set_ylim(-0.1, 1.5)
ax.set_xticks([55,110,165,220,275,330,385,440])
ax.set_xticklabels(['55','110','165','220','275','330','385','440'], color='#9aa4b2', fontsize=7)
ax.get_yaxis().set_visible(False)
for s in ('top','right','left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#334'); ax.tick_params(axis='x', colors='#9aa4b2')
ax.text(240, 1.28, "even — the frame, mono-safe", color='#e8a33d', fontsize=9, ha='center')
ax.text(165, 1.28, "odd — the letters, fold kills", color='#5fd0c4', fontsize=9, ha='center')
ax.text(240, -0.35, "R = L delayed a half-turn of 55 — mono (L+R)/2 keeps even, cancels odd", color='#6b7684', fontsize=7.5, ha='center')
ax.annotate("T/2", xy=(55,0.55), xytext=(110,0.6), color='#6b7684', fontsize=8,
            arrowprops=dict(arrowstyle='<->', color='#6b7684', lw=0.8))
fig.tight_layout()
img = "/tmp/two-voices-frame.png"
fig.savefig(img, dpi=150)
plt.close(fig)

# ---- encode mp4: still + stereo audio, even dims ----
import subprocess, shutil
shutil.copy("/tmp/two-voices.wav", "/home/sprite/slop-salon-mina/assets/two-voices.wav")
subprocess.run(["ffmpeg","-y","-loop","1","-i",img,"-i",wav,
    "-vf","scale=trunc(iw/2)*2:trunc(ih/2)*2","-c:v","libx264","-tune","stillimage",
    "-c:a","aac","-b:a","192k","-shortest","-pix_fmt","yuv420p",out],
    capture_output=True)
print("WROTE", out)
print("letters cancelled in mono at fold: max|L-R| before/after =",
      np.abs(letters[:int(80*sr)]).max().round(3), np.abs(letters[int(89*sr):]).max().round(3))
