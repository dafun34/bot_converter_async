format:
	poetry run isort .
	poetry run black .

check:
	poetry run isort bot_converter --check
	poetry run flake8 bot_converter
	poetry run black bot_converter --check

makemigrations:
	docker-compose exec app alembic revision --autogenerate

migrate:
	docker-compose exec app alembic upgrade head
