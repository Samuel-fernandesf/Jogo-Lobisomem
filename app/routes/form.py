from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database.dados import jogadores

form = Blueprint('form', __name__)

id = 1 

@form.route('/', methods=['GET', 'POST'])
def jogo_form():

    global id

    if request.method == 'POST':
        nome = request.form.get('nome')

        # Verifica se o nome já está na sessão
        if nome in session.get('jogadores', []):
            flash("Nome já está em uso. Escolha outro.", category="danger")
            return redirect(url_for('form.jogo_form'))

        #Adiciona os dados no banco dados
        jogadores.append({'id': id,
                          'nome': nome})
        id +=1

        if 'jogadores' not in session:
            session['jogadores'] = []

        if len(session['jogadores']) < 8:
            session['jogadores'].append(nome)
            session.modified = True
        else:
            flash('Limite de jogadores atingido!', category='danger')
            return redirect(url_for('form.jogo_form'))

        return redirect(url_for('form.jogo_form'))

    # Exibe o botão de iniciar jogo apenas se houver 4 ou mais jogadores
    pode_iniciar = len(session.get('jogadores', [])) >= 4
    return render_template(
        'jogo_form.html',
        jogadores=session.get('jogadores', []),
        pode_iniciar=pode_iniciar
    )

@form.route('/remover/<nome>')
def remover(nome):

    remove_jogador = None

    #Remove da sessão
    if nome in session.get('jogadores', []):
        session['jogadores'].remove(nome)
        session.modified = True    
    return redirect(url_for('form.jogo_form'))
