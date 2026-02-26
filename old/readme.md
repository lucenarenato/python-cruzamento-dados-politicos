# python-politicos

Base Python inicial para detectar risco em contratos públicos com cruzamento de bases abertas.

## O que foi criado

- Estrutura de projeto em `src/` com CLI.
- Pipeline inicial: cruzar sanções (`CEIS`) com contratos (`PNCP/ComprasNet/SIAFI exportado em CSV`).
- Regra implementada: marcar contrato cuja `contract_date` esteja dentro da janela de sanção ativa.
- Saída de resultados em CSV + resumo em JSON.

## Estrutura

```text
python-politicos/
├─ pyproject.toml
├─ .env.example
├─ readme.md
├─ HBsY2sYWgAAoPkH.jpeg
├─ HBsY2sZWMAA7tLw.jpeg
├─ HBsZYNLW4AEFWyA.jpeg
├─ HBsZYNLXcAEFrdS.jpeg
└─ src/
	└─ politicos/
		├─ cli.py
		├─ config.py
		├─ pipeline.py
		├─ models.py
		├─ connectors/
		│  ├─ csv_loader.py
		│  ├─ ceis.py
		│  └─ contracts.py
		└─ rules/
			└─ sanction_overlap.py
```

As imagens de exemplo foram mantidas no repositório.

## Requisitos

- Python 3.11+

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Rodando com Docker (local)

Atalhos com Makefile:

```bash
make init-data
make build
make up
make scan
make shell
make logs
make ps
make down
```

Perfis disponíveis:

- `cli`: execução do pipeline
- `dev`: shell interativo

Fluxo rápido recomendado para primeiro uso:

```bash
make init-data
make up
```

O alvo `init-data` cria `data/raw/ceis.csv` e `data/raw/contracts.csv` com dados de exemplo (se ainda não existirem).

Subir execução padrão (`scan-sanctions`):

```bash
docker compose --profile cli up --build
```

Executar comando avulso:

```bash
docker compose --profile cli run --rm politicos politicos scan-sanctions
```

Abrir shell interativo de desenvolvimento:

```bash
docker compose --profile dev run --rm dev-shell
```

Opcional: sobrescrever variáveis sem criar `.env`:

```bash
DATA_DIR=./data OUTPUT_DIR=./data/output docker compose --profile cli run --rm politicos politicos scan-sanctions
```

## Entradas esperadas (CSV)

### `CEIS_CSV`

Colunas mínimas:

- `cnpj_cpf`
- `name`
- `sanction_start`

Colunas opcionais:

- `sanction_end`
- `sanction_type`

### `CONTRACTS_CSV`

Colunas mínimas:

- `supplier_document`
- `supplier_name`
- `contract_date`

Colunas opcionais:

- `contract_value`
- `contract_number`
- `organ`

## Configuração

Copie `.env.example` e ajuste caminhos:

```bash
cp .env.example .env
```

Variáveis:

- `DATA_DIR`
- `CEIS_CSV`
- `CONTRACTS_CSV`
- `OUTPUT_DIR`

## Execução

```bash
politicos scan-sanctions
```

Saídas geradas em `OUTPUT_DIR`:

- `contracts_during_sanction.csv`
- `summary.json`

## Próximos passos recomendados

- Adicionar novos conectores (CNEP, CEPIM, TSE bens/doações, QSA Receita).
- Incluir camada de persistência em banco analítico (BigQuery/PostgreSQL).
- Evoluir para grafo (`Neo4j`) para detectar relações indiretas (pessoas, empresas, contratos, doações).
