"""Lottie (bodymovin 5.x) を手書きで組み立てるための小さな部品集。"""
import json, math

EASE = {
    'inout': ((0.45, 0), (0.25, 1)),
    'out':   ((0.2, 0), (0.1, 1)),
    'in':    ((0.55, 0), (0.9, 0.6)),
    'sine':  ((0.37, 0), (0.63, 1)),
    'lin':   ((0, 0), (1, 1)),
}

def rgb(h):
    h = h.lstrip('#')
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [1]

def _v(x):
    return list(x) if isinstance(x, (list, tuple)) else [x]

def anim(*keys):
    """keys: (frame, value[, ease])。ease は次のキーへの補間。hold=True で段階的に切替。"""
    out = []
    for n, k in enumerate(keys):
        t, v = k[0], k[1]
        e = k[2] if len(k) > 2 else 'inout'
        d = {'t': t, 's': _v(v)}
        if n < len(keys) - 1:
            if e == 'hold':
                d['h'] = 1
            else:
                (ox, oy), (ix, iy) = EASE[e]
                d['o'] = {'x': [ox], 'y': [oy]}
                d['i'] = {'x': [ix], 'y': [iy]}
        out.append(d)
    return {'a': 1, 'k': out}

def st(v):
    return {'a': 0, 'k': v}

def prop(v):
    return v if isinstance(v, dict) else st(v)

def path(pts, closed=False, smooth=1.0):
    """pts: (x, y) または (x, y, 'c')。'c' はとがった角。Catmull-Rom で滑らかな曲線にする。"""
    n = len(pts)
    V, I, O = [], [], []
    for i, p in enumerate(pts):
        x, y = p[0], p[1]
        corner = len(p) > 2 and p[2] == 'c'
        if closed:
            a, b = pts[(i - 1) % n], pts[(i + 1) % n]
        else:
            a = pts[i - 1] if i > 0 else p
            b = pts[i + 1] if i < n - 1 else p
        tx, ty = (b[0] - a[0]) / 6 * smooth, (b[1] - a[1]) / 6 * smooth
        if not closed and (i == 0 or i == n - 1):
            tx, ty = tx * 2, ty * 2
        if corner:
            tx = ty = 0
        V.append([round(x, 1), round(y, 1)])
        I.append([round(-tx, 1), round(-ty, 1)])
        O.append([round(tx, 1), round(ty, 1)])
    return {'ty': 'sh', 'ks': st({'i': I, 'o': O, 'v': V, 'c': closed})}

def ellipse(cx, cy, w, h):
    return {'ty': 'el', 'p': st([cx, cy]), 's': st([w, h]), 'd': 1}

def stroke(color, w):
    return {'ty': 'st', 'c': st(rgb(color)), 'o': st(100), 'w': st(w), 'lc': 2, 'lj': 2, 'ml': 4}

def fill(color):
    return {'ty': 'fl', 'c': st(rgb(color)), 'o': st(100), 'r': 1}

def trim(end):
    return {'ty': 'tm', 's': st(0), 'e': prop(end), 'o': st(0), 'm': 1}

def tr(p=(0, 0), a=(0, 0), s=100, r=0, o=100):
    lst = lambda v: v if isinstance(v, dict) else st(list(v))
    return {'ty': 'tr', 'p': lst(p), 'a': lst(a),
            's': prop([s, s]) if not isinstance(s, dict) else s,
            'r': prop(r), 'o': prop(o), 'sk': st(0), 'sa': st(0)}

def group(name, items, **t):
    return {'ty': 'gr', 'nm': name, 'it': items + [tr(**t)]}

def draw(name, shape, color, w, t0, t1, ease='inout'):
    """線が描かれていくグループ（トリムパスの終点を 0→100%）。"""
    return group(name, [shape, trim(anim((t0, 0, ease), (t1, 100))), stroke(color, w)])

def scale_anim(*keys):
    return anim(*[(k[0], [k[1], k[1]]) + tuple(k[2:]) for k in keys])

def layer(name, shapes, op, ind, p=(0, 0), a=(0, 0), s=None, r=None, o=None):
    ks = {'o': prop(o if o is not None else 100), 'r': prop(r if r is not None else 0),
          'p': prop(list(p) + [0]) if not isinstance(p, dict) else p,
          'a': st(list(a) + [0]),
          's': s if isinstance(s, dict) else st([100, 100, 100])}
    return {'ddd': 0, 'ind': ind, 'ty': 4, 'nm': name, 'sr': 1, 'ks': ks, 'ao': 0,
            'shapes': shapes, 'ip': 0, 'op': op, 'st': 0, 'bm': 0}

def comp(name, w, h, intro, op, layers, fr=30):
    """intro＝登場（1回だけ）、intro〜op＝ループ区間。markers にも区間を記録する。"""
    return {'v': '5.12.2', 'fr': fr, 'ip': 0, 'op': op, 'w': w, 'h': h, 'nm': name, 'ddd': 0,
            'assets': [], 'layers': layers,
            'markers': [{'tm': 0, 'cm': 'intro', 'dr': intro}, {'tm': intro, 'cm': 'loop', 'dr': op - intro}]}

def save(data, fn):
    s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    open(fn, 'w').write(s)
    return len(s)
