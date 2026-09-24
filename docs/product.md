# Produto — Projeto Athenas

## Visão

O Athenas é uma aplicação para centralizar tarefas, compromissos, mensagens e contexto de trabalho que hoje ficam espalhados entre diferentes ferramentas.

A visão de longo prazo é permitir que uma liderança consiga entender rapidamente:

- o que precisa de atenção;
- quais tarefas estão pendentes;
- quais compromissos estão próximos;
- quais mensagens ou assuntos exigem resposta;
- quais decisões e contextos anteriores são relevantes;
- qual deve ser o próximo passo.

A aplicação deverá evoluir para um assistente de trabalho conectado somente às fontes autorizadas pelo usuário.

## Problema

Informações importantes de trabalho normalmente ficam fragmentadas entre:

- listas de tarefas;
- e-mail;
- calendário;
- mensagens;
- anotações;
- sistemas externos.

Essa fragmentação aumenta o esforço necessário para acompanhar compromissos, lembrar decisões e definir prioridades.

O Athenas busca transformar essas informações dispersas em contexto organizado e acionável.

## Público-alvo inicial

O produto foi inicialmente pensado para profissionais em posição de liderança ou gestão que lidam diariamente com múltiplas demandas, mensagens, reuniões e prioridades.

O projeto não depende, entretanto, de um setor ou empresa específica.

A versão pública e demonstrável do Athenas deve utilizar exclusivamente dados fictícios ou dados pertencentes ao próprio usuário.

## Proposta de valor

O Athenas deve permitir que o usuário tenha um único lugar para:

- registrar e acompanhar tarefas;
- visualizar compromissos;
- relacionar informações vindas de integrações externas;
- recuperar contexto de trabalho;
- receber auxílio de IA para organização e priorização.

A IA deve complementar os fluxos do produto, não substituir a estrutura de dados e as regras da aplicação.

## Princípios do produto

### 1. Contexto antes de automação

O sistema deve primeiro organizar corretamente as informações antes de tentar automatizar decisões.

### 2. Integrações explícitas

Nenhuma fonte externa deve ser acessada sem autorização clara do usuário.

### 3. IA como ferramenta

A inteligência artificial deve consumir contexto estruturado e executar operações autorizadas através de interfaces bem definidas.

Não devemos transformar toda funcionalidade em uma chamada a um modelo.

### 4. Evolução incremental

Cada nova capacidade deve surgir de uma necessidade concreta.

Evitar implementar infraestrutura antecipadamente para cenários ainda inexistentes.

### 5. Segurança e privacidade

Credenciais, tokens, mensagens reais, dados corporativos ou outros dados sensíveis nunca devem fazer parte do repositório público.

## Capacidades atuais

O Athenas atualmente possui:

- aplicação web em Next.js;
- API FastAPI;
- PostgreSQL;
- migrations com Alembic;
- domínio de tarefas;
- criação de tarefas;
- listagem de tarefas;
- atualização de status;
- exclusão;
- prioridades;
- prazos;
- testes automatizados;
- testes de integração com PostgreSQL;
- execução reproduzível com Docker.

## Capacidades planejadas

A evolução prevista inclui:

- experiência mais completa de gestão de tarefas;
- autenticação e usuários;
- integração com Google Calendar;
- integração com Gmail;
- integração com Google Chat;
- assistente com OpenAI;
- contexto estruturado entre diferentes fontes;
- automações controladas pelo usuário;
- deploy e observabilidade.

Essas capacidades não representam compromisso com uma implementação específica ou ordem imutável.

O roadmap é o documento responsável pela sequência de desenvolvimento.

## Fora de escopo por enquanto

Não fazem parte do escopo atual:

- microserviços;
- Kubernetes;
- arquitetura distribuída;
- event sourcing;
- sistemas complexos de filas;
- colaboração entre grandes equipes;
- substituição completa de ferramentas como Gmail ou Google Calendar;
- decisões autônomas da IA sem autorização do usuário.

## Objetivo como portfólio

Além de produto funcional, o Athenas é o principal projeto de portfólio do desenvolvedor.

Por isso, o projeto deve demonstrar competências através de evidências reais no repositório:

- arquitetura compreensível;
- Git e Pull Requests;
- Python;
- FastAPI;
- TypeScript;
- React e Next.js;
- PostgreSQL;
- SQLAlchemy;
- Alembic;
- Docker;
- APIs REST;
- integrações externas;
- testes unitários;
- testes de integração;
- testes de interface;
- CI/CD;
- segurança;
- documentação;
- inteligência artificial aplicada a um problema real.

A prioridade é demonstrar domínio técnico através de software funcional, e não aumentar artificialmente a quantidade de tecnologias utilizadas.