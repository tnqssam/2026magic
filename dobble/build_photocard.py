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
    return f'<div class="pc front" id="front_{no:02d}"><span class="no">{no} / {len(SYMBOLS)}</span>{"".join(items)}</div>'


# 공식 도블 놀이 5가지 (규칙은 같게, 문장은 새로 씀)
GAMES = [
    ("1", "탑 쌓기", "카드를 많이 모으면 이겨요",
     "카드를 섞어 한 사람에게 1장씩 <b>뒷면이 보이게</b> 나눠 줘요. 남은 카드는 <b>앞면이 보이게</b> 가운데에 쌓아요.",
     "\"시작!\" 하면 모두 자기 카드를 뒤집어요. 가운데 카드와 <b>내 카드</b>에서 같은 그림을 먼저 찾아 외친 사람이 가운데 카드를 가져와 <b>내 카드 위에</b> 올려요. 이제 맨 위 카드가 내 카드예요.",
     "가운데 카드가 다 떨어지면 끝나요. <b>카드를 가장 많이 모은 사람</b>이 이겨요."),
    ("2", "우물", "카드를 먼저 다 내려놓으면 이겨요",
     "카드 1장을 <b>앞면이 보이게</b> 가운데에 놓아요. 남은 카드는 모두에게 <b>골고루</b> 나눠 줘요. 받은 카드는 뒷면이 보이게 쌓아 두었다가, \"시작!\" 하면 더미째 뒤집어요.",
     "<b>내 맨 위 카드</b>와 가운데 카드에서 같은 그림을 먼저 찾아 외친 사람이 내 카드를 <b>가운데에 내려놓아요</b>. 이제 그 카드가 새 가운데 카드예요.",
     "<b>내 카드를 가장 먼저 다 내려놓은 사람</b>이 이겨요."),
    ("3", "뜨거운 감자", "카드를 적게 받으면 이겨요",
     "여러 판을 해요. 판마다 한 사람에게 카드를 1장씩 뒷면이 보이게 나눠 줘요. 카드는 보지 말고 손에 들어요.",
     "\"시작!\" 하면 모두 카드를 뒤집어요. <b>내 카드</b>와 <b>친구 카드</b>에서 같은 그림을 먼저 찾아 외친 사람이 내 카드를 <b>그 친구 카드 위에</b> 얹어 줘요. 받은 친구는 맨 위 카드로 다시 찾아 넘겨요.",
     "그 판의 카드를 <b>모두 받게 된 사람이 그 판에서 져요</b>. 받은 카드는 자기 앞에 두고 다음 판을 해요. 카드가 다 떨어지면 끝나요. <b>모은 카드가 가장 적은 사람</b>이 이겨요."),
    ("4", "모두 잡아라", "카드를 많이 모으면 이겨요",
     "여러 판을 해요. 판마다 카드 1장을 <b>뒷면이 보이게</b> 가운데에 놓고, 그 둘레에 카드 9장을 <b>앞면이 보이게</b> 펼쳐요.",
     "\"시작!\" 하면 가운데 카드를 뒤집어요. 가운데 카드와 <b>둘레 카드 중 하나</b>에서 같은 그림을 먼저 찾아 외친 사람이 <b>그 둘레 카드를 가져가요</b>. 둘레 카드를 다 가져가면 가운데 카드는 상자에 넣고 다음 판을 해요.",
     "카드가 모자라 새 판을 펼칠 수 없으면 끝나요. <b>카드를 가장 많이 모은 사람</b>이 이겨요."),
    ("5", "깜짝 선물", "카드를 적게 가지면 이겨요",
     "한 사람에게 카드를 1장씩 <b>뒷면이 보이게</b> 나눠 줘요. 남은 카드는 <b>앞면이 보이게</b> 가운데에 쌓아요.",
     "\"시작!\" 하면 모두 자기 카드를 뒤집어요. 가운데 카드와 <b>친구 카드</b>에서 같은 그림을 먼저 찾아 외친 사람이 가운데 카드를 가져가 <b>그 친구 카드 위에</b> 올려 줘요. 원하지 않는 선물을 주는 거예요!",
     "가운데 카드가 다 떨어지면 끝나요. <b>카드가 가장 적은 사람</b>이 이겨요."),
]

GUIDE_PER_CARD = 15  # 3칸 x 5줄 (그림 위, 이름 아래)
N_GUIDE = math.ceil(len(SYMBOLS) / GUIDE_PER_CARD)
N_RULES = 2 + len(GAMES)


def info_card(cid, label, body, cls=""):
    return (
        f'<div class="pc info {cls}" id="{cid}"><div class="safe">'
        f'<div class="tag">{label}</div>{body}</div></div>'
    )


def guide_cards():
    out = []
    for k in range(N_GUIDE):
        names = SYMBOLS[k * GUIDE_PER_CARD:(k + 1) * GUIDE_PER_CARD]
        cells = "".join(
            f'<div class="gc">{art(n)}<div class="gn{" long" if len(n) >= 5 else ""}">{n}</div></div>' for n in names)
        out.append(info_card(f"guide_{k + 1}", f"그림 안내 {k + 1}/{N_GUIDE}",
                             f'<div class="ggrid">{cells}</div>', "guide"))
    return out


def rules_cards(ex_a, ex_b, no_a, no_b, same):
    def game(n, t, goal, prep, how, end):
        return (f'<div class="gh"><span class="num">{n}</span>{t}</div><div class="goal">{goal}</div>'
                f'<div class="sec"><span class="k">준비</span><p>{prep}</p></div>'
                f'<div class="sec"><span class="k">하는 방법</span><p>{how}</p></div>'
                f'<div class="sec"><span class="k">끝과 승패</span><p>{end}</p></div>')

    total = len(SYMBOLS)
    r = []
    r.append(f"""<h1>대블 설명서</h1>
<p class="lead">대블 카드에는 그림이 8개씩 있어요. <b>어떤 카드 두 장을 골라도, 똑같은 그림은 딱 하나</b>예요.
두 카드에서 같은 그림을 <b>가장 먼저 찾아 이름을 외쳐요!</b></p>
<div class="meta"><span>👥 2~8명</span><span>⏱ 한 판 5분</span></div>
<h2>모든 놀이에서 지켜요</h2>
<ul class="tips">
<li>그림 <b>이름을 먼저 외치고</b>, 그다음 카드를 움직여요.</li>
<li>둘이 동시에 외치면 <b>가위바위보</b>로 정해요.</li>
<li>카드는 돌려 봐도 괜찮아요. 이름이 헷갈리면 <b>그림 안내 카드</b>를 봐요.</li>
<li>다 놀고 나면 카드를 모두 모아 상자에 넣어요.</li>
</ul>""")
    r.append(f"""<style>.ex .it:has(img[alt="{same}"]) {{ border-radius: 50%; box-shadow: 0 0 0 1.6mm #ff2d55; }}</style>
<h2>처음 하기 전에</h2>
<p class="big">아무 카드나 2장을 펼치고 다 함께 같은 그림을 찾아 보세요.</p>
<div class="ex"><div class="wrap">{ex_a}</div><div class="wrap">{ex_b}</div></div>
<p class="big">{no_a}번, {no_b}번 카드에는 <b>{same}</b>이 똑같아요!</p>
<div class="box"><b>들어 있는 것</b><br>그림 카드 {total}장 · 그림 안내 카드 {N_GUIDE}장<br>설명서 카드 {N_RULES}장</div>""")
    for g in GAMES:  # 놀이 하나에 카드 한 장
        r.append(game(*g))
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
    # 설명서·그림 안내 카드 전용 뒷면 (그림 카드와 섞여도 바로 골라낼 수 있게)
    back += ('<div class="pc back_info" id="back_info"><div class="bi">'
             '<img class="em" src="art/03.png" alt="교표"><div class="bt">대블</div>'
             '<div class="bs">설명서 · 그림 안내</div>'
             '<div class="bk"><span>📖</span>먼저 읽어 보세요!</div></div></div>')
    css = f"""
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #ddd; display: flex; flex-wrap: wrap; gap: 6mm; padding: 6mm; }}
.pc {{ position: relative; width: {W}mm; height: {H}mm; overflow: hidden; background: #fff; flex: none; }}
.it {{ position: absolute; }}
.it img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
.no {{ position: absolute; left: 0; right: 0; bottom: {BLEED + 2.0}mm; text-align: center; font: 1.9mm sans-serif; color: #b5b5b5; }}
.back {{ background: linear-gradient(#86d6fd 0 50%, #afdd45 50% 100%); }}
.back img {{ position: absolute; left: 0; top: {(H - W) / 2}mm; width: {W}mm; height: {W}mm; display: block; }}
@font-face {{ font-family: Jua; src: url(fonts/Jua-Regular.ttf); }}
.info {{ font-family: Jua, sans-serif; color: #2b2b2b; background: #fffdf3; word-break: keep-all; }}
.safe {{ position: absolute; left: {BLEED + SAFE}mm; top: {BLEED + SAFE}mm; width: {TRIM_W - 2 * SAFE}mm;
  height: {TRIM_H - 2 * SAFE}mm; display: flex; flex-direction: column; }}
.tag {{ align-self: flex-start; background: #c1121f; color: #fff; border-radius: 2mm; padding: 0.5mm 2.2mm; font-size: 3mm; }}
.ggrid {{ flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(5, 1fr); gap: 0.8mm; margin-top: 1.5mm; }}
.gc {{ display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; border-radius: 2mm; min-width: 0; }}
.gc img {{ width: 10.5mm; height: 9mm; object-fit: contain; }}
.gn {{ font-size: 3.9mm; line-height: 1.1; margin-top: 0.6mm; white-space: nowrap; }}
.gn.long {{ font-size: 3.2mm; }}
.rules .logo img {{ width: 22mm; display: block; margin: 1mm auto 0; border-radius: 2mm; }}
.rules h1 {{ font-size: 7.5mm; color: #c1121f; text-align: center; margin: 1mm 0 1mm; font-weight: normal; }}
.rules h2 {{ font-size: 4.8mm; color: #c1121f; margin: 1.8mm 0 1mm; font-weight: normal; }}
.rules .lead {{ font-size: 3.25mm; text-align: center; line-height: 1.38; margin: 0 0 1.5mm; }}
.rules .meta {{ display: flex; justify-content: center; gap: 2mm; }}
.rules .meta span {{ background: #fff3c4; border-radius: 2mm; padding: 0.6mm 2.2mm; font-size: 3.4mm; }}
.rules .box {{ margin-top: auto; background: #e7f6ff; border-radius: 2.5mm; padding: 1.2mm 3mm; font-size: 3.3mm; line-height: 1.35; text-align: center; }}
.rules .box b {{ font-weight: normal; color: #1f4e9e; font-size: 3.8mm; }}
.rules .big {{ font-size: 3.5mm; line-height: 1.4; margin: 0 0 1.5mm; }}
.rules .big b {{ font-weight: normal; color: #c1121f; }}
.ex {{ display: flex; justify-content: center; gap: 2mm; margin: 0.6mm 0 1.4mm; }}
.ex .wrap {{ width: 23.8mm; height: 30.6mm; overflow: hidden; background: #fff; border: 0.3mm solid #aaa; border-radius: 2mm; }}
.ex .pc {{ transform: scale(0.34) translate(-2mm, -2mm); transform-origin: 0 0; }}
.ex .no {{ display: none; }}
.game {{ margin-top: 2.5mm; }}
.game + .game {{ border-top: 0.4mm dashed #ffd23f; padding-top: 2mm; margin-top: 2mm; }}
.gh {{ font-size: 5.6mm; display: flex; align-items: center; gap: 1.5mm; }}
.num {{ background: #c1121f; color: #fff; border-radius: 50%; width: 5.5mm; height: 5.5mm; display: inline-flex;
  align-items: center; justify-content: center; font-size: 3.6mm; }}
.sub {{ font-size: 3.4mm; color: #888; margin: 1mm 0 2mm; }}
ol {{ margin: 0; padding-left: 4.5mm; font-size: 3.7mm; line-height: 1.45; }}
li {{ margin-bottom: 1.6mm; }}
li b {{ color: #c1121f; font-weight: normal; }}
.goal {{ align-self: flex-start; background: #fff3c4; border-radius: 2mm; padding: 0.5mm 2.2mm; font-size: 3.1mm; margin: 1mm 0 0.6mm; }}
.sec {{ margin-top: 2.4mm; }}
.sec .k {{ display: inline-block; background: #1f4e9e; color: #fff; border-radius: 1.5mm; padding: 0.3mm 1.8mm; font-size: 3mm; }}
.sec p {{ margin: 0.5mm 0 0; font-size: 3mm; line-height: 1.32; }}
.sec b, .rules .lead b, .tips b {{ color: #c1121f; font-weight: normal; }}
.tips {{ margin: 0; padding-left: 4mm; font-size: 3.15mm; line-height: 1.34; }}
.tips li {{ margin-bottom: 1mm; }}
.bye {{ margin-top: auto; background: #f1fbe9; border-radius: 2.5mm; padding: 2.5mm 3mm; font-size: 3.4mm; line-height: 1.4; text-align: center; color: #2e7d32; }}
.back_info {{ background: #ffd23f; font-family: Jua, sans-serif; }}
.bi {{ position: absolute; left: {BLEED + SAFE}mm; top: {BLEED + SAFE}mm; width: {TRIM_W - 2 * SAFE}mm;
  height: {TRIM_H - 2 * SAFE}mm; display: flex; flex-direction: column; align-items: center; justify-content: center;
}}
.bi .em {{ width: 24mm; height: 24mm; object-fit: contain; background: #fff; border-radius: 50%; padding: 2.5mm; border: 0.9mm solid #5a3a1a; }}
.bi .bt {{ font-size: 23mm; line-height: 1; margin-top: 2mm; color: #fff; -webkit-text-stroke: 3mm #5a3a1a; paint-order: stroke fill; }}
.bi .bs {{ font-size: 5.6mm; margin-top: 3mm; color: #5a3a1a; }}
.bi .bk {{ margin-top: 7mm; background: #c1121f; color: #fff; border-radius: 3mm; padding: 1.5mm 3.5mm; font-size: 4.2mm; display: flex; gap: 1.5mm; align-items: center; }}
.rules .tag {{ margin-bottom: 3mm; }}
.rules .tag + h1, .rules .tag + h2, .rules .tag + style + h2 {{ margin-top: 0; }}
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
    print(f"rules.html: 예시 카드 {ex[0] + 1}번·{ex[1] + 1}번 / photocard.html: 그림 카드 {len(cards)}장 + 설명서 {N_RULES}장 + 그림 안내 {N_GUIDE}장 + 뒷면 2종, 작업 크기 {W:.0f}x{H:.0f}mm")


if __name__ == "__main__":
    main()
