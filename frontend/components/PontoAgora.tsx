// Ponto da caliandra que marca o que está acontecendo agora (aula em andamento).
// `claro` é para cima da faixa caliandra, onde a mesma cor sumiria.
export default function PontoAgora({ claro = false }: { claro?: boolean }) {
  return (
    <span
      aria-hidden
      className={`ponto-agora inline-block h-2 w-2 shrink-0 rounded-full ${claro ? "bg-faixa-texto-claro" : "bg-caliandra"}`}
    />
  );
}
