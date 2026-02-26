# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.integrity_service import analisar_integridade


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/monitor-integridade', methods=['GET', 'POST'])
@login_required
def monitor_integridade():
    resultado = None
    cpf_cnpj = ""

    if request.method == 'POST':
        cpf_cnpj = request.form.get('cpf_cnpj', '').strip()
        resultado = analisar_integridade(cpf_cnpj)

    return render_template(
        'home/monitor_integridade.html',
        segment='monitor_integridade',
        resultado=resultado,
        cpf_cnpj=cpf_cnpj,
    )


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
