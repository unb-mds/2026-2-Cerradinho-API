#!/usr/bin/env bash
# Regera sdk/cerradinho_sdk/_gerado a partir do OpenAPI atual do backend.
#
# O cliente de baixo nível (sdk/cerradinho_sdk/_gerado/) é gerado pelo
# openapi-python-client a partir do schema que o FastAPI já produz (RF11) -
# não é escrito à mão, pra nunca ficar fora de sincronia com os routers.
# A camada ergonômica (cerradinho_sdk/client.py) é escrita à mão por cima
# dele e não é tocada por este script.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_VENV="$RAIZ/backend/venv/bin"
SDK_DIR="$RAIZ/sdk"
# PYTHON roda o gerador e o ruff - precisa de `pip install -e "sdk/[dev]"`,
# não do venv do backend (que não tem openapi-python-client). Pode ser
# sobrescrito (ex. PYTHON=.venv/bin/python) se não for o python padrão.
PYTHON="${PYTHON:-python3}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if ! "$PYTHON" -c "import openapi_python_client" >/dev/null 2>&1; then
    echo "openapi-python-client não está instalado em '$PYTHON'." >&2
    echo "Rode: pip install -e \"$SDK_DIR\"[dev]" >&2
    echo "(ou defina PYTHON=/caminho/do/venv/com/isso, se não for o python padrão)" >&2
    exit 1
fi
if ! "$PYTHON" -c "import ruff" >/dev/null 2>&1; then
    echo "ruff não está instalado em '$PYTHON' (também vem do extra [dev] do sdk/)." >&2
    exit 1
fi

echo "Exportando o OpenAPI do backend..."
(cd "$RAIZ/backend" && "$BACKEND_VENV/python" -c "
import json
from app.main import app
with open('$TMP_DIR/openapi.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
")

echo "Gerando o cliente..."
"$PYTHON" -m openapi_python_client generate \
    --path "$TMP_DIR/openapi.json" \
    --meta none \
    --output-path "$TMP_DIR/gerado" \
    --overwrite

rm -rf "$SDK_DIR/cerradinho_sdk/_gerado"
mv "$TMP_DIR/gerado" "$SDK_DIR/cerradinho_sdk/_gerado"

cat > "$SDK_DIR/cerradinho_sdk/_gerado/__init__.py" <<'EOF'

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
EOF

echo "Formatando e verificando o código gerado..."
"$PYTHON" -m ruff format "$SDK_DIR/cerradinho_sdk/_gerado"
# E501 (linha longa) é esperado nas docstrings geradas e não é verificado
# pelo CI pra este diretório (ver sdk/ruff.toml) - ignorado explicitamente
# aqui, não escondido: qualquer outro achado (import não usado, nome
# indefinido etc.) continua falhando o script, sem `|| true` escondendo erro
# de verdade.
"$PYTHON" -m ruff check --fix --ignore E501 "$SDK_DIR/cerradinho_sdk/_gerado"

echo "Cliente regenerado em $SDK_DIR/cerradinho_sdk/_gerado"
