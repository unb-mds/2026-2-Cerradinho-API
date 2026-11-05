import asyncio
import time

import httpx

URL_BASE = "http://localhost:8000"
N_REQUISICOES_CACHE = 50
N_REQUISICOES_RATE_LIMIT = 70


async def _medir(client: httpx.AsyncClient, rota: str) -> tuple[int, float]:
    inicio = time.perf_counter()
    resposta = await client.get(rota)
    duracao = time.perf_counter() - inicio
    return resposta.status_code, duracao

async def testar_cache() -> None:
    print(f"\n== Cache: {N_REQUISICOES_CACHE} requisições concorrentes em /v1/disciplinas ==")
    async with httpx.AsyncClient(base_url=URL_BASE, timeout=30) as client:
        await client.get("/v1/disciplinas")  # Primeira requisição para popular o cache
        resultados = await asyncio.gather(
            *[_medir(client, "/v1/disciplinas") for _ in range(N_REQUISICOES_CACHE)])

    duracoes = [d for _, d in resultados]
    print(f"status: {sorted({s for s, _ in resultados})}")
    print(f"tempo médio: {sum(duracoes) / len(duracoes):.4f} segundos")
    print(f"tempo máximo: {max(duracoes):.4f} segundos")

async def testar_rate_limit() -> None:
    print(f"\n== Rate Limit: {N_REQUISICOES_RATE_LIMIT} requisições concorrentes em /v1/salas ==")
    async with httpx.AsyncClient(base_url=URL_BASE, timeout=30) as client:
        resultados = await asyncio.gather(
            *[_medir(client, "/v1/salas") for _ in range(N_REQUISICOES_RATE_LIMIT)])

    contagem: dict[int, int] = {}
    for status, _ in resultados:
        contagem[status] = contagem.get(status, 0) + 1
    print(f"contagem por status: {contagem}")
    if 429 in contagem:
        print(f"OK: limite entrou em ação, {contagem[429]} requisições foram bloqueadas")
    else:
        print("Atenção: limite não entrou em ação, nenhuma requisição foi bloqueada")

async def main() -> None:
    await testar_cache()
    await testar_rate_limit()

if __name__ == "__main__":
    asyncio.run(main())