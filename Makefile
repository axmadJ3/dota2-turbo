# Docker Compose commands
up:
	docker compose -f docker-compose-local.yml up -d

build:
	docker compose -f docker-compose-local.yml build

down:
	docker compose -f docker-compose-local.yml down

logs:
	docker compose -f docker-compose-local.yml logs -f

ps:
	docker ps

bash:
	docker compose exec web-local bash

clear:
	docker system prune -a

# Django management commands
makemigrations:
	docker compose -f docker-compose-local.yml exec web-local python manage.py makemigrations

migrate:
	docker compose -f docker-compose-local.yml exec web-local python manage.py migrate

superuser:
	docker compose -f docker-compose-local.yml exec web-local python manage.py createsuperuser

shell:
	docker compose -f docker-compose-local.yml exec web-local python manage.py shell
