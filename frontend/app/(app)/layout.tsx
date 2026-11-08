import Sidebar from "@/components/Sidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex min-h-screen flex-col md:flex-row">
            <Sidebar />
            {/* no celular, espaço pra barra de navegação fixa (4rem + área da barra de gestos do iPhone) não cobrir o fim da página */}
            <div className="flex min-w-0 flex-1 flex-col pb-[calc(4rem+env(safe-area-inset-bottom))] md:pb-0">{children}</div>
        </div>
    );
}