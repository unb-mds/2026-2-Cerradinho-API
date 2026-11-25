function iniciais(nome: string) {
    return nome.split(" ").slice(0, 2).map((parte) => parte[0]).join("");
}

export default function ProfessorAvatar({ nome, className = "h-9 w-9 text-xs" }: { nome: string; className?: string }) {
    return (
        <span className={`flex shrink-0 items-center justify-center rounded-full bg-muted-bg font-bold text-brand ${className}`}>
            {iniciais(nome)}
        </span>
    );
}