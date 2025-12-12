# ================================
#   ML Microservice - Makefile
# ================================

# ---- Colors ----
GREEN := echo [RUN]
BLUE := echo [INFO]
YELLOW := echo [WARN]
RED := echo [ERROR]

# ---- Python Interpreter ----
PYTHON=C:/Python313/python.exe

# ---- App Settings ----
APP=ml-api
PORT=8000

# ================================
# BASIC COMMANDS
# ================================

run:
	$(GREEN) Starting FastAPI server...
	$(PYTHON) -m uvicorn app.main:app --reload --port $(PORT)

train:
	$(BLUE) Training model...
	$(PYTHON) train_model.py

test:
	$(YELLOW) Running tests...
	$(PYTHON) -m pytest -q

lint:
	$(YELLOW) Linting...
	$(PYTHON) -m flake8 app/

# ================================
# DOCKER COMMANDS
# ================================

docker-build:
	$(GREEN) Building Docker image...
	docker build -t $(APP) .

docker-run:
	$(GREEN) Running Docker container...
	docker run -p $(PORT):$(PORT) $(APP)

docker-shell:
	$(BLUE) Entering container shell...
	docker run -it $(APP) sh

docker-clean:
	$(RED) Cleaning Docker system...
	docker system prune -f

# ================================
# MODELS
# ================================

model-list:
	$(BLUE) Listing models...
	dir app/models

model-load:
	$(GREEN) Loading model version $(v)...
	curl -X GET "http://localhost:$(PORT)/switch-model/$(v)"

# ================================
# DEFAULT
# ================================

help:
	@echo "Available commands:"
	@echo " make run"
	@echo " make train"
	@echo " make test"
	@echo " make docker-build"
	@echo " make docker-run"
	@echo " make model-list"
	@echo " make model-load v=v2"
