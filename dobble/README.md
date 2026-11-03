# 학교사랑 도블 (대흘초등학교)

- 그림 57개, 한 장에 8개, 카드 57장 (9cm 정사각형)
- 어떤 두 카드를 골라도 같은 그림이 **정확히 1개**
- `dobble_cards.pdf`: 바로 인쇄할 수 있는 파일 (1쪽 그림 도감 + 카드 10쪽, A4)
- `cards.csv`: 카드별 그림 조합표 (엑셀에서 바로 열림)

## 다시 만들기
그림 목록은 `make_cards.py`, 그림은 `icons.py`(SVG)에 있습니다.

```bash
python3 build_print.py
node make_pdf.js
```
