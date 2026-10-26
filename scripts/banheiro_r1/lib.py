# -*- coding: utf-8 -*-
"""Primitivas de desenho do caderno de paginação (A3 deitado, PDF vetorial)."""
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm

FD = '/usr/share/fonts/truetype/liberation/LiberationSerif-'
pdfmetrics.registerFont(TTFont('S', FD + 'Regular.ttf'))
pdfmetrics.registerFont(TTFont('S-B', FD + 'Bold.ttf'))
pdfmetrics.registerFont(TTFont('S-I', FD + 'Italic.ttf'))
pdfmetrics.registerFont(TTFont('S-BI', FD + 'BoldItalic.ttf'))
pdfmetrics.registerFontFamily('S', normal='S', bold='S-B', italic='S-I', boldItalic='S-BI')

PW, PH = 1190.55, 841.89           # A3 deitado em pt
MG = 40                              # margem

K = black
K70 = HexColor('#4d4d4d'); K45 = HexColor('#8c8c8c'); K20 = HexColor('#cccccc'); K08 = HexColor('#ebebeb')
CIANO = HexColor('#00e5ff'); CIANO18 = HexColor('#d7f7fb'); CIANO40 = HexColor('#9eeef7')
AMARELO = HexColor('#ffff00'); AMARELO45 = HexColor('#fffb8a')
MAGENTA = HexColor('#e6007e'); MAGENTA12 = HexColor('#fde0ef')
GROUT = HexColor('#bdbdbd')
# CMYK: branco = Bleu inteira, amarelo = corte, ciano = Nuage, ciano + amarelo = Nuage cortada, magenta = eixo e alertas
BLEU = HexColor('#ffffff'); BLEU_CUT = AMARELO45; NUAGE = CIANO40; NUAGE_CUT = HexColor('#c9f3b0'); JUNTA = HexColor('#a6a6a6')
OK = HexColor('#1b7a3a')

def f(v, d=1):
    """número pt-BR"""
    s = ('%.' + str(d) + 'f') % v
    if d and '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s.replace('.', ',')

def fx(v, d=2):
    s = ('%.' + str(d) + 'f') % v
    return s.replace('.', ',')

def txt(c, x, y, s, size=8, font='S', col=K, anchor='l', rot=0, ls=0):
    c.saveState()
    c.setFillColor(col); c.setFont(font, size)
    if rot:
        c.translate(x, y); c.rotate(rot); x = y = 0
    if ls:
        t = c.beginText(); t.setFont(font, size); t.setCharSpace(ls); t.setFillColor(col)
        w = pdfmetrics.stringWidth(s, font, size) + ls * len(s)
        ox = x - (w / 2 if anchor == 'c' else (w if anchor == 'r' else 0))
        t.setTextOrigin(ox, y); t.textOut(s); c.drawText(t)
    else:
        if anchor == 'c': c.drawCentredString(x, y, s)
        elif anchor == 'r': c.drawRightString(x, y, s)
        else: c.drawString(x, y, s)
    c.restoreState()

def para(c, x, y, w, s, size=8.4, lead=None, font='S', col=K, maxlines=None):
    """Parágrafo com quebra; y é o topo. Retorna y logo abaixo."""
    lead = lead or size * 1.32
    lines = simpleSplit(s, font, size, w)
    if maxlines: lines = lines[:maxlines]
    for ln in lines:
        y -= lead
        txt(c, x, y + lead * 0.22, ln, size, font, col)
    return y

def rich(c, x, y, w, head, body, size=8.4, gap=5):
    """Título em negrito + corpo; y topo."""
    y = para(c, x, y, w, head, size, font='S-B')
    y = para(c, x, y, w, body, size)
    return y - gap

def line(c, x0, y0, x1, y1, w=0.6, col=K, dash=None):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(w)
    if dash: c.setDash(list(dash), 0)
    c.line(x0, y0, x1, y1); c.restoreState()

def rect(c, x, y, w, h, fill=None, stroke=K, sw=0.5, dash=None):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(sw)
    if dash: c.setDash(list(dash), 0)
    c.rect(x, y, w, h, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    c.restoreState()

def hatch(c, x, y, w, h, step=5, col=K45, sw=0.4):
    c.saveState()
    p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(col); c.setLineWidth(sw)
    t = -h
    while t < w:
        c.line(x + t, y, x + t + h, y + h); t += step
    c.restoreState()

def header(c, titulo, sub, nfolha, total, tag='R2'):
    txt(c, MG, PH - 34, 'MAXHAUS / MAIN FLOOR  ·  BANHEIRO  ·  CADERNO TÉCNICO DE REFORMA', 7.4, 'S-B', K70, ls=0.9)
    txt(c, MG, PH - 70, titulo, 25, 'S-B')
    para(c, MG, PH - 76, 760, sub, 9.2, 12, 'S', K70, maxlines=3)
    txt(c, PW - MG, PH - 34, tag + '  ·  26.10.2026  ·  MODELO R47', 7.4, 'S-B', K70, 'r', ls=0.6)
    txt(c, PW - MG, PH - 66, '%02d' % nfolha, 34, 'S-B', K, 'r')
    txt(c, PW - MG, PH - 80, 'de %02d' % total, 8.4, 'S', K70, 'r')
    line(c, MG, PH - 112, PW - MG, PH - 112, 1.0, K)

def footer(c, nfolha, total, extra=None):
    line(c, MG, 52, PW - MG, 52, 0.6, K20)
    t1 = ('Medidas do modelo R47: banheiro 1.423 × 2.583 mm, superfícies a 2.391 mm, peça nominal 75 × 155 mm, junta 2 mm. '
          'Refazer a paginação com a peça do lote e a medida de obra antes de cortar (Prancha 20).')
    t2 = extra or ('Coordenação técnica para conferência: não liberado para obra sem levantamento de campo e responsável técnico.')
    txt(c, MG, 38, t1, 6.9, 'S', K70)
    txt(c, MG, 28, t2, 6.9, 'S-B', MAGENTA)
    txt(c, PW - MG, 28, 'Prancha %02d / %02d' % (nfolha, total), 7.4, 'S', K70, 'r')

def table(c, x, y, widths, head, rows, size=7.8, pad=3.4, hfill=K08, zebra=True, aligns=None, bold_first=False, hsize=None):
    """Tabela com quebra de linha. y = topo. Retorna y da base."""
    hsize = hsize or size
    n = len(widths)
    aligns = aligns or ['l'] * n
    def cell_lines(s, w, font):
        return simpleSplit(str(s), font, size, w - 2 * pad)
    # cabeçalho
    if head:
        hl = [simpleSplit(str(h), 'S-B', hsize, widths[i] - 2 * pad) for i, h in enumerate(head)]
        hh = max(len(l) for l in hl) * hsize * 1.25 + 2 * pad
        rect(c, x, y - hh, sum(widths), hh, hfill, None)
        cx = x
        for i, l in enumerate(hl):
            yy = y - pad - hsize * 0.95
            for ln in l:
                if aligns[i] == 'r': txt(c, cx + widths[i] - pad, yy, ln, hsize, 'S-B', K, 'r')
                elif aligns[i] == 'c': txt(c, cx + widths[i] / 2, yy, ln, hsize, 'S-B', K, 'c')
                else: txt(c, cx + pad, yy, ln, hsize, 'S-B')
                yy -= hsize * 1.25
            cx += widths[i]
        line(c, x, y - hh, x + sum(widths), y - hh, 0.8, K)
        y -= hh
    for ri, r in enumerate(rows):
        fill = None
        col = K
        if isinstance(r, dict):
            fill = r.get('fill'); col = r.get('col', K); cells = r['cells']; bold_row = r.get('bold', False)
        else:
            cells = r; bold_row = False
        fonts = ['S-B' if (bold_row or (bold_first and i == 0)) else 'S' for i in range(n)]
        cl = [cell_lines(cells[i], widths[i], fonts[i]) for i in range(n)]
        rh = max(len(l) for l in cl) * size * 1.25 + 2 * pad
        if fill is not None: rect(c, x, y - rh, sum(widths), rh, fill, None)
        elif zebra and ri % 2 == 1: rect(c, x, y - rh, sum(widths), rh, HexColor('#f6f6f6'), None)
        cx = x
        for i, l in enumerate(cl):
            yy = y - pad - size * 0.95
            for ln in l:
                if aligns[i] == 'r': txt(c, cx + widths[i] - pad, yy, ln, size, fonts[i], col, 'r')
                elif aligns[i] == 'c': txt(c, cx + widths[i] / 2, yy, ln, size, fonts[i], col, 'c')
                else: txt(c, cx + pad, yy, ln, size, fonts[i], col)
                yy -= size * 1.25
            cx += widths[i]
        y -= rh
        line(c, x, y, x + sum(widths), y, 0.3, K20)
    line(c, x, y, x + sum(widths), y, 0.8, K)
    return y

def section(c, x, y, s, w=None):
    txt(c, x, y, s.upper(), 8.4, 'S-B', K70, ls=1.0)
    if w: line(c, x, y - 4, x + w, y - 4, 0.5, K20)
    return y - 14

def dimh(c, x0, x1, y, label, size=6.6, tick=3.5, col=K70, above=True, bold=False):
    line(c, x0, y, x1, y, 0.5, col)
    line(c, x0, y - tick, x0, y + tick, 0.5, col); line(c, x1, y - tick, x1, y + tick, 0.5, col)
    if label:
        w = pdfmetrics.stringWidth(label, 'S-B' if bold else 'S', size)
        if (x1 - x0) >= w + 2:
            txt(c, (x0 + x1) / 2, y + (2.2 if above else -size - 1.2), label, size, 'S-B' if bold else 'S', K, 'c')
        else:
            txt(c, (x0 + x1) / 2, y + (2.2 if above else -size - 1.2), label, size, 'S-B' if bold else 'S', K, 'c')

def dimv(c, x, y0, y1, label, size=6.6, tick=3.5, col=K70, left=True, bold=False):
    line(c, x, y0, x, y1, 0.5, col)
    line(c, x - tick, y0, x + tick, y0, 0.5, col); line(c, x - tick, y1, x + tick, y1, 0.5, col)
    if label:
        txt(c, x + (-2.6 if left else 2.6 + size * 0.7), (y0 + y1) / 2, label, size, 'S-B' if bold else 'S', K, 'c', rot=90)

def legend(c, x, y, items, size=7.2, gapx=14):
    for kind, label in items:
        if kind == 'full': rect(c, x, y - 1, 11, 8, white, K, 0.5)
        elif kind == 'cut': rect(c, x, y - 1, 11, 8, AMARELO45, K, 0.5)
        elif kind == 'wet': rect(c, x, y - 1, 11, 8, CIANO18, K, 0.5)
        elif kind == 'door': rect(c, x, y - 1, 11, 8, white, K, 0.5); hatch(c, x, y - 1, 11, 8, 3)
        elif kind == 'k01': rect(c, x + 4, y - 1, 3, 8, CIANO, K, 0.4)
        elif kind == 'axis': line(c, x, y + 3, x + 11, y + 3, 0.8, MAGENTA, (4, 1.6, 1, 1.6))
        elif kind == 'crit': rect(c, x, y - 1, 11, 8, MAGENTA12, MAGENTA, 0.8)
        txt(c, x + 15, y, label, size, 'S', K)
        x += 15 + pdfmetrics.stringWidth(label, 'S', size) + gapx
    return x
