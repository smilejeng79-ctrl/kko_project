# 인쇄용 가이드 빌드

`소규모제조업_산업안전보건_실행가이드_인쇄용.pdf`의 원본입니다.

- `c_front.py` 표지·활용법·한눈에 보기, `c_a1.py`~`c_a7.py` 영역 1~7, `c_ap.py` 부록
- `lib.py` 화면 구성 요소, `style.css` 디자인(색상·여백·글꼴)
- 글꼴: Pretendard (SIL Open Font License)

```bash
python3 main.py c_front,c_a1,c_a2,c_a3,c_a4,c_a5,c_a6,c_a7,c_ap guide.html
node pdf.js "$PWD/guide.html" "$PWD/guide.pdf"   # Playwright(Chromium) 필요
```
