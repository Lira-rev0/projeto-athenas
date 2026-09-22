import Link from "next/link";

import { isApiHealthy } from "@/lib/health";

export const dynamic = "force-dynamic";

export default async function Home() {
  const apiHealthy = await isApiHealthy();

  return (
    <main className="shell">
      <header className="masthead">
        <Link className="brand" href="/" aria-label="Athenas, página inicial">
          <span className="brand-mark" aria-hidden="true">A</span>
          ATHENAS
        </Link>
        <span className="phase">Fase 01 · Fundação</span>
      </header>

      <section className="intro" aria-labelledby="title">
        <p className="eyebrow">PROJETO EM DESENVOLVIMENTO</p>
        <h1 id="title">Mais contexto.<br />Mais clareza para liderar.</h1>
        <p className="lead">
          O Athenas está sendo construído para reunir tarefas, compromissos e
          mensagens em um só lugar — e ajudar lideranças a organizar o que importa.
        </p>
      </section>

      <section className="status-panel" aria-labelledby="status-title">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">PRIMEIROS PASSOS</p>
            <h2 id="status-title">A fundação está tomando forma.</h2>
          </div>
          <form action="/" method="get">
            <button type="submit">Verificar novamente <span aria-hidden="true">↗</span></button>
          </form>
        </div>
        <dl className="status-grid">
          <div className="status-item">
            <dt>Frontend</dt>
            <dd><span className="dot online" />Em funcionamento</dd>
            <dd className="status-description">Você está acessando a aplicação.</dd>
          </div>
          <div className="status-item">
            <dt>API</dt>
            <dd>
              <span className={`dot ${apiHealthy ? "online" : "offline"}`} />
              {apiHealthy ? "Conectada" : "Indisponível no momento"}
            </dd>
            <dd className="status-description">
              {apiHealthy ? "A API respondeu à verificação de saúde." : "Não foi possível confirmar a conexão. Tente novamente."}
            </dd>
          </div>
        </dl>
        <p className="status-note">
          Estado verificado ao carregar esta página. A verificação da API não inclui o banco de dados.
        </p>
      </section>

      <footer>
        <span>Projeto Athenas</span>
        <p>Fundação técnica em construção. Funcionalidades e integrações virão nas próximas etapas.</p>
      </footer>
    </main>
  );
}
