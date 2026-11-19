import { BookIcon, BowlIcon, DoorOpenIcon, UserIcon } from "@/components/Icons";

// Os quatro módulos do app, cada um com uma cor do cerrado. As classes ficam
// escritas por extenso pra o Tailwind enxergar.
//   cor: ícone e detalhe em fundo claro · viva: na sidebar verde-escura
//   fundo: tinta suave atrás do ícone · borda: marca do item ativo na navegação
// `curto` é o rótulo da barra inferior do celular, onde cada item tem ~1/5 da largura.
export const MODULOS = [
  {
    href: "/disciplinas",
    label: "Disciplinas",
    curto: "Disciplinas",
    Icon: BookIcon,
    cor: "text-buriti",
    viva: "text-buriti-viva",
    fundo: "bg-buriti/12",
    borda: "border-buriti-viva",
  },
  {
    href: "/cardapio",
    label: "Cardápio",
    curto: "Cardápio",
    Icon: BowlIcon,
    cor: "text-ipe",
    viva: "text-ipe-viva",
    fundo: "bg-ipe/15",
    borda: "border-ipe-viva",
  },
  {
    href: "/professores",
    label: "Professores",
    curto: "Professores",
    Icon: UserIcon,
    cor: "text-terra",
    viva: "text-terra-viva",
    fundo: "bg-terra/12",
    borda: "border-terra-viva",
  },
  {
    href: "/salas/vazias",
    label: "Salas Vazias",
    curto: "Salas",
    Icon: DoorOpenIcon,
    cor: "text-caliandra",
    viva: "text-caliandra-viva",
    fundo: "bg-caliandra/12",
    borda: "border-caliandra-viva",
  },
] as const;

export type Modulo = (typeof MODULOS)[number];

export function modulo(href: Modulo["href"]): Modulo {
  return MODULOS.find((m) => m.href === href)!;
}
