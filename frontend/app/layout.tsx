import type { Metadata } from "next";
import { DM_Sans, DM_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
});

const dmMono = DM_Mono({
  variable: "--font-dm-mono",
  weight: ["400", "500"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Cerradinho",
  description: "API aberta que consolida dados institucionais da UnB.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="pt-Br"
      className={`${dmSans.variable} ${dmMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col md:flex-row">
        <Sidebar />
        {/* pb-16: no celular, espaço pra barra de navegação fixa não cobrir o fim da página */}
        <div className="flex min-w-0 flex-1 flex-col pb-16 md:pb-0">{children}</div>
      </body>
    </html>
  );
}
