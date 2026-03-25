# Taskflow Portfolio

Gerenciador de tarefas fullstack com frontend moderno (HTML, CSS e JavaScript puro) e API Node.js com Express.

## Estrutura

- frontend: interface responsiva com dark mode, filtros e busca
- backend: API REST com persistencia em arquivo JSON

## Requisitos atendidos

- Layout moderno e responsivo (mobile-first)
- Dark mode com persistencia no localStorage
- Navbar/sidebar de navegacao
- CRUD de tarefas: adicionar, concluir/reabrir e excluir
- Reordenacao com drag and drop (arrastar e soltar)
- Filtros: todas, pendentes, concluidas
- Busca por titulo
- Animacoes de entrada e remocao de cards
- Backend em Node.js + Express + CORS
- Rotas GET/POST/PUT/DELETE em /tasks
- Sincronizacao da ordem no backend via PUT /tasks/reorder
- Persistencia em backend/tasks.json
- Contador de pendentes
- Exportacao de tarefas em JSON
- Validacao de formulario (titulo obrigatorio)

## Checklist final da proposta

- [x] Estrutura frontend/backend criada
- [x] Backend com Express e CORS
- [x] CRUD completo de tarefas
- [x] Frontend responsivo e moderno
- [x] Dark mode com persistencia
- [x] Filtros e busca por titulo
- [x] Animacoes ao adicionar/remover
- [x] Drag and drop com sincronizacao no backend
- [ ] Publicacao no GitHub (executar comandos abaixo)

## Como rodar

### 1) Backend

Na pasta backend:

npm install
node server.js

API disponivel em:

<http://localhost:3000/tasks>

### 2) Frontend

Abra a pasta frontend no VS Code e inicie com Live Server (porta 5500).

URL esperada:

<http://127.0.0.1:5500/frontend/index.html>

## Endpoints

- GET /tasks: lista todas as tarefas
- POST /tasks: cria tarefa
- PUT /tasks/:id: atualiza tarefa (ex: completed)
- DELETE /tasks/:id: remove tarefa

### Exemplo de payload POST

{
  "title": "Estudar API",
  "description": "Revisar endpoints do projeto",
  "priority": "media",
  "dueDate": "2026-03-25"
}
