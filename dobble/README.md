# 학교사랑 도블 (대흘초등학교)

## 포토카드 주문 (퍼블로그, 70x90mm)
- `daeble_photocard_70x90.zip`: 그림 카드 `front_01~57.png`, 설명서 카드 `rules_1~7.png`, 그림 안내 카드 `guide_1~4.png`, 뒷면 2종: 그림 카드용 `back.png`, 설명서·그림 안내 카드용 `back_info.png`
- 필통·메달의 별 무늬는 '별' 그림과 헷갈리지 않게 지움 (`fix_icons.py`)
- 작업 크기 74x94mm(사방 2mm 재단 여백), 300dpi, 874x1110px
- 그림은 재단선에서 4mm 안쪽에만 배치 (밀림 1~2mm, 둥근 모서리 5mm 대비)
- 다시 만들기: `python3 crop_sheet.py art/sheet.webp && python3 fix_icons.py && python3 make_cards.py && python3 build_print.py && python3 build_photocard.py && node make_photocard.js && node make_pdf.js`

## 예전 A4 인쇄용 (정사각형 9cm)

- 그림 57개, 한 장에 8개, 카드 57장 (9cm 정사각형)
- 어떤 두 카드를 골라도 같은 그림이 **정확히 1개**
- `dobble_cards_duplex.pdf`: 양면 인쇄용 카드 (앞면·뒷면 번갈아 20쪽, A4, 긴 쪽 넘김)
- `dobble_guide.pdf`: 그림 안내 1쪽 (따로 인쇄)
- `dobble_rules.pdf`: 게임 방법 1쪽 (놀이 4가지)
- `cards.csv`: 카드별 그림 조합표 (엑셀에서 바로 열림)

## 다시 만들기
그림 목록은 `make_cards.py`에 있습니다. 그림은 `art/sheet.webp`(57개를 순서대로 모은 시트)에서 잘라 `art/`에 저장합니다. (`icons.py`는 이전에 쓰던 SVG 그림입니다.)

```bash
python3 crop_sheet.py art/sheet.webp
python3 build_print.py
node make_pdf.js
```
