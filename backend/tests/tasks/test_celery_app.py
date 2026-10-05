import inspect
import json
import subprocess
import sys
from pathlib import Path

import pytest

from app.celery_app import celery_app

BACKEND_DIR = Path(__file__).resolve().parents[2]

TASKS_ESPERADAS = [
    "app.tasks.scraping.scrape_disciplinas_task",
    "app.tasks.cardapio.scrape_cardapio_task",
]

AGENDAMENTOS = sorted(celery_app.conf.beat_schedule.items())
IDS_AGENDAMENTOS = [nome for nome, _ in AGENDAMENTOS]

# carrega só o celery_app e os módulos do include=[...], igual o worker faz ao subir
_BOOT_DO_WORKER = """
import json
from app.celery_app import celery_app
celery_app.loader.import_default_modules()
print(json.dumps(sorted(celery_app.tasks)))
"""


@pytest.fixture(scope="module")
def tasks_do_worker():
    # processo novo de propósito: aqui dentro o test_scraping.py já importou
    # app.tasks.scraping, o que registra a task mesmo que ela saia do include
    resultado = subprocess.run(
        [sys.executable, "-c", _BOOT_DO_WORKER], cwd=BACKEND_DIR, capture_output=True, text=True, check=True
    )
    return set(json.loads(resultado.stdout.strip().splitlines()[-1]))


@pytest.mark.parametrize("nome_task", TASKS_ESPERADAS)
def test_task_registrada_no_boot_do_worker(tasks_do_worker, nome_task):
    # regressão: o autodiscover procurava app.tasks.tasks e a task de disciplinas
    # nunca era registrada, então o agendamento semanal não rodava
    assert nome_task in tasks_do_worker


def test_existe_agendamento_para_cada_task():
    agendadas = {entrada["task"] for _, entrada in AGENDAMENTOS}
    assert agendadas == set(TASKS_ESPERADAS)


@pytest.mark.parametrize("nome_agendamento, entrada", AGENDAMENTOS, ids=IDS_AGENDAMENTOS)
def test_agendamento_aponta_para_task_registrada(tasks_do_worker, nome_agendamento, entrada):
    assert entrada["task"] in tasks_do_worker, f"{nome_agendamento} agenda uma task que o worker não conhece"


@pytest.mark.parametrize("nome_agendamento, entrada", AGENDAMENTOS, ids=IDS_AGENDAMENTOS)
def test_agendamento_passa_argumentos_compativeis_com_a_task(nome_agendamento, entrada):
    # regressão: o agendamento chegou a chamar scrape_disciplinas_task sem
    # nivel/ano/periodo - o CI passava e a task só quebraria no domingo, no worker
    celery_app.loader.import_default_modules()
    task = celery_app.tasks[entrada["task"]]
    try:
        inspect.signature(task.run).bind(*entrada.get("args", ()), **entrada.get("kwargs", {}))
    except TypeError as erro:
        pytest.fail(f"{nome_agendamento} chama {entrada['task']} com argumentos inválidos: {erro}")
