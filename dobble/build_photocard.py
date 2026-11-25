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


GAMES = [
    ("1", "같은 그림 찾기", "처음 하는 친구 연습 놀이", [
        "카드 두 장을 앞면이 보이게 가운데에 놓아요.",
        "두 카드에 똑같이 있는 그림을 찾아 이름을 외쳐요.",
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
        "카드 한 장을 앞면이 보이게 가운데에 놓고, 나머지는 모두 골고루 나눠 가져요.",
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

GUIDE_PER_CARD = 15  # 3칸 x 5줄
N_GUIDE = math.ceil(len(SYMBOLS) / GUIDE_PER_CARD)
N_RULES = 7


def info_card(cid, label, body, cls=""):
    return (
        f'<div class="pc info {cls}" id="{cid}"><div class="safe">'
        f'<div class="tag">{label}</div>{body}</div></div>'
    )


def guide_cards():
    out = []
    for k in range(N_GUIDE):
        names = SYMBOLS[k * GUIDE_PER_CARD:(k + 1) * GUIDE_PER_CARD]
        cells = "".join(f'<div class="gc">{art(n)}<div class="gn">{n}</div></div>' for n in names)
        out.append(info_card(f"guide_{k + 1}", f"그림 안내 {k + 1}/{N_GUIDE}",
                             f'<div class="ggrid">{cells}</div>', "guide"))
    return out


def rules_cards(ex_a, ex_b, no_a, no_b, same):
    def game(n, t, sub, steps):
        return (f'<div class="game"><div class="gh"><span class="num">{n}</span>{t}</div>'
                f'<div class="sub">{sub}</div><ol>{"".join(f"<li>{s}</li>" for s in steps)}</ol></div>')

    total = len(SYMBOLS)
    r = []
    r.append(f"""<div class="logo"><img src="art/back_inner.png" alt="대블"></div>
<h1>대블 설명서</h1>
<p class="lead">대흘초 그림 {total}개가 숨어 있는 카드 놀이예요. 같은 그림을 누가 먼저 찾을까요?</p>
<div class="meta"><span>👥 2~8명</span><span>⏱ 한 판 5분</span></div>
<div class="box"><b>들어 있는 것</b><br>그림 카드 {total}장<br>그림 안내 카드 {N_GUIDE}장<br>설명서 카드 {N_RULES}장</div>""")
    r.append(f"""<style>.ex .it:has(img[alt="{same}"]) {{ border-radius: 50%; box-shadow: 0 0 0 1.6mm #ff2d55; }}</style>
<h2>딱 하나만 같아요!</h2>
<p class="big">어떤 그림 카드 두 장을 골라도 똑같은 그림이 <b>딱 하나</b> 있어요.</p>
<div class="ex"><div class="wrap">{ex_a}</div><div class="wrap">{ex_b}</div></div>
<p class="big">{no_a}번, {no_b}번 카드에는 <b>{same}</b>이 똑같아요.<br>같은 그림을 찾으면 <b>이름을 외쳐요!</b></p>""")
    for g in GAMES:  # 놀이 하나에 카드 한 장
        r.append(game(*g))
    r.append("""<h2>🌺 함께 지켜요</h2><ul class="tips">
<li>카드를 잡기 전에 그림 이름을 먼저 외쳐요.</li>
<li>이름을 틀리게 외치면 그 카드는 못 가져가요. 그리고 다음 카드 한 장이 나올 때까지 쉬어요.</li>
<li>둘이 동시에 외치면 가위바위보로 정해요.</li>
<li>카드는 돌려 봐도 괜찮아요. 그림은 여러 방향으로 놓여 있어요.</li>
<li>이름이 생각나지 않으면 그림 안내 카드를 보고 함께 불러요.</li>
</ul><div class="bye">다 놀고 나면 카드를 모두 모아 상자에 넣어 주세요. 고마워요!</div>""")
    return [info_card(f"rules_{i + 1}", f"설명서 {i + 1}/{N_RULES}", body, "rules") for i, body in enumerate(r)]


def main():
    rng = random.Random(20261109)
    cards = build_cards()
    front_list = [front_html(i + 1, c, rng) for i, c in enumerate(cards)]
    fronts = "".join(front_list)
    # 게임 방법 안내: '학교사랑'이 함께 들어 있는 실제 카드 두 장을 예시로
    ex = [i for i, c in enumerate(cards) if "학교사랑" in c][:2]
    with open("rules.html", "w", encoding="utf-8") as f:
        f.write(rules_html(front_list[ex[0]], front_list[ex[1]], cards[ex[0]], cards[ex[1]], ex[0] + 1, ex[1] + 1))
    same = (set(cards[ex[0]]) & set(cards[ex[1]])).pop()
    def as_example(h):  # 예시 카드는 id가 겹치지 않게
        return h.replace('id="front_', 'id="ex_')

    infos = rules_cards(as_example(front_list[ex[0]]), as_example(front_list[ex[1]]), ex[0] + 1, ex[1] + 1, same) + guide_cards()
    infos_html = "".join(infos)
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
@font-face {{ font-family: Jua; src: url(fonts/Jua-Regular.ttf); }}
.info {{ font-family: Jua, sans-serif; color: #2b2b2b; background: #fffdf3; word-break: keep-all; }}
.safe {{ position: absolute; left: {BLEED + SAFE}mm; top: {BLEED + SAFE}mm; width: {TRIM_W - 2 * SAFE}mm;
  height: {TRIM_H - 2 * SAFE}mm; display: flex; flex-direction: column; }}
.tag {{ align-self: flex-start; background: #c1121f; color: #fff; border-radius: 2mm; padding: 0.5mm 2.2mm; font-size: 3mm; }}
.ggrid {{ flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(5, 1fr); gap: 0.8mm; margin-top: 1.5mm; }}
.gc {{ display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; border-radius: 2mm; }}
.gc img {{ width: 11mm; height: 9.5mm; object-fit: contain; }}
.gn {{ font-size: 3.3mm; line-height: 1.1; margin-top: 0.4mm; text-align: center; }}
.rules .logo img {{ width: 22mm; display: block; margin: 1mm auto 0; border-radius: 2mm; }}
.rules h1 {{ font-size: 8.5mm; color: #c1121f; text-align: center; margin: 1.5mm 0 1mm; font-weight: normal; }}
.rules h2 {{ font-size: 6mm; color: #c1121f; margin: 2mm 0 1.5mm; font-weight: normal; }}
.rules .lead {{ font-size: 3.6mm; text-align: center; line-height: 1.35; margin: 0 0 1.5mm; }}
.rules .meta {{ display: flex; justify-content: center; gap: 2mm; }}
.rules .meta span {{ background: #fff3c4; border-radius: 2mm; padding: 0.6mm 2.2mm; font-size: 3.4mm; }}
.rules .box {{ margin-top: auto; background: #e7f6ff; border-radius: 2.5mm; padding: 1.8mm 3mm; font-size: 3.3mm; line-height: 1.35; text-align: center; }}
.rules .box b {{ font-weight: normal; color: #1f4e9e; font-size: 3.8mm; }}
.rules .big {{ font-size: 3.8mm; line-height: 1.45; margin: 0 0 2mm; }}
.rules .big b {{ font-weight: normal; color: #c1121f; }}
.ex {{ display: flex; justify-content: center; gap: 2mm; margin: 1mm 0 3mm; }}
.ex .wrap {{ width: 26.6mm; height: 34.2mm; overflow: hidden; background: #fff; border: 0.3mm solid #aaa; border-radius: 2mm; }}
.ex .pc {{ transform: scale(0.38) translate(-2mm, -2mm); transform-origin: 0 0; }}
.ex .no {{ display: none; }}
.game {{ margin-top: 2.5mm; }}
.game + .game {{ border-top: 0.4mm dashed #ffd23f; padding-top: 2mm; margin-top: 2mm; }}
.gh {{ font-size: 6mm; display: flex; align-items: center; gap: 1.5mm; }}
.num {{ background: #c1121f; color: #fff; border-radius: 50%; width: 5.5mm; height: 5.5mm; display: inline-flex;
  align-items: center; justify-content: center; font-size: 3.6mm; }}
.sub {{ font-size: 3.4mm; color: #888; margin: 1mm 0 2mm; }}
ol {{ margin: 0; padding-left: 4.5mm; font-size: 3.7mm; line-height: 1.45; }}
li {{ margin-bottom: 1.6mm; }}
li b {{ color: #c1121f; font-weight: normal; }}
.tips {{ margin: 0; padding-left: 4mm; font-size: 3.5mm; line-height: 1.45; }}
.tips li {{ margin-bottom: 1.2mm; }}
.bye {{ margin-top: auto; background: #f1fbe9; border-radius: 2.5mm; padding: 2.5mm 3mm; font-size: 3.4mm; line-height: 1.4; text-align: center; color: #2e7d32; }}
/* 미리보기용 선: 파일로 저장할 때는 숨김 */
.guides .pc::after {{ content: ""; position: absolute; left: {BLEED}mm; top: {BLEED}mm; width: {TRIM_W}mm;
  height: {TRIM_H}mm; border: 0.25mm solid #e63946; border-radius: 5mm; }}
.guides .pc::before {{ content: ""; position: absolute; left: {BLEED + SAFE}mm; top: {BLEED + SAFE}mm;
  width: {TRIM_W - 2 * SAFE}mm; height: {TRIM_H - 2 * SAFE}mm; border: 0.2mm dashed #3a86ff; z-index: 1; }}
"""
    html = (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>대블 포토카드</title>'
        f"<style>{css}</style></head><body>{back}{infos_html}{fronts}</body></html>"
    )
    with open("photocard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"rules.html: 예시 카드 {ex[0] + 1}번·{ex[1] + 1}번 / photocard.html: 그림 카드 {len(cards)}장 + 설명서 {N_RULES}장 + 그림 안내 {N_GUIDE}장 + 뒷면 1장, 작업 크기 {W:.0f}x{H:.0f}mm")


if __name__ == "__main__":
    main()
