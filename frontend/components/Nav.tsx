import Link from "next/link";

export default function Nav() {
    return (
        <nav>
            <Link href="/disciplinas">Disciplinas</Link>
            {" | "}
            <Link href="/cardapio">Cardápio</Link>
            {" | "}
            <Link href="/professores">Professores</Link>
            {" | "}
            <Link href="/salas">Salas</Link>
        </nav>
    );
}