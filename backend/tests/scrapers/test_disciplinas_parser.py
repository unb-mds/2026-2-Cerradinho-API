from pathlib import Path

from app.scrapers.disciplinas.parser import parse_turmas

FIXTURE = Path(__file__).parent / "fixtures" / "turmas_fcte_gama_2026_2.html"
FIXTURE_VAGAS_EM_BRANCO = Path(__file__).parent / "fixtures" / "turma_vagas_em_branco.html"


def test_parse_turmas_extrai_disciplinas_e_turmas():
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    assert len(turmas) > 0

    primeira = turmas[0]
    assert primeira.disciplina_codigo
    assert primeira.disciplina_nome
    assert primeira.numero
    assert primeira.professores, "toda turma deveria ter ao menos um professor"
    assert primeira.sala.descricao


def test_parse_turmas_agrupa_turmas_sob_a_disciplina_correta():
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    algoritmos_em_grafos = [t for t in turmas if t.disciplina_nome == "ALGORITMOS EM GRAFOS"]
    assert len(algoritmos_em_grafos) >= 1
    assert algoritmos_em_grafos[0].disciplina_codigo == "FCTE0005"


def test_parse_turmas_corta_intervalo_de_datas_do_codigo_de_horario():
    """O SIGAA junta código e intervalo de datas no mesmo texto
    ("6T2345 (10/08/2026 - 14/12/2026)"). Guardar isso inteiro estoura o
    String(20) de Horario.codigo e derruba a gravação."""
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    algoritmos_em_grafos = next(t for t in turmas if t.disciplina_nome == "ALGORITMOS EM GRAFOS")
    assert [h.codigo for h in algoritmos_em_grafos.horarios] == ["6T2345"]
    assert "(" not in algoritmos_em_grafos.horarios[0].codigo


def test_parse_turmas_mantem_todos_os_dias_de_turma_com_varios_horarios():
    """Uma turma com aula em vários dias vem com um único horário, e os
    códigos de todos os dias ficam juntos no mesmo texto — só o intervalo
    de datas deve ser cortado, não os dias."""
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    topicos_aeroespacial = next(
        t for t in turmas if t.disciplina_nome == "TÓPICOS ESPECIAIS EM ENGENHARIA AEROESPACIAL"
    )
    codigo = topicos_aeroespacial.horarios[0].codigo
    assert "35M5" in codigo and "35T1" in codigo
    assert "(" not in codigo


def test_parse_turmas_codigo_de_horario_cabe_na_coluna_do_banco():
    """Regressão do bug do Vitor: nenhum código de horário pode passar de
    20 caracteres (String(20) em Horario.codigo), senão a gravação falha
    com StringDataRightTruncation."""
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    for turma in turmas:
        for horario in turma.horarios:
            assert len(horario.codigo) <= 20, f"código {horario.codigo!r} estoura String(20)"


def test_parse_turmas_com_docente_a_definir_trata_vagas_em_branco_como_zero():
    """Achado ao rodar contra o SIGAA de verdade (unidade 672, Ceilândia):
    turma com docente "A DEFINIR" vem com a célula de vagas ofertadas em
    branco, e converter string vazia pra int quebrava o parser inteiro no
    meio da unidade."""
    html = FIXTURE_VAGAS_EM_BRANCO.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    assert len(turmas) == 1
    assert turmas[0].vagas_ofertadas == 0
    assert turmas[0].vagas_ocupadas == 0
