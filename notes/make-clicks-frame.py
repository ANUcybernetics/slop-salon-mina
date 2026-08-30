from PIL import Image, ImageDraw
import numpy as np

W, H = 1280, 720
BG = (18, 15, 12)          # near-black, warm
CREAM = (232, 224, 208)
FAINT = (232, 224, 208, 90)
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im, 'RGBA')

cx = W // 2
rho = (0.076 / 204.0) ** (1.0 / 22.0)
mags = 204.0 * rho ** np.arange(23)
cents = mags * np.where(np.arange(23) % 2 == 0, 1.0, -1.0)

# the count's line — the centre the misses never reach
d.line([(cx, 170), (cx, 560)], fill=FAINT, width=2)

# the wait: 23 clicks, alternating sides, shrinking toward the line
y0 = 210
step = 14
for k, c in enumerate(cents):
    y = y0 + k * step
    m = abs(c)
    off = 300 * (m / 204.0) ** 0.8
    r = 2.5 + 9.0 * (m / 204.0) ** 0.6
    x = cx + (off if c > 0 else -off)
    d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM)

# the 24th — the landing, withheld: an empty ring on the line
y24 = y0 + 23 * step
d.ellipse([cx - 7, y24 - 7, cx + 7, y24 + 7], outline=(232, 224, 208, 200), width=2)

# a faint frame at the bottom: the count's name, tiny
d.text((cx - 16, 620), "110", fill=(232, 224, 208, 120))

im.save('/home/sprite/slop-salon-mina/assets/clicks-of-nothing-frame.png')
print('saved', im.size)
