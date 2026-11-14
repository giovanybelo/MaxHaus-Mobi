# -*- coding: utf-8 -*-
"""Monta grades de conferência (4 folhas por imagem). Uso: grade.py pasta saida prefixo [dpi]"""
import glob, os, sys, pymupdf
pasta, saida, pref = sys.argv[1:4]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 62
fs = sorted(glob.glob(os.path.join(pasta, pref + '*-A3.pdf')))
for k in range(0, len(fs), 4):
    out = pymupdf.open(); W, H = 1191 * 2, 842 * 2
    pg = out.new_page(width=W, height=H)
    for i, f in enumerate(fs[k:k + 4]):
        pg.show_pdf_page(pymupdf.Rect((i % 2) * W / 2, (i // 2) * H / 2, (i % 2 + 1) * W / 2, (i // 2 + 1) * H / 2), pymupdf.open(f), 0)
    pg.get_pixmap(dpi=dpi).save(os.path.join(saida, '%s_%02d.png' % (pref.lower().replace('-', ''), k // 4)))
print(len(fs))
