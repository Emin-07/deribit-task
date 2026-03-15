.PHONY: requirements requirements-prod requirements-dev run test down clean

test:
	docker-compose exec app uv run pytest -v tests/

requirements: requirements-prod requirements-dev
	@echo "✅ All requirements files updated!"

requirements-prod:
	uv pip compile pyproject.toml -o requirements.txt
	@echo "✅ Production requirements generated"

requirements-dev:
	uv pip compile pyproject.toml --extra dev -o requirements-dev.txt
	@echo "✅ Development requirements generated"

run:
	docker-compose up --build

down:
	docker-compose down

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true