import PageHeader from "@/components/PageHeader";
import SwaggerViewer from "./SwaggerViewer";

export default function DesenvolvedoresPage() {
    return (
        <main className="flex flex-1 flex-col pb-10">
            <PageHeader title="Desenvolvedores" sub="Documentação interativa da API" />
            <div className="px-10 pt-5">
                <SwaggerViewer />
            </div>
        </main>
    );
}