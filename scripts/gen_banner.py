#!/usr/bin/env python3
"""Generate animated particle ZASHARI banner.

Design:
  - chunky 7x9 letter font
  - each lit cell is rendered as a 2x2 sub-grid of identically-sized
    particles, so when formed the text is a tidy high-resolution dot
    matrix (no jittered messiness)
  - particles scatter to random offsets when dispersed, then re-form
    on a 6s loop with a 3s hold in the formed state
"""
import random
import math
import sys

# 7-wide x 9-tall chunky pixel font.  '1' = lit cell.
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
PX = 6                   # cell size (smaller -> tighter letters)
SUB = 2                  # 2x2 sub-grid per cell -> 4 dots per lit cell
GAP = 8                  # gap between letters
LETTER_W = 7 * PX
LETTER_H = 9 * PX
PAD = 90                 # canvas padding for scattered particles
RADIUS = 1.2             # uniform dot radius

total_letters_w = len(WORD) * LETTER_W + (len(WORD) - 1) * GAP
svg_w = total_letters_w + 2 * PAD
svg_h = LETTER_H + 2 * PAD

random.seed(17)

# Even sub-grid positions inside a PX-sized cell, anchored at cell top-left.
sub_step = PX / SUB
sub_offsets = [
    (sub_step * (s + 0.5), sub_step * (t + 0.5))
    for s in range(SUB) for t in range(SUB)
]

# Two colors only - mostly primary, sparse brighter highlight - sizes stay uniform.
PRIMARY = "#ff8c42"
HIGHLIGHT = "#ffb86c"

particles = []
for li, ch in enumerate(WORD):
    bmp = LETTERS[ch]
    base_x = PAD + li * (LETTER_W + GAP)
    for r, row in enumerate(bmp):
        for c, val in enumerate(row):
            if val == "1":
                cell_x = base_x + c * PX
                cell_y = PAD + r * PX
                for (ox, oy) in sub_offsets:
                    fx = cell_x + ox
                    fy = cell_y + oy
                    angle = random.uniform(0, 2 * math.pi)
                    dist = random.uniform(110, 240)
                    dx = math.cos(angle) * dist
                    dy = math.sin(angle) * dist
                    delay = round(random.uniform(0, 0.22), 3)
                    color = HIGHLIGHT if random.random() < 0.12 else PRIMARY
                    particles.append((fx, fy, dx, dy, delay, color))

style = """
<defs>
  <style><![CDATA[
    .p {
      animation: cyc 6s cubic-bezier(0.45, 0, 0.2, 1) infinite;
      will-change: transform, opacity;
    }
    @keyframes cyc {
      0%   { transform: translate(var(--dx), var(--dy)); opacity: 0.12; }
      22%  { transform: translate(0, 0);                 opacity: 1;    }
      72%  { transform: translate(0, 0);                 opacity: 1;    }
      100% { transform: translate(var(--dx), var(--dy)); opacity: 0.12; }
    }
  ]]></style>
</defs>
"""

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" '
    f'width="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-label="ZASHARI">',
    style,
]

for fx, fy, dx, dy, delay, color in particles:
    parts.append(
        f'<circle class="p" cx="{fx:.2f}" cy="{fy:.2f}" r="{RADIUS}" fill="{color}" '
        f'style="--dx:{dx:.1f}px;--dy:{dy:.1f}px;animation-delay:{delay}s" />'
    )

parts.append('</svg>')

print('\n'.join(parts))
print(f'\n<!-- particles: {len(particles)} | size: {svg_w}x{svg_h} -->', file=sys.stderr)
