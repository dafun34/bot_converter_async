format:
	poetry run isort .
	poetry run black .

check:
	poetry run isort . --check
	poetry run flake8 .
	poetry run black . --check

makemigrations:
	docker-compose exec app alembic revision --autogenerate

migrate:
	docker-compose exec app alembic upgrade head
