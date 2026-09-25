"""糸巻き（タイル08）：糸巻きが描かれ → 白い糸が上から巻き付いて下へ抜ける → 回っているように糸がわずかに伸び縮みするループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE = '#434343', '#FFFFFF'
OX, OY, W, H = 135, 0, 260, 507
INTRO, OP = 72, 147

# ── 糸巻き本体（濃いグレー） ──
flange_top = path([(196, 192), (174, 172), (171, 151), (193, 137), (230, 131), (275, 135), (311, 148), (333, 168),
                   (335, 192), (318, 208)])
body_top = path([(196, 192), (218, 184), (250, 181), (283, 188), (302, 205)])
side_l = path([(195, 196), (193, 280), (192, 362)])
side_r = path([(305, 208), (308, 280), (309, 355)])
# 下のつば：本体の後ろに隠れる上側の弧は描かない
flange_bot = path([(193, 362), (176, 378), (185, 398), (225, 410), (290, 408), (330, 395), (336, 375), (310, 359)])
spool = [draw('flange_top', flange_top, DARK, 8, 0, 14), draw('body_top', body_top, DARK, 7, 8, 16),
         draw('side_l', side_l, DARK, 8, 12, 22), draw('side_r', side_r, DARK, 8, 14, 24),
         draw('flange_bot', flange_bot, DARK, 8, 18, 32)]

# ── 白い糸：上の端 → らせん（4.5回巻き）→ 下の端 ──
upper = [(247, 0), (230, 30), (190, 80), (160, 120), (148, 160), (150, 190)]
CX, RX, RY, Y0, Y1 = 242, 80, 17, 209, 343
helix, N = [], 96
for i in range(N + 1):
    t = math.pi - i / N * 9 * math.pi               # 左端から手前側へ巻き始め、右端で終わる
    rx = RX + 9 * math.sin(t * 0.37)                 # 巻きごとに幅と位置を少し揺らす（手巻きらしく）
    cx = CX + 6 * math.sin(t * 0.53)
    x = cx + rx * math.cos(t)
    y = Y0 + RY * math.sin(t) + (Y1 - Y0) * i / N - 0.13 * (x - CX)   # 右上がりに傾ける
    helix.append((x, y))
lower = [(345, 362), (362, 395), (370, 425), (350, 460), (300, 510)]
thread_pts = upper + helix + lower
cut1, cut2 = len(upper) - 1, len(upper) + len(helix) - 1
t_up, t_helix, t_low = split_path(thread_pts, [cut1, cut2])
thread = group('thread', [
    draw('lower', t_low, WHITE, 8.5, 66, 74, 'out'),
    draw('helix', t_helix, WHITE, 7.5, 34, 66, 'lin'),
    draw('upper', t_up, WHITE, 8.5, 26, 34, 'in'),
], a=(CX, 275), p=(CX, 275),
    # 巻いた糸が、糸巻きが回っているようにわずかに伸び縮み
    s=anim((0, [100, 100], 'hold'), (INTRO, [100, 100], 'sine'), (INTRO + 19, [97, 100], 'sine'),
           (INTRO + 38, [100, 100], 'sine'), (INTRO + 57, [97, 100], 'sine'), (OP, [100, 100])))

B = (258, 400)
root = layer('糸巻き', [thread] + spool, OP, 1, a=B,
             p=anim((0, [B[0] - OX, B[1] - OY, 0], 'hold'), (INTRO, [B[0] - OX, B[1] - OY, 0], 'sine'),
                    (INTRO + 37, [B[0] - OX, B[1] - OY - 2, 0], 'sine'), (OP, [B[0] - OX, B[1] - OY, 0])))
if __name__ == '__main__':
    print(save(comp('spool', W, H, INTRO, OP, [root]), os.path.join(OUT, 'spool.json')))
