"""人物と歯車と光（タイル10）：人物が描かれ → 歯車の円 → 歯車 → 手の先に白い玉 → きらめき → 歯車が回り、きらめきが瞬くループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE, GREEN = '#434343', '#FFFFFF', '#338A75'
OX, OY, W, H = 88, 110, 365, 315
INTRO, OP = 66, 156                      # ループ3秒で歯車が1歯分（45°）回る

# ── 人物（黒い線） ──
body = path([(143, 345), (138, 330), (133, 300), (133, 265), (140, 232), (155, 212), (170, 203), (178, 212),
             (176, 232, 'c'), (200, 210), (225, 190), (247, 172, 'c'), (242, 200), (235, 235, 'c'), (262, 205),
             (290, 178), (322, 160, 'c'), (318, 200), (313, 250), (307, 322)])
wing = path([(132, 278), (100, 300, 'c'), (118, 312), (138, 326)])
hand = path([(310, 265), (335, 268), (350, 255), (357, 232), (361, 210)])
tick = path([(358, 222), (372, 225)])
eyes = [ellipse(281, 238, 5, 5), ellipse(288, 240, 5, 5)]
person = [
    group('eyes', eyes + [fill(DARK)], o=anim((34, 0, 'hold'), (35, 100, 'hold'), (OP, 100))),
    draw('tick', tick, DARK, 5, 32, 35), draw('hand', hand, DARK, 6.5, 26, 34, 'out'),
    draw('wing', wing, DARK, 6, 10, 20), draw('body', body, DARK, 7, 0, 30, 'inout'),
]

# ── 歯車（白い円の中）：ループ中ゆっくり回る ──
GC = (206, 358)
def gear_pts(r_out=47, r_in=36, teeth=8):
    pts, step = [], 360 / teeth
    for k in range(teeth):
        a = -90 - step * 0.25 + k * step
        for da, r in ((0, r_in), (2, r_out), (step * 0.5 - 2, r_out), (step * 0.5, r_in)):
            t = math.radians(a + da)
            pts.append((GC[0] + r * math.cos(t), GC[1] + r * math.sin(t), 'c'))
    return pts
gear = group('gear', [
    group('hole', [ellipse(GC[0], GC[1] + 2, 50, 55), stroke(DARK, 6.5), fill(WHITE)],
          a=GC, p=GC, s=scale_anim((34, 0, 'out'), (42, 100, 'hold'), (OP, 100))),
    draw('teeth', path(gear_pts(), closed=True), DARK, 7.5, 26, 42, 'inout'),
    group('body', [path(gear_pts(), closed=True), fill(GREEN)], o=anim((30, 0, 'out'), (40, 100, 'hold'), (OP, 100))),
], a=GC, p=GC, r=anim((0, 0, 'hold'), (INTRO, 0, 'lin'), (OP, 45)))
gear_disk = group('gear_disk', [ellipse(GC[0], GC[1], 112, 108), fill(WHITE)], a=GC, p=GC,
                  s=scale_anim((18, 0, 'out'), (27, 106, 'inout'), (32, 100, 'hold'), (OP, 100)))

# ── 白い玉ときらめき ──
OC = (392, 182)
orb = group('orb', [ellipse(OC[0], OC[1], 72, 72), fill(WHITE)], a=OC,
            p=anim((0, list(OC), 'hold'), (INTRO, list(OC), 'sine'), (INTRO + 45, [OC[0], OC[1] - 3], 'sine'), (OP, list(OC))),
            s=scale_anim((32, 0, 'out'), (40, 110, 'inout'), (45, 100, 'hold'), (OP, 100)))
SPARKS = [(415, 130, 7), (352, 157, 5), (435, 162, 4.5), (437, 202, 4), (417, 225, 5.5), (380, 237, 4.5)]
sparks = []
for i, (x, y, r) in enumerate(SPARKS):
    t = 42 + i * 2
    tw = INTRO + (i * 14) % 80            # ループ中、1つずつずらして瞬く
    sparks.append(group(f'spark{i}', [path([(x - r, y + r * 0.3), (x + r, y - r * 0.3)]), path([(x + r * 0.3, y - r), (x - r * 0.2, y + r)]),
                                      stroke(WHITE, 3)], a=(x, y), p=(x, y),
                        s=scale_anim((t, 0, 'out'), (t + 5, 100, 'hold'), (tw, 100, 'sine'), (tw + 8, 45, 'sine'),
                                     (tw + 16, 100, 'hold'), (OP, 100))))
root = layer('人物と歯車と光', person + sparks + [orb, gear, gear_disk], OP, 1, p=(-OX, -OY))
if __name__ == '__main__':
    print(save(comp('idea-gear', W, H, INTRO, OP, [root]), os.path.join(OUT, 'idea-gear.json')))
