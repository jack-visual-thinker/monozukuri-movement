"""循環（タイル05）：稜線 → 上向きの矢印 → 白い円がぽん → 循環の矢印が順に描かれ → 点線が落ちる → 矢印がゆっくり円を回るループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 240, 20, 600, 480
INTRO, OP = 72, 372                       # ループは10秒で1周（静かに回る）
CX, CY, RX, RY = 604, 164, 134, 129

def ring_pts(a0, a1, r_add=0, n=14):
    return [(CX + (RX + r_add) * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             CY + (RY + r_add) * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def head(tip, ang, l=24, spread=34):
    """矢じり：進む向き ang（度）の逆向きに、左右へ開いた2本の短い線"""
    back = math.radians(ang + 180)
    a, b = back + math.radians(spread), back - math.radians(spread)
    return path([(tip[0] + l * math.cos(a), tip[1] + l * math.sin(a)), (tip[0], tip[1], 'c'),
                 (tip[0] + l * math.cos(b), tip[1] + l * math.sin(b))])

def arc_arrow(name, a0, a1, t0, t1):
    pts = ring_pts(a0, a1, 1)
    tip = pts[-1]
    tangent = math.degrees(math.atan2(RY * math.cos(math.radians(a1)), -RX * math.sin(math.radians(a1))))
    return group(name, [
        group('head', [head(tip, tangent), stroke(DARK, 9)], o=anim((t1 - 1, 0, 'hold'), (t1, 100, 'hold'), (OP, 100))),
        draw('arc', path(pts), DARK, 10, t0, t1, 'inout'),
    ])

arrows = group('cycle', [
    arc_arrow('arc1', 224, 356, 34, 44),
    arc_arrow('arc2', 27, 113, 42, 51),
    arc_arrow('arc3', 134, 193, 49, 57),
], a=(CX, CY), p=(CX, CY),
    r=anim((0, 0, 'hold'), (INTRO, 0, 'lin'), (OP, 360)))

disk = group('disk', [ellipse(CX, CY, 2 * RX, 2 * RY), fill(WHITE)], a=(CX, CY), p=(CX, CY),
             s=scale_anim((24, 0, 'out'), (34, 106, 'inout'), (40, 100, 'hold'), (OP, 100)))

# ── 下の部分：稜線・地面のかすれ・上向きの矢印・点線の矢印 ──
ridge = path([(240, 432), (300, 410), (350, 388, 'c'), (400, 404), (460, 421), (545, 430), (562, 446),
              (620, 452), (700, 456), (822, 466)])
# 地面のかすれ：細かいジグザグと横線
import random
random.seed(5)
zig, x = [], 462
while x < 640:
    zig.append((x, 463 + (1 if len(zig) % 2 else -1) * random.uniform(2.5, 7)))
    x += random.uniform(4, 9)
ground = [path(zig, smooth=0.4),
          path([(470, 472), (540, 474), (600, 478), (690, 478)]),
          path([(560, 484), (620, 486), (700, 482)])]
rise = path([(415, 386), (450, 380), (480, 360), (500, 318)])
rise_head = head((500, 316), -70, 18, 34)
# 点線：まっすぐ落ちてから右へ曲がる
dots = [ellipse(665 + 46 * (i / 6) ** 2, 306 + 80 * i / 6, 6, 7) for i in range(7)]
tri = path([(722, 392, 'c'), (746, 404, 'c'), (724, 410, 'c')], closed=True)

lower = [
    group('tri', [tri, stroke(DARK, 3.5)], a=(730, 402), p=(730, 402),
          s=scale_anim((64, 0, 'out'), (69, 100, 'hold'), (OP, 100))),
] + [group(f'dot{i}', [d, fill(DARK)], o=anim((56 + i * 1.5, 0, 'hold'), (57 + i * 1.5, 100, 'hold'), (OP, 100)))
     for i, d in enumerate(dots)] + [
    group('rise_head', [rise_head, stroke(DARK, 7.5)], o=anim((27, 0, 'hold'), (28, 100, 'hold'), (OP, 100))),
    draw('rise', rise, DARK, 8, 18, 28, 'inout'),
] + [draw(f'ground{i}', g, DARK, 3.5, 8 + i * 3, 20 + i * 3, 'out') for i, g in enumerate(ground)] + [
    draw('ridge', ridge, DARK, 7.5, 0, 20, 'inout'),
]
root = layer('循環', [arrows, disk] + lower, OP, 1, p=(-OX, -OY))
if __name__ == '__main__':
    print(save(comp('cycle', W, H, INTRO, OP, [root]), os.path.join(OUT, 'cycle.json')))
