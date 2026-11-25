"""퍼블로그 포토카드(70x90mm) 주문용 파일 만들기.

- 상품(재단) 크기 70x90mm, 작업 크기 74x94mm (사방 2mm 재단 여백)
- 300dpi PNG: 874x1110px
- 업체가 1~2mm 밀릴 수 있고 모서리를 5mm 둥글게 자르므로,
  그림은 재단선에서 4mm 안쪽(안전 영역)에만 놓는다.

python3 build_photocard.py  ->  photocard.html
node make_photocard.js       ->  photocard/front_01.png ... front_57.png, back.png, 미리보기
"""
import math
import random

from build_print import MEASURE, SYMBOLS, art, rules_html
from make_cards import build_cards

TRIM_W, TRIM_H = 70.0, 90.0   # 상품 크기 (mm)
BLEED = 2.0                   # 재단 여백 (mm)
SAFE = 4.0                    # 재단선에서 그림까지 최소 거리 (밀림 2mm + 둥근 모서리 여유)
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
RADII = [17.5, 14.5, 12.2, 11, 10, 9.3, 8.5, 8]  # 그림 자리 (반지름, mm): 크고 작게


def layout(rng):
    """그림 8개를 안전 영역 안에 겹치지 않게 무작위 배치. [(cx, cy, r, 회전각)] (작업 크기 기준 mm)"""
    x0, x1 = BLEED + SAFE, W - BLEED - SAFE
    y0, y1 = BLEED + SAFE, H - BLEED - SAFE
    for attempt in range(6000):
        scale = max(0.8, 1.0 - attempt * 0.0003)
        placed = []
        for r0 in RADII:
            r = r0 * scale
            for _ in range(300):
                x = rng.uniform(x0 + r, x1 - r)
                y = rng.uniform(y0 + r, y1 - r)
                if all(math.hypot(x - px, y - py) >= r + pr for px, py, pr, _ in placed):
                    placed.append((x, y, r, rng.uniform(0, 360)))
                    break
            else:
                break
        if len(placed) == len(RADII):
            return placed
    raise RuntimeError("배치 실패")


def front_html(no, names, rng):
    order = names[:]
    rng.shuffle(order)
    order.sort(key=lambda n: -MEASURE[n][0] // 25)  # 선명한 그림을 큰 자리에
    items = []
    for name, (x, y, r, rot) in zip(order, layout(rng)):
        size = 2 * r * MEASURE[name][1]  # 어느 방향으로 돌려도 원 안에 들어가는 크기
        items.append(
            f'<div class="it" style="left:{x - size / 2:.2f}mm;top:{y - size / 2:.2f}mm;'
            f'width:{size:.2f}mm;height:{size:.2f}mm;transform:rotate({rot:.0f}deg)">{art(name)}</div>'
        )
    return f'<div class="pc front" id="front_{no:02d}"><span class="no">{no}</span>{"".join(items)}</div>'


def main():
    rng = random.Random(20261109)
    cards = build_cards()
    front_list = [front_html(i + 1, c, rng) for i, c in enumerate(cards)]
    fronts = "".join(front_list)
    # 게임 방법 안내: '학교사랑'이 함께 들어 있는 실제 카드 두 장을 예시로
    ex = [i for i, c in enumerate(cards) if "학교사랑" in c][:2]
    with open("rules.html", "w", encoding="utf-8") as f:
        f.write(rules_html(front_list[ex[0]], front_list[ex[1]], cards[ex[0]], cards[ex[1]], ex[0] + 1, ex[1] + 1))
    back = '<div class="pc back" id="back"><img src="art/back_inner.png" alt="대블"></div>'
    css = f"""
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #ddd; display: flex; flex-wrap: wrap; gap: 6mm; padding: 6mm; }}
.pc {{ position: relative; width: {W}mm; height: {H}mm; overflow: hidden; background: #fff; flex: none; }}
.it {{ position: absolute; }}
.it img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
.no {{ position: absolute; right: {BLEED + SAFE}mm; bottom: {BLEED + SAFE - 2.5}mm; font: 2.2mm sans-serif; color: #c8c8c8; }}
.back {{ background: linear-gradient(#86d6fd 0 50%, #afdd45 50% 100%); }}
.back img {{ position: absolute; left: 0; top: {(H - W) / 2}mm; width: {W}mm; height: {W}mm; display: block; }}
/* 미리보기용 선: 파일로 저장할 때는 숨김 */
.guides .pc::after {{ content: ""; position: absolute; left: {BLEED}mm; top: {BLEED}mm; width: {TRIM_W}mm;
  height: {TRIM_H}mm; border: 0.25mm solid #e63946; border-radius: 5mm; }}
.guides .pc::before {{ content: ""; position: absolute; left: {BLEED + SAFE}mm; top: {BLEED + SAFE}mm;
  width: {TRIM_W - 2 * SAFE}mm; height: {TRIM_H - 2 * SAFE}mm; border: 0.2mm dashed #3a86ff; z-index: 1; }}
"""
    html = (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>대블 포토카드</title>'
        f"<style>{css}</style></head><body>{back}{fronts}</body></html>"
    )
    with open("photocard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"rules.html: 예시 카드 {ex[0] + 1}번·{ex[1] + 1}번 / photocard.html: 앞면 {len(cards)}장 + 뒷면 1장, 작업 크기 {W:.0f}x{H:.0f}mm")


if __name__ == "__main__":
    main()
