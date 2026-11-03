"""인쇄용 카드 HTML 생성 (A4 한 장에 9cm 정사각형 카드 6장).

python3 build_print.py  ->  print.html
그 다음 node make_pdf.js  ->  dobble_cards.pdf
"""
import math
import random

from make_cards import SYMBOLS, build_cards


def art(name):
    return f'<img src="art/{SYMBOLS.index(name):02d}.png" alt="{name}">'

CARD = 90.0      # 카드 한 변 (mm)
PAD = 3.0        # 테두리 안쪽 여백 (mm)
RADII = [21, 17.5, 14.5, 13, 12, 11, 10, 9.5]  # 그림 자리 (반지름, mm): 실제 도블처럼 크고 작게
FILL = 0.84     # 자리 안에서 그림이 차지하는 비율 (돌려도 넘치지 않게)
TILT = 35       # 회전 최대 각도: 1학년이 알아보기 쉽게 많이 뒤집지 않음


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
                    placed.append((x, y, r, rng.uniform(-TILT, TILT)))
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
    items = []
    for name, (x, y, r, rot) in zip(order, layout(rng)):
        size = 2 * r * FILL
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
        pages.append(f'<section class="page cards">{"".join(front)}</section>')
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
.blank {{ outline: none; }}
.no {{ position: absolute; right: 2.2mm; bottom: 1.2mm; font-size: 2.2mm; color: #bbb; }}
.it {{ position: absolute; }}
.it img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
.guide {{ padding: 12mm 12mm; }}
.guide h1 {{ margin: 0 0 2mm; font-size: 8mm; text-align: center; }}
.guide p {{ margin: 0 0 6mm; font-size: 4mm; text-align: center; color: #444; }}
.grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 2mm 1mm; }}
.cell {{ text-align: center; }}
.cell img {{ width: 18mm; height: 18mm; object-fit: contain; }}
.nm {{ font-size: 2.9mm; line-height: 1.2; }}
"""
    def doc(title, body):
        return (
            '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            f"<title>{title}</title><style>{css}</style></head><body>{body}</body></html>"
        )

    with open("print.html", "w", encoding="utf-8") as f:
        f.write(doc("대블 카드 (양면)", "".join(pages)))
    with open("guide.html", "w", encoding="utf-8") as f:
        f.write(doc("대블 그림 도감", guide))
    print(f"print.html: 카드 {len(cards)}장, 앞뒤 {len(pages)}쪽 / guide.html: 그림 도감 1쪽")

if __name__ == "__main__":
    main()
