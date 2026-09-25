"""固有技術：白い面がふわっと → 円柱が弾んで → 縦長の部品が降りて回転して止まる → 小部品が下から → 全体がごく小さく揺れるループ"""
import os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

DARK, WHITE, ORANGE = '#434343', '#FFFFFF', '#E78014'
OX, OY, W, H = 95, 90, 310, 320
INTRO, OP = 60, 135                        # 30fps：登場 2.0秒 / ループ 2.5秒
SW = 7

def pop_in(t0, dur=14):
    """ふわっと：透明度と大きさ 92%→100%"""
    return dict(o=anim((t0, 0, 'out'), (t0 + dur, 100, 'hold'), (OP, 100)),
                s=scale_anim((t0, 92, 'out'), (t0 + dur, 100, 'hold'), (OP, 100)))

# ── 白い面（矢印の三角・円柱の後ろの面・小部品の後ろの紙） ──
tri = path([(232, 254, 'c'), (313, 143, 'c'), (390, 224, 'c')], closed=True)
blob = path([(168, 242), (204, 249), (232, 268), (240, 300), (231, 334), (214, 352), (184, 358),
             (148, 353), (122, 333), (112, 302), (124, 263)], closed=True)
paper = path([(287, 308, 'c'), (321, 317, 'c'), (341, 336, 'c'), (336, 376, 'c'), (300, 368, 'c'), (280, 356, 'c')], closed=True)
whites = [
    group('tri', [tri, fill(WHITE), stroke(WHITE, 4)], a=(311, 207), p=(311, 207), **pop_in(0)),
    group('blob', [blob, fill(WHITE)], a=(176, 300), p=(176, 300), **pop_in(4)),
    group('paper', [paper, fill(WHITE), stroke(WHITE, 3)], a=(310, 342), p=(310, 342), **pop_in(8)),
]

# ── 円柱：底を支点に、弾むように出現 ──
cyl_body = path([(138, 282), (139, 306), (160, 326), (196, 332), (235, 322), (248, 302), (248, 282)])
cyl_top = ellipse(193, 280, 110, 46)
CP = (193, 332)
cylinder = group('cylinder', [
    group('top', [cyl_top, stroke(DARK, SW), fill(ORANGE)]),
    group('body', [cyl_body, stroke(DARK, SW)]),
    group('bodyfill', [path([(138, 282, 'c'), (139, 306), (160, 326), (196, 332), (235, 322), (248, 302), (248, 282, 'c')], closed=True), fill(ORANGE)]),
], a=CP, p=CP,
    s=scale_anim((12, 0, 'out'), (22, 110, 'inout'), (28, 95, 'inout'), (33, 100, 'hold'), (OP, 100)),
    o=anim((12, 0, 'out'), (16, 100, 'hold'), (OP, 100)))

# ── 縦長の部品：上から降りてきて、少し回転して止まる ──
cap = path([(297, 123), (325, 110), (353, 117), (354, 133), (342, 147), (337, 160), (331, 177), (312, 188),
            (285, 188), (283, 176), (295, 162), (297, 140)], closed=True)
body = path([(282, 190), (280, 240), (287, 262), (293, 293), (315, 302), (338, 300), (343, 267), (349, 200), (353, 137)])
body_fill = path([(282, 186), (280, 240), (287, 262), (293, 293), (315, 302), (338, 300), (343, 267), (349, 200),
                  (353, 128), (330, 120), (296, 130)], closed=True)
grooves = [path([(287, 202), (301, 204), (315, 202)]), path([(287, 213), (301, 216), (315, 217)]),
           path([(293, 228), (303, 231), (313, 233)]), path([(290, 243), (300, 246), (310, 250)])]
TP = (316, 300)
tall = group('tall', [
    group('cap', [cap, stroke(DARK, SW), fill(ORANGE)]),
    group('grooves', grooves + [stroke(DARK, 2.5)]),
    group('body', [body, stroke(DARK, SW)]),
    group('bodyfill', [body_fill, fill(ORANGE)]),
], a=TP,
    p=anim((24, [TP[0], TP[1] - 60], 'in'), (38, [TP[0], TP[1]], 'out'), (43, [TP[0], TP[1] - 4], 'inout'),
           (48, [TP[0], TP[1]], 'hold'), (OP, [TP[0], TP[1]])),
    r=anim((24, -10, 'inout'), (40, 4, 'inout'), (47, -1.5, 'inout'), (52, 0, 'hold'), (OP, 0)),
    o=anim((24, 0, 'out'), (29, 100, 'hold'), (OP, 100)))

# ── 小さな部品：下からスッと ──
small = path([(260, 385), (264, 370), (290, 351), (306, 351), (313, 367), (315, 384), (308, 397), (272, 391)], closed=True)
small_line = path([(262, 378), (282, 375), (313, 378)])
SP = (287, 390)
small_part = group('small', [
    group('line', [small_line, stroke(DARK, SW - 1)]),
    group('outline', [small, stroke(DARK, SW), fill(ORANGE)]),
], a=SP,
    p=anim((40, [SP[0], SP[1] + 34], 'out'), (54, [SP[0], SP[1]], 'hold'), (OP, [SP[0], SP[1]])),
    o=anim((40, 0, 'out'), (47, 100, 'hold'), (OP, 100)))

shapes = [small_part, tall, cylinder, whites[2], whites[0], whites[1]]

# ループ：全体を下中央を支点にごくわずかに揺らす（±0.6°、上下1px）
BP = (260, 360)
root = layer('固有技術', shapes, OP, 1, a=BP,
             p=anim((0, [BP[0] - OX, BP[1] - OY, 0], 'hold'), (INTRO, [BP[0] - OX, BP[1] - OY, 0], 'sine'),
                    (INTRO + 19, [BP[0] - OX, BP[1] - OY - 1, 0], 'sine'), (INTRO + 38, [BP[0] - OX, BP[1] - OY, 0], 'sine'),
                    (INTRO + 57, [BP[0] - OX, BP[1] - OY - 1, 0], 'sine'), (OP, [BP[0] - OX, BP[1] - OY, 0])),
             r=anim((0, 0, 'hold'), (INTRO, 0, 'sine'), (INTRO + 19, 0.6, 'sine'), (INTRO + 38, 0, 'sine'),
                    (INTRO + 57, -0.6, 'sine'), (OP, 0)))
print(save(comp('core-technology', W, H, INTRO, OP, [root]), os.path.join(OUT, 'core-technology.json')))
