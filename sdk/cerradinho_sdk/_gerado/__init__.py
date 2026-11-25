"""Cliente HTTP gerado a partir do OpenAPI da Cerradinho API (RF11/RF13).

GERADO - não edite à mão. Rode `sdk/scripts/gerar_cliente.sh` pra regenerar
depois de mudar um router do backend. A camada ergonômica fica em
`cerradinho_sdk.client.CerradinhoClient`, que usa este módulo por baixo.
"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
