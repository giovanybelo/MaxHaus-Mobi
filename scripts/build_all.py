# -*- coding: utf-8 -*-
"""Gera todo o caderno MaxHaus MainFloor e fecha o PDF A3 multipágina."""
import os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(RAIZ, 'scripts')
PRANCHAS = os.path.join(RAIZ, 'pranchas')
sys.path.insert(0, SCRIPTS)

# ordem do caderno
# (script, folhas geradas) — o script de pisos gera duas de uma vez
FOLHAS = [
    ('prancha_01_planta.py',     ['prancha-01-planta-cotada.svg']),
    ('prancha_02_demolicao.py',  ['prancha-02-demolicao.svg']),
    ('prancha_03_pisos.py',      ['prancha-03-piso-cumaru.svg',
                                  'prancha-04-piso-monolitico.svg']),
    ('prancha_04_teto.py',       ['prancha-05-teto.svg']),
    ('prancha_05_eletrica.py',   ['prancha-06-eletrica.svg']),
    ('prancha_06_esquadrias.py', ['prancha-07-esquadrias.svg']),
]

def main():
    for script, _ in FOLHAS:
        subprocess.check_call([sys.executable, os.path.join(SCRIPTS, script)])
    subprocess.check_call([sys.executable, os.path.join(SCRIPTS, 'build_html.py')])

    from base_mainfloor import exportar_pdf_a3
    svgs = [os.path.join(PRANCHAS, n) for _, nomes in FOLHAS for n in nomes]
    caderno = os.path.join(PRANCHAS, 'caderno-mainfloor-A3.pdf')
    exportar_pdf_a3(svgs, caderno,
                    'MaxHaus MainFloor — caderno de estudo preliminar (A3)')
    print('caderno:', caderno, '%d folhas' % len(svgs))

if __name__ == '__main__':
    main()
