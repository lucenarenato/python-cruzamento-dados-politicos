# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
import re
import json

from apps.home.integrity_service import analisar_integridade
from apps.home.api_services import consultar_multiplas_fontes, calcular_nivel_risco
from apps.home.data_crossing_service import (
    analisar_dados_locais,
    detectar_padroes_suspeitos
)
from apps.models import ConsultaIntegridade, RISK_LEVEL
from apps import db

def _determinar_tipo_documento(documento: str) -> str:
    """Determina se é CPF ou CNPJ"""
    digitos = re.sub(r'\D', '', documento)
    if len(digitos) == 11:
        return 'CPF'
    elif len(digitos) == 14:
        return 'CNPJ'
    return 'DESCONHECIDO'

def _obter_ip_cliente() -> str:
    """Obtém o IP do cliente da requisição"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
    return request.remote_addr or '0.0.0.0'


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
    historico = []

    try:
        if request.method == 'POST':
            cpf_cnpj = request.form.get('cpf_cnpj', '').strip()
            cpf_cnpj_limpo = re.sub(r'\D', '', cpf_cnpj)
            
            try:
                print(f"[MONITOR] Iniciando análise para: {cpf_cnpj}")
                resultado = analisar_integridade(cpf_cnpj)
                print(f"[MONITOR] Análise concluída")
                
                # Determinar nível de risco
                nivel_risco_str = resultado.get('resumo', {}).get('nivel_risco', 'medio')
                try:
                    nivel_risco = RISK_LEVEL[nivel_risco_str]
                except KeyError:
                    nivel_risco = RISK_LEVEL.medio
                
                # Determinar se encontrou registros
                ceis_ok = resultado.get('ceis', {}).get('ok', False)
                portal_ok = resultado.get('portal', {}).get('ok', False)
                
                # Criar registro de consulta
                print(f"[MONITOR] Criando registro de consulta")
                consulta = ConsultaIntegridade(
                    cpf_cnpj=cpf_cnpj_limpo,
                    tipo_documento=_determinar_tipo_documento(cpf_cnpj),
                    nivel_risco=nivel_risco,
                    encontrado_ceis=ceis_ok and resultado.get('ceis', {}).get('total_registros', 0) > 0,
                    encontrado_portal=portal_ok and resultado.get('portal', {}).get('total_registros', 0) > 0,
                    dados_ceis=resultado.get('ceis', {}).get('dados', []),
                    dados_portal=resultado.get('portal', {}).get('dados', []),
                    resultado_completo=resultado,
                    usuario_id=current_user.id if current_user.is_authenticated else None,
                    ip_origem=_obter_ip_cliente()
                )
                
                # Salvar no banco de dados
                print(f"[MONITOR] Salvando no banco de dados")
                consulta.save()
                print(f"[MONITOR] Salvo com sucesso")
                
                # Carregar histórico após salvar
                print(f"[MONITOR] Buscando histórico para {cpf_cnpj_limpo}")
                historico = ConsultaIntegridade.find_by_cpf_cnpj(cpf_cnpj_limpo)
                print(f"[MONITOR] Encontrados {len(historico)} registros no histórico")
                
            except Exception as e:
                import traceback
                print(f"[ERROR] Erro em monitor_integridade - Tipo: {type(e).__name__}")
                print(f"[ERROR] Mensagem: {str(e)}")
                print(f"[ERROR] Traceback:\n{traceback.format_exc()}")
                erro = f"Erro ao processar consulta: {str(e)}"

        return render_template(
            'home/monitor_integridade.html',
            segment='monitor_integridade',
            resultado=resultado,
            cpf_cnpj=cpf_cnpj,
            erro=erro,
            historico=historico or []
        )
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Erro fatal em monitor_integridade:")
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return render_template(
            'home/monitor_integridade.html',
            segment='monitor_integridade',
            resultado=None,
            cpf_cnpj="",
            erro=f"Erro ao carregar página: {str(e)}",
            historico=[]
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
