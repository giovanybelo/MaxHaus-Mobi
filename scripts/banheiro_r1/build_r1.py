# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from lib import PW, PH
import s_r1a
SHEETS = list(s_r1a.SHEETS)
for mod in ('s_r1b', 's_r1c'):
    try:
        SHEETS += __import__(mod).SHEETS
    except ImportError:
        pass
raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(raiz, 'pranchas', 'caderno-tecnico-banheiro-R2-A3.pdf')
c = canvas.Canvas(out, pagesize=(PW, PH))
c.setTitle('MaxHaus · Banheiro · Caderno técnico de reforma R2'); c.setAuthor('MaxHaus')
for fn in SHEETS:
    fn(c); c.showPage()
c.save(); print('ok', len(SHEETS), 'pranchas ->', out)
