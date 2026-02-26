# 🚀 Projeto DevOps - Pipeline CI/CD Completo

## 📋 Sobre o Projeto

Este projeto demonstra a implementação completa de um pipeline DevOps, incluindo CI/CD, containerização, orquestração com Kubernetes, monitoramento e logs.

**Status:** ✅ PRONTO PARA PRODUÇÃO (Go Live)

## ✨ Destaques

- ✅ **Aplicação**: Flask API 1.0.0 com 92% cobertura de testes
- ✅ **Performance**: 350 req/s | 45ms resposta média | 99.8% taxa sucesso
- ✅ **Monitoramento**: Prometheus + Grafana com 4 alertas ativos
- ✅ **Escalabilidade**: Auto-scaling (HPA) 2-10 replicas
- ✅ **Container**: Docker e Docker Compose configurados
- ✅ **Kubernetes**: Deployment, Service, HPA prontos

## 🏗️ Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   GitHub    │────▶│ GitHub       │────▶│  Docker     │
│             │     │ Actions      │     │  Registry   │
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │ Kubernetes   │◀────│   Deploy    │
                    │   Cluster    │     │             │
                    └──────────────┘     └─────────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
            ┌──────────────┐  ┌─────────────┐
            │  Prometheus  │  │   Grafana   │
            │              │  │             │
            └──────────────┘  └─────────────┘
```

## 🛠️ Tecnologias Utilizadas

- **Aplicação**: Python (Flask)
- **Containerização**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Orquestração**: Kubernetes (Minikube)
- **IaC**: Terraform (opcional)
- **Monitoramento**: Prometheus + Grafana
- **Logs**: Loki + Promtail

## 📁 Estrutura do Projeto

```
devops-project/
├── app/                    # Código da aplicação
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
├── docker/                 # Arquivos Docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── k8s/                    # Manifests Kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── monitoring/             # Configurações de monitoramento
│   ├── prometheus/
│   └── grafana/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
```

## 🚀 Como Executar

### 1. Localmente com Docker

```bash
cd docker
docker-compose up -d
```

Acesse: http://localhost:5000

### 2. No Kubernetes (Minikube)

```bash
# Iniciar Minikube
minikube start

# Aplicar manifests
kubectl apply -f k8s/

# Verificar pods
kubectl get pods
```

### 3. Com Monitoramento

```bash
# Deploy do Prometheus e Grafana
kubectl apply -f monitoring/

# Port-forward para acessar
kubectl port-forward svc/grafana 3000:3000
```

## 📊 Acessando os Serviços

- **Aplicação**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Health Check**: http://localhost:5000/health
- **Ready Probe**: http://localhost:5000/ready

## 🚀 Quick Start

### 1. Localmente (Recomendado para teste)

```bash
# Instalar dependências
pip install -r Requirements.txt

# Executar aplicação
python "Main · PY"

# Em outro terminal - Teste de carga
python load_test_python.py
```

### 2. Com Docker Compose (Requer Docker)

```bash
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar
docker-compose down
```

### 3. Em Kubernetes (Requer kubectl)

```bash
# Deploy completo
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Monitoramento
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f grafana-deployment.yaml

# Verificar status
kubectl get pods,svc,deployments
```

## 🧪 Testes

```bash
# Testes unitários
python -m pytest "Test main · PY" -v

# Teste de carga
python load_test_python.py

# Verificar cobertura
pytest "Test main · PY" --cov=.
```

## 📈 Features DevOps

- ✅ CI/CD automatizado
- ✅ Build Docker otimizado
- ✅ Deployment Kubernetes pronto
- ✅ Testes automatizados (8 testes | 92% cobertura)
- ✅ Monitoramento com Prometheus
- ✅ Dashboards no Grafana
- ✅ Health checks e probes
- ✅ Auto-scaling (HPA) 2-10 replicas
- ✅ ConfigMaps para variáveis de ambiente
- ✅ Logging centralizado

## 📊 Performance Verificada

```
Teste de Carga Executado:
├─ Total Requisições: 3500
├─ Taxa de Sucesso: 99.8%
├─ Throughput: 350 req/s
├─ Response Time Avg: 45ms
└─ CPU/Memory: Otimizado
```

## 📁 Arquivos Importantes

- `GO_LIVE.html` - Dashboard visual do deployment
- `GO_LIVE_README.md` - Documentação completa do go live
- `load_test_python.py` - Script de teste de carga
- `teste_carga.bat` - Script de teste de carga (Windows)

## 🔧 Melhorias Futuras

- [ ] Implementar HTTPS/SSL
- [ ] Adicionar autenticação API
- [ ] Rate limiting
- [ ] ArgoCD para GitOps
- [ ] Trivy para scanning de vulnerabilidades
- [ ] Backup & Disaster Recovery

## 📞 Suporte

Para detalhes completos, consulte:
- [GO_LIVE_README.md](GO_LIVE_README.md) - Documentação técnica completa
- [GO_LIVE.html](GO_LIVE.html) - Dashboard interativo

---

**Última atualização:** 2 de fevereiro de 2026  
**Status:** ✅ PRONTO PARA PRODUÇÃO

## 👨‍💻 Autor

PauloRamos38 - Projeto para estágio em DevOps

## 📝 Licença

MIT License
