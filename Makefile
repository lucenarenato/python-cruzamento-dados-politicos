.PHONY: help build up scan shell logs ps down

help:
	@echo "Alvos disponíveis:"
	@echo "  make build  - Build da imagem Docker"
	@echo "  make up     - Executa pipeline padrão (scan-sanctions)"
	@echo "  make scan   - Executa scan avulso e remove container"
	@echo "  make shell  - Abre shell interativo no container"
	@echo "  make logs   - Exibe logs do serviço politicos"
	@echo "  make ps     - Lista status dos serviços"
	@echo "  make down   - Remove recursos do compose"

build:
	docker compose --profile cli build

up:
	docker compose --profile cli up --build

scan:
	docker compose --profile cli run --rm politicos politicos scan-sanctions

shell:
	docker compose --profile dev run --rm dev-shell

logs:
	docker compose --profile cli logs -f politicos

ps:
	docker compose ps

down:
	docker compose down --remove-orphans