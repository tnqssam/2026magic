"""퍼블로그 케이스용 이미지 (정사각형 JPG).

- case/cover.jpg: 큰 칸. 노란 테두리를 빼고 그림이 끝까지 차게 (어디서 잘려도 어색하지 않게)
- 작은 칸 3개: A안(학교 상징) / B안(게임 정보). 중요한 내용은 가운데에만
python3 build_case.py && node make_case.js
"""
from PIL import Image
from make_cards import SYMBOLS


def art(name):
    return f"../art/{SYMBOLS.index(name):02d}.png"


SMALL = {
    "a1_camellia": ("교화", "동백꽃", art("동백꽃")),
    "a2_emblem": ("대흘초", "교표", art("교표")),
    "a3_tree": ("교목", "조록나무", art("조록나무")),
    "b1_players": ("함께", "2~8명", art("학생")),
    "b2_time": ("한 판", "5분", art("시계")),
    "b3_cards": ("그림 카드", "57장", art("학교사랑")),
}


def main():
    Image.open("art/back_inner.png").convert("RGB").save(
        "case/cover.jpg", quality=95, subsampling=0, dpi=(300, 300))
    cells = "".join(
        f'<div class="sq" id="{k}"><div class="badge"><img src="{img}"></div>'
        f'<div class="t1">{t1}</div><div class="t2">{t2}</div></div>'
        for k, (t1, t2, img) in SMALL.items()
    )
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>대블 케이스</title><style>
@font-face {{ font-family: Jua; src: url(../fonts/Jua-Regular.ttf); }}
body {{ margin: 0; background: #fff; }}
.sq {{ width: 800px; height: 800px; position: relative; overflow: hidden; font-family: Jua, sans-serif;
  background: linear-gradient(#86d6fd 0 72%, #afdd45 72% 100%); display: flex; flex-direction: column;
  align-items: center; justify-content: center; }}
.badge {{ width: 380px; height: 380px; border-radius: 50%; background: #fff; border: 14px solid #ffc800;
  display: flex; align-items: center; justify-content: center; box-sizing: border-box; }}
.badge img {{ width: 250px; height: 250px; object-fit: contain; }}
.t1 {{ margin-top: 18px; font-size: 52px; color: #fff; -webkit-text-stroke: 10px #5a3a1a; paint-order: stroke fill; line-height: 1; }}
.t2 {{ margin-top: 6px; font-size: 96px; color: #ffd000; -webkit-text-stroke: 16px #5a3a1a; paint-order: stroke fill; line-height: 1.05; }}
</style></head><body>{cells}</body></html>"""
    with open("case/small.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("case/cover.jpg, case/small.html 저장")


if __name__ == "__main__":
    main()
