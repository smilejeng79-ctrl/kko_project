# 인쇄용 가이드 빌드

`소규모제조업_산업안전보건_실행가이드_인쇄용.pdf`의 원본입니다.

- `c_front.py` 표지·활용법·한눈에 보기, `c_a1.py`~`c_a7.py` 영역 1~7, `c_ap.py` 부록
- `lib.py` 화면 구성 요소, `style.css` 디자인(색상·여백·글꼴)
- 글꼴: Pretendard (SIL Open Font License)

```bash
python3 main.py c_front,c_a1,c_a2,c_a3,c_a4,c_a5,c_a6,c_a7,c_ap guide.html
node pdf.js "$PWD/guide.html" "$PWD/guide.pdf"   # Playwright(Chromium) 필요
```

## 인쇄·제본 설정
- 양면 인쇄 + 좌측 링바인더 기준: 홀수 쪽은 왼쪽, 짝수 쪽은 오른쪽이 제본(구멍) 쪽입니다.
- 제본 쪽 여백은 `lib.py`의 `GUTTER`(15mm), 바깥쪽은 `OUTER`(8mm)로 조정합니다. 본문은 여기에 10mm가 더해집니다.
- 영역 번호 상자·인덱스 탭·쪽번호는 항상 바깥쪽에 배치됩니다.
