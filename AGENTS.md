AGENTS.md
# Projeto Athenas - Instrucoes para agentes

## Objetivo

O Projeto Athenas possui dois objetivos complementares:

1. Construir uma aplicacao real para organizacao de tarefas, compromissos, mensagens e informacoes relevantes para liderancas.
2. Servir como projeto principal de portfolio profissional no GitHub, demonstrando competencias valorizadas em vagas de desenvolvimento de software.

O projeto deve privilegiar qualidade demonstravel, clareza arquitetural, boas praticas e aprendizado profissional.

## Fontes de verdade do projeto

Antes de implementar mudanças relevantes, leia:

- `README.md`: estado atual e instruções de execução;
- `docs/product.md`: visão, problema, escopo e princípios do produto;
- `docs/architecture.md`: arquitetura técnica atual;
- `docs/roadmap.md`: sequência de evolução planejada.

O conteúdo atual do repositório tem prioridade sobre contexto de conversas anteriores.

Chats, prompts e memória de agentes são auxiliares e não devem substituir a documentação versionada.

Quando uma implementação alterar produto, arquitetura ou roadmap, atualize somente os documentos realmente afetados.

## Visao do produto

O Athenas deve futuramente integrar fontes como:

- Gmail
- Google Calendar
- Google Chat
- sistema proprio de tarefas e demandas
- OpenAI
- outras integracoes via API

A aplicacao devera unificar essas informacoes e permitir que um assistente de IA ajude o usuario a entender prioridades, compromissos, pendencias e contexto de trabalho.

## Stack definida

### Backend
- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- pytest
- uv

### Frontend
- Node.js
- TypeScript
- React
- Next.js
- pnpm

### Dados
- PostgreSQL
- pgvector

### Infraestrutura
- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions futuramente

### IA e integracoes
- OpenAI API
- Google OAuth
- Gmail API
- Google Calendar API
- Google Chat API

## Estrategia arquitetural

O repositorio deve ser organizado como monorepo, inicialmente contendo backend e frontend independentes.

Preferir arquitetura simples, modular e evolutiva.

Nao introduzir microservicos, Kubernetes, filas complexas ou infraestrutura distribuida sem necessidade concreta.

Separar claramente:

- API
- dominio
- servicos
- persistencia
- integracoes externas
- configuracao

## Regras de desenvolvimento

- Implementar de forma incremental.
- Evitar overengineering.
- Evitar arquivos ou abstrações sem uso real.
- Manter codigo legivel e tipado.
- Criar testes automatizados para comportamentos relevantes.
- Manter responsabilidades bem separadas.
- Preferir funcoes e componentes pequenos.
- Nao duplicar logica.
- Documentar decisoes arquiteturais relevantes.
- Atualizar README quando comandos ou arquitetura mudarem.
- Rodar testes antes de considerar uma tarefa concluida.

## Portfolio

O codigo deve ser compreensivel por outro desenvolvedor ou recrutador sem contexto previo.

Sempre que fizer sentido:

- manter README claro
- registrar arquitetura
- usar commits coerentes
- incluir testes
- incluir exemplos de configuracao
- demonstrar boas praticas de Git
- preparar CI/CD
- facilitar execucao local

Nao adicionar complexidade apenas para parecer mais avancado.

## Seguranca

Nunca commitar:

- tokens
- senhas
- API keys
- credenciais OAuth
- cookies
- dados reais de usuarios
- emails corporativos reais
- informacoes confidenciais da Pontual Garantidora

Usar arquivos `.env` locais e fornecer `.env.example`.

Dados usados em demonstracoes publicas devem ser ficticios.

## Ambiente

O projeto deve funcionar com:

- Python 3.13
- uv
- Node.js 24
- pnpm
- Docker Desktop / Docker Engine
- Docker Compose

Nao depender de instalacao local de PostgreSQL.

PostgreSQL e pgvector devem rodar via Docker.

## Metodo de trabalho

Antes de implementar alteracoes grandes:

1. inspecionar a estrutura existente
2. entender o objetivo da etapa
3. propor uma solucao simples
4. implementar
5. testar
6. documentar o que mudou

Evitar alterar partes nao relacionadas ao objetivo atual.

Quando houver varias solucoes validas, favorecer aquela que:

1. seja profissionalmente defensavel
2. ensine conceitos relevantes
3. produza evidencias uteis para portfolio
4. mantenha o sistema simples
