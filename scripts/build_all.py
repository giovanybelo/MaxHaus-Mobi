# -*- coding: utf-8 -*-
"""Gera todo o caderno MaxHaus MainFloor e fecha o PDF A3 multipágina."""
import os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(RAIZ, 'scripts')
PRANCHAS = os.path.join(RAIZ, 'pranchas')
sys.path.insert(0, SCRIPTS)

# ordem do caderno
FOLHAS = [
    ('prancha_02_demolicao.py',  'prancha-02-demolicao.svg'),
    ('prancha_03_pisos.py',      'prancha-03-piso-monolitico.svg'),
    ('prancha_04_teto.py',       'prancha-04-teto.svg'),
    ('prancha_05_eletrica.py',   'prancha-05-eletrica.svg'),
]

def main():
    for script, _ in FOLHAS:
        subprocess.check_call([sys.executable, os.path.join(SCRIPTS, script)])
    subprocess.check_call([sys.executable, os.path.join(SCRIPTS, 'build_html.py')])

    from base_mainfloor import exportar_pdf_a3
    svgs = [os.path.join(PRANCHAS, nome) for _, nome in FOLHAS]
    caderno = os.path.join(PRANCHAS, 'caderno-mainfloor-A3.pdf')
    exportar_pdf_a3(svgs, caderno,
                    'MaxHaus MainFloor — caderno de estudo preliminar (A3)')
    print('caderno:', caderno, '%d folhas' % len(svgs))

if __name__ == '__main__':
    main()
