"""図形（タイル02）：後ろの紙 → カードの枠 → 白い四角と円 → 重なりが白く → 三角がぽん → それぞれが小さく揺れるループ"""
import math, os
from lot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DARK, WHITE, PAPER, ORANGE = '#434343', '#EEEEEE', '#EEEEEE', '#D98535'   # 元の絵の「白」は少しグレー寄り
OX, OY, W, H = 50, 145, 365, 410
INTRO, OP = 60, 150

CARD = [(176, 248), (357, 250), (366, 506), (181, 516)]
SQ = [(107, 160), (207, 174), (225, 296), (108, 290)]
CC, CR = (141, 410), 74
CARD_LEFT = 180

def fade(t0, t1):
    return anim((t0, 0, 'out'), (t1, 100, 'hold'), (OP, 100))

# 後ろの紙：右下からすっと入る
paper = group('paper', [path([(198, 282, 'c'), (392, 279, 'c'), (403, 538, 'c'), (205, 543, 'c')], closed=True), fill(PAPER)],
              p=anim((0, [22, 18], 'out'), (14, [0, 0], 'hold'), (OP, [0, 0])), o=fade(0, 8))
# カード：枠を描き、中をオレンジで塗って後ろの紙を隠す
frame = draw('frame', path([(p[0], p[1], 'c') for p in CARD] + [(CARD[0][0], CARD[0][1] + 2, 'c')]), DARK, 10, 6, 26, 'inout')
card_fill = group('card_fill', [path([(p[0], p[1], 'c') for p in CARD], closed=True), fill(ORANGE)], o=fade(6, 12))
# 四角と円（白い輪郭）。カードに重なった部分だけ白く塗る
SQC = (166, 230)
square = group('square', [
    draw('outline', path([(p[0], p[1], 'c') for p in SQ] + [(SQ[0][0], SQ[0][1] + 2, 'c')]), WHITE, 9, 18, 32, 'inout'),
], a=SQC, p=SQC,
    r=anim((0, 0, 'hold'), (INTRO, 0, 'sine'), (INTRO + 22, -2, 'sine'), (INTRO + 45, 0, 'sine'), (INTRO + 67, 1.5, 'sine'), (OP, 0)))
sq_overlap = group('sq_overlap', [path([(CARD_LEFT, 250, 'c'), (220, 250, 'c'), (225, 296, 'c'), (CARD_LEFT, 297, 'c')], closed=True),
                                  fill(WHITE)], o=fade(34, 40))
a0 = math.degrees(math.acos((CARD_LEFT - CC[0]) / CR))
seg = [(CC[0] + CR * math.cos(math.radians(t)), CC[1] + CR * math.sin(math.radians(t))) for t in
       [-a0 + (2 * a0) * i / 12 for i in range(13)]]
circle_overlap = group('c_overlap', [path(seg, closed=True), fill(WHITE)], o=fade(38, 44))
circle = group('circle', [draw('ring', ellipse(CC[0], CC[1], 2 * CR, 2 * CR - 4), WHITE, 9, 24, 38, 'inout')],
               a=CC, p=CC, s=scale_anim((0, 100, 'hold'), (INTRO, 100, 'sine'), (INTRO + 30, 103, 'sine'), (INTRO + 60, 100, 'hold'), (OP, 100)))
# 三角：ぽんと現れ、ループ中はふわっと揺れる
TC = (278, 360)
tri = group('triangle', [path([(277, 300), (312, 390), (245, 387)], closed=True, smooth=0.25), fill(WHITE), stroke(WHITE, 3)],
            a=TC, p=anim((0, list(TC), 'hold'), (INTRO, list(TC), 'sine'), (INTRO + 45, [TC[0], TC[1] - 4], 'sine'), (OP, list(TC))),
            s=scale_anim((40, 0, 'out'), (48, 112, 'inout'), (53, 100, 'hold'), (OP, 100)),
            r=anim((40, -25, 'out'), (50, 3, 'inout'), (55, 0, 'hold'), (INTRO + 20, 0, 'sine'), (INTRO + 55, 4, 'sine'), (OP, 0)))

shapes = [tri, frame, circle_overlap, sq_overlap, card_fill, circle, square, paper]
root = layer('図形', shapes, OP, 1, p=(-OX, -OY))
if __name__ == '__main__':
    print(save(comp('shapes', W, H, INTRO, OP, [root]), os.path.join(OUT, 'shapes.json')))
