# 🚀 Guia Rápido de Uso

## Início Rápido em 5 Minutos

### 1. Configuração Básica

```bash
# Clone e entre no diretório
git clone https://github.com/lucenarenato/python-cruzamento-dados-politicos.git
cd python-cruzamento-dados-politicos

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Configure o .env
cp env.sample .env
nano .env  # Adicione sua TRANSPARENCIA_API_KEY
```

### 2. Execute a Aplicação

```bash
python run.py
```

Acesse: http://localhost:5085

### 3. Faça Login

Use as credenciais padrão (se configuradas) ou crie uma conta.

### 4. Teste as Funcionalidades

#### 📊 Dashboard
- Veja estatísticas gerais
- Identifique padrões suspeitos
- Acesse links rápidos

#### 🔍 Monitor de Integridade
1. Clique em "Monitor Integridade" no menu
2. Digite um CPF ou CNPJ (apenas números)
3. Clique em "Cruzar dados"
4. Veja o resultado com nível de risco

#### 🎯 Análise Completa
1. Acesse "Análise Completa"
2. Digite CPF (11 dígitos) ou CNPJ (14 dígitos)
3. Clique em "Consultar Todas as Fontes"
4. Veja resultados de todas as APIs:
   - CEIS (Sancionados)
   - CNEP (Punidos)
   - CEPIM (Impedidos)
   - Contratos Federais
   - Convênios
   - Receita Federal (CNPJ)
   - PNCP (Contratos)

#### ⚠️ Sanções vs Contratos
1. Acesse "Sanções vs Contratos"
2. Veja empresas que contrataram durante sanção
3. Analise valores irregulares
4. Clique em "Ver Detalhes" para mais informações

## 🔑 Obter Chave da API do Portal da Transparência

### Passo a Passo

1. Acesse: http://api.portaldatransparencia.gov.br/

2. Clique em "Solicitar Chave"

3. Preencha o formulário:
   - Nome completo
   - Email válido
   - Motivo do uso

4. Receberá a chave por email

5. Adicione ao `.env`:
   ```env
   TRANSPARENCIA_API_KEY=sua_chave_aqui
   ```

6. Reinicie a aplicação

## 📥 Importar Dados Locais (Opcional)

### CEIS (Empresas Sancionadas)

```bash
# Criar diretório
mkdir -p old/data/raw

# Baixar CEIS
curl -o old/data/raw/ceis.csv \
  https://portaldatransparencia.gov.br/download-de-dados/ceis

# Ou baixe manualmente:
# https://portaldatransparencia.gov.br/download-de-dados/ceis
```

### Contratos Públicos

```bash
# Baixar contratos
curl -o old/data/raw/contracts.csv \
  https://portaldatransparencia.gov.br/download-de-dados/contratos

# Ou baixe manualmente
```

## 🧪 Testar com Dados de Exemplo

### Criar CSV de Exemplo

**old/data/raw/ceis.csv:**
```csv
cnpj_cpf,name,sanction_start,sanction_end,sanction_type,orgao_sancionador
12345678000190,Empresa Teste LTDA,2023-01-01,2025-12-31,Suspensão Temporária,CGU
98765432000100,Construtora ABC S/A,2022-06-15,2024-06-15,Declaração de Inidoneidade,TCU
11122233000145,Serviços XYZ LTDA,2023-03-01,2026-03-01,Impedimento de Licitar,Ministério da Saúde
```

**old/data/raw/contracts.csv:**
```csv
cpf_cnpj,nome,numero,orgao,valor,data_assinatura,objeto
12345678000190,Empresa Teste LTDA,2023/001,Ministério da Saúde,500000.00,2023-06-15,Prestação de serviços médicos
12345678000190,Empresa Teste LTDA,2023/002,INCRA,300000.00,2023-08-20,Consultoria técnica
98765432000100,Construtora ABC S/A,2023/010,DNIT,2000000.00,2023-02-10,Construção de rodovia
11122233000145,Serviços XYZ LTDA,2024/005,FUNAI,150000.00,2024-01-30,Levantamento topográfico
```

## 🎯 Casos de Uso

### Caso 1: Verificar se uma Empresa Está Sancionada

```
1. Acesse "Análise Completa"
2. Digite o CNPJ: 12345678000190
3. Resultado mostrará:
   - ✅ Se está em CEIS, CNEP ou CEPIM
   - ✅ Contratos ativos
   - ✅ Nível de risco
```

### Caso 2: Encontrar Contratos Irregulares

```
1. Acesse "Sanções vs Contratos"
2. Veja lista de empresas sancionadas que contrataram
3. Clique em "Ver Detalhes" de uma empresa
4. Veja todos os contratos firmados durante sanção
```

### Caso 3: Monitorar CPF de Político

```
1. Acesse "Análise Completa"
2. Digite CPF: 12345678901
3. Sistema consultará:
   - Sanções
   - Contratos em nome do CPF
   - Convênios
   - (Futuro: Bens do TSE, empresas vinculadas)
```

## 📊 Interpretando Resultados

### Níveis de Risco

| Badge | Significado |
|-------|-------------|
| 🔴 **CRÍTICO** | Sanção ativa em CEIS/CNEP |
| 🟠 **ALTO** | Impedido de licitar |
| 🟡 **MÉDIO** | Muitos contratos ou convênios |
| 🟢 **BAIXO** | Poucos ou nenhum registro |

### Alertas

- **"Encontrado em CEIS"** → Empresa sancionada
- **"X contratos federais"** → Informativo
- **"CONTRATO DURANTE SANÇÃO ATIVA"** → Irregularidade grave

## 🐛 Solução de Problemas

### Erro: API Key não configurada

```
Solução: Configure TRANSPARENCIA_API_KEY no .env
```

### Erro: Arquivo CEIS não encontrado

```
Solução: 
1. Crie o diretório: mkdir -p old/data/raw
2. Baixe o CEIS ou crie um CSV de exemplo
```

### Erro: Nenhum dado no Dashboard

```
Solução:
1. Importe dados locais (CEIS e Contratos)
2. Ou ignore - use as outras funcionalidades
```

### API retorna erro 401

```
Solução: Verifique se a chave da API está correta
```

### Timeout em consultas

```
Solução: 
1. Verifique conexão com internet
2. Algumas APIs podem estar lentas - tente novamente
```

## 🔄 Atualizando Dados

### Manual

```bash
# Download CEIS atualizado
curl -o old/data/raw/ceis.csv [URL]

# Download contratos
curl -o old/data/raw/contracts.csv [URL]

# Reinicie a aplicação
```

### Automático (Futuro)

```python
# Em desenvolvimento
python scripts/update_databases.py
```

## 📞 Precisa de Ajuda?

- 📖 Documentação completa: [SISTEMA_README.md](SISTEMA_README.md)
- 🐛 Reportar bug: [GitHub Issues](https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/lucenarenato/python-cruzamento-dados-politicos/discussions)

## ⚡ Dicas Pro

### 1. Consultas em Lote
Use a API JSON:
```bash
curl http://localhost:5085/api/consultar/12345678000190
```

### 2. Automatizar Análises
```python
from apps.home.api_services import consultar_multiplas_fontes

cnpjs = ["12345678000190", "98765432000100"]
for cnpj in cnpjs:
    resultado = consultar_multiplas_fontes(cnpj)
    print(f"{cnpj}: {resultado['avaliacao']['nivel_risco']}")
```

### 3. Exportar Resultados
```python
import json
from apps.home.data_crossing_service import analisar_dados_locais

dados = analisar_dados_locais()
with open("relatorio.json", "w") as f:
    json.dump(dados, f, indent=2)
```

---

**Pronto!** Agora você está apto a usar o sistema de cruzamento de dados. 🎉
