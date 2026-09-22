import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Athenas | Fundação do projeto",
  description:
    "Um espaço para reunir tarefas, compromissos e contexto de trabalho. Projeto em desenvolvimento.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
