# Sistema de Auditoria de Consultas - Monitor de Integridade

## Resumo das Alterações

Foi implementado um sistema completo de auditoria e armazenamento de histórico para as consultas realizadas no módulo de **Monitor de Integridade** (http://localhost:5085/monitor-integridade).

### O que foi feito:

#### 1. **Novo Modelo de Banco de Dados: `ConsultaIntegridade`**
   - **Arquivo:** `apps/models.py`
   - **Tabela:** `consultas_integridade`
   - **Campos principais:**
     - `cpf_cnpj`: CPF ou CNPJ consultado (indexado)
     - `tipo_documento`: 'CPF' ou 'CNPJ'
     - `nivel_risco`: Nível de risco detectado (ENUM: baixo, médio, alto, crítico)
     - `encontrado_ceis`: Se foi encontrado em registros CEIS
     - `encontrado_portal`: Se foi encontrado no Portal da Transparência
     - `dados_ceis`: JSON com registros CEIS encontrados
     - `dados_portal`: JSON com dados do Portal
     - `resultado_completo`: JSON com análise completa
     - `data_consulta`: Data/hora da consulta (indexada)
     - `usuario_id`: ID do usuário que fez a consulta
     - `ip_origem`: IP de origem da requisição

#### 2. **Atualização da Rota `/monitor-integridade`**
   - **Arquivo:** `apps/home/routes.py`
   - **Novas funcionalidades:**
     - Automaticamente salva cada consulta no banco de dados
     - Armazena resultado completo em JSON
     - Registra IP do cliente e usuário autenticado
     - Carrega histórico de consultas anteriores para o mesmo documento
     - Detecta e armazena tipo de documento (CPF/CNPJ)

#### 3. **Atualização do Template**
   - **Arquivo:** `templates/home/monitor_integridade.html`
   - **Novas seções:**
     - Tabela com histórico de todas as consultas para o documento
     - Exibe data/hora, nível de risco, resultados CEIS/Portal
     - Mostra quem (usuário/IP) fez cada consulta

#### 4. **Correção do Caminho dos Dados**
   - Ajustado `_default_ceis_csv_path()` em `apps/home/integrity_service.py`
   - Mudou de `.parents[3]` para `.parents[2]` (caminho correto)
   - Criada estrutura `data/raw/` na raiz do projeto

## Como Usar

### 1. **Reiniciar a Aplicação**
Após estas mudanças, reinicie o Docker:

```bash
docker-compose down
docker-compose up --build
```

A tabela `consultas_integridade` será criada automaticamente pelo `db.create_all()`.

### 2. **Realizar uma Consulta**
1. Acesse http://localhost:5085/monitor-integridade
2. Digite um CPF ou CNPJ válido
3. Clique em "Cruzar dados"
4. A consulta será:
   - Processada
   - Resultado exibido na tela
   - Salva automaticamente no banco de dados
   - Histórico carregado para visualização

### 3. **Visualizar Histórico**
Ao consultar novamente o mesmo documento, a tabela "Histórico de Consultas" mostrará:
- Data e hora de cada consulta
- Nível de risco encontrado
- Se havia registros em CEIS
- Se havia registros no Portal da Transparência
- Quem fez a consulta (usuário ou IP)

## Benefícios

1. **Auditoria Completa**: Rastreia todas as consultas realizadas
2. **Histórico de Riscos**: Vê evolução de riscos para uma entidade ao longo do tempo
3. **Conformidade**: Registra quem consultou o quê e quando
4. **Análise Posterior**: Dados armazenados em JSON para análise futura
5. **Segurança**: IP de origem registrado para investigação de abusos

## Queries Úteis

### Consultar histórico de um documento:
```python
from apps.models import ConsultaIntegridade

# Última consulta
ultima = ConsultaIntegridade.find_by_cpf_cnpj("12345678901")[-1]

# Todas as consultas
todas = ConsultaIntegridade.find_by_cpf_cnpj("12345678901")

# Consultas recentes (últimos 30 dias)
recentes = ConsultaIntegridade.get_recent(dias=30)

# Consultas por nível de risco
altos_riscos = ConsultaIntegridade.get_by_risk_level(RISK_LEVEL.alto)
```

## Estrutura de Dados Armazenada

O campo `resultado_completo` armazena a resposta completa:

```json
{
  "documento": "12345678901",
  "portal": {
    "ok": false,
    "erro": "Erro HTTP 403 ao consultar API.",
    "detalhes": ""
  },
  "ceis": {
    "ok": true,
    "documento": "12345678901",
    "fonte": "CEIS (arquivo local)",
    "arquivo": "/path/to/data/raw/ceis.csv",
    "total_registros": 0,
    "dados": []
  },
  "resumo": {
    "nivel_risco": "baixo",
    "motivos": ["Nenhum registro encontrado nas fontes consultadas."],
    "fontes_consultadas": 2,
    "total_registros": 0
  }
}
```

## Próximos Passos Sugeridos

1. Criar uma rota de visualização de relatórios por nível de risco
2. Adicionar filtros por data no histórico
3. Exportar dados em CSV/JSON
4. Dashboard com estatísticas de consultas
5. Alertas automáticos para mudanças de risco
6. Backup periódico dos dados em JSON
