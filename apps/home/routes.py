# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.integrity_service import analisar_integridade
from apps.home.api_services import consultar_multiplas_fontes, calcular_nivel_risco
from apps.home.data_crossing_service import (
    analisar_dados_locais,
    detectar_padroes_suspeitos
)


@blueprint.route('/index')
@login_required
def index():
    """Dashboard principal com estatísticas"""
    try:
        # Carregar estatísticas dos dados locais
        analise = analisar_dados_locais()
        padroes = detectar_padroes_suspeitos(analise)
        
        return render_template(
            'home/index.html',
            segment='index',
            stats=analise,
            padroes=padroes
        )
    except Exception as e:
        # Se não houver dados, exibir dashboard vazio
        return render_template(
            'home/index.html',
            segment='index',
            stats=None,
            erro=str(e)
        )


@blueprint.route('/monitor-integridade', methods=['GET', 'POST'])
@login_required
def monitor_integridade():
    resultado = None
    cpf_cnpj = ""
    erro = None

    if request.method == 'POST':
        cpf_cnpj = request.form.get('cpf_cnpj', '').strip()
        try:
            resultado = analisar_integridade(cpf_cnpj)
        except Exception as e:
            erro = f"Erro ao processar consulta: {str(e)}"

    return render_template(
        'home/monitor_integridade.html',
        segment='monitor_integridade',
        resultado=resultado,
        cpf_cnpj=cpf_cnpj,
        erro=erro
    )


@blueprint.route('/analise-completa', methods=['GET', 'POST'])
@login_required
def analise_completa():
    """Análise completa consultando múltiplas APIs"""
    resultado = None
    cpf_cnpj = ""

    if request.method == 'POST':
        cpf_cnpj = request.form.get('cpf_cnpj', '').strip()
        
        # Consultar múltiplas fontes
        dados = consultar_multiplas_fontes(cpf_cnpj)
        
        # Calcular nível de risco
        avaliacao = calcular_nivel_risco(dados)
        
        resultado = {
            "documento": dados.get("documento"),
            "tipo": dados.get("tipo"),
            "documento_formatado": dados.get("documento_formatado"),
            "fontes": dados.get("fontes", {}),
            "avaliacao": avaliacao
        }

    return render_template(
        'home/analise_completa.html',
        segment='analise_completa',
        resultado=resultado,
        cpf_cnpj=cpf_cnpj,
    )


@blueprint.route('/sancoes-contratos')
@login_required
def sancoes_contratos():
    """Visualização de sanções vs contratos"""
    try:
        analise = analisar_dados_locais()
        
        return render_template(
            'home/sancoes_contratos.html',
            segment='sancoes_contratos',
            dados=analise
        )
    except Exception as e:
        return render_template(
            'home/sancoes_contratos.html',
            segment='sancoes_contratos',
            dados=None,
            erro=str(e)
        )


@blueprint.route('/api/estatisticas')
@login_required
def api_estatisticas():
    """API JSON com estatísticas"""
    try:
        analise = analisar_dados_locais()
        return jsonify(analise)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@blueprint.route('/api/consultar/<cpf_cnpj>')
@login_required
def api_consultar(cpf_cnpj):
    """API JSON para consultar CPF/CNPJ"""
    try:
        dados = consultar_multiplas_fontes(cpf_cnpj)
        avaliacao = calcular_nivel_risco(dados)
        dados["avaliacao"] = avaliacao
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
