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
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Exportando o OpenAPI do backend..."
(cd "$RAIZ/backend" && "$BACKEND_VENV/python" -c "
import json
from app.main import app
with open('$TMP_DIR/openapi.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
")

echo "Gerando o cliente..."
"$BACKEND_VENV/openapi-python-client" generate \
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

"$BACKEND_VENV/ruff" format "$SDK_DIR/cerradinho_sdk/_gerado" >/dev/null
"$BACKEND_VENV/ruff" check --fix --unsafe-fixes "$SDK_DIR/cerradinho_sdk/_gerado" >/dev/null || true

echo "Cliente regenerado em $SDK_DIR/cerradinho_sdk/_gerado"
