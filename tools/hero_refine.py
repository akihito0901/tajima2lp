# 2026-10-19 本人「ヒーローごちゃごちゃ、洗練させよう」
# 要素を減らす：リボン・明滅・黄色い丸帯・丸3つをやめ、
#   上＝小さな見出し1行＋「無料体験」＋細い1行、下＝「整えて、支える」＋施術名1行＋強みを1行の文字で。
# 旧LP（index.html）と LPパート2（tools/body.html・tools/hx.css）の両方に同じものを入れる
import re, sys
from pathlib import Path

NEW_HTML = '''<div class="hx-top">
        <p class="hx-kick">ご好評につき延長<i></i>10/31（土）まで</p>
        <h1 id="hx-title" class="hx-title"><span class="hx-free">無料体験</span><span class="sr-only">。身体の土台から整えるコアバランス整体（福岡市城南区 田島2丁目の整骨院）</span></h1>
        <p class="hx-line">セット施術 通常<s>8,800円</s>　新たに<b>30</b>名様限定</p>
      </div>
      <div class="hx-bottom">
        <p class="hx-sub">整えて、支える。</p>
        <p class="hx-name">コアバランス整体<span>×</span>ダイナフィット</p>
        <p class="hx-feat">国家資格・施術歴10年<i></i>寝たまま服の上から<i></i>駐車場4台</p>
      </div>'''

# 既存の .hx-* を上書きする（後ろに足すので、こちらが勝つ）
NEW_CSS = '''
/* ── ヒーロー（洗練版 2026-10-19）── 上書き */
.hx-veil{background:linear-gradient(180deg,rgba(255,251,240,.96) 0%,rgba(255,248,230,.9) 26%,rgba(255,246,222,0) 40%,rgba(30,22,8,0) 58%,rgba(30,22,8,.55) 74%,rgba(24,18,6,.9) 100%)}
.hx-top{top:min(14vw,64px);padding:0 22px;text-align:center}
.hx-kick{display:flex;align-items:center;justify-content:center;gap:10px;margin:0 0 6px;color:#8a5a00;font-size:min(3.6vw,15px);font-weight:700;letter-spacing:.14em}
.hx-kick i{width:1px;height:1em;background:currentColor;opacity:.5}
.hx-title{margin:0}
.hx-free{display:block;color:#2b200c;font-family:var(--font-mincho);font-size:min(19vw,84px);font-weight:700;letter-spacing:.08em;line-height:1.1;text-shadow:0 1px 0 rgba(255,255,255,.8)}
.hx-line{margin:8px 0 0;color:#3a2c14;font-size:min(3.7vw,15.5px);font-weight:700;letter-spacing:.04em}
.hx-line s{margin:0 .15em;color:#8a7a5f;text-decoration-color:#c2410c}
.hx-line b{margin:0 .1em;color:#c2410c;font-size:1.35em;font-family:var(--font-mincho)}
.hx-bottom{bottom:min(7vw,32px);padding:0 20px;text-align:center;color:#fff}
.hx-sub{margin:0 0 4px;font-family:var(--font-mincho);font-size:min(4.4vw,19px);font-weight:700;letter-spacing:.3em;color:#ffe9a8;text-shadow:0 2px 8px rgba(0,0,0,.45)}
.hx-name{margin:0 0 10px;font-family:var(--font-mincho);font-size:min(7.2vw,31px);font-weight:700;letter-spacing:.04em;line-height:1.3;text-shadow:0 3px 12px rgba(0,0,0,.5)}
.hx-name::after{content:none}
.hx-name span{margin:0 .25em;color:#ffd43b;font-size:.8em}
.hx-feat{display:flex;justify-content:center;align-items:center;gap:10px;flex-wrap:wrap;margin:0;font-size:min(3.3vw,13.5px);font-weight:700;letter-spacing:.04em;color:#fff3c8}
.hx-feat i{width:1px;height:1em;background:rgba(255,243,200,.6)}
'''


def swap(html):
    i = html.index('<div class="hx-top">'); j = html.index('</section>', i)
    return html[:i] + NEW_HTML + '\n    ' + html[j:]


lp = Path(r'C:\Users\sanji\AI\作業中\tajima2lp\index.html')
s = lp.read_text(encoding='utf-8')
s = swap(s)
if '洗練版 2026-10-19' not in s:
    k = s.index('</style>')
    s = s[:k] + NEW_CSS + s[k:]
lp.write_text(s, encoding='utf-8')

p2 = Path(r'C:\Users\sanji\AI\作業中\tajima2lp_パート2\tools')
b = (p2 / 'body.html').read_text(encoding='utf-8')
(p2 / 'body.html').write_text(swap(b), encoding='utf-8')
c = (p2 / 'hx.css').read_text(encoding='utf-8')
if '洗練版 2026-10-19' not in c:
    (p2 / 'hx.css').write_text(c + NEW_CSS, encoding='utf-8')
print('ok')
