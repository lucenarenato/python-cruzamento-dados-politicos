.PHONY: help build up scan shell logs down

help:
	@echo "Alvos disponíveis:"
	@echo "  make build  - Build da imagem Docker"
	@echo "  make up     - Executa pipeline padrão (scan-sanctions)"
	@echo "  make scan   - Executa scan avulso e remove container"
	@echo "  make shell  - Abre shell interativo no container"
	@echo "  make logs   - Exibe logs do serviço politicos"
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

down:
	docker compose down --remove-orphans