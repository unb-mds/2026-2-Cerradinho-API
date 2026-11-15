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
    """Regressão do bug do Vitor: código de horário não pode passar do
    String(100) de Horario.codigo, senão a gravação falha com
    StringDataRightTruncation. Turma com aula em vários turnos junta os
    segmentos num só código ("35M5 35T1"), e algumas unidades (Darcy)
    chegam a 4+ segmentos - por isso o limite não é mais 20."""
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    for turma in turmas:
        for horario in turma.horarios:
            assert len(horario.codigo) <= 100, f"código {horario.codigo!r} estoura String(100)"


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


# Testes escritos a partir dos mutantes sobreviventes do teste de mutação
# (RNF09, `python -m scripts.mutacao app/scrapers/disciplinas/parser.py`):
# os testes com a fixture real não conferiam cada campo da turma.

LINHA_COMPLETA = """
<tr class="linhaPar">
  <td> 03 </td>
  <td>
    2026.2
  </td>
  <td>
    ANA SOUZA (60h)<br/>
    BRUNO LIMA (30h)
  </td>
  <td>
    24M12 (10/08/2026 - 14/12/2026)
    <div class="popUp">
        Segunda-feira 08:00 às 09:50  <br>
    </div>
  </td>
  <td>
    6T23 (10/08/2026 - 14/12/2026)
  </td>
  <td> 45 </td>
  <td> 12 </td>
  <td> FCTE - I9 </td>
</tr>
"""


def _tabela(*linhas: str) -> str:
    agrupador = (
        '<tr class="agrupador"><td colspan="8">'
        '<span class="tituloDisciplina">FGA0242 - MÉTODOS DE DESENVOLVIMENTO DE SOFTWARE</span></td></tr>'
    )
    return f'<div id="turmasAbertas"><table class="listagem"><tbody>{agrupador}{"".join(linhas)}</tbody></table></div>'


def test_parse_turmas_le_cada_coluna_no_campo_certo_e_sem_espacos():
    [turma] = parse_turmas(_tabela(LINHA_COMPLETA))

    assert turma.model_dump() == {
        "disciplina_codigo": "FGA0242",
        "disciplina_nome": "MÉTODOS DE DESENVOLVIMENTO DE SOFTWARE",
        "numero": "03",
        "ano_periodo": "2026.2",
        "professores": [{"nome": "ANA SOUZA (60h)"}, {"nome": "BRUNO LIMA (30h)"}],
        "horarios": [
            {"codigo": "24M12", "descricao": "Segunda-feira 08:00 às 09:50"},
            {"codigo": "6T23", "descricao": ""},
        ],
        "sala": {"descricao": "FCTE - I9"},
        "vagas_ofertadas": 45,
        "vagas_ocupadas": 12,
    }


def test_parse_turmas_aceita_linha_com_coluna_a_mais_no_fim():
    linha_com_coluna_extra = LINHA_COMPLETA.replace("</tr>", "<td>coluna nova</td></tr>")

    [turma] = parse_turmas(_tabela(linha_com_coluna_extra))

    assert (turma.numero, turma.sala.descricao) == ("03", "FCTE - I9")


def test_parse_turmas_tabela_sem_tbody_devolve_vazio():
    assert parse_turmas('<div id="turmasAbertas"><table class="listagem"></table></div>') == []


def test_parse_turmas_ignora_linha_de_tabela_aninhada_dentro_de_uma_celula():
    aninhada = "<table><tr>" + "<td>x</td>" * 8 + "</tr></table>"
    linha = LINHA_COMPLETA.replace("<td> FCTE - I9 </td>", f"<td> FCTE - I9 {aninhada}</td>")

    turmas = parse_turmas(_tabela(linha))

    assert [t.numero for t in turmas] == ["03"]
