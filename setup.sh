#!/bin/bash

# Script de Instalação Rápida
# Sistema de Cruzamento de Dados Abertos

set -e

echo "🚀 Iniciando instalação do Sistema de Cruzamento de Dados..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.9 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detectado"

# Criar ambiente virtual
echo ""
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Atualizar pip
echo ""
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo ""
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Configurar .env
echo ""
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp env.sample .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua TRANSPARENCIA_API_KEY"
    echo "   Obtenha em: http://api.portaldatransparencia.gov.br/"
else
    echo "✅ Arquivo .env já existe"
fi

# Criar diretórios de dados
echo ""
echo "📁 Criando diretórios de dados..."
mkdir -p old/data/raw
mkdir -p data

# Popular banco de dados (opcional)
echo ""
read -p "Deseja popular o banco com dados de exemplo? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "💾 Populando banco de dados..."
    python populate_db.py
fi

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Edite o arquivo .env e adicione sua TRANSPARENCIA_API_KEY"
echo "   2. Execute: python run.py"
echo "   3. Acesse: http://localhost:5085"
echo ""
echo "📚 Documentação:"
echo "   - Guia Rápido: QUICK_START.md"
echo "   - Documentação Completa: SISTEMA_README.md"
echo ""
echo "🎉 Pronto para começar!"
