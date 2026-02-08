ARGS=

.PHONY: install
install:
	@echo "\nInstalling dependencies..."
	uv sync
	uv run pre-commit install
# 	uv run playwright install-deps
	uv run playwright install

.PHONY: format
format:
	@echo "\nFormating code..."
	uv run ruff format $(ARGS)

.PHONY: lint
lint:
	@echo "\nLinting code..."
	uv run ruff check --fix $(ARGS)

.PHONY: test
test:
	@echo "\nRunning tests..."
	@echo "Skipping for now"

.PHONY: clean
clean:
	@rm -rf build dist *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name .pytest_cache -exec rm -rf {} +
	@find . -type d -name .mypy_cache -exec rm -rf {} +
	@find . -type d -name .ruff_cache -exec rm -rf {} +

.PHONY: run-cli
run-cli:
	uv run src/backend/run_cli.py $(ARGS)

.PHONY: run-backend
run-backend:
	uv run uvicorn src.backend.app:app --reload --host 0.0.0.0 --port 8000

.PHONY: run-frontend
run-frontend:
	cd src/frontend && uv run reflex run --backend-port 8080

.PHONY: all
all: install lint format test
