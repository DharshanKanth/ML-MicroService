# ================================
#   ML Microservice - Makefile
# ================================

# ---- Colors ----
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[1;34m
RED := \033[0;31m
NC := \033[0m   # No Color

# ---- Environment ----
include .env
export $(shell sed 's/=.*//' .env)

APP=ml-api
PORT=8000

# ================================
# BASIC COMMANDS
# ================================

run:
	@echo "$(GREEN)[RUN] Starting FastAPI server...$(NC)"
	uvicorn app.main:app --reload --port $(PORT)

train:
	@echo "$(BLUE)[TRAIN] Training model and saving version…$(NC)"
	python train_model.py

test:
	@echo "$(YELLOW)[TEST] Running unit tests…$(NC)"
	pytest -q

lint:
	@echo "$(YELLOW)[LINT] Checking code style with flake8…$(NC)"
	flake8 app/

# ================================
# DOCKER COMMANDS
# ================================

docker-build:
	@echo "$(GREEN)[DOCKER] Building Docker image '$(APP)'…$(NC)"
	docker build -t $(APP) .

docker-run:
	@echo "$(GREEN)[DOCKER] Running container on port $(PORT)…$(NC)"
	docker run -p $(PORT):$(PORT) $(APP)

docker-shell:
	@echo "$(BLUE)[DOCKER] Entering container shell…$(NC)"
	docker run -it $(APP) /bin/sh

docker-clean:
	@echo "$(RED)[DOCKER] Removing unused images & containers…$(NC)"
	docker system prune -f

# ================================
# MODEL VERSIONING
# ================================

model-list:
	@echo "$(BLUE)[MODELS] Available model versions:$(NC)"
	@ls app/models

model-load:
	@echo "$(GREEN)[MODEL] Loading model version $(v)…$(NC)"
	curl -X GET "http://localhost:$(PORT)/switch-model/$(v)"

# ================================
# UTILITIES
# ================================

show-env:
	@echo "$(BLUE)[ENV] Current environment variables:$(NC)"
	@cat .env

logs:
	@echo "$(YELLOW)[LOGS] Showing API logs…$(NC)"
	docker logs $$(docker ps -q --filter ancestor=$(APP))

clean-cache:
	@echo "$(RED)[CLEAN] Removing __pycache__…$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} +

# ================================
# CI/CD HELPERS
# ================================

ci-test:
	@echo "$(GREEN)[CI] Running tests for pipeline…$(NC)"
	pytest -q

ci-build:
	@echo "$(GREEN)[CI] Building docker for pipeline…$(NC)"
	docker build -t $(APP) .

# ================================
# ARCHITECTURE DISPLAY
# ================================

architecture:
	@echo "$(BLUE)--------------------------------------$(NC)"
	@echo "$(BLUE)       ML MICROSERVICE ARCHITECTURE    $(NC)"
	@echo "$(BLUE)--------------------------------------$(NC)"
	@echo "User → FastAPI → Middleware → Model Cache"
	@echo "Model Loader → Versioned Models (v1, v2)"
	@echo "Docker Container → Health/Ready Probes"
	@echo "CI/CD → Docker Build → GitHub Actions"
	@echo "$(BLUE)--------------------------------------$(NC)"

# ================================
# DEFAULT
# ================================

help:
	@echo "\n$(YELLOW)Available Commands:$(NC)"
	@echo " make run                 - Start FastAPI server"
	@echo " make train               - Train the ML model"
	@echo " make test                - Run unit tests"
	@echo " make lint                - Lint code"
	@echo " make docker-build        - Build Docker image"
	@echo " make docker-run          - Run docker container"
	@echo " make docker-shell        - Enter container"
	@echo " make model-list          - Show available model versions"
	@echo " make model-load v=v2     - Load model version v2"
	@echo " make clean-cache         - Remove caches"
	@echo " make architecture         - Print architecture overview"
