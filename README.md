# Sistema de Cruzamento de Dados Abertos - Governo Federal 🇧🇷

Sistema Python/Flask para **identificar empresas sancionadas que continuam recebendo contratos públicos** através do cruzamento inteligente de múltiplas bases de dados abertas do governo federal brasileiro.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Objetivo

Detectar irregularidades e possível corrupção através da análise automatizada de dados públicos:

- ✅ Empresas sancionadas (CEIS, CNEP, CEPIM)
- ✅ Contratos públicos federais
- ✅ Dados de políticos (TSE)
- ✅ Vínculos empresariais (QSA Receita Federal)

### 💡 Casos de Uso Real

O sistema é capaz de identificar irregularidades como:
- **+2M de contratos analisados**
- **+R$ 11 trilhões em valor total**
- **+R$ 7 bilhões em contratos firmados durante sanção ativa** (proibidos por lei)

## 🚀 Quick Start

```bash
# 1. Clonar repositório
git clone https://github.com/lucenarenato/python-cruzamento-dados-politicos.git
cd python-cruzamento-dados-politicos

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp env.sample .env
nano .env  # Adicione TRANSPARENCIA_API_KEY

# 5. (Opcional) Popular banco com dados de exemplo
python populate_db.py

# 6. Executar aplicação
python run.py
```

Acesse: **http://localhost:5085**

## 📚 Documentação

- 📖 [**Guia Rápido (5 min)**](QUICK_START.md) - Comece aqui!
- 📘 [**Documentação Completa**](SISTEMA_README.md) - Todas as funcionalidades
- 📝 [**Anotações do Projeto**](Anotacoes.md) - Ideias e planejamento

## ✨ Funcionalidades

### 📊 Dashboard Inteligente
- Estatísticas em tempo real de contratos e sanções
- Alertas automáticos de padrões suspeitos
- Top empresas com contratos irregulares
- Métricas de valores irregulares totais

### 🔍 Monitor de Integridade
- Consulta rápida de CPF/CNPJ
- Busca no Portal da Transparência
- Verificação em bases locais (CEIS)
- Avaliação automática de nível de risco

### 🎯 Análise Completa MultiAPI
Consulta integrada em **8+ fontes de dados**:

| Fonte | Descrição |
|-------|-----------|
| **CEIS** | Cadastro de Empresas Inidôneas e Sancionadas (CGU) |
| **CNEP** | Cadastro Nacional de Empresas Punidas (CGU) |
| **CEPIM** | Empresas Impedidas de Licitar (CGU) |
| **Contratos** | Contratos Federais (Portal da Transparência) |
| **Convênios** | Convênios Federais |
| **CNPJ/QSA** | Dados Receita Federal + Quadro de Sócios |
| **PNCP** | Portal Nacional de Contratações Públicas |
| **TSE** | Dados Eleitorais (Candidaturas, Bens, Doações) |

### ⚠️ Sanções vs Contratos
- Cruzamento automático de sanções e contratos
- Detecção de contratos durante período de sanção
- Análise de valores irregulares totais
- Detalhamento por empresa com modal interativo

### 🤖 Detecção Automática de Padrões
- Múltiplos contratos durante sanção ativa
- Contratos de alto valor em empresas sancionadas
- Taxa de irregularidade elevada
- Vínculos de políticos com empresas irregulares

## 🏗️ Arquitetura Técnica

```
apps/
├── models.py                      # SQLAlchemy: Sanção, Contrato, Alerta, Político
├── home/
│   ├── routes.py                 # Flask routes + API endpoints
│   ├── integrity_service.py      # Serviço básico de integridade
│   ├── api_services.py          # Clientes para APIs públicas
│   └── data_crossing_service.py # Motor de cruzamento de dados
templates/home/
├── index.html                    # Dashboard principal
├── analise_completa.html        # Análise multiAPI
├── sancoes_contratos.html       # Visualização de irregularidades
└── monitor_integridade.html     # Monitor simples
```

## 🔑 Obter Chave da API

### Portal da Transparência (Obrigatório)

1. Acesse: http://api.portaldatransparencia.gov.br/
2. Clique em "Solicitar Chave"
3. Preencha o formulário com seu email
4. Receba a chave por email
5. Adicione ao `.env`:

```env
TRANSPARENCIA_API_KEY=sua_chave_aqui
```

## 📥 Importar Dados (Opcional)

### CEIS - Empresas Sancionadas

```bash
mkdir -p old/data/raw
# Baixar de: https://portaldatransparencia.gov.br/download-de-dados/ceis
# Salvar em: old/data/raw/ceis.csv
```

### Contratos Públicos

```bash
# Baixar de: https://portaldatransparencia.gov.br/download-de-dados/contratos
# Salvar em: old/data/raw/contracts.csv
```

## 🎨 Interface

Sistema construído com **Black Dashboard** (Bootstrap 5) com tema dark otimizado para visualização de dados.

![Dashboard Preview](https://user-images.githubusercontent.com/51070104/196730732-dda1794b-93ce-48cb-bc5c-182411495512.png)

<br />

## 📡 API REST JSON

O sistema expõe endpoints JSON para integração:

### Estatísticas Gerais
```bash
GET /api/estatisticas
```

**Resposta:**
```json
{
	"total_sancoes": 1234,
	"total_contratos": 5678,
	"total_irregularidades": 89,
	"valor_total_contratos": 11000000000.00,
	"valor_irregular": 7000000000.00,
	"percentual_irregular": 63.64,
	"empresas_irregulares": [...]
}
```

### Consultar CPF/CNPJ
```bash
GET /api/consultar/<cpf_cnpj>
```

**Exemplo:**
```bash
curl http://localhost:5085/api/consultar/12345678000190
```

**Resposta:**
```json
{
	"documento": "12345678000190",
	"tipo": "CNPJ",
	"documento_formatado": "12.345.678/0001-90",
	"avaliacao": {
		"nivel_risco": "critico",
		"pontuacao": 100,
		"alertas": ["Encontrado em CEIS (2 registro(s))"],
		"total_fontes_consultadas": 8,
		"fontes_com_dados": 3
	},
	"fontes": {
		"ceis": {"ok": true, "total": 2, "dados": [...]},
		"cnep": {"ok": true, "total": 0},
		"contratos": {"ok": true, "total": 5, "dados": [...]}
	}
}
```

## 🧪 Exemplos de Uso

### Python - Consulta Programática

```python
from apps.home.api_services import consultar_multiplas_fontes, calcular_nivel_risco

# Consultar CNPJ
dados = consultar_multiplas_fontes("12345678000190")

# Avaliar risco
avaliacao = calcular_nivel_risco(dados)

print(f"Nível de Risco: {avaliacao['nivel_risco']}")
print(f"Alertas: {avaliacao['alertas']}")
```

### Python - Análise de Dados Locais

```python
from apps.home.data_crossing_service import analisar_dados_locais, detectar_padroes_suspeitos

# Analisar dados locais CEIS + Contratos
analise = analisar_dados_locais()

print(f"Irregularidades encontradas: {analise['total_irregularidades']}")
print(f"Valor irregular: R$ {analise['valor_irregular']:,.2f}")

# Detectar padrões
padroes = detectar_padroes_suspeitos(analise)
for padrao in padroes:
		print(f"{padrao['tipo']}: {padrao['descricao']}")
```

### Curl - Via API

```bash
# Consultar empresa
curl -s http://localhost:5085/api/consultar/12345678000190 | jq '.avaliacao'

# Obter estatísticas
curl -s http://localhost:5085/api/estatisticas | jq '.total_irregularidades'
```

## 📊 Níveis de Risco

| Nível | Pontuação | Critérios |
|-------|-----------|-----------|
| 🔴 **CRÍTICO** | ≥ 50 | CEIS ou CNEP |
| 🟠 **ALTO** | 30-49 | CEPIM + Contratos |
| 🟡 **MÉDIO** | 10-29 | Múltiplos contratos |
| 🟢 **BAIXO** | < 10 | Poucos registros |

## 🐳 Deploy com Docker

### Build e Run

```bash
# Build da imagem
docker build -t cruzamento-dados .

# Executar container
docker run -d \
	-p 5085:5000 \
	-e TRANSPARENCIA_API_KEY=sua_chave \
	--name cruzamento-dados \
	cruzamento-dados
```

### Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## 🚀 Deploy na Nuvem

### Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Fork este repositório
2. Conecte ao Render
3. Configure `TRANSPARENCIA_API_KEY` nas variáveis de ambiente
4. Deploy automático!

### Heroku

```bash
# Login
heroku login

# Criar app
heroku create meu-cruzamento-dados

# Configurar variáveis
heroku config:set TRANSPARENCIA_API_KEY=sua_chave

# Deploy
git push heroku main
```

## 🗂️ Estrutura de Dados

### Modelos SQLAlchemy

**Sancao**
```python
cpf_cnpj: String(14)
nome_sancionado: String(256)
tipo_sancao: String(100)  # CEIS, CNEP, CEPIM
data_inicio_sancao: Date
data_fim_sancao: Date
orgao_sancionador: String(256)
fonte: String(50)
```

**Contrato**
```python
cpf_cnpj_contratado: String(14)
numero_contrato: String(100)
valor: Numeric(15, 2)
data_assinatura: Date
orgao_contratante: String(256)
objeto: Text
```

**AlertaIntegridade**
```python
cpf_cnpj: String(14)
tipo_alerta: String(100)
nivel_risco: Enum(RISK_LEVEL)
descricao: Text
dados_json: JSON
```

## 🔒 Segurança

- ✅ Autenticação obrigatória (Flask-Login)
- ✅ Sanitização de inputs
- ✅ Rate limiting em APIs
- ✅ HTTPS recomendado em produção
- ✅ Variáveis sensíveis em `.env`
- ✅ CORS configurável

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Áreas para Contribuição

- 📊 Novos gráficos e visualizações
- 🔌 Integração com mais APIs públicas
- 🧪 Testes unitários e de integração
- 📝 Documentação e tutoriais
- 🌐 Internacionalização (i18n)
- 🎨 Melhorias de UI/UX

## 📈 Roadmap

### Em Desenvolvimento
- [ ] Integração com Neo4j para grafos de relacionamento
- [ ] Download automático de bases do TSE
- [ ] Análise temporal de evolução patrimonial
- [ ] Detecção de "laranjas" (intermediários)
- [ ] Exportação de relatórios PDF/Excel

### Planejado
- [ ] API GraphQL
- [ ] Dashboard em tempo real (WebSockets)
- [ ] Machine Learning para detecção de padrões
- [ ] Integração com Junta Comercial estaduais
- [ ] App mobile (React Native/Flutter)
- [ ] Sistema de notificações por email/WhatsApp

## 📚 Bases de Dados Disponíveis

### ✅ Implementadas
- Portal da Transparência (CEIS, CNEP, CEPIM, Contratos, Convênios)
- Receita Federal (CNPJ/QSA via ReceitaWS)
- PNCP (Portal Nacional de Contratações)

### 🔜 Em Integração
- TSE (Candidaturas, Bens, Doações)
- DOU/DOEs (Diários Oficiais)
- TCU (Auditorias e Acórdãos)
- DataJud CNJ (Processos Judiciais)

### 📋 Lista Completa (79 Bases)

Veja a lista completa de 79 bases de dados públicas brasileiras disponíveis no arquivo [Anotacoes.md](Anotacoes.md).

## 🆘 Troubleshooting

### Erro: "API Key não configurada"
**Solução:** Configure `TRANSPARENCIA_API_KEY` no arquivo `.env`

### Erro: "Nenhum dado no Dashboard"
**Solução:** Importe dados locais ou ignore - use as funcionalidades de consulta online

### Erro: "ReceitaWS timeout"
**Solução:** ReceitaWS é uma API não oficial e pode ter instabilidades. Tente novamente.

### Erro: "Module not found"
**Solução:** Execute `pip install -r requirements.txt`

## 📞 Suporte

- 📖 [Documentação Completa](SISTEMA_README.md)
- 🐛 [Reportar Bug](https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues)
- 💬 [Discussões](https://github.com/lucenarenato/python-cruzamento-dados-politicos/discussions)
- 📧 Email: (adicione seu email aqui)

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## 👥 Autores

- **Renato Lucena** - [@lucenarenato](https://github.com/lucenarenato)

## 🙏 Agradecimentos

- **CGU** - Controladoria Geral da União (Portal da Transparência)
- **Creative Tim** - Black Dashboard Theme
- **AppSeed** - Flask Boilerplate Base
- Comunidade Open Source brasileira

## ⚖️ Aviso Legal

Este sistema é uma **ferramenta de análise de dados públicos** para fins de transparência e controle social. Os resultados devem ser interpretados como **indicadores para investigação mais aprofundada**, não como prova definitiva de irregularidades. 

O uso dos dados deve respeitar:
- Lei de Acesso à Informação (LAI - Lei 12.527/2011)
- Lei Geral de Proteção de Dados (LGPD - Lei 13.709/2018)
- Código de Ética e boas práticas de uso de dados públicos

---

## 🌟 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela!**

[Reportar Bug](https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues) · [Solicitar Feature](https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues) · [Contribuir](CONTRIBUTING.md)

</div>

---

## 🔗 Links Úteis

- [Portal da Transparência](http://portaldatransparencia.gov.br/)
- [API Portal da Transparência](http://api.portaldatransparencia.gov.br/)
- [PNCP - Portal Nacional de Contratações](https://pncp.gov.br/)
- [TSE Dados Abertos](https://dadosabertos.tse.jus.br/)
- [Base dos Dados](https://basedosdados.org/)
- [Querido Diário](https://queridodiario.ok.org.br/)

<br />

**Baseado no template Flask Black Dashboard** - Adaptado para análise de dados abertos brasileiros.
