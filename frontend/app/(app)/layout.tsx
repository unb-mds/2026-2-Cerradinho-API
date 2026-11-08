import Sidebar from "@/components/Sidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex min-h-screen flex-col md:flex-row">
            <Sidebar />
            {/* pb-16: no celular, espaço pra barra de navegação fixa não cobrir o fim da página */}
            <div className="flex min-w-0 flex-1 flex-col pb-16 md:pb-0">{children}</div>
        </div>
    );
}