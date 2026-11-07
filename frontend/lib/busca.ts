export function normalizar(texto: string): string {
    return texto.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();
}

export function casaBusca(busca: string, ...campos: string[]): boolean {
    const termos = normalizar(busca).split(/\s+/).filter(Boolean);
    if (termos.length === 0) return true;
    const alvo = normalizar(campos.join(" "));
    return termos.every((termo) => alvo.includes(termo));
}