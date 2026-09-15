const professoresMock = [
    { id: "1", nome: "Ana Souza", departamento: "FGA", disciplinas: ["FGA0071", "FGA0066"] },
    { id: "2", nome: "Carlos Lima", departamento: "CIC", disciplinas: ["CIC0004"] },
    { id: "3", nome: "Beatriz Alves", departamento: "CIC", disciplinas: ["CIC0097"] },
];

export default function ProfessoresPage() {
    return (
        <main>
            <h1>Professores</h1>
            <ul>
                {professoresMock.map((p) => (
                    <li key={p.id}>
                        {p.nome} — {p.departamento} — Disciplinas: {p.disciplinas.join(", ")}
                    </li>
                ))}
            </ul>
        </main>
    );
}