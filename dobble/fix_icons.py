"""'별'과 헷갈리는 그림 고치기: 필통의 노란 별, 메달 가운데 별을 지운다.
(별이 따로 있으므로 아이가 필통·메달을 보고 '별!'이라고 외치면 안 됨)
crop_sheet.py 다음에 실행: python3 fix_icons.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
from make_cards import SYMBOLS


def path(name):
    return f"art/{SYMBOLS.index(name):02d}.png"


def fix_pencil_case():
    im = Image.open(path("필통")).convert("RGBA")
    a = np.asarray(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    h, w = r.shape
    yellow = (r > 170) & (g > 150) & (b < 140) & (al > 200)
    yellow[:, : w // 3] = False  # 왼쪽 지퍼 손잡이는 남김
    lab, n = nd.label(yellow)
    sizes = nd.sum(yellow, lab, range(1, n + 1))
    star = lab == (int(np.argmax(sizes)) + 1)
    star = nd.binary_fill_holes(nd.binary_dilation(star, iterations=4)) & (al > 200) & (r + g + b > 250)
    ring = nd.binary_dilation(star, iterations=5) & ~star & (b > 150) & (r < 150)
    blue = np.median(a[ring][:, :3], axis=0).astype(int)
    a[star, :3] = blue
    Image.fromarray(a.astype(np.uint8), "RGBA").save(path("필통"))


def fix_medal():
    im = Image.open(path("메달")).convert("RGBA")
    a = np.asarray(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    h, w = r.shape
    # 메달 가운데의 주황색 별 테두리
    orange = (r > 180) & (g > 90) & (g < 175) & (b < 90) & (al > 200)
    orange[: h // 2] = False
    ys, xs = np.nonzero(orange)
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    rad = max(ys.max() - ys.min(), xs.max() - xs.min()) / 2 + 2
    yy, xx = np.mgrid[0:h, 0:w]
    disk = (yy - cy) ** 2 + (xx - cx) ** 2 <= rad ** 2
    gold_pick = disk & ~nd.binary_dilation(orange, iterations=2) & (r > 200) & (g > 180) & (b < 120)
    gold = np.median(a[gold_pick][:, :3], axis=0).astype(int)
    a[disk, :3] = gold
    out = Image.fromarray(a.astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(out)
    font = ImageFont.truetype("fonts/Jua-Regular.ttf", int(rad * 1.7))
    d.text((cx, cy + rad * 0.08), "1", font=font, fill=(190, 120, 0, 255), anchor="mm")
    out.save(path("메달"))


if __name__ == "__main__":
    fix_pencil_case()
    fix_medal()
    print("필통·메달의 별 무늬를 지웠어요")
