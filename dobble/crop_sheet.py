"""그림 한 장(시트)에서 57개 그림을 잘라 art/ 폴더에 PNG(투명 배경)로 저장.

python3 crop_sheet.py <시트 이미지>
시트 순서는 make_cards.SYMBOLS 순서와 같아야 한다 (줄마다 개수: ROW_COUNTS).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from make_cards import SYMBOLS

ROW_COUNTS = [6, 7, 7, 6, 7, 7, 7, 7, 3]
# 시트 그림 대신 따로 받은 그림으로 바꿀 것 {번호: 파일}
OVERRIDES = {35: "art/jungle_gym.webp"}  # 그네 -> 정글짐
assert sum(ROW_COUNTS) == len(SYMBOLS)


def transparent(a):
    """흰 배경을 투명으로 (밝을수록 투명하게, 경계는 부드럽게)"""
    ink = a.min(axis=2) < 235
    rgba = np.dstack([a, np.full(a.shape[:2], 255)]).astype(np.uint8)
    alpha = np.clip((250 - a.min(axis=2)) * 255 / 30, 0, 255)
    outside = ~nd.binary_fill_holes(nd.binary_dilation(ink, iterations=1))
    rgba[..., 3] = np.where(outside, alpha, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def main(path):
    img = Image.open(path).convert("RGB")
    a = np.asarray(img).astype(int)
    ink = a.min(axis=2) < 235
    lab, n = nd.label(nd.binary_dilation(ink, iterations=2))
    comps = []
    for i, sl in enumerate(nd.find_objects(lab)):
        if (lab[sl] == i + 1).sum() < 40:
            continue
        comps.append((i + 1, (sl[0].start + sl[0].stop) / 2, sl[0].stop - sl[0].start))

    # 줄 나누기: 큰 조각들의 세로 중심에서 가장 큰 간격 8곳을 자른다
    cy = sorted(y for _, y, h in comps if h > 40)
    gaps = sorted(range(len(cy) - 1), key=lambda i: cy[i + 1] - cy[i])[-(len(ROW_COUNTS) - 1):]
    cuts = sorted((cy[i] + cy[i + 1]) / 2 for i in gaps)
    rows = [[] for _ in ROW_COUNTS]
    for lid, y, _ in comps:
        rows[sum(y > t for t in cuts)].append(lid)

    boxes = []
    for ids, k in zip(rows, ROW_COUNTS):
        m = np.isin(lab, ids) & ink
        col = m.any(axis=0)
        # 빈 세로 띠 중 가장 넓은 k-1곳에서 자른다
        xs = np.flatnonzero(col)
        runs, start = [], None
        for x in range(xs[0], xs[-1] + 1):
            if not col[x] and start is None:
                start = x
            if col[x] and start is not None:
                runs.append((start, x))
                start = None
        runs = sorted(sorted(runs, key=lambda r: r[1] - r[0])[-(k - 1):])
        edges = [xs[0]] + [v for r in runs for v in r] + [xs[-1] + 1]
        segs = list(zip(edges[::2], edges[1::2]))
        colsum = m.sum(axis=0)
        while len(segs) < k:  # 붙어 있는 두 그림: 가장 넓은 구간을 잉크가 가장 적은 곳에서 나눈다
            j = max(range(len(segs)), key=lambda j: segs[j][1] - segs[j][0])
            x0, x1 = segs[j]
            lo, hi = x0 + (x1 - x0) * 3 // 10, x0 + (x1 - x0) * 7 // 10
            cut = lo + int(np.argmin(colsum[lo:hi]))
            segs[j:j + 1] = [(x0, cut), (cut, x1)]
        edges = [v for sgm in segs for v in sgm]
        for x0, x1 in zip(edges[::2], edges[1::2]):
            sub = m[:, x0:x1]
            ys = np.flatnonzero(sub.any(axis=1))
            boxes.append((ys[0], ys[-1] + 1, x0, x1))
    assert len(boxes) == len(SYMBOLS)

    out = np.asarray(transparent(a))
    # 그림마다 "중심이 그 칸 안에 있는 조각"만 모아서 자른다
    # (칸 경계로 자르면 붙어 있던 이웃 그림이 잘리거나 딸려 오기 때문)
    plab, pn = nd.label(out[..., 3] > 20)
    boxid = np.full(plab.shape, -1)
    for k, (y0, y1, x0, x1) in enumerate(boxes):
        boxid[y0:y1, x0:x1] = k
    pix_owner = np.full(plab.shape, -1)
    for j, sl in enumerate(nd.find_objects(plab), 1):
        m = plab[sl] == j
        ids = boxid[sl][m]
        ids = ids[ids >= 0]
        if len(ids) == 0:
            continue
        cnt = np.bincount(ids)
        sub = pix_owner[sl]
        if cnt.max() >= 0.9 * len(ids):  # 거의 한 칸 안에 있으면 통째로 그 그림
            sub[m] = cnt.argmax()
        else:  # 두 그림이 붙은 조각: 칸 경계로 나눔
            sub[m] = boxid[sl][m]
    print(f"art/ 폴더에 그림 {len(boxes)}개 저장")
    for i in range(len(boxes)):
        keep = pix_owner == i
        ys, xs = np.nonzero(keep)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        c = out[y0:y1, x0:x1].copy()
        c[~keep[y0:y1, x0:x1], 3] = 0
        # 아주 작은 부스러기 지우기
        cl, cn = nd.label(c[..., 3] > 20)
        if cn > 1:
            sizes = nd.sum(np.ones_like(cl), cl, range(1, cn + 1))
            for j, sz in enumerate(sizes, 1):
                if sz < sizes.max() * 0.03:
                    c[cl == j, 3] = 0
        crop = Image.fromarray(c, "RGBA")
        crop.crop(crop.getbbox()).save(f"art/{i:02d}.png")
    for i, src in OVERRIDES.items():
        src_im = Image.open(src).convert("RGBA")
        white = Image.new("RGBA", src_im.size, "white")
        white.alpha_composite(src_im)  # 투명 배경은 흰색으로 바꾼 뒤 처리
        im = transparent(np.asarray(white.convert("RGB")).astype(int))
        im = im.crop(im.getbbox())
        im.thumbnail((400, 400), Image.LANCZOS)
        im.save(f"art/{i:02d}.png")


if __name__ == "__main__":
    main(sys.argv[1])
