# encoding: UTF-8
# R23 — Alternativo A: drywall sala de TV/quarto (R01) 0,17 m ao norte,
# levando junto a porta de correr P03, o trilho e os móveis encostados nela.
#
# Como rodar: abrir MaxHaus_R22_MALAGA_RAIO20.skp no SketchUp,
# Janela > Console Ruby e digitar:  load '/caminho/para/r23_drywall_r01.rb'
#
# Nada é gravado por cima do R22: o resultado sai como R23 numa pasta nova,
# ao lado das anteriores. Se a parede não for achada com segurança, o script
# para sem mexer em nada e lista os candidatos; aí basta preencher DRYWALL_ID.

DESLOC_M     = 0.17   # quanto a parede anda (planta: 0,17 m ao norte)
DRYWALL_ID   = nil    # persistent_id da drywall, se a busca automática falhar
SENTIDO_Y    = nil    # +1 ou -1 para forçar o sentido; nil = automático
# Posição esperada da R01 no modelo, convertida da planta do scan (45,66 pt/m)
# usando o canto Málaga do R21/R22 como amarração. Serve só de filtro.
ESPERADO     = { x: [1.344, 5.421], y: [-2.890, -2.790] }
FOLGA_SALA   = 0.25   # móveis da sala de TV até esta distância da face andam junto
FOLGA_QUARTO = 0.05   # móveis do quarto encostados na face andam junto

m = Sketchup.active_model
raise 'Abra o R22 antes de rodar o R23' unless m.path.include?('R22')
out = File.join(File.dirname(File.dirname(m.path)), '2026-10-05_R23')

# ---------------------------------------------------------------- utilidades
def r23_bb_mundo(e, ptr)
  bb = Geom::BoundingBox.new
  (0..7).each { |i| bb.add(e.bounds.corner(i).transform(ptr)) }
  bb
end

def r23_dims(bb)
  [bb.width.to_m, bb.height.to_m, bb.depth.to_m] # x, y, z
end

# Percorre grupos e componentes visíveis; o bloco decide se desce no filho.
# `pais` é a linhagem do item, para não mover um filho junto com o pai.
def r23_percorrer(ents, ptr, pais, &blk)
  ents.each do |e|
    next unless e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
    next if e.hidden? || (e.layer && !e.layer.visible?)
    desce = blk.call(e, ptr, pais)
    r23_percorrer(e.definition.entities, ptr * e.transformation, pais + [e], &blk) if desce && pais.size < 4
  end
end

def r23_nome(e)
  n = e.name.to_s
  n = e.definition.name.to_s if n.empty? && e.respond_to?(:definition)
  n.empty? ? '(sem nome)' : n
end

def r23_fmt(bb)
  format('x %.2f..%.2f  y %.2f..%.2f  z %.2f..%.2f',
         bb.min.x.to_m, bb.max.x.to_m, bb.min.y.to_m, bb.max.y.to_m,
         bb.min.z.to_m, bb.max.z.to_m)
end

# ---------------------------------------------------- 1. achar a drywall R01
todos = []
r23_percorrer(m.entities, Geom::Transformation.new, []) do |e, ptr, pais|
  bb = r23_bb_mundo(e, ptr)
  todos << [e, ptr, bb, pais]
  dx, dy, = r23_dims(bb)
  dx > 3.5 || dy > 3.5 # contêiner grande: desce para ver o que tem dentro
end

ex = (ESPERADO[:x][0] + ESPERADO[:x][1]) / 2
ey = (ESPERADO[:y][0] + ESPERADO[:y][1]) / 2
candidatos = todos.select do |e, _ptr, bb|
  dx, dy, dz = r23_dims(bb)
  dy.between?(0.05, 0.16) && dx >= 2.5 && dz >= 2.0
end
candidatos.sort_by! do |_e, _ptr, bb|
  c = bb.center
  (c.x.to_m - ex).abs + (c.y.to_m - ey).abs
end

parede =
  if DRYWALL_ID
    todos.find { |e, *| e.persistent_id == DRYWALL_ID }
  else
    perto = candidatos.select do |_e, _ptr, bb|
      (bb.center.y.to_m - ey).abs < 0.6 && (bb.center.x.to_m - ex).abs < 1.2
    end
    nomeada = perto.select { |e, *| r23_nome(e) =~ /drywall|R01|divis/i }
    if nomeada.size == 1 then nomeada.first
    elsif perto.size == 1 then perto.first
    end
  end

unless parede
  puts '=== R23 parado: drywall R01 não identificada com segurança ==='
  puts 'Candidatos (paredes finas no eixo Y, >= 2,5 m, mais perto do esperado primeiro):'
  candidatos.first(12).each do |e, _ptr, bb|
    puts format('  id %-10s %-45s %s', e.persistent_id, r23_nome(e), r23_fmt(bb))
  end
  puts 'Grupos com nome de parede/drywall:'
  todos.select { |e, *| r23_nome(e) =~ /drywall|parede|R01|divis/i }.first(20).each do |e, _ptr, bb|
    puts format('  id %-10s %-45s %s', e.persistent_id, r23_nome(e), r23_fmt(bb))
  end
  puts 'Preencha DRYWALL_ID no topo do arquivo com o id certo e rode de novo.'
  raise 'R23: drywall não encontrada — nada foi alterado'
end

pe, pptr, pbb = parede
wy0 = pbb.min.y.to_m
wy1 = pbb.max.y.to_m
wx0 = pbb.min.x.to_m
wx1 = pbb.max.x.to_m

# --------------------------------------- 2. de que lado fica a sala de TV?
# A sala de TV (~4,6 m até a parede oposta) é mais funda que o quarto (~2,6 m).
# Raios horizontais a 1,50 m, dos dois lados, decidem o sentido.
def r23_alcance(m, x, y, sentido)
  hit = m.raytest([Geom::Point3d.new(x.m, y.m, 1.5.m), Geom::Vector3d.new(0, sentido, 0)], true)
  hit ? (hit[0].y.to_m - y).abs : 99.0
end

sentido = SENTIDO_Y
unless sentido
  xs = [0.2, 0.4, 0.6, 0.8].map { |f| wx0 + f * (wx1 - wx0) }
  mais  = xs.map { |x| r23_alcance(m, x, wy1 + 0.02, 1) }.max
  menos = xs.map { |x| r23_alcance(m, x, wy0 - 0.02, -1) }.max
  sentido = mais >= menos ? 1 : -1
  puts format('Alcance +Y %.2f m / -Y %.2f m -> sala de TV em %sY', mais, menos, sentido > 0 ? '+' : '-')
  puts 'AVISO: sentido diferente do previsto pela planta (+Y); confira as imagens.' if sentido < 0
end
face_sala   = sentido > 0 ? wy1 : wy0
face_quarto = sentido > 0 ? wy0 : wy1

# ----------------------------- 3. o que anda junto: parede, porta, trilho, móveis
mover = []
todos.each do |e, ptr, bb, pais|
  dx, dy, = r23_dims(bb)
  next if (dx > 3.5 || dy > 3.5) && e != pe # contêineres não andam inteiros
  y0 = bb.min.y.to_m
  y1 = bb.max.y.to_m
  x_sobrep = [bb.max.x.to_m, wx1].min - [bb.min.x.to_m, wx0].max
  next if x_sobrep < 0.05
  next if y0 < wy0 - 0.02 && y1 > wy1 + 0.02 # atravessa a parede (paredes ortogonais)

  # gap medido para fora da face, de cada lado
  gap_sala   = sentido > 0 ? y0 - face_sala : face_sala - y1
  gap_quarto = sentido > 0 ? face_quarto - y1 : y0 - face_quarto
  na_faixa   = y0 >= wy0 - 0.03 && y1 <= wy1 + 0.03 && dy <= 0.25

  motivo =
    if e == pe then 'drywall R01'
    elsif na_faixa then 'na linha da parede (porta, trilho, rodapé)'
    elsif gap_sala.between?(-0.01, FOLGA_SALA) then format('sala de TV, a %.2f m da face', gap_sala)
    elsif gap_quarto.between?(-0.01, FOLGA_QUARTO) then 'quarto, encostado na face'
    end
  mover << [e, ptr, motivo, pais] if motivo
end

# Filho de algo que já anda (porta dentro do grupo da parede, p. ex.) não anda de novo.
movidos = mover.map(&:first)
mover.reject! { |_e, _ptr, _m, pais| (pais & movidos).any? }

# ---------------------------------------------------------------- 4. aplicar
Dir.mkdir(out) unless Dir.exist?(out)
m.start_operation('R23 drywall R01 0,17 m ao norte', true)
begin
  v_mundo = Geom::Vector3d.new(0, (sentido * DESLOC_M).m, 0)
  mover.each do |e, ptr, *|
    v = v_mundo.transform(ptr.inverse)
    e.transform!(Geom::Transformation.translation(v))
  end
  pe.set_attribute('Projeto', 'R23_deslocamento_m', DESLOC_M)
  pe.set_attribute('Projeto', 'R23_nota', 'Quarto 2,71 m livres / 14,08 m²; sala de TV 22,32 m²')
  m.commit_operation
rescue => ex
  m.abort_operation rescue nil
  raise ex
end

# ------------------------------------------- 5. conferência, imagens e salvar
nbb = r23_bb_mundo(pe, pptr)
puts '=== R23 aplicado ==='
puts format('Drywall %s (id %s): y %.3f..%.3f -> %.3f..%.3f m',
            r23_nome(pe), pe.persistent_id, wy0, wy1, nbb.min.y.to_m, nbb.max.y.to_m)
mover.each do |e, _ptr, motivo, _pais|
  puts format('  movido  id %-10s %-40s %s', e.persistent_id, r23_nome(e), motivo)
end

m.pages.each do |p|
  p.use_hidden = false if p.respond_to?(:use_hidden=)
  p.use_hidden_objects = false if p.respond_to?(:use_hidden_objects=)
end
cx = (wx0 + wx1) / 2
fy = nbb.center.y.to_m
cam = lambda do |eye, alvo, fov|
  m.active_view.camera = Sketchup::Camera.new(Geom::Point3d.new(eye.map(&:m)),
                                               Geom::Point3d.new(alvo.map(&:m)), Z_AXIS, true, fov)
end
vistas = [
  ['01_Sala_TV_drywall_R01', [cx - 0.9, fy + sentido * 3.6, 1.65], [cx, fy, 1.20], 65],
  ['02_Quarto_drywall_R01',  [cx + 0.6, fy - sentido * 2.3, 1.60], [cx - 0.4, fy, 1.20], 75]
]
vistas.each do |nome, eye, alvo, fov|
  cam.call(eye, alvo, fov)
  m.active_view.write_image(filename: File.join(out, nome + '.png'), width: 1600, height: 1200, antialias: true)
  m.pages.add('R23 | ' + nome)
end
# planta vista de cima, ortogonal, centrada na parede
top = Sketchup::Camera.new(Geom::Point3d.new(cx.m, fy.m, 20.m), Geom::Point3d.new(cx.m, fy.m, 0), Y_AXIS, false)
top.height = 9.5.m
m.active_view.camera = top
m.active_view.write_image(filename: File.join(out, '03_Planta_drywall_R01.png'), width: 1600, height: 1200, antialias: true)
m.pages.add('R23 | 03_Planta_drywall_R01')
cam.call(*vistas.first[1..3])

raise 'Falha salvar' unless m.save(File.join(out, 'MaxHaus_R23_DRYWALL_R01.skp'))
fontes = File.join(out, '_fontes')
Dir.mkdir(fontes) unless Dir.exist?(fontes)
File.write(File.join(fontes, File.basename(__FILE__)), File.read(__FILE__)) if File.exist?(__FILE__)
puts "R23_SALVO; #{mover.size} itens deslocados #{DESLOC_M} m"
UI.messagebox("R23 salvo em #{out}\n#{mover.size} itens deslocados #{DESLOC_M} m (parede, porta e móveis).\nDetalhes no Console Ruby.")
