ARGS=

.PHONY: install
install:
	@echo "\nInstalling dependencies..."
	uv sync
	uv run pre-commit install
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

.PHONY: run
run:
	uv run src/main.py $(ARGS)

.PHONY: all
all: install lint format test
