"""歯車の太陽と芽（タイル04）：地面 → 芽が伸びて葉が開く → 太陽と歯車 → 光が点灯 → 歯車が回り、光が脈打ち、芽がそよぐループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 60, 20, 430, 440
INTRO, OP = 66, 156                      # ループ3秒で歯車が1歯分（45°）回る
SC = (268, 177)                          # 太陽の中心

# ── 太陽：白い円・歯車（歯8枚）・内側の輪・光 ──
def gear_pts(r_out=76, r_in=53, teeth=8):
    pts, step = [], 360 / teeth
    for k in range(teeth):
        a = -90 - step * 0.25 + k * step
        for da, r in ((0, r_in), (2, r_out), (step * 0.5 - 2, r_out), (step * 0.5, r_in)):
            t = math.radians(a + da)
            pts.append((SC[0] + r * math.cos(t), SC[1] + r * math.sin(t), 'c'))
    return pts
gear = group('gear', [
    draw('ring', ellipse(SC[0], SC[1], 72, 78), DARK, 9, 34, 46),
    draw('teeth', path(gear_pts(), closed=True), DARK, 8.5, 24, 42, 'inout'),
], a=SC, p=SC, r=anim((0, 0, 'hold'), (INTRO, 0, 'lin'), (OP, 45)))
disk = group('disk', [path([(268, 96), (318, 104), (345, 140), (349, 185), (340, 228), (300, 254), (255, 256),
                             (212, 240), (190, 205), (190, 150), (215, 112)], closed=True), fill(WHITE)],
             a=SC, p=SC, s=scale_anim((18, 0, 'out'), (28, 105, 'inout'), (33, 100, 'hold'), (OP, 100)))
rays = []
for i, ang in enumerate([-90, -45, 2, 45, 90, 135, 180, -128]):
    t = math.radians(ang)
    p0 = (SC[0] + 104 * math.cos(t), SC[1] + 104 * math.sin(t))
    p1 = (SC[0] + 130 * math.cos(t), SC[1] + 130 * math.sin(t))
    f = 42 + i * 2
    rays.append(group(f'ray{i}', [path([p0, p1]), stroke(WHITE, 7.5)], a=p0, p=p0,
                      s=scale_anim((f, 0, 'out'), (f + 4, 100, 'hold'), (OP, 100))))
# 光は太陽の中心を支点に、ループ中ゆっくり脈打つ
ray_group = group('rays', rays, a=SC, p=SC,
                  s=scale_anim((0, 100, 'hold'), (INTRO, 100, 'sine'), (INTRO + 45, 106, 'sine'), (OP, 100)))

# ── 芽と地面 ──
def leaf(base, tip, w):
    """付け根 base から先 tip へ伸びる、ふくらんだ葉（閉じた形）"""
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    nx, ny = -dy, dx
    L = math.hypot(nx, ny) or 1
    nx, ny = nx / L * w, ny / L * w
    m1 = (base[0] + dx * 0.45 + nx, base[1] + dy * 0.45 + ny)
    m2 = (base[0] + dx * 0.45 - nx, base[1] + dy * 0.45 - ny)
    return path([(base[0], base[1], 'c'), m1, tip, m2], closed=True, smooth=1.1)

ground = path([(62, 438), (150, 436), (250, 437), (330, 438), (420, 435), (488, 434)])
# （付け根x, 地面y, 茎の上y, 左の葉(先, 幅, 白塗り), 右の葉, 位相）
SPROUTS = [
    (105, 447, 398, ((68, 392), 11, False), ((136, 414), 9, False), 0),
    (231, 437, 358, ((168, 368), 17, False), ((266, 372), 10, False), 1),
    (322, 447, 390, ((292, 380), 10, True), ((366, 406), 12, True), 2),
    (431, 442, 372, ((396, 372), 14, False), ((470, 390), 12, False), 3),
]
sprouts = []
for n, (x, gy, ty, lf, rf, ph) in enumerate(SPROUTS):
    t0 = 8 + n * 4
    leaves = []
    for side, (tip, w, white) in (('l', lf), ('r', rf)):
        items = [leaf((x, ty), tip, w), stroke(DARK, 6)] + ([fill(WHITE)] if white else [])
        leaves.append(group('leaf' + side, items, a=(x, ty), p=(x, ty),
                            s=scale_anim((t0 + 10, 0, 'out'), (t0 + 16, 110, 'inout'), (t0 + 20, 100, 'hold'), (OP, 100))))
    stem = draw('stem', path([(x, gy), (x + 1, (gy + ty) / 2), (x, ty)]), DARK, 6.5, t0, t0 + 11, 'out')
    sway = 2.5 if ph % 2 == 0 else -2.5
    sprouts.append(group(f'sprout{n}', leaves + [stem], a=(x, gy), p=(x, gy),
                         r=anim((0, 0, 'hold'), (INTRO + ph * 5, 0, 'sine'), (INTRO + ph * 5 + 22, sway, 'sine'),
                                (INTRO + ph * 5 + 45, 0, 'sine'), (INTRO + ph * 5 + 67, -sway * 0.6, 'sine'),
                                (OP - 20 + ph * 5, 0, 'hold'), (OP, 0))))
shapes = [gear, disk, ray_group] + sprouts + [draw('ground', ground, DARK, 7, 0, 14, 'inout')]
root = layer('歯車の太陽と芽', shapes, OP, 1, p=(-OX, -OY))
if __name__ == '__main__':
    print(save(comp('sun-sprouts', W, H, INTRO, OP, [root]), os.path.join(OUT, 'sun-sprouts.json')))
