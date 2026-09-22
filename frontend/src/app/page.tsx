import Link from "next/link";

import { CreateTaskForm, TaskList } from "@/app/task-workspace";
import { isApiHealthy } from "@/lib/health";
import { listTasks } from "@/lib/task-api";

export const dynamic = "force-dynamic";

export default async function Home() {
  const [apiHealthy, tasks] = await Promise.all([isApiHealthy(), listTasks()]);

  return (
    <main className="shell">
      <header className="masthead">
        <Link className="brand" href="/" aria-label="Athenas, página inicial">
          <span className="brand-mark" aria-hidden="true">A</span>
          ATHENAS
        </Link>
        <span className="phase">Fase 02 · Tarefas</span>
      </header>

      <section className="intro" aria-labelledby="intro-title">
        <p className="eyebrow">CLAREZA PARA O SEU DIA</p>
        <h1 id="intro-title">Organize o que importa.</h1>
        <p className="lead">Tire as pendências da cabeça. Reúna suas tarefas, defina prioridades e acompanhe cada próximo passo.</p>
      </section>

      <div className="workspace">
        <CreateTaskForm />
        <TaskList tasks={tasks} />
      </div>

      <footer>
        <div className="api-status" title="A verificação da API não inclui o banco de dados.">
          <span className={`dot ${apiHealthy ? "online" : "offline"}`} aria-hidden="true" />
          <span>{apiHealthy ? "API conectada" : "API indisponível"}</span>
        </div>
        <p>Projeto Athenas · Um passo de cada vez.<br />Conexão verificada ao carregar a página; não inclui o banco.</p>
      </footer>
    </main>
  );
}
