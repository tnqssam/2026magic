"""학교사랑 도블 카드 조합표 생성기.

7차 유한사영평면으로 57장 x 8개 조합을 만들고,
어떤 두 카드도 공통 그림이 정확히 1개인지 검증한 뒤 CSV로 저장한다.
"""
import csv
import itertools

SYMBOLS = [
    "조록나무", "동백꽃", "학교", "교표", "개교기념일", "연필", "지우개", "가위",
    "가방", "국어", "수학", "칠판", "시계", "의자", "책상", "우유",
    "버스", "배드민턴", "컴퓨터", "줄넘기", "돌하르방", "은행잎", "연못", "선생님",
    "학생", "학교사랑", "미끄럼틀", "축구", "농구", "돌담", "자", "딱풀",
    "태극기", "사물함", "급식", "정글짐", "귤", "우산", "새싹", "실내화",
    "빗자루", "크레파스", "시소", "마이크", "별", "피아노", "바이올린", "기타",
    "벚꽃", "탬버린", "호박", "토마토", "필통", "바구니", "훌라후프", "메달",
    "풍선",
]
N = 7  # 한 장 그림 수 = N + 1 = 8, 그림 수 = N*N + N + 1 = 57
assert len(SYMBOLS) == N * N + N + 1 and len(set(SYMBOLS)) == len(SYMBOLS)

def build_cards():
    cards = []
    for i in range(N):  # 기울기 i인 직선들
        for j in range(N):
            cards.append([N * x + (i * x + j) % N for x in range(N)] + [N * N + i])
    for x in range(N):  # 세로 직선들
        cards.append([N * x + y for y in range(N)] + [N * N + N])
    cards.append([N * N + i for i in range(N + 1)])  # 무한원 직선

    for a, b in itertools.combinations(cards, 2):
        assert len(set(a) & set(b)) == 1
    for s in range(len(SYMBOLS)):
        assert sum(s in c for c in cards) == N + 1
    return [[SYMBOLS[s] for s in c] for c in cards]


if __name__ == "__main__":
    cards = build_cards()
    with open("cards.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["카드"] + [f"그림{k}" for k in range(1, N + 2)])
        for n, c in enumerate(cards, 1):
            w.writerow([n] + c)
    print(f"OK: {len(cards)}장 생성, 모든 카드 쌍의 공통 그림이 정확히 1개")
