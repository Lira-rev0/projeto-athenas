# Projeto Athenas

Uma aplicação em desenvolvimento para reunir tarefas, compromissos, mensagens e contexto de trabalho de lideranças em um único lugar. O objetivo é reduzir a fragmentação das informações e, futuramente, apoiar a organização e a priorização com um assistente conectado às fontes autorizadas pelo usuário.

O Athenas também é um projeto de portfólio: código legível, decisões justificadas, testes e uma execução local reproduzível têm prioridade sobre complexidade.

## Status: Fase 1 — fundação

- Backend FastAPI com `GET /health` e `GET /health/database`.
- Página inicial com estado real da API, consultado no servidor a cada acesso.
- PostgreSQL em Docker, com pgvector habilitado pela primeira migration.
- Testes de saúde e configuração, lint e verificação de tipos.
- Nenhuma tabela de domínio ou integração externa implementada.

Esta base é destinada ao desenvolvimento local. Autenticação, HTTPS, gestão de segredos e credenciais de banco com privilégios restritos serão necessários antes de qualquer publicação. As portas do Compose são vinculadas a `127.0.0.1`.

## Arquitetura e stack

```mermaid
flowchart LR
    Browser[Navegador] --> Frontend[Next.js / React]
    Frontend -->|GET /health pelo servidor| Backend[FastAPI]
    Backend -->|SQLAlchemy + Psycopg| Database[(PostgreSQL + pgvector)]
    Alembic[Alembic] -->|Migrations| Database
```

| Camada | Tecnologias |
| --- | --- |
| Backend | Python 3.13, FastAPI, Pydantic Settings, SQLAlchemy 2.x, Psycopg 3, Alembic |
| Frontend | Node.js 24, Next.js 16, React 19, TypeScript, pnpm |
| Banco | PostgreSQL 17 e pgvector 0.8.6 |
| Qualidade | pytest, Ruff, ESLint e TypeScript |
| Execução | uv, Docker e Docker Compose |

Frontend e backend são projetos independentes dentro do monorepo, com dependências fixadas em `pnpm-lock.yaml` e `uv.lock`. Consulte as [decisões e o fluxo dos componentes](docs/architecture.md).

## Requisitos

Para executar tudo em containers:

- Git.
- Docker Engine e Docker Compose, ou Docker Desktop com WSL2 no Windows.
- Portas locais 3000, 8000 e 5432 disponíveis, ou alternativas no `.env`.

Para desenvolver e executar as verificações fora dos containers, também é preciso ter Python 3.13 disponível via uv, uv, Node.js 24 e pnpm 12.4.1. Não é necessária uma instalação local de PostgreSQL.

## Execução rápida com Docker

Na raiz do repositório, copie o exemplo de configuração:

```powershell
# PowerShell
Copy-Item .env.example .env
```

```sh
# Linux/macOS
cp .env.example .env
```

O exemplo contém somente valores fictícios de desenvolvimento. Preserve um `.env` existente; a cópia é necessária apenas na primeira execução. Depois:

```sh
docker compose config --quiet
docker compose up --build --wait
docker compose ps
```

O banco recebe um volume persistente. Depois que ele fica disponível, o backend executa `alembic upgrade head` antes de iniciar a API. O frontend aguarda a saúde do backend. O Compose usa builds de produção; alterações no código exigem rebuild.

| Endereço padrão | Resultado esperado |
| --- | --- |
| [localhost:3000](http://localhost:3000) | Página do Athenas com API conectada |
| [localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa da API |
| [localhost:8000/health](http://localhost:8000/health) | HTTP 200, `{"status":"ok"}` |
| [localhost:8000/health/database](http://localhost:8000/health/database) | HTTP 200, `{"status":"ok"}`, após consulta real ao banco |

Comandos úteis:

```sh
docker compose logs --tail=100 backend frontend database
docker compose exec backend alembic current
docker compose down
```

`down` preserva os dados. Não use `down --volumes` se quiser mantê-los. A alteração de `POSTGRES_PASSWORD` no `.env` não altera a senha de um banco já inicializado no volume; mantenha os valores consistentes.

## Desenvolvimento com recarga automática

Use este modo como alternativa ao Compose completo para evitar conflito de portas. Se os três serviços estiverem rodando, execute `docker compose down` primeiro. Com o `.env` da raiz preparado, inicie apenas o banco:

```sh
docker compose up -d --wait database
```

Em um terminal para o backend:

```sh
cd backend
uv sync --locked
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Em outro terminal, partindo da raiz:

```sh
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

O backend lê o `.env` da raiz automaticamente. O frontend usa `http://127.0.0.1:8000` por padrão. Se a API estiver em outra porta, copie `frontend/.env.example` para `frontend/.env.local` e ajuste `API_BASE_URL`. Essa variável permanece no servidor e não é exposta ao navegador.

`BACKEND_PORT` e `FRONTEND_PORT` no `.env` configuram apenas as portas publicadas pelo Compose. No modo local, ajuste `--port` no uvicorn e use `pnpm dev --port 3001` se precisar de outras portas. O Compose conecta os serviços por seus nomes e portas internos.

## Testes e verificações

No diretório `backend`:

```sh
uv sync --locked
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run alembic upgrade head --sql
```

Os testes unitários não precisam de banco. Eles verificam liveness independente do banco, sucesso da consulta, HTTP 503 em falhas de conexão/consulta, recuperação após timeout e proteção dos detalhes sensíveis. Os dois testes de integração são ignorados por padrão e aparecem como `skipped`, nunca como aprovados.

Com o banco disponível e as migrations aplicadas, execute a integração real a partir de `backend`:

```powershell
# PowerShell
$env:ATHENAS_RUN_INTEGRATION = "1"
uv run pytest -m integration
Remove-Item Env:ATHENAS_RUN_INTEGRATION
```

```sh
# Linux/macOS
ATHENAS_RUN_INTEGRATION=1 uv run pytest -m integration
```

No diretório `frontend`:

```sh
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

O lint é executado separadamente do build, conforme o [fluxo do Next.js](https://nextjs.org/docs/app/getting-started/installation). Para verificar o build local em execução, use `pnpm start`.

Para uma inspeção manual dos endpoints no PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/health/database
```

O primeiro endpoint verifica apenas a API. O segundo executa `SELECT 1` no banco e devolve HTTP 503 com `{"detail":"Database unavailable"}` quando a conexão ou a consulta falha, sem retornar credenciais ou detalhes internos.

## Migrations

Dentro de `backend`, com o banco em execução:

```sh
uv run alembic current
uv run alembic upgrade head
# Somente depois de adicionar modelos de domínio:
uv run alembic revision --autogenerate -m "describe schema change"
```

Os futuros modelos devem herdar de `app.db.base.Base` e ser importados em `migrations/env.py` para que o Alembic os encontre. Sempre revise uma migration gerada antes de aplicá-la. Não usamos `create_all()` no startup da aplicação.

A migration inicial cria apenas a extensão `vector`. O Alembic mantém sua tabela de controle `alembic_version`. O rollback remove a extensão sem `CASCADE`, de modo que objetos dependentes futuros impeçam a remoção acidental.

## Estrutura principal

```text
projeto-athenas/
├── backend/
│   ├── app/
│   │   ├── api/routes/health.py
│   │   ├── core/config.py
│   │   ├── db/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── uv.lock
│   └── Dockerfile
├── frontend/
│   ├── src/app/
│   ├── src/lib/health.ts
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── Dockerfile
├── docs/architecture.md
├── compose.yaml
├── .env.example
├── .gitignore
├── AGENTS.md
└── README.md
```

As regras permanentes de contribuição estão em [AGENTS.md](AGENTS.md). Arquivos `.env`, ambientes virtuais, dependências, caches e dados locais não devem ser versionados. Os exemplos e testes usam exclusivamente dados fictícios.

## Próximos passos planejados

1. Definir o primeiro fluxo de tarefas e demandas, seus campos e critérios de aceite.
2. Implementar o primeiro módulo de domínio com migration, API, testes e interface.
3. Automatizar as verificações em GitHub Actions.
4. Planejar autenticação e autorização antes de conectar dados pessoais ou corporativos.
5. Integrar gradualmente Google OAuth, Gmail, Calendar, Chat e OpenAI.

Integrações, RAG, embeddings e automações inteligentes pertencem a etapas futuras. Esta fase não inclui autenticação real, filas, Redis, microserviços ou Kubernetes.
