# -*- coding: utf-8 -*-
"""Motor de paginação simétrica (cm). Cortes iguais nas duas pontas, eixo central."""
import math
KERF = 0.2          # perda do disco de corte (cm)
JNOM = 0.30         # junta nominal (cm)
MINFRAC = 0.40      # corte mínimo aceito como "confortável" (fração da peça)
HARD = 1/3          # abaixo disso é crítico

def orig_edges(W, a, j, o):
    """Reproduz a régua do Paginador antigo: peças começam em o + i*(a+j)."""
    m = a + j; first = None; last = None
    i = math.floor(-o / m) - 1
    pcs = []
    while o + i*m < W:
        x0 = o + i*m; v0 = max(0, x0); v1 = min(W, x0 + a)
        if v1 - v0 > 0.05: pcs.append((v0, v1 - v0))
        i += 1
    return pcs[0][1], pcs[-1][1], len(pcs)

def plan_axis(W, a, jmin=JNOM, jmax=JNOM, jnom=JNOM, kerf=KERF):
    """Escolhe n (peças inteiras) e junta j. Retorna dict."""
    half = (a - kerf) / 2
    cands = []
    for n in range(1, int(W // a) + 2):
        c_nom = (W - n*a - (n+1)*jnom) / 2
        if not (0 < c_nom < a): continue
        jh = (W - n*a - (a - kerf)) / (n + 1)
        cands.append((n, c_nom, jh))
    if not cands: raise ValueError('sem solução')
    # 1) meia peça exata dentro da faixa de junta
    for n, c_nom, jh in cands:
        if jmin - 1e-9 <= jh <= jmax + 1e-9 and jmin != jmax:
            return dict(n=n, j=jh, c=half, mode='meia', jh=jh)
    # 2) junta nominal; corte >= MINFRAC, mais perto da meia peça
    ok = [(abs(c - half), n, c) for n, c, jh in cands if c >= MINFRAC * a]
    if ok:
        _, n, c = min(ok); return dict(n=n, j=jnom, c=c, mode='nominal', jh=[x for x in cands if x[0]==n][0][2])
    n, c, jh = max(cands, key=lambda t: t[1])
    return dict(n=n, j=jnom, c=c, mode='fraco', jh=jh)

def spans(W, a, p):
    """Faixas (x0,x1,tipo) ao longo do eixo; tipo 'c' = corte, 'f' = inteira."""
    n, j, c = p['n'], p['j'], p['c']
    out = [(0, c, 'c')]
    x = c + j
    for i in range(n):
        out.append((x, x + a, 'f')); x += a + j
    out.append((W - c, W, 'c'))
    return out

def classify(c, a):
    f = c / a
    return 'ok' if f >= MINFRAC else ('atencao' if f >= HARD else 'critico')

if __name__ == '__main__':
    print('== Reprodução dos arquivos recebidos ==')
    casos = [
      ('N/S 7x15',  143, 240, 7.5, 15.5, 5.3, 8.1),
      ('N/S 15x15', 143, 240, 15.5, 15.5, 8.1, 6.6),
      ('L/O 7x15',  264, 240, 7.5, 15.5, 0.0, 9.5),
      ('L/O 15x15', 264, 240, 15.5, 15.5, 5.6, 9.5),
      ('L 15x15',   358, 260, 15.5, 15.5, 11.6, 11.6),
    ]
    for nome, W, H, a, b, ox, oy in casos:
        l, r, nc = orig_edges(W, a, 0.3, ox)
        t, bt, nr = orig_edges(H, b, 0.3, oy)
        print(f'{nome:10s} esq {l:5.2f} ({l/a*100:3.0f}%)  dir {r:5.2f} ({r/a*100:3.0f}%)  Δ={abs(l-r):4.2f} | topo {t:5.2f} ({t/b*100:3.0f}%) base {bt:5.2f} ({bt/b*100:3.0f}%) Δ={abs(t-bt):4.2f} | {nc}x{nr}')
    print('\n== Novo plano simétrico ==')
    for fmt, a in (('A 15,5x15,5', 15.5), ('B 7,5x15,5', 7.5)):
        for W in (143, 264, 358):
            p = plan_axis(W, a, 0.25, 0.35)
            print(fmt, 'W', W, p, f"{p['c']/a*100:.0f}%", classify(p['c'], a))
    for H in (240, 260):
        p = plan_axis(H, 15.5); print('H', H, p, f"{p['c']/15.5*100:.0f}%")
