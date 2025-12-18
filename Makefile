.PHONY: fmt lint test dev

fmt:
	cd backend && python -m black app && python -m isort app
	cd frontend && npm run format

lint:
	cd backend && python -m ruff check app && python -m mypy app
	cd frontend && npm run lint

test:
	cd backend && pytest

dev:
	docker compose -f infra/docker-compose.yml up --build
