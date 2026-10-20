# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from lib import *
import sheets_a as SA
try:
    import sheets_b as SB
except ImportError:
    SB = None
try:
    import sheets_c as SC
except ImportError:
    SC = None

SHEETS = [SA.s01, SA.s02, SA.s03, SA.s04]
if SB: SHEETS += SB.SHEETS
if SC: SHEETS += SC.SHEETS

def main(out='caderno.pdf'):
    c = canvas.Canvas(out, pagesize=(PW, PH))
    c.setTitle('MaxHaus · Banheiro · Projeto executivo de paginação de revestimento')
    c.setAuthor('MaxHaus')
    for fn in SHEETS:
        fn(c); c.showPage()
    c.save()
    print('ok', len(SHEETS), 'folhas ->', out)

if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(raiz, 'pranchas', 'paginacao-banheiro-projeto-executivo-A3.pdf'))
