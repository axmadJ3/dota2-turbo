# Docker Compose commands
up:
	docker compose -f docker-compose-local.yml up -d

build:
	docker compose -f docker-compose-local.yml build

down:
	docker compose -f docker-compose-local.yml down

stop:
	docker compose -f docker-compose-local.yml stop

logs:
	docker compose -f docker-compose-local.yml logs -f

ps:
	docker ps

clear:
	docker system prune -a

bash:
	docker compose -f docker-compose-local.yml exec web bash


# Django management commands
makemigrations:
	docker compose -f docker-compose-local.yml exec web python manage.py makemigrations

migrate:
	docker compose -f docker-compose-local.yml exec web python manage.py migrate

superuser:
	docker compose -f docker-compose-local.yml exec web python manage.py createsuperuser

shell:
	docker compose -f docker-compose-local.yml exec web python manage.py shell
