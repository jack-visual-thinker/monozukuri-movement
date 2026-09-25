"""ヒーローのタイルから動かすイラストを消した「無地のタイル」を作る（周りの地の色で自然に埋める）。
python3 animations/src/make_blanks.py 02 03 04 ..."""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
BG = {'02': (217, 133, 53), '04': (217, 133, 53), '05': (51, 138, 117), '07': (211, 194, 167),
      '08': (211, 194, 167), '10': (51, 138, 117), '12': (51, 138, 117)}
ONLY_DARK = {'03'}      # 竜巻：後ろの白いV字は残し、濃いグレーの渦だけ消す

def fill_v(a, m, out):
    """竜巻の後ろの白いV字：各行の左右の縁の位置を読み取り、線に隠れて読めない行は上下から補間する。
    消した所を「縁の内側は白・外側は緑」で塗り分ける（見えている縁は元の手描きのまま）"""
    H, W, _ = a.shape
    green = np.array([51, 137, 117], np.uint8); white = np.array([255, 255, 255], np.uint8)
    is_w = a.min(2) > 200
    run = 6                                           # 白が6px続いたら V の内側とみなす（紙のざらつき対策）
    ys, left, right = [], [], []
    for y in range(H):
        row = is_w[y]
        ok = np.convolve(row.astype(int), np.ones(run, int), 'valid') == run
        idx = np.nonzero(ok[20:W - 20 - run])[0] + 20
        if len(idx) == 0:
            continue
        xl, xr = idx.min(), idx.max() + run - 1
        # 縁の周りが消す範囲に入っていたら、その行の読み取りは信用しない
        if m[y, max(xl - 3, 0):xl + 3].any() or m[y, xr - 2:min(xr + 4, W)].any():
            continue
        ys.append(y); left.append(xl); right.append(xr)
    yy = np.arange(H)
    xl = np.interp(yy, ys, left); xr = np.interp(yy, ys, right)
    X = np.arange(W)[None, :]
    inside = (X >= xl[:, None]) & (X <= xr[:, None])
    fillc = np.where(inside[..., None], white, green)
    out = out.copy(); out[m] = fillc[m]
    return out

for n in sys.argv[1:]:
    im = Image.open(os.path.join(ROOT, f'images/hero/tile-{n}.png')).convert('RGB')
    a = np.asarray(im).astype(int)
    H, W, _ = a.shape
    yy, xx = np.mgrid[0:H, 0:W]
    if n in ONLY_DARK:
        # 濃いグレーの線と、その周りの淡いグレーのにじみ（彩度が低く、白ほど明るくない）
        core = (a.max(2) < 150) & ((a.max(2) - a.min(2)) < 40)
        m = (a.max(2) < 236) & ((a.max(2) - a.min(2)) < 30) & ndimage.binary_dilation(core, iterations=4)
        m = ndimage.binary_dilation(m, iterations=1)
    else:
        m = np.abs(a - np.array(BG[n])).sum(2) > 40
    m = ndimage.binary_dilation(m, iterations=2)
    R = 34   # 角の丸みと、外周の縁取りは触らない
    corner = ((xx < R) | (xx > W - 1 - R)) & ((yy < R) | (yy > H - 1 - R))
    border = (xx < 4) | (xx > W - 5) | (yy < 4) | (yy > H - 5)
    inner = m & ~corner & ~border
    # 外周の縁取りは基本的に残すが、内側でイラストが続いている所（線がタイルの端まで伸びている所）は外周も消す
    cy, cx = np.clip(yy, 4, H - 5), np.clip(xx, 4, W - 5)
    m = inner | (border & ~corner & inner[cy, cx])
    _, (iy, ix) = ndimage.distance_transform_edt(m, return_indices=True)
    out = a[iy, ix].astype(np.uint8)
    if n in ONLY_DARK:
        out = fill_v(a, m, out)
    Image.fromarray(out, 'RGB').save(os.path.join(ROOT, f'images/hero/tile-{n}-blank.png'), optimize=True)
    print(n, 'removed px:', int(m.sum()))
