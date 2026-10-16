import html as _h

AREAS = {
    'a1': ('01', '안전보건 관리체계', '#2e5c8e', '#406b98'),
    'a2': ('02', '위험성평가', '#c05e37', '#c55e35'),
    'a3': ('03', '비상 상황대응 및 사고대응', '#b0791e', '#d99a3b'),
    'a4': ('04', '작업환경측정', '#2e7e71', '#33907b'),
    'a5': ('05', '근로자 건강검진', '#9a4563', '#a5506d'),
    'a6': ('06', '안전보건교육', '#557a40', '#5e8648'),
    'a7': ('07', '현장 안전보건조치', '#5c6079', '#676b86'),
    'ap': ('부록', '소규모 사업장 안전보건 의무 총정리', '#3e3d45', '#47464e'),
    'fr': ('GUIDE', '가이드 활용 · 한눈에 보기', '#2e5c8e', '#406b98'),
}
NAVY = '#14375e'


def e(s):
    return _h.escape(s, quote=False)


def rich(s):
    """**bold**, [[red]], {{gray}} inline markup on escaped text."""
    s = e(s).replace('&amp;nbsp;', '&nbsp;').replace('&lt;br&gt;', '<br>')
    import re
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<span class="em">\1</span>', s)
    s = re.sub(r'\{\{(.+?)\}\}', r'<span class="mut">\1</span>', s)
    return s


TABS = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'ap']
TABNAME = {'a1': '관리체계', 'a2': '위험성평가', 'a3': '비상대응', 'a4': '작업환경측정', 'a5': '건강검진', 'a6': '안전보건교육', 'a7': '현장조치', 'ap': '부록'}
TAB_TOP, TAB_STEP, TAB_H = 6, 31.5, 29   # mm, measured from the bottom edge of the header margin (21mm)
FOOT = '소규모 제조업 산업안전보건법 준수사항 안내'


def tab_label(k):
    num = AREAS[k][0]
    return TABNAME[k] if not num.isdigit() else '%s  %s' % (num, TABNAME[k])


def page_css():
    out = []
    for k, (num, title, dark, badge) in AREAS.items():
        tab = ''
        if k in TABS:
            i = TABS.index(k)
            tab = ' @right-top{content:"%s";height:%smm;margin-top:%smm;background:%s;color:#fff;font:700 7.6pt P;letter-spacing:.6pt;text-align:center;vertical-align:middle;border-radius:2mm 0 0 2mm;writing-mode:vertical-rl}\n' % (tab_label(k), TAB_H, TAB_TOP + i * TAB_STEP, badge)
        out.append('''@page %(k)s{
 @top-left{content:"%(num)s";width:16mm;margin-bottom:9mm;background:%(badge)s;font:700 %(nsz)s P;color:#fff;text-align:center;vertical-align:middle}
 @top-center{content:"%(title)s";width:170mm;margin-bottom:9mm;background:%(navy)s;font:700 10pt P;color:#fff;text-align:left;vertical-align:middle;padding-left:6mm}
 @top-right{content:"";width:16mm;margin-bottom:9mm;background:%(navy)s}
 @top-right-corner{content:"";margin-bottom:9mm;background:%(navy)s}
%(tab)s}
@page %(k)s:right{
 @bottom-left{content:"%(foot)s";width:120mm;text-align:left;font:500 7.5pt P;color:#8a94a3;padding-left:18mm;vertical-align:middle}
 @bottom-right{content:counter(page);width:60mm;text-align:right;font:700 8.5pt P;color:%(navy)s;padding-right:10mm;vertical-align:middle}
}
@page %(k)s:left{
 @bottom-left{content:counter(page);width:60mm;text-align:left;font:700 8.5pt P;color:%(navy)s;padding-left:18mm;vertical-align:middle}
 @bottom-right{content:"%(foot)s";width:120mm;text-align:right;font:500 7.5pt P;color:#8a94a3;padding-right:10mm;vertical-align:middle}
}''' % dict(k=k, num=num, title=title, badge=badge, navy=NAVY, tab=tab, foot=FOOT,
            nsz='10.5pt' if len(num) <= 2 else '7.5pt'))
    return '\n'.join(out)


# ---------- components ----------
class B:
    def __init__(self):
        self.parts = []

    def add(self, s):
        self.parts.append(s)
        return self

    def html(self):
        return '\n'.join(self.parts)


BADGE_DOT = {'red': '#ff6b57', 'orange': '#ffb347', 'bolt': '#ffd27a', 'plain': None}


def divider(key, title_lines, badges, sub_lines, box, bottom):
    num, title, dark, badge = AREAS[key]
    big = str(int(num)) if num.isdigit() else num
    label = 'AREA&nbsp;&nbsp;%s' % num if num.isdigit() else 'APPENDIX'
    t = '<br>'.join(e(x) for x in title_lines)
    bd = ''.join('<span class="dv-badge">%s%s</span>' % ('<i style="background:%s"></i>' % BADGE_DOT[c] if BADGE_DOT[c] else '', e(txt)) for c, txt in badges)
    bd = '<div class="dv-badges">%s</div>' % bd if bd else ''
    sub = '<br>'.join(rich(x) for x in sub_lines)
    i = TABS.index(key)
    tab = '<div class="dv-tab" style="top:%smm;height:%smm;color:%s">%s</div>' % (21 + TAB_TOP + i * TAB_STEP, TAB_H, dark, e(tab_label(key)))
    return '''<section class="divider" style="background:%s">
<div class="big">%s</div>%s
<div class="dv-in"><div class="dv-label">%s</div><div class="dv-line"></div>
<h1>%s</h1>%s<p class="dv-sub">%s</p></div>
<div class="dv-box">%s</div>
<div class="dv-secs">%s</div></section>''' % (dark, e(big), tab, label, t, bd, sub, rich(box), rich(bottom))


def area_open(key):
    return '<div class="area" style="page:%s;--ac:%s;--ab:%s">' % (key, AREAS[key][3], AREAS[key][2])


def area_close():
    return '</div>'


def lead(*paras):
    return '<div class="lead">%s</div>' % ''.join('<p>%s</p>' % rich(p) for p in paras)


def sec(title):
    return '<h3 class="sec">%s</h3>' % e(title)


def kv(rows, warn_last=True):
    trs = []
    for i, (k, v) in enumerate(rows):
        cls = ' class="warn"' if (warn_last and i == len(rows) - 1 and k.startswith('미이행')) else ''
        vv = v if isinstance(v, str) else '<br>'.join(rich(x) for x in v)
        if isinstance(v, str):
            vv = rich(v)
        trs.append('<tr%s><th>%s</th><td>%s</td></tr>' % (cls, e(k), vv))
    return '<table class="kv"><colgroup><col style="width:27mm"><col></colgroup>%s</table>' % ''.join(trs)


def lawbox(items, warn=None, badge='5인 이상 · 위반 시 형사처벌', title='중대재해처벌법(중처법) 추가 의무'):
    lis = ''.join('<div class="li"><div class="lt">%s</div><div class="ld">%s</div></div>' % (rich(t), rich(d)) for t, d in items)
    w = '<div class="lw"><span class="ic">!</span>%s</div>' % rich(warn) if warn else ''
    return '<div class="law"><div class="lh"><span>%s</span><span class="badge">%s</span></div><div class="lb">%s%s</div></div>' % (e(title), e(badge), lis, w)


def sub(code, title, tag=None):
    t = '<span class="tag">%s</span>' % e(tag) if tag else ''
    return '<h2 class="sub"><span class="code">%s</span>%s%s</h2>' % (e(code), e(title), t)


def steps(items):
    cells = ''.join('<div class="st"><div class="sn">STEP %d</div><div class="stt">%s</div><div class="sts">%s</div></div>' % (i + 1, e(a), e(b)) for i, (a, b) in enumerate(items))
    return '<div class="steps n%d">%s</div>' % (len(items), cells)


CIR = '①②③④⑤⑥⑦⑧⑨'


def matrix(rows):
    """rows: list of (label, [step texts]) ; step text may be list of lines"""
    trs = []
    for lab, vals in rows:
        cls = ' class="caution"' if lab == '주의사항' else ''
        if len(vals) == 1:
            body = '<br>'.join(rich(x) for x in (vals[0] if isinstance(vals[0], list) else [vals[0]]))
        else:
            items = []
            for i, v in enumerate(vals):
                if not v:
                    continue
                lines = v if isinstance(v, list) else [v]
                items.append('<div class="mi"><span class="mn">%d</span><div>%s</div></div>' % (i + 1, '<br>'.join(rich(x) for x in lines)))
            body = ''.join(items)
        trs.append('<tr%s><th>%s</th><td>%s</td></tr>' % (cls, e(lab), body))
    return '<table class="mx"><colgroup><col style="width:22mm"><col></colgroup>%s</table>' % ''.join(trs)


def check(items, warns=(), title='실행 체크'):
    lis = ''.join('<li><span class="cb"></span>%s</li>' % rich(x) for x in items)
    ws = ''.join('<div class="cw"><span class="ic">!</span>%s</div>' % rich(w) for w in warns)
    return '<div class="check"><div class="ch"><span class="tick"></span>%s</div><ul>%s</ul>%s</div>' % (e(title), lis, ws)


def form(title, body, page=False):
    return '<div class="form%s">' % (' fpage' if page else '') + '<div class="fh"><span class="fi"></span>서식 예시 — %s</div><div class="fb">%s</div></div>' % (e(title), body)


def table(head, rows, widths=None, cls='dt', center=()):
    cg = ''
    if widths:
        cg = '<colgroup>%s</colgroup>' % ''.join('<col style="width:%s">' % w for w in widths)
    th = ''.join('<th>%s</th>' % rich(h) for h in head)
    trs = []
    for r in rows:
        if isinstance(r, tuple) and r and r[0] == '__group__':
            trs.append('<tr class="grp"><td colspan="%d">%s</td></tr>' % (len(head), rich(r[1])))
            continue
        tds = []
        for j, c in enumerate(r):
            ccls = ' class="c"' if j in center else ''
            if isinstance(c, list):
                c = '<br>'.join(rich(x) for x in c)
            else:
                c = rich(c)
            tds.append('<td%s>%s</td>' % (ccls, c))
        trs.append('<tr>%s</tr>' % ''.join(tds))
    return '<table class="%s">%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (cls, cg, th, ''.join(trs))


def records(rows):
    return sec('기록 및 보관') + table(['보존 서류', '보존 방법 및 기간'], rows, widths=['38mm', None])


def qa(items):
    out = []
    for q, a in items:
        aa = ''.join('<p>%s</p>' % rich(x) for x in (a if isinstance(a, list) else [a]))
        out.append('<div class="qa"><div class="q"><span class="qb">Q</span>%s</div><div class="a">%s</div></div>' % (rich(q), aa))
    return sec('자주 묻는 질문') + ''.join(out)


def note(text, kind='tip'):
    ic = {'tip': '✓', 'warn': '!', 'info': 'i', 'new': 'N'}[kind]
    return '<div class="note %s"><span class="ic">%s</span><div>%s</div></div>' % (kind, ic, rich(text))


def para(text, cls=''):
    return '<p class="%s">%s</p>' % (cls, rich(text))


def h4(text):
    return '<h4>%s</h4>' % rich(text)


def raw(s):
    return s
SP = ''
