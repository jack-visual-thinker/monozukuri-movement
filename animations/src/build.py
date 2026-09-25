"""3つのLottie JSONと preview.html をまとめて作り直す：python3 animations/src/build.py"""
import gzip, os, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')
# カードの色はヒーローのタイルと同じ色にしてある
ITEMS = [('craftsmanship', '匠の精神と品質', '#D3C2A7'),
         ('shapes', '図形', '#D98535'),
         ('tornado', '竜巻', '#FFFFFF'),
         ('sun-sprouts', '歯車の太陽と芽', '#D98535'),
         ('cycle', '循環', '#338A75'),
         ('skill-transfer', '人づくり・技能伝承', '#D3C2A7'),
         ('signal', 'ロボットと目', '#D3C2A7'),
         ('spool', '糸巻き', '#D3C2A7'),
         ('idea-gear', '人物と歯車と光', '#338A75'),
         ('core-technology', '固有技術', '#D98535')]

for script in ('craftsmanship.py', 'core_technology.py', 'skill_transfer.py', 'shapes.py', 'tornado.py',
               'sun_sprouts.py', 'cycle.py', 'signal.py', 'spool.py', 'idea_gear.py'):
    runpy.run_path(os.path.join(HERE, script), run_name='__main__')

tpl = open(os.path.join(HERE, 'preview_template.html'), encoding='utf-8').read()
cards, data = [], []
for fn, title, bg in ITEMS:
    s = open(os.path.join(OUT, fn + '.json'), encoding='utf-8').read()
    kb, gz = len(s.encode()) / 1024, len(gzip.compress(s.encode(), 9)) / 1024
    cards.append(f'''<figure class="card">
      <div class="stage" style="--bg: {bg}"><div data-lottie="data-{fn}" role="img" aria-label="{title}"></div></div>
      <figcaption><b>{title}</b><small>{fn}.json ・ {kb:.1f}KB（gzip {gz:.1f}KB）</small></figcaption>
    </figure>''')
    data.append(f'<script type="application/json" id="data-{fn}">{s}</script>')
html = tpl.replace('<!--CARDS-->', '\n    '.join(cards)).replace(
    '<!--DATA-->', '<!-- 直接ファイルを開いても動くよう、JSON（animations/*.json と同じ内容）を埋め込み -->\n' + '\n'.join(data))
open(os.path.join(OUT, 'preview.html'), 'w', encoding='utf-8').write(html)
print('preview.html', len(html))
