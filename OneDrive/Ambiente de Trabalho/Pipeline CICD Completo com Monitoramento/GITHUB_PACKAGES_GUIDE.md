# GitHub Packages - Guia de Uso

## 🐳 Docker Registry (Container Registry)

### Como está configurado:
- **Registry**: GitHub Container Registry (ghcr.io)
- **Imagem**: `ghcr.io/PauloRamos38/pipeline-cicd-monitoramento`
- **Triggers**: Push em `main` ou criação de tags `v*`

### Para usar a imagem Docker:

```bash
# Login no GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull da imagem
docker pull ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest

# Rodar a aplicação
docker run -p 5000:5000 ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest

# Testar health endpoint
curl http://localhost:5000/health
```

### Usar no Kubernetes:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pipeline-api
spec:
  containers:
  - name: api
    image: ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest
    ports:
    - containerPort: 5000
    env:
    - name: ENVIRONMENT
      value: production
    livenessProbe:
      httpGet:
        path: /health
        port: 5000
      initialDelaySeconds: 10
      periodSeconds: 30
    readinessProbe:
      httpGet:
        path: /ready
        port: 5000
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Usar no Docker Compose:

```yaml
version: '3.8'

services:
  api:
    image: ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:latest
    ports:
      - "5000:5000"
    environment:
      ENVIRONMENT: production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
```

---

## 📦 Python Package Registry

### Como está configurado:
- **Registry**: GitHub Packages (Python)
- **Pacote**: `pipeline-cicd-api`
- **Triggers**: Criação de tags `v*`

### Para usar o pacote Python:

#### 1. Configurar autenticação no `~/.pypirc`:

```ini
[distutils]
index-servers =
    github

[github]
repository: https://npm.pkg.github.com/PauloRamos38/pipeline-cicd-monitoramento
username: __token__
password: seu_github_token
```

#### 2. Instalar o pacote:

```bash
# Com pip (requer configuração do .pypirc acima)
pip install --index-url https://npm.pkg.github.com/PauloRamos38 pipeline-cicd-api

# Ou via requirements.txt:
# echo "pipeline-cicd-api @ git+https://github.com/PauloRamos38/pipeline-cicd-monitoramento@main" >> requirements.txt
```

#### 3. Usar no código Python:

```python
from main import app, tasks

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=False)
```

---

## 🚀 Como Triggerar as Publicações

### Docker Image (Automático):
```bash
# Automaticamente ao fazer push em main
git push origin main

# Ou com tag para versão específica
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Python Package (Com tag):
```bash
# Criar uma tag para triggerar a publicação
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# A workflow vai:
# 1. Build da distribuição Python
# 2. Rodar testes
# 3. Publicar no GitHub Packages
# 4. Upload de coverage para Codecov
```

---

## 📊 Visualizar Publicações

### Docker Registry:
1. Ir para: https://github.com/PauloRamos38/pipeline-cicd-monitoramento/pkgs/container/pipeline-cicd-monitoramento
2. Você verá todas as imagens publicadas com suas versões

### Python Package:
1. Ir para: https://github.com/PauloRamos38?tab=packages&repo_name=pipeline-cicd-monitoramento
2. Você verá o pacote `pipeline-cicd-api` com suas versões

---

## 🔐 Configurações de Segurança

### Permissões necessárias (já configuradas):
- ✅ `contents: read` - Ler código do repositório
- ✅ `packages: write` - Publicar pacotes
- ✅ `GITHUB_TOKEN` - Token automático do GitHub Actions

### Para usar privately:
Os pacotes são privados por padrão. Membros da organização podem acessar com:

```bash
# Login
gh auth login

# Instalar
pip install pipeline-cicd-api
```

---

## 📝 Workflows

### publish-docker.yml:
- **Trigger**: Push em `main` ou tags `v*`
- **Ações**:
  1. Build da imagem Docker
  2. Push para ghcr.io
  3. Testa a imagem (rodando pytest e health check)
  4. Cache para builds mais rápidos

### publish-python.yml:
- **Trigger**: Criação de tag `v*`
- **Ações**:
  1. Build do pacote Python
  2. Valida o pacote com `twine check`
  3. Publica no GitHub Packages
  4. Roda testes
  5. Upload de coverage para Codecov

---

## 🔄 Pipeline Completo

```
Seu código
    ↓
Push para GitHub
    ↓
Docker: Build automático → Teste → Publica em ghcr.io
Python: (Apenas em tags) Build → Teste → Publica em GitHub Packages
    ↓
Pronto para usar em qualquer lugar!
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Deploy no Kubernetes

```bash
# 1. Fazer tag
git tag v2.0.0
git push origin v2.0.0

# 2. GitHub Actions publica automaticamente
# 3. Atualizar seu deployment.yaml
kubectl set image deployment/api api=ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:v2.0.0
```

### Exemplo 2: Usar em outro projeto Python

```bash
# requirements.txt
pipeline-cicd-api==1.0.0  # após instalar do GitHub Packages

# Seu código
from main import app
app.run()
```

### Exemplo 3: Pipeline CI/CD completo

```yaml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy no Kubernetes
        run: |
          kubectl set image deployment/api \
            api=ghcr.io/PauloRamos38/pipeline-cicd-monitoramento:${{ github.ref_name }}
```

---

## ✅ Checklist

- [x] Docker Registry configurado
- [x] Python Package Registry configurado
- [x] Workflows de publicação automática
- [x] Testes integrados nos workflows
- [x] Health checks configurados
- [x] Dockerfile pronto para produção
- [x] setup.py com metadados corretos
- [x] Documentação completa

**Tudo pronto para usar! 🚀**
