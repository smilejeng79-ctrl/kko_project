import importlib, sys
from lib import page_css
mods = sys.argv[1].split(',')
body = ''.join(importlib.import_module(m).build() for m in mods)
css = open('style.css').read() + '\n' + page_css()
open(sys.argv[2], 'w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>소규모 제조업 산업안전보건법 준수사항 안내</title><style>%s</style></head><body>%s</body></html>' % (css, body))
