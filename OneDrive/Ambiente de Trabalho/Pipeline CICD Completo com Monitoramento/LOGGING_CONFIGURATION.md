# Configuração de Logging e Tratamento de Erros

## 🎯 Objetivo

Garantir que a aplicação roda com logs profissionais e limpos, sem erros desnecessários no console.

---

## 📋 Arquivos de Configuração

### 1. `gunicorn_config.py`
Configuração do servidor WSGI (Gunicorn):
- **Workers**: Configurado automaticamente (CPU cores)
- **Timeout**: 60 segundos
- **Logging**: Formato profissional e parsável
- **Hooks**: Mensagens de inicialização e encerramento

### 2. `logging_config.py`
Configuração de logging da aplicação:
- **Console**: Logs estruturados e legíveis
- **Arquivo**: Logs com rotação automática (10MB)
- **Níveis**: INFO (produção) ou DEBUG (desenvolvimento)
- **Supressão**: Reduz ruído de bibliotecas externas

### 3. `main.py`
Aplicação Flask com tratamento de erros:
- **Error Handlers**: 404 e 500 com respostas JSON
- **Logging**: Cada ação registrada
- **Validação**: Entrada validada antes de processar

---

## 🔧 Como Funciona

### Fluxo de Log

```
Requisição HTTP
    ↓
Gunicorn recebe
    ↓
main.py processa
    ↓
Logging Configuration
    ├─ Console (stdout) → Você vê em tempo real
    └─ Arquivo (rotating) → Histórico
    ↓
Resposta HTTP
```

### Níveis de Log

| Nível | Quando usado | Exemplo |
|-------|-------------|---------|
| **DEBUG** | Desenvolvimento | Valores de variáveis, stack traces |
| **INFO** | Produção | Requisições, criações de objetos |
| **WARNING** | Algo suspeito | Arquivo não encontrado, timeout |
| **ERROR** | Erro na lógica | Falha ao processar request |
| **CRITICAL** | Sistema quebrou | Conexão perdida, OUT OF MEMORY |

---

## 🚀 Usando em Diferentes Ambientes

### Produção (Docker)

```bash
docker run -e ENVIRONMENT=production -e LOG_LEVEL=info minha-app
```

**Console limpo:**
```
2026-02-04 10:30:45 | main | INFO     | ✅ Server started with 4 workers
2026-02-04 10:30:45 | main | INFO     | 🚀 Listening on 0.0.0.0:5000
2026-02-04 10:30:50 | main | INFO     | POST /tasks - Created task 1
```

### Desenvolvimento (Local)

```bash
ENVIRONMENT=development LOG_LEVEL=debug python main.py
```

**Console detalhado:**
```
2026-02-04 10:30:45 | main | INFO     | setup_logging:30 | ✅ Server started with 4 workers
2026-02-04 10:30:50 | main | DEBUG    | create_task:98 | Validating task: {'title': 'Test'}
2026-02-04 10:30:50 | main | INFO     | create_task:115 | POST /tasks - Created task 1
```

---

## 🛡️ Tratamento de Erros

### Tipos de Erros Tratados

#### 1. **Erros 4xx (Cliente)**
- 400: Requisição inválida
- 404: Recurso não encontrado
- Retorna JSON com mensagem clara

#### 2. **Erros 5xx (Servidor)**
- 500: Erro interno
- Registra em log
- Retorna JSON sem exposer detalhes

#### 3. **Erros de Validação**
- Campos faltando
- Tipos incorretos
- Registra e retorna 400

---

## 📊 Exemplo de Logs Esperados

### Cenário: Criar Task

**Request:**
```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Nova task"}'
```

**Logs (produção):**
```
2026-02-04 10:30:50 | main | INFO     | POST /tasks - Created task 1
```

**Logs (desenvolvimento):**
```
2026-02-04 10:30:50 | main | DEBUG    | create_task:98 | Incoming request data: {'title': 'Nova task'}
2026-02-04 10:30:50 | main | DEBUG    | create_task:105 | task_id_counter incremented to 1
2026-02-04 10:30:50 | main | INFO     | create_task:115 | POST /tasks - Created task 1
```

---

## ⚠️ Erros que NÃO devem aparecer

❌ **Não deve ver:**
```
WARNING: This is a development server. Do not use it in production!
/usr/local/lib/python3.11/site-packages/werkzeug/__init__.py:193
```

❌ **Não deve ver:**
```
[2026-02-04 10:30:50 +0000] [15] [INFO] Worker spawned (pid: 15)
[2026-02-04 10:30:50 +0000] [16] [INFO] Worker spawned (pid: 16)
```

✅ **Deve ver (limpo):**
```
2026-02-04 10:30:50 | main | INFO     | ✅ Server started with 4 workers
2026-02-04 10:30:50 | main | INFO     | 🚀 Listening on 0.0.0.0:5000
```

---

## 🔍 Monitorando Logs

### Em Docker

```bash
# Ver logs em tempo real
docker logs -f nome-container

# Ver últimas 100 linhas
docker logs --tail 100 nome-container

# Com filtro (apenas ERROs)
docker logs nome-container | grep ERROR
```

### Em Kubernetes

```bash
# Ver logs do pod
kubectl logs deployment/meu-deployment

# Seguir logs em tempo real
kubectl logs -f deployment/meu-deployment

# Ver logs anteriores (se pod crasheou)
kubectl logs deployment/meu-deployment --previous
```

### Em Arquivo

```bash
# Logar vai criar /tmp/pipeline-api-20260204.log
# Com rotação automática a cada 10MB
ls -lh /tmp/pipeline-api-*.log

# Acompanhar novo arquivo
tail -f /tmp/pipeline-api-20260204.log
```

---

## 🎛️ Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `ENVIRONMENT` | production | Modo: production ou development |
| `LOG_LEVEL` | INFO | Nível de log: DEBUG, INFO, WARNING, ERROR |
| `LOG_DIR` | /tmp | Diretório para logs em arquivo |
| `FLASK_APP` | main.py | Arquivo principal da aplicação |
| `PORT` | 5000 | Porta da aplicação |

---

## 💡 Exemplos de Uso

### Exemplo 1: Produção com logs reduzidos

```bash
docker run \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=warning \
  ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest
```

### Exemplo 2: Desenvolvimento com debug

```bash
docker run \
  -e ENVIRONMENT=development \
  -e LOG_LEVEL=debug \
  ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest
```

### Exemplo 3: Logs em arquivo

```bash
docker run \
  -v /var/log/app:/tmp \
  -e LOG_DIR=/tmp \
  ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest
```

---

## ✅ Checklist de Verificação

Ao rodar a aplicação, você deve ver:

- [x] ✅ Server started with X workers
- [x] 🚀 Listening on 0.0.0.0:5000
- [x] Nenhuma mensagem de WARNING ou ERROR
- [x] Logs limpos e legíveis
- [x] Health check funcionando: GET /health → 200

Você NÃO deve ver:

- [ ] Stacktraces desnecessários
- [ ] Warnings de desenvolvimento
- [ ] Mensagens de "localhost" ou "insecure"
- [ ] Erros de módulos não carregados
- [ ] Warnings de deprecation desnecessários

---

## 🚨 Resolvendo Problemas

### Problema: Muitos logs desnecessários

**Solução:**
```bash
docker run -e LOG_LEVEL=warning seu-container
```

### Problema: Não consigo ver nada

**Solução:**
```bash
docker run -e LOG_LEVEL=debug seu-container
```

### Problema: Logs aparecem e desaparecem

**Solução:** Use `docker logs -f` para seguir em tempo real

### Problema: Arquivo de log muito grande

**Solução:** Está configurado para rotação automática em 10MB
- Antigos: `/tmp/pipeline-api-20260203.log`
- Atual: `/tmp/pipeline-api-20260204.log`

---

## 📈 Métricas de Log

Tipo de eventos registrados:

1. **Inicialização** (INFO)
   - Server started
   - Listening on port
   - Workers spawned

2. **Requisições** (INFO)
   - GET /tasks
   - POST /tasks (task created)
   - PUT /tasks/<id> (updated)
   - DELETE /tasks/<id> (deleted)

3. **Validação** (WARNING)
   - Missing required field
   - Invalid data type

4. **Erros** (ERROR)
   - Task not found
   - Internal server error

5. **Encerramento** (INFO)
   - Shutting down server
   - Cleanup completed

---

**Tudo configurado para um console limpo, profissional e sem ruídos! 🎉**
