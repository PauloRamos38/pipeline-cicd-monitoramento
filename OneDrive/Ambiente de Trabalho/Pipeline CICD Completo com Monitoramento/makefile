.PHONY: help install test build run clean docker-build docker-run k8s-deploy k8s-delete monitoring

help: ## Mostra esta mensagem de ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências do projeto
	pip install -r app/requirements.txt

test: ## Executa os testes
	cd app && pytest tests/ -v --cov=. --cov-report=html

lint: ## Verifica a qualidade do código
	flake8 app/ --count --statistics
	black --check app/

format: ## Formata o código
	black app/

run: ## Executa a aplicação localmente
	cd app && python main.py

docker-build: ## Faz build da imagem Docker
	docker build -t devops-app:latest -f docker/Dockerfile .

docker-run: ## Executa a aplicação com Docker
	cd docker && docker-compose up -d

docker-stop: ## Para os containers Docker
	cd docker && docker-compose down

docker-logs: ## Mostra os logs dos containers
	cd docker && docker-compose logs -f

k8s-deploy: ## Deploy no Kubernetes
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/hpa.yaml

k8s-delete: ## Remove recursos do Kubernetes
	kubectl delete -f k8s/

k8s-status: ## Verifica o status dos pods
	kubectl get pods,svc,deployments

monitoring: ## Deploy do monitoramento (Prometheus + Grafana)
	kubectl apply -f monitoring/prometheus-deployment.yaml
	kubectl apply -f monitoring/grafana-deployment.yaml

monitoring-delete: ## Remove o monitoramento
	kubectl delete -f monitoring/

port-forward: ## Port forward dos serviços
	@echo "Acessar Grafana em http://localhost:3000"
	kubectl port-forward svc/grafana 3000:3000 &
	@echo "Acessar Prometheus em http://localhost:9090"
	kubectl port-forward svc/prometheus 9090:9090 &
	@echo "Acessar App em http://localhost:5000"
	kubectl port-forward svc/devops-app-service 5000:80 &

clean: ## Remove arquivos temporários
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

minikube-start: ## Inicia o Minikube
	minikube start --driver=docker --cpus=4 --memory=8192

minikube-stop: ## Para o Minikube
	minikube stop

minikube-delete: ## Deleta o cluster Minikube
	minikube delete