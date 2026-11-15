# -*- coding: utf-8 -*-
"""Gera os dois cadernos do banheiro: Executivo (BE-xx) e Técnico (BT-xx)."""
import os
import sys
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import exportar_pdf_a3, exportar_png

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA = os.path.join(RAIZ, 'banheiro', 'executivo-E2')


def gerar(nome_mod, caderno, titulo, so=None):
    mod = importlib.import_module(nome_mod)
    svgs = []
    for fn in mod.FOLHAS:
        r = fn()
        f = r[0] if isinstance(r, tuple) else r
        if so and not any(s in f.cod for s in so):
            continue
        caminho = f.salvar(PASTA)
        exportar_pdf_a3([caminho], os.path.join(PASTA, f.cod + '-A3.pdf'), 'MaxHaus 81 — Banheiro — ' + f.cod)
        svgs.append(caminho)
    if not so:
        exportar_pdf_a3(svgs, os.path.join(PASTA, caderno), titulo)
    print(nome_mod, len(svgs), 'folhas')


if __name__ == '__main__':
    so = set(sys.argv[1:])
    for nome_mod, caderno, titulo in MODULOS if (MODULOS := [
            ('exec_all', 'Banheiro_Caderno_Executivo_E2_A3.pdf', 'MaxHaus 81 — Banheiro — Caderno Executivo E2 (A3)'),
            ('tecnico', 'Banheiro_Caderno_Tecnico_E2_A3.pdf', 'MaxHaus 81 — Banheiro — Caderno Técnico E2 (A3)')]) else []:
        try:
            gerar(nome_mod, caderno, titulo, so)
        except ModuleNotFoundError as e:
            print('pendente:', e)
