"""인쇄용 카드 HTML 생성 (A4 한 장에 9cm 정사각형 카드 6장).

python3 build_print.py  ->  print.html
그 다음 node make_pdf.js  ->  dobble_cards.pdf
"""
import math
import random

import numpy as np
from PIL import Image

from make_cards import SYMBOLS, build_cards


def _measure(i):
    """(긴 변 화소 수, 그림 중심에서 가장 먼 색칠된 점까지 거리의 비율)"""
    im = Image.open(f"art/{i:02d}.png")
    w, h = im.size
    a = np.asarray(im)[..., 3] > 20
    ys, xs = np.nonzero(a)
    reach = np.sqrt((xs + 0.5 - w / 2) ** 2 + (ys + 0.5 - h / 2) ** 2).max()
    return max(w, h), max(w, h) / (2 * reach)


MEASURE = {n: _measure(i) for i, n in enumerate(SYMBOLS)}
PIXELS = {n: m[0] for n, m in MEASURE.items()}


def art(name):
    return f'<img src="art/{SYMBOLS.index(name):02d}.png" alt="{name}">'

CARD = 90.0      # 카드 한 변 (mm)
PAD = 3.0        # 테두리 안쪽 여백 (mm)
RADII = [21, 17.5, 14.5, 13, 12, 11, 10, 9.5]  # 그림 자리 (반지름, mm): 실제 도블처럼 크고 작게
# 아이들이 둘러앉아 하므로 실제 도블처럼 0~360도 어느 방향이든 돌린다.
# 그림은 어떻게 돌려도 자기 원(반지름 r) 밖으로 나가지 않는 크기로 넣는다.


def layout(rng):
    """그림 8개를 겹치지 않게 무작위 배치. [(cx, cy, r, 회전각)]"""
    lo, hi = PAD, CARD - PAD
    for attempt in range(4000):
        scale = max(0.8, 1.0 - attempt * 0.0004)
        placed = []
        ok = True
        for r0 in RADII:
            r = r0 * scale
            for _ in range(300):
                x = rng.uniform(lo + r, hi - r)
                y = rng.uniform(lo + r, hi - r)
                if all(math.hypot(x - px, y - py) >= r + pr for px, py, pr, _ in placed):
                    placed.append((x, y, r, rng.uniform(0, 360)))
                    break
            else:
                ok = False
                break
        if ok:
            return placed
    raise RuntimeError("배치 실패")


def card_html(no, names, rng):
    order = names[:]
    rng.shuffle(order)
    # 화소가 많은(선명한) 그림일수록 큰 자리에 놓아 확대해도 흐려지지 않게
    order.sort(key=lambda n: -PIXELS[n] // 25)
    items = []
    for name, (x, y, r, rot) in zip(order, layout(rng)):
        size = 2 * r * MEASURE[name][1]  # 돌려도 원 안에 들어가는 크기
        items.append(
            f'<div class="it" style="left:{x - size / 2:.2f}mm;top:{y - size / 2:.2f}mm;'
            f'width:{size:.2f}mm;height:{size:.2f}mm;transform:rotate({rot:.0f}deg)">'
            f"{art(name)}</div>"
        )
    return f'<div class="card"><span class="no">{no}</span>{"".join(items)}</div>'


def main():
    rng = random.Random(20261109)  # 개교기념일 11/9
    cards = build_cards()
    pages = []

    # 그림 도감 (따로 인쇄)
    cells = "".join(
        f'<div class="cell">{art(s)}<div class="nm">{s}</div></div>' for s in SYMBOLS
    )
    guide = (
        '<section class="page guide"><h1>대블 · 그림 57개</h1>'
        '<p>어떤 두 카드를 골라도 같은 그림이 꼭 하나 있어요. 먼저 찾아서 이름을 외치면 이겨요!</p>'
        f'<div class="grid">{cells}</div></section>'
    )

    # 양면 인쇄: 앞면 쪽 다음에 뒷면 쪽. 긴 쪽 넘김이면 좌우가 바뀌므로 뒷면은 칸을 좌우 반전
    back = '<div class="card back"><img src="art/back.webp" alt="대블"></div>'
    blank = '<div class="card blank"></div>'
    htmls = [card_html(i + 1, c, rng) for i, c in enumerate(cards)]
    for p in range(0, len(htmls), 6):
        front = htmls[p:p + 6]
        # 칸이 모자라면 빈 칸으로 채워 앞뒤 모두 3줄 배치를 유지 (위치가 어긋나지 않게)
        pad = [blank] * (6 - len(front))
        pages.append(f'<section class="page cards">{"".join(front + pad)}</section>')
        cells = [back] * len(front) + [blank] * (6 - len(front))
        mirrored = [cells[r * 2 + c] for r in range(3) for c in (1, 0)]
        pages.append(f'<section class="page cards">{"".join(mirrored)}</section>')

    css = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'WenQuanYi Zen Hei', 'Noto Sans KR', sans-serif; background: #fff; }}
.page {{ width: 210mm; height: 297mm; page-break-after: always; overflow: hidden; }}
.cards {{ display: grid; grid-template-columns: repeat(2, {CARD}mm); grid-auto-rows: {CARD}mm;
  gap: 0; justify-content: center; align-content: center; }}
.card {{ position: relative; width: {CARD}mm; height: {CARD}mm; outline: 0.25mm solid #888;
  background: #fff; }}
.back {{ outline: 0.15mm solid #666; overflow: hidden; }}
.back img {{ width: 100%; height: 100%; display: block; object-fit: cover; }}
.blank {{ outline: none; background: none; }}
.no {{ position: absolute; right: 2.2mm; bottom: 1.2mm; font-size: 2.2mm; color: #bbb; }}
.it {{ position: absolute; }}
.it img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
@font-face {{ font-family: Jua; src: url(fonts/Jua-Regular.ttf); }}
.guide {{ padding: 10mm 10mm; font-family: Jua, sans-serif; }}
.guide h1 {{ margin: 0 0 1.5mm; font-size: 11mm; text-align: center; color: #c1121f; font-weight: normal; }}
.guide p {{ margin: 0 0 5mm; font-size: 4.6mm; text-align: center; color: #444; }}
.grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 3.2mm 1mm; }}
.cell {{ text-align: center; }}
.cell img {{ width: 21mm; height: 21mm; object-fit: contain; }}
.nm {{ font-size: 5mm; line-height: 1.1; margin-top: 0.6mm; color: #222; }}
"""
    def doc(title, body):
        return (
            '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            f"<title>{title}</title><style>{css}</style></head><body>{body}</body></html>"
        )

    with open("print.html", "w", encoding="utf-8") as f:
        f.write(doc("대블 카드 (양면)", "".join(pages)))
    with open("rules.html", "w", encoding="utf-8") as f:
        # 예시: '학교사랑'이 함께 들어 있는 실제 카드 두 장
        ex = [i for i, c in enumerate(cards) if "학교사랑" in c][:2]
        f.write(rules_html(htmls[ex[0]], htmls[ex[1]], cards[ex[0]], cards[ex[1]], ex[0] + 1, ex[1] + 1))
    with open("guide.html", "w", encoding="utf-8") as f:
        f.write(doc("대블 그림 도감", guide))
    print(f"print.html: 카드 {len(cards)}장, 앞뒤 {len(pages)}쪽 / guide.html: 그림 도감 1쪽 / rules.html: 게임 방법 1쪽")


def rules_html(card_a, card_b, names_a, names_b, no_a, no_b):
    """게임 방법 안내 (A4 1쪽). 예시는 실제 카드 두 장."""
    same = (set(names_a) & set(names_b)).pop()
    games = [
        ("1", "같은 그림 찾기", "처음 하는 친구들 연습 놀이", [
            "카드 두 장을 앞면이 보이게 가운데에 놓아요.",
            "두 카드에 똑같이 있는 그림을 찾아 이름을 크게 외쳐요.",
            "맞힌 친구가 먼저 놓인 카드를 가져가요. 새 카드를 한 장 펼쳐 남은 카드와 비교해요.",
            "카드가 다 떨어지면 카드를 가장 많이 모은 친구가 이겨요!",
        ]),
        ("2", "높이높이 탑 쌓기", "카드를 많이 모으면 이겨요", [
            "모두 카드를 한 장씩 앞면이 보이게 내 앞에 놓아요. 남은 카드는 앞면이 보이게 가운데에 쌓아요.",
            "가운데 맨 위 카드와 <b>내 카드</b>에 같은 그림을 찾아 외쳐요.",
            "맞히면 가운데 카드를 가져와 내 카드 위에 올려요. 이제 그 카드가 내 카드예요.",
            "가운데 카드가 다 떨어지면 탑이 가장 높은 친구가 이겨요!",
        ]),
        ("3", "카드 빨리 버리기", "카드를 먼저 다 없애면 이겨요", [
            "카드 한 장을 앞면이 보이게 가운데에 놓고, 나머지는 모두 똑같이 나눠 가져요.",
            "내 카드 더미를 뒤집어 맨 위 카드만 보이게 내 앞에 놓아요.",
            "내 맨 위 카드와 가운데 카드에 같은 그림을 외치고, 내 카드를 가운데에 올려요.",
            "내 카드를 가장 먼저 다 버린 친구가 이겨요!",
        ]),
        ("4", "깜짝 선물 주기", "카드를 적게 가지면 이겨요", [
            "모두 카드를 한 장씩 앞면이 보이게 내 앞에 놓아요. 남은 카드는 가운데에 쌓아요.",
            "가운데 맨 위 카드와 <b>친구 카드</b>에 같은 그림을 찾아 외쳐요.",
            "맞히면 가운데 카드를 그 친구에게 선물해요. 친구 카드 위에 올려 줘요.",
            "가운데 카드가 다 떨어지면 카드가 가장 적은 친구가 이겨요!",
        ]),
    ]
    gl = "".join(
        f'<div class="game"><div class="gh"><span class="num">{n}</span>{t}<span class="sub">{sub}</span></div>'
        f'<ol>{"".join(f"<li>{x}</li>" for x in steps)}</ol></div>'
        for n, t, sub, steps in games
    )
    css = f"""
@page {{ size: A4; margin: 0; }}
@font-face {{ font-family: Jua; src: url(fonts/Jua-Regular.ttf); }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Jua, sans-serif; color: #2b2b2b; background: #fff; }}
.page {{ width: 210mm; height: 297mm; padding: 9mm 12mm; overflow: hidden; position: relative; }}
.top {{ display: flex; align-items: center; gap: 5mm; }}
.top img {{ width: 28mm; height: 28mm; border: 0.3mm solid #ddd; }}
h1 {{ margin: 0; font-size: 13mm; color: #c1121f; font-weight: normal; line-height: 1; }}
.lead {{ font-size: 5.2mm; margin-top: 2mm; line-height: 1.35; }}
.meta {{ display: flex; gap: 2.5mm; margin-top: 3mm; }}
.meta span {{ background: #fff3c4; border-radius: 3mm; padding: 1mm 3mm; font-size: 4.2mm; }}
.rule {{ margin-top: 3.5mm; background: #e7f6ff; border-radius: 4mm; padding: 3mm 5mm; display: flex; align-items: center; gap: 4mm; }}
.rule .txt {{ flex: 1; font-size: 4.8mm; line-height: 1.35; }}
.rule .txt b {{ color: #c1121f; font-weight: normal; font-size: 6mm; }}
.ex {{ display: flex; gap: 2mm; }}
.ex .wrap {{ width: 38mm; height: 38mm; overflow: hidden; background: #fff; border: 0.3mm solid #aaa; }}
.ex .card {{ position: relative; width: {CARD}mm; height: {CARD}mm; transform: scale(0.4222); transform-origin: 0 0; }}
.ex .no {{ display: none; }}
.it {{ position: absolute; }}
.it img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
.ex .it:has(img[alt="{same}"]) {{ border-radius: 50%; box-shadow: 0 0 0 1.6mm #ff2d55; }}
.games {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin-top: 3.5mm; }}
.game {{ border: 0.6mm solid #ffd23f; border-radius: 4mm; padding: 3mm 4mm; }}
.gh {{ font-size: 6mm; display: flex; align-items: baseline; gap: 2mm; flex-wrap: wrap; }}
.num {{ background: #c1121f; color: #fff; border-radius: 50%; width: 7.5mm; height: 7.5mm; display: inline-flex;
  align-items: center; justify-content: center; font-size: 5mm; align-self: center; }}
.sub {{ font-size: 3.8mm; color: #777; }}
ol {{ margin: 1.5mm 0 0; padding-left: 5mm; font-size: 4mm; line-height: 1.35; }}
li {{ margin-bottom: 1mm; }}
li b {{ color: #c1121f; font-weight: normal; }}
.tips {{ margin-top: 3.5mm; background: #f1fbe9; border-radius: 4mm; padding: 2.5mm 5mm; font-size: 4.1mm; line-height: 1.38; }}
.tips h2 {{ margin: 0 0 1mm; font-size: 5.5mm; font-weight: normal; color: #2e7d32; }}
.tips ul {{ margin: 0; padding-left: 5mm; }}
"""
    body = f"""<section class="page">
<div class="top"><img src="art/back.webp" alt="대블">
<div><h1>대블 게임 방법</h1>
<div class="lead">대흘초 그림 57개가 숨어 있는 카드 놀이예요.<br>같은 그림을 누가 먼저 찾을까요?</div>
<div class="meta"><span>👥 2~8명</span><span>⏱ 한 판 5분</span><span>🃏 카드 57장</span></div></div></div>
<div class="rule"><div class="ex"><div class="wrap">{card_a}</div><div class="wrap">{card_b}</div></div>
<div class="txt">어떤 카드 두 장을 골라도<br>똑같은 그림이 <b>딱 하나</b> 있어요!<br>
이 두 카드({no_a}번, {no_b}번)에는<br><b>{same}</b>이 똑같아요.<br>같은 그림을 찾으면 <b>이름을 외쳐요.</b></div></div>
<div class="games">{gl}</div>
<div class="tips"><h2>🌺 함께 지켜요</h2><ul>
<li>카드를 잡기 전에 그림 이름을 먼저 외쳐요.</li>\n<li>이름을 틀리게 외치면 그 카드는 못 가져가요. 그리고 다음 카드 한 장이 나올 때까지 쉬어요.</li>
<li>둘이 동시에 외치면 가위바위보로 정해요.</li>
<li>카드는 돌려 봐도 괜찮아요. 그림은 여러 방향으로 놓여 있어요.</li>
<li>이름이 생각나지 않으면 '그림 안내' 종이를 보고 함께 불러요.</li>
</ul></div>
</section>"""
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        f"<title>대블 게임 방법</title><style>{css}</style></head><body>{body}</body></html>"
    )


if __name__ == "__main__":
    main()
