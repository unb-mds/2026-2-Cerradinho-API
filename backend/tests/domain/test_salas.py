from app.domain.salas import horario_para_intervalos_por_dia


def test_horario_para_intervalos_junta_aulas_consecutivas_num_bloco():
    assert horario_para_intervalos_por_dia("6T2345") == {"6": [("14:00", "17:50")]}


def test_horario_para_intervalos_separa_blocos_nao_consecutivos():
    # M1 e M3 não são consecutivos (falta M2) - dois blocos, não um
    assert horario_para_intervalos_por_dia("2M13") == {"2": [("08:00", "08:55"), ("10:00", "10:55")]}


def test_horario_para_intervalos_junta_na_virada_de_turno_sem_intervalo():
    # M5->T1 é direto, sem intervalo (ver comentário em _INICIO_AULA)
    assert horario_para_intervalos_por_dia("24M5 24T1") == {
        "2": [("12:00", "13:50")],
        "4": [("12:00", "13:50")],
    }


def test_horario_para_intervalos_combina_turno_e_dia_colados_com_espaco():
    # achado real: "35T6  35N1" -> "18:00 às 19:50" nos dois dias
    assert horario_para_intervalos_por_dia("35T6  35N1") == {
        "3": [("18:00", "19:50")],
        "5": [("18:00", "19:50")],
    }


def test_horario_para_intervalos_ignora_segmento_fora_do_padrao():
    assert horario_para_intervalos_por_dia("lixo") == {}
