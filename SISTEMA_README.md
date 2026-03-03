# Sistema de Cruzamento de Dados Abertos do Governo Federal

Sistema Python/Flask para identificar empresas sancionadas que continuam recebendo contratos públicos através do cruzamento de múltiplas bases de dados abertas do governo federal brasileiro.

## 🎯 Objetivo

Detectar irregularidades e possível corrupção através da análise automatizada de:
- Empresas sancionadas (CEIS, CNEP, CEPIM)
- Contratos públicos federais
- Dados de políticos (TSE)
- Vínculos empresariais (QSA Receita Federal)

## 📊 Funcionalidades

### Dashboard Principal
- Estatísticas em tempo real de contratos analisados
- Alertas de padrões suspeitos detectados
- Top empresas com contratos durante sanção
- Métricas de valor total irregular

### Monitor de Integridade
- Consulta rápida de CPF/CNPJ
- Busca no Portal da Transparência
- Verificação em base local de CEIS
- Avaliação de nível de risco

### Análise Completa
Consulta integrada em múltiplas fontes:
- **CEIS** - Cadastro de Empresas Inidôneas e Sancionadas
- **CNEP** - Cadastro Nacional de Empresas Punidas
- **CEPIM** - Cadastro de Entidades Privadas Sem Fins Lucrativos Impedidas
- **Contratos Federais** - Portal da Transparência
- **Convênios** - Portal da Transparência
- **CNPJ/QSA** - Receita Federal (via ReceitaWS)
- **PNCP** - Portal Nacional de Contratações Públicas
- **TSE** - Dados eleitorais (candidaturas, bens, doações)

### Sanções vs Contratos
- Cruzamento automático de sanções e contratos
- Detecção de contratos firmados durante período de sanção
- Análise de valor irregular total
- Detalhamento por empresa

## 🏗️ Arquitetura

```
apps/
├── models.py                  # Modelos de dados (Sanção, Contrato, Alerta, Político)
├── home/
│   ├── routes.py             # Rotas do Flask
│   ├── integrity_service.py  # Serviço básico de integridade
│   ├── api_services.py       # Clientes para APIs públicas
│   └── data_crossing_service.py  # Lógica de cruzamento de dados
templates/home/
├── index.html                # Dashboard principal
├── monitor_integridade.html  # Monitor simples
├── analise_completa.html     # Análise com múltiplas APIs
└── sancoes_contratos.html    # Visualização de irregularidades
```

## 🚀 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/lucenarenato/python-cruzamento-dados-politicos.git
cd python-cruzamento-dados-politicos
```

### 2. Configurar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo:
```bash
cp env.sample .env
```

Edite o arquivo `.env` e configure:

```env
# Flask
FLASK_APP=run.py
SECRET_KEY=S3cr3t_K#Key
DEBUG=True

# API do Portal da Transparência
# Obtenha sua chave em: http://api.portaldatransparencia.gov.br/
TRANSPARENCIA_API_KEY=sua_chave_aqui

# Banco de dados
DATABASE_URL=sqlite:///db.sqlite3

# Caminhos para dados locais (opcional)
CEIS_CSV=old/data/raw/ceis.csv
CONTRACTS_CSV=old/data/raw/contracts.csv
```

### 5. Inicializar banco de dados

```bash
flask db upgrade
# ou
python run.py
```

### 6. Executar a aplicação

```bash
python run.py
```

Acesse: `http://localhost:5085`

## 📡 APIs Utilizadas

### Portal da Transparência (Requer API Key)
```python
from apps.home.api_services import PortalTransparenciaAPI

api = PortalTransparenciaAPI()
resultado = api.buscar_ceis("00000000000000")
```

Endpoints disponíveis:
- `/ceis` - Empresas Inidôneas
- `/cnep` - Empresas Punidas
- `/cepim` - Impedidos de Licitar
- `/contratos` - Contratos Federais
- `/convenios` - Convênios

**Obter chave:** http://api.portaldatransparencia.gov.br/

### Receita Federal (CNPJ)
```python
from apps.home.api_services import ReceitaFederalAPI

api = ReceitaFederalAPI()
resultado = api.consultar_cnpj("00000000000000")
```

Usa ReceitaWS (API não oficial, gratuita)

### PNCP - Portal Nacional de Contratações
```python
from apps.home.api_services import PNCPAPI

api = PNCPAPI()
resultado = api.buscar_contratos("00000000000000", dias=365)
```

### Análise Completa
```python
from apps.home.api_services import consultar_multiplas_fontes, calcular_nivel_risco

dados = consultar_multiplas_fontes("00000000000000")
avaliacao = calcular_nivel_risco(dados)
```

## 📥 Importação de Dados

### CEIS (Empresas Sancionadas)

1. Acesse: https://portaldatransparencia.gov.br/download-de-dados/ceis
2. Baixe o CSV mais recente
3. Coloque em `old/data/raw/ceis.csv`

Formato esperado:
```csv
cnpj_cpf,name,sanction_start,sanction_end,sanction_type,orgao_sancionador
00000000000000,Empresa XYZ,2023-01-01,2025-12-31,Suspensão,CGU
```

### Contratos Públicos

1. Acesse: https://portaldatransparencia.gov.br/download-de-dados/contratos
2. Baixe o CSV
3. Coloque em `old/data/raw/contracts.csv`

Formato esperado:
```csv
cpf_cnpj,nome,numero,orgao,valor,data_assinatura,objeto
00000000000000,Empresa ABC,2023/001,Ministério da Saúde,1000000.00,2023-06-15,Prestação de serviços
```

## 🔍 Exemplos de Uso

### Consultar CPF/CNPJ

1. Acesse "Análise Completa" no menu
2. Digite o CPF (11 dígitos) ou CNPJ (14 dígitos)
3. Clique em "Consultar Todas as Fontes"
4. Visualize os resultados de todas as bases

### Ver Irregularidades

1. Acesse "Sanções vs Contratos" no menu
2. Visualize empresas que contrataram durante sanção
3. Clique em "Ver Detalhes" para análise completa

### API JSON

Endpoints disponíveis:

```bash
# Estatísticas gerais
GET /api/estatisticas

# Consultar documento
GET /api/consultar/00000000000000
```

Exemplo de resposta:
```json
{
  "documento": "00000000000000",
  "tipo": "CNPJ",
  "avaliacao": {
    "nivel_risco": "critico",
    "pontuacao": 100,
    "alertas": ["Encontrado em CEIS"]
  },
  "fontes": {
    "ceis": {"ok": true, "total": 1},
    "contratos": {"ok": true, "total": 5}
  }
}
```

## 📊 Níveis de Risco

| Nível | Pontuação | Critérios |
|-------|-----------|-----------|
| **Crítico** | ≥ 50 | CEIS, CNEP ou CEPIM |
| **Alto** | 30-49 | CEPIM + Contratos |
| **Médio** | 10-29 | Muitos contratos |
| **Baixo** | < 10 | Poucos ou nenhum registro |

## 🗂️ Modelos de Dados

### Sancao
- cpf_cnpj
- nome_sancionado
- tipo_sancao
- data_inicio/fim_sancao
- orgao_sancionador
- fonte

### Contrato
- cpf_cnpj_contratado
- numero_contrato
- valor
- data_assinatura
- orgao_contratante
- objeto

### AlertaIntegridade
- cpf_cnpj
- tipo_alerta
- nivel_risco
- descricao
- dados_json

### PoliticoProfile
- cpf
- nome
- partido
- cargo
- bens_declarados
- empresas_vinculadas

## 🎨 Interface

O sistema usa o template **Black Dashboard** com tema escuro otimizado para visualização de dados.

### Componentes
- Cards de estatísticas
- Tabelas responsivas
- Alertas coloridos por nível de risco
- Modais de detalhes
- Formulários de consulta

## 🔐 Segurança

- Autenticação obrigatória (Flask-Login)
- Sanitização de inputs
- Rate limiting em APIs externas
- Logs de auditoria
- Variáveis sensíveis em .env

## 📈 Roadmap

- [ ] Integração com Neo4j para grafos de relacionamento
- [ ] Download automático de bases do TSE
- [ ] Análise de evolução patrimonial
- [ ] Detecção de laranjas (intermediários)
- [ ] API GraphQL
- [ ] Dashboard em tempo real (WebSockets)
- [ ] Exportação de relatórios PDF
- [ ] Integração com Junta Comercial (QSA completo)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md).

## 📚 Bases de Dados Suportadas

### Implementadas
✅ Portal da Transparência (CEIS, CNEP, CEPIM, Contratos, Convênios)
✅ Receita Federal (CNPJ/QSA)
✅ PNCP (Contratos)

### Planejadas
🔜 TSE (Candidaturas, Bens, Doações)
🔜 DOU/DOEs (Diários Oficiais)
🔜 TCU (Auditorias)
🔜 DataJud CNJ
🔜 Base dos Dados

## 🆘 Suporte

- Issues: https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues
- Email: contato@exemplo.com

## 👥 Autores

- Renato Lucena - [@lucenarenato](https://github.com/lucenarenato)

---

**Aviso Legal:** Este sistema é uma ferramenta de análise de dados públicos. Os resultados devem ser interpretados como indicadores para investigação mais aprofundada, não como prova definitiva de irregularidades.
