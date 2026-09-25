"""人づくり・技能伝承：人物が線で描かれ → 中の円 → 大きな円が遅れて広がる → 周りの白い線が順に点灯 → 2つの円がゆっくり脈打つループ"""
import math, random
import os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 15, 100, 485, 350
INTRO, OP = 72, 147                         # 30fps：登場 2.4秒 / ループ 2.5秒
random.seed(3)

# ── 人物（黒い線） ──
body = path([(54, 432), (48, 392), (40, 352), (36, 336), (42, 326, 'c'), (60, 316), (74, 312), (84, 318),
             (88, 334), (90, 350, 'c'), (110, 318), (133, 289, 'c'), (130, 318), (126, 350, 'c'),
             (150, 310), (172, 283), (190, 265, 'c'), (188, 330), (187, 380), (186, 407)])
hook = path([(230, 328), (216, 338)])
hand = path([(214, 334), (215, 355), (211, 370), (197, 378), (188, 379)])
leg = path([(90, 388), (98, 404), (118, 413), (137, 408, 'c'), (139, 420), (140, 432)])
eyes = [ellipse(152, 357, 5, 6), ellipse(164, 358, 5, 6)]

# ── 円：小（人物の頭）・中・大。白い輪＋重なり部分を白く塗る ──
SMALL, MID, BIG = (160, 333, 55), (275, 295, 88), (373, 254, 107)

def lens(c1, c2, n=18):
    """2つの円が重なる部分（レンズ形）を折れ線で。"""
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    d = math.hypot(x2 - x1, y2 - y1)
    a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    mx, my = x1 + a * ux, y1 + a * uy
    p1, p2 = (mx - h * uy, my + h * ux), (mx + h * uy, my - h * ux)
    def arc(c, pa, pb, inside):
        cx, cy, r = c
        t1, t2 = math.atan2(pa[1] - cy, pa[0] - cx), math.atan2(pb[1] - cy, pb[0] - cx)
        mid_dir = math.atan2(inside[1] - cy, inside[0] - cx)
        # 内側（相手の円の中心方向）を通る向きの弧を選ぶ
        span = (t2 - t1) % (2 * math.pi)
        if abs(((t1 + span / 2) - mid_dir + math.pi) % (2 * math.pi) - math.pi) > math.pi / 2:
            span -= 2 * math.pi
        return [(cx + r * math.cos(t1 + span * i / n), cy + r * math.sin(t1 + span * i / n)) for i in range(n)]
    pts = arc(c1, p1, p2, (x2, y2)) + arc(c2, p2, p1, (x1, y1))
    pts[0] = pts[0] + ('c',)
    pts[n] = pts[n] + ('c',)
    return path(pts, closed=True, smooth=0.9)

def rays(c, angles, t0, gap=14):
    """円の周りの短い放射線。1本ずつパッと点灯する。"""
    cx, cy, r = c
    out = []
    for i, a in enumerate(angles):
        a = math.radians(a)
        l = random.uniform(11, 21)
        r0 = r + gap + random.uniform(-2, 3)
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        p1 = (cx + (r0 + l) * math.cos(a), cy + (r0 + l) * math.sin(a))
        t = t0 + i
        out.append(group(f'ray{i}', [path([p0, p1]), stroke(WHITE, random.uniform(6, 8))],
                         a=p0, p=p0, s=scale_anim((t, 40, 'out'), (t + 4, 100, 'hold'), (OP, 100)),
                         o=anim((t, 0, 'hold'), (t + 1, 100, 'hold'), (OP, 100))))
    return out

def circle(name, c, t0, t1, loop_keys, extra=()):
    cx, cy, r = c
    return group(name, list(extra) + [group('ring', [ellipse(cx, cy, 2 * r, 2 * r), stroke(WHITE, 8)])],
                 a=(cx, cy), p=(cx, cy),
                 s=scale_anim((t0, 0, 'out'), (t1 - 4, 104, 'inout'), (t1, 100, 'hold'), *loop_keys),
                 o=anim((t0, 0, 'out'), (t0 + 4, 100, 'hold'), (OP, 100)))

# ループ中の脈動：中の円と大きな円は位相をずらして、ゆっくり膨らんで戻る
mid_loop = [(INTRO, 100, 'sine'), (INTRO + 30, 103, 'sine'), (INTRO + 60, 100, 'hold'), (OP, 100)]
big_loop = [(INTRO, 100, 'hold'), (INTRO + 15, 100, 'sine'), (INTRO + 45, 102.5, 'sine'), (OP, 100)]
mid_rays = rays(MID, [-140, -128, -116, -104, 118, 104], 48)
big_rays = rays(BIG, [-122, -112, -102, -92, -82, -72, 60, 70, 80, 90, 100, 110, 122], 54)
small_rays = rays(SMALL, [-112, -97, 58, 72], 44)

mid = circle('mid', MID, 24, 40, mid_loop, mid_rays)
big = circle('big', BIG, 34, 52, big_loop,
             big_rays + [group('lens', [lens(MID, BIG), fill(WHITE)],
                               o=anim((40, 0, 'out'), (50, 100, 'hold'), (OP, 100)))])
SX, SY, SR = SMALL
small = group('head', small_rays + [
    group('inner', [ellipse(SX - 8, SY + 9, 84, 88), fill(WHITE)]),
    group('ring', [ellipse(SX, SY, 2 * SR, 2 * SR), stroke(WHITE, 8)]),
], a=(SX, SY), p=(SX, SY),
    s=scale_anim((4, 80, 'out'), (20, 100, 'hold'), (OP, 100)),
    o=anim((4, 0, 'out'), (14, 100, 'hold'), (OP, 100)))

person = [
    group('eyes', eyes + [fill(DARK)], o=anim((30, 0, 'hold'), (31, 100, 'hold'), (OP, 100))),
    draw('hook', hook, DARK, 8, 22, 26),
    draw('hand', hand, DARK, 8, 24, 32),
    draw('leg', leg, DARK, 8, 18, 28),
    draw('body', body, DARK, 8.5, 0, 26),
]
root = layer('人づくり・技能伝承', person + [small, mid, big], OP, 1, p=(-OX, -OY))
print(save(comp('skill-transfer', W, H, INTRO, OP, [root]), os.path.join(OUT, 'skill-transfer.json')))
