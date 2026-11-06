"""SDK Python pra Cerradinho API (RF13).

>>> from cerradinho_sdk import CerradinhoClient
>>> with CerradinhoClient("https://api.<ip>.sslip.io") as cerradinho:
...     cerradinho.listar_disciplinas()
"""

from .client import CerradinhoClient, ProfessorNaoEncontrado, RespostaInesperada

__all__ = ["CerradinhoClient", "ProfessorNaoEncontrado", "RespostaInesperada"]

__version__ = "1.0.0"
