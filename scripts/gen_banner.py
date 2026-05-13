#!/usr/bin/env python3
"""Generate animated particle ZASHARI banner — orange palette, chunky 7x9 font."""
import random
import math
import sys

# Chunky 7-wide x 9-tall pixel font.  '1' = lit cell, '0' = empty.
LETTERS = {
    'Z': [
        "1111111",
        "1111111",
        "0000011",
        "0000110",
        "0001100",
        "0011000",
        "0110000",
        "1111111",
        "1111111",
    ],
    'A': [
        "0011100",
        "0111110",
        "1100011",
        "1100011",
        "1111111",
        "1111111",
        "1100011",
        "1100011",
        "1100011",
    ],
    'S': [
        "0111110",
        "1111111",
        "1100000",
        "1100000",
        "0111110",
        "0000011",
        "0000011",
        "1111111",
        "1111110",
    ],
    'H': [
        "1100011",
        "1100011",
        "1100011",
        "1100011",
        "1111111",
        "1111111",
        "1100011",
        "1100011",
        "1100011",
    ],
    'R': [
        "1111110",
        "1100011",
        "1100011",
        "1100011",
        "1111110",
        "1110000",
        "1101100",
        "1100110",
        "1100011",
    ],
    'I': [
        "1111111",
        "1111111",
        "0011100",
        "0011100",
        "0011100",
        "0011100",
        "0011100",
        "1111111",
        "1111111",
    ],
}

WORD = "ZASHARI"
PX = 10              # pixel cell size
GAP = 14             # gap between letters (~1.4 cells)
LETTER_W = 7 * PX
LETTER_H = 9 * PX
PAD = 120            # canvas padding so dispersed particles have room

total_letters_w = len(WORD) * LETTER_W + (len(WORD) - 1) * GAP
svg_w = total_letters_w + 2 * PAD
svg_h = LETTER_H + 2 * PAD

random.seed(11)

# Orange palette — main + warm accents.  Weighted so the bright orange dominates.
PALETTE = (
    ['#ff8c42'] * 70 +   # primary warm orange
    ['#ffb86c'] * 18 +   # lighter peach
    ['#ff6b35'] * 8  +   # deeper red-orange highlight
    ['#fde68a'] * 4      # rare cream sparkle
)

particles = []
for li, ch in enumerate(WORD):
    bmp = LETTERS[ch]
    base_x = PAD + li * (LETTER_W + GAP)
    for r, row in enumerate(bmp):
        for c, val in enumerate(row):
            if val == "1":
                # Center of the lit cell
                cx = base_x + c * PX + PX / 2
                cy = PAD + r * PX + PX / 2
                # Multiple particles per cell to give the strokes weight
                # Main particle + 1-2 jitter satellites
                for k in range(2):
                    jx = random.uniform(-PX * 0.35, PX * 0.35)
                    jy = random.uniform(-PX * 0.35, PX * 0.35)
                    fx = cx + jx
                    fy = cy + jy
                    # Scattered offset: random direction + randomized distance
                    angle = random.uniform(0, 2 * math.pi)
                    dist = random.uniform(140, 320)
                    dx = math.cos(angle) * dist
                    dy = math.sin(angle) * dist
                    # Slight per-particle delay for organic feel
                    delay = round(random.uniform(0, 0.28), 3)
                    radius = round(random.uniform(2.2, 4.2), 2)
                    color = random.choice(PALETTE)
                    particles.append((fx, fy, dx, dy, delay, radius, color))

style = """
<defs>
  <style><![CDATA[
    .p {
      animation: cyc 6s cubic-bezier(0.45, 0, 0.2, 1) infinite;
      will-change: transform, opacity;
    }
    @keyframes cyc {
      0%   { transform: translate(var(--dx), var(--dy)); opacity: 0.15; }
      22%  { transform: translate(0, 0);                 opacity: 1;    }
      72%  { transform: translate(0, 0);                 opacity: 1;    }
      100% { transform: translate(var(--dx), var(--dy)); opacity: 0.15; }
    }
  ]]></style>
</defs>
"""

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" '
    f'width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="ZASHARI">',
    style,
]

for fx, fy, dx, dy, delay, r, color in particles:
    parts.append(
        f'<circle class="p" cx="{fx:.1f}" cy="{fy:.1f}" r="{r}" fill="{color}" '
        f'style="--dx:{dx:.1f}px;--dy:{dy:.1f}px;animation-delay:{delay}s" />'
    )

parts.append('</svg>')

print('\n'.join(parts))
print(f'\n<!-- particles: {len(particles)} | size: {svg_w}x{svg_h} -->', file=sys.stderr)
