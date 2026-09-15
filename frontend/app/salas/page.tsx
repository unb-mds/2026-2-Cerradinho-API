const salasMock = [
    { id: "1", codigo: "BSA-T01", predio: "BSA Sul", capacidade: 50 },
    { id: "2", codigo: "FGA-A1", predio: "UnB Gama", capacidade: 40 },
    { id: "3", codigo: "ICC-Norte-101", predio: "ICC Norte", capacidade: 60 },
];

export default function SalasPage() {
    return (
        <main>
            <h1>Salas</h1>
            <ul>
                {salasMock.map((s) => (
                    <li key={s.id}>
                        {s.codigo} — {s.predio} — Capacidade: {s.capacidade}
                    </li>
                ))}
            </ul>
        </main>
    );
}