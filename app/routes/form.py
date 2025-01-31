from flask import Blueprint, render_template, redirect, url_for, request, session

form = Blueprint('form', __name__)

@form.route('/', methods=['GET', 'POST'])
def jogo_form():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if 'jogadores' not in session:
            session['jogadores'] = []

        if len(session['jogadores']) < 8:
            session['jogadores'].append(nome)
            session.modified = True

        return redirect(url_for('form.jogo_form'))

    # Exibe o botão de iniciar jogo apenas se houver 4 ou mais jogadores
    pode_iniciar = len(session.get('jogadores', [])) >= 4
    return render_template(
        'jogo_form.html',
        jogadores=session.get('jogadores', []),
        pode_iniciar=pode_iniciar
    )