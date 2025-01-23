from flask import Blueprint, render_template, redirect, url_for, request, session
from database.dados import jogadores
import random

form = Blueprint('form', __name__)

@form.route('/', methods = ['GET', 'POST'])
def jogo_form():
    return render_template('jogo_form.html')

@form.route('/adicionar_form', methods = ['GET', 'POST'])
def adicionar_form():

    if request.method == 'POST':
        nome = request.form.get('nome')
        if 'jogadores' not in session:
            session['jogadores'] = []
        session['jogadores'].append(nome)
        session.modified = True
        return redirect(url_for('home.biblioteca'))
    return render_template('jogo_form.html')
