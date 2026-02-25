.PHONY: help init-data build up scan shell logs ps down

help:
	@echo "Alvos disponíveis:"
	@echo "  make init-data - Cria CSVs de exemplo em data/raw"
	@echo "  make build  - Build da imagem Docker"
	@echo "  make up     - Executa pipeline padrão (scan-sanctions)"
	@echo "  make scan   - Executa scan avulso e remove container"
	@echo "  make shell  - Abre shell interativo no container"
	@echo "  make logs   - Exibe logs do serviço politicos"
	@echo "  make ps     - Lista status dos serviços"
	@echo "  make down   - Remove recursos do compose"

build:
	docker compose --profile cli build

init-data:
	mkdir -p data/raw data/output
	@if [ ! -f data/raw/ceis.csv ]; then \
		echo "source_id,cnpj_cpf,name,sanction_start,sanction_end,sanction_type" > data/raw/ceis.csv; \
		echo "CEIS,12345678000190,Empresa Exemplo Sancionada,2025-01-01,2026-12-31,INIDONEIDADE" >> data/raw/ceis.csv; \
		echo "CEIS de exemplo criado em data/raw/ceis.csv"; \
	else \
		echo "Arquivo já existe: data/raw/ceis.csv"; \
	fi
	@if [ ! -f data/raw/contracts.csv ]; then \
		echo "source_id,supplier_document,supplier_name,contract_date,contract_value,contract_number,organ" > data/raw/contracts.csv; \
		echo "PNCP,12345678000190,Empresa Exemplo Sancionada,2025-06-10,150000.00,CONTR-001,MINISTERIO X" >> data/raw/contracts.csv; \
		echo "PNCP,00999999000100,Fornecedor Regular,2025-06-10,50000.00,CONTR-002,MINISTERIO Y" >> data/raw/contracts.csv; \
		echo "Contratos de exemplo criado em data/raw/contracts.csv"; \
	else \
		echo "Arquivo já existe: data/raw/contracts.csv"; \
	fi

up: init-data
	docker compose --profile cli up --build

scan: init-data
	docker compose --profile cli run --rm politicos politicos scan-sanctions

shell:
	docker compose --profile dev run --rm dev-shell

logs:
	docker compose --profile cli logs -f politicos

ps:
	docker compose ps

down:
	docker compose down --remove-orphans