"""content.py 로 한글(HWPX) 안내지를 만든다."""
import sys
from pathlib import Path

from hwpx import HwpxDocument

sys.path.insert(0, str(Path(__file__).parent))
from content import AFTER, CHECK_GUIDE, INFO, PREP, STEPS, SUBTITLE, TITLE  # noqa: E402

FONT = "맑은 고딕"
NAVY = "#1F3864"
HEAD_FILL = "#1F3864"
SOFT_FILL = "#DEEAF6"
TOTAL_W = 48000  # A4 본문 폭(여백 15mm) 근사, HWPUNIT

doc = HwpxDocument.new()
doc.page.setup(paper_size="A4", margins_mm={"left": 15, "right": 15, "top": 15, "bottom": 15})
st = doc.styles


def run(size=10, bold=False, color=None):
    return st.ensure_run(font=FONT, size=size, bold=bold, color=color)


CENTER = st.ensure_paragraph_format(alignment="CENTER")
LEFT = st.ensure_paragraph_format(alignment="LEFT")
GRID = st.ensure_border_fill(border_color="#7F7F7F")
HEAD_BF = st.ensure_border_fill(border_color="#7F7F7F", fill_color=HEAD_FILL)
SOFT_BF = st.ensure_border_fill(border_color="#7F7F7F", fill_color=SOFT_FILL)


def para(text="", size=10, bold=False, color=None, align=LEFT):
    p = doc.add_paragraph("", para_pr_id_ref=align, inherit_style=False)
    p.add_run(text, char_pr_id_ref=run(size, bold, color))
    return p


def fill(cell, lines, size=9.5, bold=False, color=None, align=LEFT):
    """셀 내용을 여러 줄 문단으로 채운다."""
    if isinstance(lines, str):
        lines = [lines]
    first = cell.paragraphs[0]
    for r in list(first.runs):
        r.element.getparent().remove(r.element)
    first.element.set("paraPrIDRef", str(align))
    first.add_run(lines[0], char_pr_id_ref=run(size, bold, color))
    for line in lines[1:]:
        cell.add_paragraph(line, para_pr_id_ref=align, char_pr_id_ref=run(size, bold, color))


def table(rows, cols, widths):
    t = doc.add_table(rows, cols, width=TOTAL_W, border_fill_id_ref=GRID)
    t.set_column_widths(widths)
    return t


def header_row(t, labels):
    for c, label in enumerate(labels):
        t.set_cell_border_fill(0, c, HEAD_BF)
        fill(t.cell(0, c), label, size=10, bold=True, color="#FFFFFF", align=CENTER)


def section_title(text):
    para("")
    para(text, size=13, bold=True, color=NAVY)


# ── 제목 ─────────────────────────────────────────────
para(SUBTITLE, size=11, color="#595959", align=CENTER)
para(TITLE, size=18, bold=True, color=NAVY, align=CENTER)
para("")

# ── 기본 정보 ────────────────────────────────────────
t = table(len(INFO), 2, [1, 4])
for r, (k, v) in enumerate(INFO):
    t.set_cell_border_fill(r, 0, SOFT_BF)
    fill(t.cell(r, 0), k, size=10, bold=True, align=CENTER)
    fill(t.cell(r, 1), v, size=10)

# ── 당일 진행 순서 ───────────────────────────────────
total = sum(s[3] for s in STEPS)
section_title(f"1. 당일 진행 순서 (총 약 {total}분)")
para("※ 3번(20분)을 제외한 소요시간은 권장 기준이며 사업장 여건에 맞게 조정합니다.",
     size=9, color="#595959")
t = table(len(STEPS) + 1, 5, [6, 20, 11, 7, 43])
header_row(t, ["순서", "단계", "장소", "시간", "진행 내용"])
for r, (no, name, place, mins, items, _todo) in enumerate(STEPS, start=1):
    fill(t.cell(r, 0), no, size=11, bold=True, color=NAVY, align=CENTER)
    fill(t.cell(r, 1), name, size=10, bold=True)
    fill(t.cell(r, 2), place, align=CENTER)
    fill(t.cell(r, 3), f"{mins}분", align=CENTER)
    fill(t.cell(r, 4), [f"• {i}" for i in items])
    if no == "3":
        for c in range(5):
            t.set_cell_border_fill(r, c, SOFT_BF)

# ── 점검표 체크 방법·주의사항 ────────────────────────
section_title("2. 대책제안점검표 체크 방법·주의사항 (3단계에서 참여자에게 안내)")
t = table(len(CHECK_GUIDE), 2, [1, 5])
for r, (k, items) in enumerate(CHECK_GUIDE):
    t.set_cell_border_fill(r, 0, SOFT_BF)
    fill(t.cell(r, 0), k, size=10, bold=True, align=CENTER)
    fill(t.cell(r, 1), [f"• {i}" for i in items])

# ── 단계별 담당자 할 일 ──────────────────────────────
section_title("3. 단계별 담당자 할 일")
t = table(len(STEPS) + 1, 3, [6, 20, 40])
header_row(t, ["순서", "단계", "담당자 할 일"])
for r, (no, name, *_rest, todo) in enumerate(STEPS, start=1):
    fill(t.cell(r, 0), no, bold=True, align=CENTER)
    fill(t.cell(r, 1), name)
    fill(t.cell(r, 2), todo)

# ── 사전 준비물 ──────────────────────────────────────
section_title("4. 사전 준비물 체크")
t = table(len(PREP) + 1, 2, [9, 1])
header_row(t, ["준비물", "확인"])
for r, item in enumerate(PREP, start=1):
    fill(t.cell(r, 0), item)
    fill(t.cell(r, 1), "□", size=11, align=CENTER)

# ── 마무리 후 할 일 ──────────────────────────────────
section_title("5. 위험성평가 후 할 일")
t = table(len(AFTER) + 1, 2, [1, 5])
header_row(t, ["시점", "할 일"])
for r, (when, what) in enumerate(AFTER, start=1):
    t.set_cell_border_fill(r, 0, SOFT_BF)
    fill(t.cell(r, 0), when, bold=True, align=CENTER)
    fill(t.cell(r, 1), what)

para("")
para("※ 위험성평가는 노동자가 참여해야 합니다(산업안전보건법 제36조). "
     "참석자 명단과 진행 사진은 반드시 보관하세요.", size=9, color="#595959")

out = Path(__file__).parent / "위험성평가_당일운영절차_안내지.hwpx"
doc.save_to_path(out)
print(out)
