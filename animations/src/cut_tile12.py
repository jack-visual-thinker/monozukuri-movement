"""タイル12（円柱の中の世界）を、元の絵のまま3つの部品に切り分ける。
lid＝上のふた / walls＝側面の白い点線 / world＝下の世界。python3 animations/src/cut_tile12.py"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
im = Image.open(os.path.join(ROOT, 'images/hero/tile-12.png')).convert('RGB')
a = np.asarray(im).astype(int)
bg = np.array([51, 138, 117])                     # タイルの緑
d = np.abs(a - bg).sum(2)
H, W = d.shape
yy, xx = np.mgrid[0:H, 0:W]
m = ndimage.binary_dilation(d > 40, iterations=2) & (yy > 285) & (yy < 760) & (xx > 70) & (xx < 425)
white = ndimage.binary_dilation(a.min(2) > 190, iterations=2)
side = ((xx < 95) & (yy >= 480) & (yy < 720)) | ((xx > 385) & (yy >= 545) & (yy < 720))
walls = m & side & white & ~(a.max(2) < 110)      # 濃いグレー（下の世界の楕円）は含めない
lid = m & (yy < 548) & ~walls
world = m & (yy >= 548) & ~walls

for name, mask in (('lid', lid), ('walls', walls), ('world', world)):
    ys, xs = np.nonzero(mask)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    rgba = np.dstack([a.astype(np.uint8), (mask * 255).astype(np.uint8)])[y0:y1, x0:x1].copy()
    rgba[rgba[..., 3] == 0, :3] = 0
    Image.fromarray(rgba, 'RGBA').save(os.path.join(ROOT, f'images/hero/parts/tile-12-{name}.png'), optimize=True)
    # index.html に書く位置（タイルに対する%）
    print(f'{name}: left:{x0 / W * 100:.3f}%;top:{y0 / H * 100:.3f}%;width:{(x1 - x0) / W * 100:.3f}%;height:{(y1 - y0) / H * 100:.3f}%')
