"""縦糸と横糸（warp-weft-icon.png）を、線が描かれていくSVGにする。
python3 animations/src/weave_svg.py header → ヘッダーのロゴマーク / hero → ヒーローのタイル09
出力したSVGを index.html の該当箇所に貼り付ける。座標は元画像（2000×2000）基準。"""
import json, os, sys
# 元画像から読み取った縦糸3本の左右の輪郭（y, 左端x, 右端x）
B=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weave_bars.json')))
tops={'orange':(629,369),'green':(1009,385),'beige':(1374,378)}
bottoms={'orange':(606,1623),'green':(962,1685),'beige':(1350,1700)}
def f(v): return ('%.1f'%v).rstrip('0').rstrip('.')
def smooth(pts,closed=True):
  n=len(pts); d='M%s,%s'%(f(pts[0][0]),f(pts[0][1]))
  rng=range(n) if closed else range(n-1)
  for i in rng:
    p0=pts[(i-1)%n] if closed or i>0 else pts[i]; p1=pts[i]; p2=pts[(i+1)%n]
    p3=pts[(i+2)%n] if closed or i+2<n else p2
    c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
    d+=' C%s,%s %s,%s %s,%s'%tuple(f(v) for v in (*c1,*c2,*p2))
  return d+(' Z' if closed else '')
bars={}
for k,rows in B.items():
  rows=rows[::2]
  left=[(l,y) for y,l,r in rows]; right=[(r,y) for y,l,r in rows][::-1]
  outline=[tops[k]]+left+[bottoms[k]]+right
  center=[tops[k]]+[((l+r)/2,y) for y,l,r in rows]+[bottoms[k]]
  bars[k]=(smooth(outline),smooth(center[::3]+[center[-1]],closed=False))
line=("M1995,598 C1700,585 1300,568 1000,560 C850,556 750,549 650,550 C230,555 230,790 650,776 "
 "C850,775 1100,772 1350,788 C1660,808 1660,935 1350,944 C1150,955 950,958 650,947 "
 "C252,950 252,1175 650,1168 C900,1168 1100,1175 1300,1185 C1665,1210 1665,1400 1300,1402 C900,1400 500,1385 160,1386")
# 横糸が縦糸の「下」をくぐる交差（ここだけ縦糸をもう一度上に重ねる）
over={'orange':[776,1168],'green':[557,957,1400],'beige':[786,1186]}
xr={'orange':(540,700),'green':(900,1070),'beige':(1230,1420)}
colors={'orange':'#E78014','green':'#338A75','beige':'#D7C1A4'}

def bez(p,t):
  u=1-t; return tuple(u**3*p[0][i]+3*u*u*t*p[1][i]+3*u*t*t*p[2][i]+t**3*p[3][i] for i in (0,1))
def wedge(seg,keep,hw):
  pts=[bez(seg,i/120) for i in range(121)]; pts=[q for q in pts if keep(q[0])]
  top=[(x,y-hw(x)) for x,y in pts]; bot=[(x,y+hw(x)) for x,y in pts][::-1]
  return 'M'+' L'.join('%.0f,%.1f'%q for q in top+bot)+' Z'

def build(P, W, WIDEN, cls, viewbox, bar_colors, weft_d, taper=True, extra=''):
  cx={'orange':625,'green':1005,'beige':1365}
  xr={k:(cx[k]-120,cx[k]+120) for k in cx}
  defs=[]
  if taper:
    half=W/2+1
    right=wedge(((1995,598),(1700,585),(1300,568),(1000,560)),lambda x:x>=1490,lambda x:1+half*min(1,max(0,(2000-x)/500))**0.8)
    left=wedge(((1300,1402),(900,1400),(500,1385),(160,1386)),lambda x:x<=490,lambda x:1+half*min(1,max(0,(x-155)/325))**0.8)
    defs.append(f'''<mask id="{P}m-weft" maskUnits="userSpaceOnUse" x="0" y="0" width="2000" height="2000"><rect width="2000" height="2000" fill="#fff"/><rect x="1500" y="520" width="500" height="140" fill="#000"/><path d="{right}" fill="#fff"/><rect x="0" y="1320" width="480" height="130" fill="#000"/><path d="{left}" fill="#fff"/></mask>''')
  body=[];tops_=[]
  for k in ['orange','green','beige']:
    o,c=bars[k]
    tf=f'translate({cx[k]} 0) scale({WIDEN} 1) translate(-{cx[k]} 0)'
    defs.append(f'<mask id="{P}m-{k}" maskUnits="userSpaceOnUse" x="0" y="0" width="2000" height="2000"><path class="warp-reveal" d="{c}" transform="{tf}" pathLength="1" fill="none" stroke="#fff" stroke-width="140" stroke-linecap="round"/></mask>')
    defs.append(f'<clipPath id="{P}c-{k}">'+''.join(f'<rect x="{xr[k][0]}" y="{y-60}" width="{xr[k][1]-xr[k][0]}" height="120"/>' for y in over[k])+'</clipPath>')
    shape=f'<g mask="url(#{P}m-{k})"><path d="{o}" transform="{tf}" fill="{bar_colors[k]}"/></g>'
    body.append(shape); tops_.append(f'<g clip-path="url(#{P}c-{k})">{shape}</g>')
  n='\n        '
  mask=f' mask="url(#{P}m-weft)"' if taper else ''
  return f'''<svg class="{cls}" viewBox="{viewbox}"{extra} aria-hidden="true" focusable="false">
        <defs>{n}{n.join(defs)}
        </defs>{n}{n.join(body)}
        <path class="weft"{mask} d="{weft_d}" pathLength="1" fill="none" stroke="#434343" stroke-width="{W}" stroke-linecap="round"/>{n}{n.join(tops_)}
      </svg>'''

if __name__ == '__main__':
  which = sys.argv[1] if len(sys.argv) > 1 else 'header'
  if which == 'header':
    # ヘッダー用：小さく表示しても読めるよう線と縦糸を太らせ、余白を切り詰める。横糸の両端は細く抜く
    print(build('logo-', 64, 1.45, 'weave-anim logo-mark', '130 330 1880 1390', colors, line))
  else:
    # ヒーローのタイル09（元画像を約0.22倍した絵）：縦糸は白、横糸はタイルの端まで伸ばす
    white={k:'#FFFFFF' for k in colors}
    d='M2130,604 L1995,598'+line[len('M1995,598'):]+' L20,1387'
    print(build('hw-', 34, 1.3, 'hero-motion hero-weave', '147.6 -149.6 1855.6 2295.6', white, d, taper=False,
                extra=' preserveAspectRatio="none"'))
