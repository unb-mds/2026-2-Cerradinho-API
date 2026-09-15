const cardapioMock = [
    { dia: "Segunda", refeicao: "Almoço", pratoPrincipal: "Frango grelhado", opcaoVegetariana: "Grão-de-bico", sobremesa: "Fruta" },
    { dia: "Terça", refeicao: "Almoço", pratoPrincipal: "Carne de panela", opcaoVegetariana: "Tofu ao molho", sobremesa: "Gelatina" },
    { dia: "Quarta", refeicao: "Almoço", pratoPrincipal: "Peixe assado", opcaoVegetariana: "Legumes salteados", sobremesa: "Fruta" },
];

export default function CardapioPage() {
    return (
        <main>
            <h1>Cardápio do RU</h1>
            <ul>
                {cardapioMock.map((c) => (
                    <li key={c.dia}>
                        {c.dia} ({c.refeicao}) — {c.pratoPrincipal} / Veg: {c.opcaoVegetariana} — {c.sobremesa}
                    </li>
                ))}
            </ul>
        </main>
    );
}