"""ロボットと目（タイル07）：ケーブルと箱 → アンテナ → 目までケーブル → 目 → 白い泡がぽこぽこ → 光が伸びる
→ 泡がふわふわ、光が脈打ち、ロボットがまばたきするループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 0, 90, 505, 295
INTRO, OP = 66, 156
EC = (297, 247)                          # 目の中心

# ── ロボット（箱・アンテナ・目） ──
cable_l = path([(0, 247), (30, 247), (57, 247)])
box = path([(57, 214, 'c'), (100, 206), (140, 208), (176, 215, 'c'), (183, 242), (190, 279, 'c'), (160, 288),
            (100, 288), (68, 285, 'c'), (58, 262), (57, 214, 'c')], smooth=0.8)
antenna = path([(112, 205), (112, 190), (112, 177)])
BLINK_T = INTRO + 50
robot_eyes = group('robot_eyes', [path([(150, 225), (150, 240)]), path([(160, 229), (160, 241)]), stroke(DARK, 5)],
                   a=(155, 234), p=(155, 234),
                   o=anim((22, 0, 'hold'), (23, 100, 'hold'), (OP, 100)),
                   s=anim((0, [100, 100], 'hold'), (BLINK_T, [100, 100], 'inout'), (BLINK_T + 3, [100, 10], 'inout'),
                          (BLINK_T + 6, [100, 100], 'hold'), (OP, [100, 100])))
ball = group('ball', [ellipse(112, 170, 13, 13), stroke(DARK, 5)], a=(112, 177), p=(112, 177),
             s=scale_anim((22, 0, 'out'), (27, 115, 'inout'), (30, 100, 'hold'), (OP, 100)))
robot = [robot_eyes, ball, draw('antenna', antenna, DARK, 5.5, 16, 22),
         draw('box', box, DARK, 9.5, 4, 20, 'inout'), draw('cable_l', cable_l, DARK, 6, 0, 6, 'in')]

# ── ケーブルと目 ──
cable_m = path([(191, 250), (220, 248), (248, 245)])
eye = path([(248, 240), (262, 214), (282, 202), (318, 204), (340, 230), (342, 262), (322, 283), (300, 291),
            (272, 281), (251, 262), (248, 240)])
pupils = group('pupils', [path([(307, 215), (307, 237)]), path([(318, 220), (318, 240)]), stroke(DARK, 5.5)],
               o=anim((38, 0, 'hold'), (39, 100, 'hold'), (OP, 100)))
eye_parts = [pupils, draw('eye', eye, DARK, 10, 26, 38, 'inout'), draw('cable_m', cable_m, DARK, 6, 20, 27)]

# ── 白い泡（中心, 横半径, 縦半径） ──
BLOBS = [((350, 227), 47, 54), ((397, 130), 35, 35), ((456, 220), 36, 39), ((382, 318), 40, 42),
         ((287, 161), 12, 11), ((299, 312), 6, 6), ((310, 352), 10, 10), ((403, 202), 5, 5), ((331, 296), 4, 4)]
blobs = []
for i, ((x, y), rx, ry) in enumerate(BLOBS):
    t = 36 + i * 2
    ph = INTRO + (i * 17) % 60
    blobs.append(group(f'blob{i}', [ellipse(x, y, 2 * rx, 2 * ry), fill(WHITE)], a=(x, y),
                       p=anim((0, [x, y], 'hold'), (ph, [x, y], 'sine'), (ph + 15, [x, y - 3], 'sine'), (ph + 30, [x, y], 'hold'), (OP, [x, y])),
                       s=scale_anim((t, 0, 'out'), (t + 6, 110, 'inout'), (t + 10, 100, 'hold'), (OP, 100))))

# ── 光（目から外へ伸びる線） ──
RAYS = [((320, 185), (342, 112)), ((347, 205), (470, 135)), ((357, 244), (482, 246)),
        ((360, 290), (465, 352)), ((320, 300), (357, 375))]
rays = [draw(f'ray{i}', path([a, b]), DARK, 5.5, 46 + i * 2, 54 + i * 2, 'out') for i, (a, b) in enumerate(RAYS)]
ray_group = group('rays', rays, a=EC, p=EC,
                  s=scale_anim((0, 100, 'hold'), (INTRO, 100, 'sine'), (INTRO + 45, 104, 'sine'), (OP, 100)))

root = layer('ロボットと目', eye_parts + robot + [ray_group] + blobs, OP, 1, p=(-OX, -OY))
if __name__ == '__main__':
    print(save(comp('signal', W, H, INTRO, OP, [root]), os.path.join(OUT, 'signal.json')))
