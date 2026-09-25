"""匠の精神と品質：輪郭が描かれ → 頭の白い線が順に → 器が持ち上がって現れ → 震え → 静かな呼吸ループ"""
import math
import os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 85, 262, 310, 390          # 元タイル座標からの切り出し
INTRO, OP = 66, 141                        # 30fps：登場 2.2秒 / ループ 2.5秒

outline = path([(304, 506), (296, 470), (287, 440), (279, 424, 'c'), (290, 408), (300, 380), (300, 345),
                (291, 312), (272, 290), (240, 279), (208, 283), (186, 298), (175, 322), (178, 352),
                (193, 380), (222, 405, 'c'), (200, 420), (182, 437), (156, 468), (133, 505), (116, 545), (107, 581)])
arm = path([(183, 437), (184, 466), (194, 494), (214, 512), (240, 521), (252, 530), (257, 546)])

import random
random.seed(7)
def curl(cx, cy, r, turn0, turns=1.5, n=13):
    """不ぞろいな小さな渦（半径と縦横比を揺らして手描きらしく）。"""
    pts, sq = [], random.uniform(1.05, 1.3)
    for i in range(n):
        a = math.radians(turn0) + 2 * math.pi * turns * i / (n - 1)
        rr = r * random.uniform(0.75, 1.15)
        pts.append((cx - 4 + rr * 0.8 * math.cos(a), cy - 2 + rr * sq * 0.9 * math.sin(a)))
    return path(pts)

curls = [(207, 320, 14, 200), (222, 302, 13, 150), (241, 297, 13, 120), (257, 306, 12, 60),
         (250, 322, 12, 20), (232, 318, 13, 300), (217, 334, 11, 250), (210, 348, 9, 200)]

# ── 器（持ち上がって現れ、ループ中に軽く震える） ──
cup_fill = path([(259, 521, 'c'), (282, 510), (305, 507), (330, 510), (352, 527, 'c'), (346, 568),
                 (341, 604, 'c'), (308, 613), (274, 601, 'c'), (266, 560)], closed=True)
cup_side_l = path([(262, 530), (266, 562), (272, 596)])
cup_side_r = path([(350, 530), (345, 568), (341, 605)])
cup_bottom = path([(273, 600), (306, 611), (340, 604)])
nub = path([(324, 509, 'c'), (333, 499, 'c'), (342, 513, 'c'), (330, 515, 'c')], closed=True)
marks = [path([(267, 555), (283, 557), (298, 557)]), path([(268, 567), (280, 569), (292, 569)]),
         path([(272, 579), (280, 580), (288, 580)])]
saucer = path([(262, 582), (244, 596), (250, 618), (300, 632), (354, 628), (374, 614), (366, 598), (348, 586)])

PIV = (306, 612)   # 器の底：ここを支点に持ち上げ・震え
cup_items = [
    group('rim', [ellipse(305, 524, 94, 30), stroke(DARK, 6.5), fill(WHITE)]),
    group('lines', [cup_side_l, cup_side_r, cup_bottom, stroke(DARK, 7)]),
    group('nub', [nub, fill(DARK), stroke(DARK, 3)]),
] + [draw(f'mark{i}', m, DARK, 4, 50 + i * 3, 58 + i * 3) for i, m in enumerate(marks)] + [
    group('body', [cup_fill, fill(WHITE)]),
]
cup = group('cup', cup_items, a=PIV,
            p=anim((40, [PIV[0], PIV[1] + 12], 'out'), (52, [PIV[0], PIV[1] - 3]), (60, [PIV[0], PIV[1]], 'hold'), (OP, [PIV[0], PIV[1]])),
            s=scale_anim((40, 94, 'out'), (54, 100, 'hold'), (OP, 100)),
            o=anim((40, 0, 'out'), (48, 100, 'hold'), (OP, 100)),
            # 震え：ループの頭と中ほどで、ごく小さく2回
            r=anim((INTRO, 0, 'sine'), (INTRO + 4, 1.1, 'sine'), (INTRO + 8, -0.9, 'sine'), (INTRO + 12, 0.6, 'sine'),
                   (INTRO + 16, -0.3, 'sine'), (INTRO + 20, 0, 'hold'), (INTRO + 40, 0, 'sine'), (INTRO + 44, 0.7, 'sine'),
                   (INTRO + 48, -0.6, 'sine'), (INTRO + 52, 0.3, 'sine'), (INTRO + 56, 0, 'hold'), (OP, 0)))

shapes = (
    [draw(f'curl{i}', curl(*c), WHITE, 5.5, 30 + i * 3, 37 + i * 3, 'out') for i, c in enumerate(curls)] +
    [cup,
     draw('saucer', saucer, DARK, 6.5, 36, 54),
     draw('arm', arm, DARK, 7, 22, 40),
     draw('outline', outline, DARK, 7, 0, 36)]
)

# 全体：底を支点に、ループ中だけ静かに呼吸（約0.7%＝上端で2px程度）
BP = (300, 630)
root = layer('匠', shapes, OP, 1, p=(BP[0] - OX, BP[1] - OY), a=BP,
             s=anim((0, [100, 100, 100], 'hold'), (INTRO, [100, 100, 100], 'sine'),
                    (INTRO + 37, [100.5, 100.7, 100], 'sine'), (OP, [100, 100, 100])))
print(save(comp('craftsmanship', W, H, INTRO, OP, [root]), os.path.join(OUT, 'craftsmanship.json')))
