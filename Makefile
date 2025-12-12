# ================================
#   ML Microservice - Makefile (Windows Compatible)
# ================================

# ---- Colors (Windows-safe minimal) ----
GREEN = [RUN]
BLUE = [INFO]
YELLOW = [WARN]
RED = [ERR]

APP = ml-api
PORT = 8000

# ================================
# BASIC COMMANDS
# ================================

run:
	@echo $(GREEN) Starting FastAPI server...
	python -m uvicorn app.main:app --reload --port $(PORT)

train:
	@echo $(BLUE) Training model...
	python train_model.py

test:
	@echo $(YELLOW) Running tests...
	pytest -q

lint:
	@echo $(YELLOW) Linting code...
	flake8 app/

# ================================
# DOCKER COMMANDS
# ================================

docker-build:
	@echo $(GREEN) Building Docker image...
	docker build -t $(APP) .

docker-run:
	@echo $(GREEN) Running Docker container...
	docker run -p $(PORT):$(PORT) $(APP)

docker-shell:
	@echo $(BLUE) Entering container shell...
	docker run -it $(APP) /bin/sh

docker-clean:
	@echo $(RED) Cleaning unused Docker data...
	docker system prune -f

# ================================
# MODEL VERSIONING
# ================================

model-list:
	@echo $(BLUE) Listing models...
	@dir app\\models

model-load:
	@echo $(GREEN) Loading model version $(v)...
	curl -X GET "http://localhost:$(PORT)/switch-model/$(v)"

# ================================
# UTILITIES
# ================================

show-env:
	@echo $(BLUE) Showing .env content:
	@type .env

clean-cache:
	@echo $(RED) Removing __pycache__...
	@if exist __pycache__ rmdir /s /q __pycache__

# ================================
# DEFAULT COMMAND
# ================================

help:
	@echo Available commands:
	@echo make run
	@echo make train
	@echo make test
	@echo make docker-build
	@echo make docker-run
	@echo make model-load v=v1
