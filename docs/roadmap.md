# Roadmap — Projeto Athenas

Este documento registra a direção atual do desenvolvimento do Athenas.

O roadmap não é imutável. As fases podem ser ajustadas conforme o produto evolui, desde que mudanças relevantes sejam documentadas.

Legenda:

- ✅ concluída
- 🚧 em andamento
- ⏳ planejada

## Fase 1 — Fundação técnica ✅

Objetivo: criar uma base profissional e reproduzível para o desenvolvimento.

Entregue:

- monorepo;
- FastAPI;
- Next.js;
- TypeScript;
- PostgreSQL 17;
- pgvector;
- SQLAlchemy;
- Alembic;
- Docker Compose;
- endpoints de saúde;
- testes;
- lint e type checking;
- documentação inicial de arquitetura.

Resultado:

Frontend, backend e banco executando de forma integrada e reproduzível.

---

## Fase 2 — Primeiro vertical slice: tarefas ✅

Objetivo: implementar o primeiro domínio real de ponta a ponta.

Entregue:

- entidade Task;
- UUID;
- título;
- descrição;
- status;
- prioridade;
- prazo;
- timestamps;
- migration versionada;
- CRUD REST;
- filtros de API;
- validação com Pydantic;
- serviço de tarefas;
- tratamento de transações;
- testes de unidade;
- testes de integração com PostgreSQL real;
- interface de tarefas;
- criação;
- mudança de status;
- exclusão;
- feedback de erro e sucesso.

Resultado:

Primeiro fluxo funcional completo:

Frontend → API → regras → persistência → PostgreSQL.

---

## Fase 3 — Maturidade do fluxo de tarefas e qualidade ⏳

Objetivo: transformar o primeiro vertical slice em um fluxo mais completo e automatizar sua validação.

Planejado:

### Produto

- edição completa de tarefas pela interface;
- filtros por status e prioridade na interface;
- paginação;
- melhorias de usabilidade quando justificadas pelo fluxo real.

### Testes

- introduzir testes E2E automatizados de navegador;
- cobrir os principais fluxos:
  - criação;
  - edição;
  - filtro;
  - mudança de status;
  - exclusão;
  - falhas relevantes.

### CI

Criar GitHub Actions para executar automaticamente em Pull Requests:

Backend:

- pytest;
- Ruff;
- verificação de formatação.

Frontend:

- ESLint;
- TypeScript;
- build.

Avaliar a execução dos testes de integração com PostgreSQL dentro do CI.

Resultado esperado:

Pull Requests do Athenas passam a possuir validação automática e o fluxo principal de tarefas fica coberto de ponta a ponta.

---

## Fase 4 — Identidade e autorização ⏳

Objetivo: preparar o sistema para dados pertencentes a usuários reais.

Planejado:

- entidade de usuário;
- autenticação;
- Google OAuth;
- sessão segura;
- associação de tarefas a usuários;
- autorização;
- proteção das rotas;
- testes de isolamento entre usuários.

Nenhuma integração com e-mails ou calendários reais deve ocorrer antes desta fase.

---

## Fase 5 — Google Calendar ⏳

Objetivo: realizar a primeira integração externa de produtividade.

Planejado:

- conexão autorizada com Google Calendar;
- leitura de calendários;
- leitura de eventos;
- persistência ou sincronização somente quando necessário;
- tratamento de renovação/revogação de autorização;
- representação de compromissos no Athenas.

Resultado esperado:

O usuário consegue consultar tarefas e compromissos no mesmo produto.

---

## Fase 6 — Gmail ⏳

Objetivo: incorporar contexto relevante de e-mail.

Planejado:

- acesso autorizado ao Gmail;
- leitura controlada de mensagens;
- identificação de mensagens relevantes;
- associação entre mensagens e demandas quando houver regra clara;
- tratamento seguro de conteúdo externo.

Evitar transformar automaticamente todo e-mail em tarefa.

---

## Fase 7 — Assistente de IA ⏳

Objetivo: adicionar inteligência artificial sobre dados estruturados e autorizados.

Planejado:

- integração com OpenAI;
- chat do Athenas;
- ferramentas para consultar tarefas;
- ferramentas para consultar calendário;
- ferramentas para consultar contexto permitido;
- respostas fundamentadas nos dados disponíveis;
- ações somente mediante autorização adequada.

RAG, embeddings e pgvector devem ser adicionados somente se houver caso de uso que justifique recuperação semântica.

---

## Fase 8 — Google Chat e novas fontes ⏳

Objetivo: ampliar as fontes de contexto disponíveis ao Athenas.

Planejado:

- avaliar capacidades e restrições da API do Google Chat;
- integrar somente os dados e operações tecnicamente viáveis;
- manter conectores desacoplados da lógica principal do domínio.

Outras integrações poderão ser avaliadas posteriormente.

---

## Fase 9 — Publicação e maturidade operacional ⏳

Objetivo: transformar o projeto local em uma aplicação demonstrável publicamente.

Planejado:

- ambiente de deploy;
- banco gerenciado;
- HTTPS;
- gestão de secrets;
- migrations no deploy;
- logging estruturado;
- observabilidade básica;
- monitoramento de erros;
- estratégia de backup;
- documentação de operação.

Revisar também:

- segurança;
- dependências;
- performance;
- acessibilidade;
- experiência mobile.

---

## Princípios do roadmap

O Athenas não deve avançar de fase apenas para aumentar a quantidade de funcionalidades.

Antes de cada nova fase:

1. confirmar que a fase anterior está estável;
2. revisar o problema que a próxima fase resolve;
3. manter o menor escopo capaz de demonstrar o conceito;
4. implementar testes relevantes;
5. atualizar documentação;
6. concluir através de Pull Request.

Decisões arquiteturais importantes podem gerar ADRs em `docs/decisions/`.