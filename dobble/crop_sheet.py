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
assert sum(ROW_COUNTS) == len(SYMBOLS)


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

    rgba = np.dstack([a, np.full(a.shape[:2], 255)]).astype(np.uint8)
    # 흰 배경을 투명으로 (밝을수록 투명하게, 경계는 부드럽게)
    light = a.min(axis=2)
    alpha = np.clip((250 - light) * 255 / 30, 0, 255)
    outside = ~nd.binary_fill_holes(nd.binary_dilation(ink, iterations=1))
    rgba[..., 3] = np.where(outside, alpha, 255).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    print(f"art/ 폴더에 그림 {len(boxes)}개 저장")
    for i, (name, (y0, y1, x0, x1)) in enumerate(zip(SYMBOLS, boxes)):
        p = 3
        crop = out.crop((max(0, x0 - p), max(0, y0 - p), x1 + p, y1 + p))
        # 옆 그림에서 딸려 온 작은 조각 지우기
        c = np.asarray(crop).copy()
        cl, cn = nd.label(c[..., 3] > 20)
        if cn > 1:
            sizes = nd.sum(np.ones_like(cl), cl, range(1, cn + 1))
            for j, sz in enumerate(sizes, 1):
                if sz < sizes.max() * 0.03:
                    c[cl == j, 3] = 0
            crop = Image.fromarray(c, "RGBA")
        crop = crop.crop(crop.getbbox())
        crop.save(f"art/{i:02d}.png")


if __name__ == "__main__":
    main(sys.argv[1])
