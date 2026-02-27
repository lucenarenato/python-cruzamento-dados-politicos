# Guia de Contribuição

Obrigado por considerar contribuir com o Sistema de Cruzamento de Dados Abertos! 🎉

## 🤝 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/python-cruzamento-dados-politicos.git
cd python-cruzamento-dados-politicos

# Adicione o repositório original como upstream
git remote add upstream https://github.com/lucenarenato/python-cruzamento-dados-politicos.git
```

### 2. Crie uma Branch

```bash
# Atualize seu main
git checkout main
git pull upstream main

# Crie uma branch para sua feature/fix
git checkout -b feature/minha-nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 3. Desenvolva

```bash
# Configure o ambiente
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Faça suas alterações
# Execute testes (quando disponíveis)
# python -m pytest

# Execute a aplicação para testar
python run.py
```

### 4. Commit

```bash
# Adicione os arquivos modificados
git add .

# Faça commit com mensagem descritiva
git commit -m "feat: adiciona integração com API do TSE"
```

#### Padrão de Mensagens de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `style:` - Formatação, ponto e vírgula, etc
- `refactor:` - Refatoração de código
- `test:` - Adição de testes
- `chore:` - Manutenção, dependências, etc

**Exemplos:**
```
feat: adiciona consulta à API do TCU
fix: corrige cálculo de nível de risco
docs: atualiza instruções de instalação
refactor: melhora performance do cruzamento de dados
```

### 5. Push e Pull Request

```bash
# Push para seu fork
git push origin feature/minha-nova-funcionalidade

# Abra um Pull Request no GitHub
# Descreva suas mudanças detalhadamente
```

## 📋 Checklist do Pull Request

Antes de submeter, verifique:

- [ ] O código segue o estilo do projeto (PEP 8 para Python)
- [ ] Comentários e documentação estão atualizados
- [ ] Não há warnings ou erros no console
- [ ] Testei localmente as mudanças
- [ ] Atualizei o README se necessário
- [ ] Adicionei exemplos de uso se for nova funcionalidade
- [ ] O commit message segue o padrão

## 🎯 Áreas para Contribuição

### Prioridade Alta

1. **Testes Unitários**
   - Criar testes para `api_services.py`
   - Testes para `data_crossing_service.py`
   - Testes de integração das rotas

2. **Integração com TSE**
   - Parser de arquivos CSV do TSE
   - Importação de candidaturas
   - Análise de bens declarados
   - Cruzamento de doações

3. **Visualizações**
   - Gráficos com Chart.js
   - Timeline de sanções
   - Mapa de calor de irregularidades
   - Grafos de relacionamentos (NetworkX/D3.js)

### Prioridade Média

4. **Performance**
   - Cache de consultas API
   - Otimização de queries SQL
   - Lazy loading de dados
   - Paginação em tabelas

5. **Exportação**
   - Relatórios PDF
   - Exportação para Excel
   - JSON estruturado
   - CSV customizado

6. **Novas APIs**
   - DOU (Diários Oficiais)
   - TCU (Tribunal de Contas)
   - DataJud CNJ
   - Juntas Comerciais estaduais

### Outras Contribuições

7. **Documentação**
   - Tutoriais em vídeo
   - Artigos no blog
   - Exemplos de uso real
   - Tradução para inglês

8. **UI/UX**
   - Melhorias de interface
   - Responsividade mobile
   - Modo claro/escuro
   - Acessibilidade (WCAG)

## 🏗️ Estrutura do Projeto

```
apps/
├── __init__.py           # Inicialização Flask
├── config.py             # Configurações
├── models.py             # Modelos SQLAlchemy
├── authentication/       # Sistema de login
├── home/
│   ├── routes.py        # Rotas principais
│   ├── api_services.py  # Clientes API
│   └── data_crossing_service.py  # Lógica de cruzamento
├── charts/              # Gráficos (a expandir)
└── dyn_dt/              # Tabelas dinâmicas

templates/home/          # Templates Jinja2
static/assets/           # CSS, JS, imagens
```

## 💻 Configuração de Desenvolvimento

### Variáveis de Ambiente

```env
# .env para desenvolvimento
DEBUG=True
FLASK_ENV=development
SECRET_KEY=chave-de-desenvolvimento
TRANSPARENCIA_API_KEY=sua_chave_aqui
DATABASE_URL=sqlite:///db.sqlite3
```

### Executar em Modo Debug

```bash
# Com auto-reload
export FLASK_DEBUG=1
python run.py

# Ou
flask run --debug
```

### Executar Testes (Futuro)

```bash
# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Com cobertura
pytest --cov=apps tests/
```

## 📝 Estilo de Código

### Python (PEP 8)

```python
# Use type hints
def consultar_cnpj(cnpj: str) -> dict[str, Any]:
    """
    Consulta CNPJ na Receita Federal
    
    Args:
        cnpj: CNPJ com 14 dígitos
        
    Returns:
        Dicionário com dados do CNPJ
    """
    pass

# Nomes descritivos
valor_irregular = calcular_valor_irregular(contratos)

# Docstrings em português (projeto brasileiro)
# Código em inglês quando fizer sentido técnico
```

### SQL/Queries

```python
# Evite consultas N+1
empresas = Sancao.query.options(
    db.joinedload(Sancao.contratos)
).all()

# Use índices
cpf_cnpj = db.Column(db.String(14), index=True)
```

### Templates

```html
<!-- HTML semântico -->
<section class="dashboard">
  <header>
    <h1>{{ titulo }}</h1>
  </header>
  
  <!-- Classes Bootstrap -->
  <div class="card">
    <div class="card-body">
      {{ conteudo }}
    </div>
  </div>
</section>
```

## 🐛 Reportando Bugs

### Template de Issue

```markdown
**Descrição do Bug**
Descrição clara do problema

**Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

**Comportamento Esperado**
O que deveria acontecer

**Screenshots**
Se aplicável, adicione capturas de tela

**Ambiente:**
 - OS: [e.g. Ubuntu 22.04]
 - Python: [e.g. 3.11]
 - Flask: [e.g. 3.0.0]

**Informações Adicionais**
Qualquer contexto sobre o problema
```

## 💡 Solicitando Features

### Template de Feature Request

```markdown
**A feature resolve um problema?**
Descrição clara do problema: "Eu sempre fico frustrado quando [...]"

**Solução Proposta**
Descrição clara da solução desejada

**Alternativas Consideradas**
Outras soluções que você considerou

**Contexto Adicional**
Screenshots, referências, etc.
```

## 🔍 Code Review

### O que verificamos

- [ ] Código funciona corretamente
- [ ] Não quebra funcionalidades existentes
- [ ] Segue o estilo do projeto
- [ ] Está bem documentado
- [ ] Testes passam (quando houver)
- [ ] Sem dados sensíveis no código
- [ ] Performance adequada

### Feedback

- Seja construtivo e respeitoso
- Explique o "porquê" das sugestões
- Aprecie o esforço do contribuidor
- Use emojis: 👍 ✅ 🎉 💡 🐛

## 📜 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

## 🙏 Reconhecimento

Todos os contribuidores serão adicionados ao README e ao CONTRIBUTORS.md!

## 📞 Contato

- Issues: [GitHub Issues](https://github.com/lucenarenato/python-cruzamento-dados-politicos/issues)
- Discussões: [GitHub Discussions](https://github.com/lucenarenato/python-cruzamento-dados-politicos/discussions)

---

**Obrigado por contribuir! 🚀**
