from flask import Blueprint, render_template, redirect, url_for, request
from database.dados import jogadores
id = 0
form = Blueprint('form', __name__)

@form.route('/', methods = ['GET', 'POST'])
def jogo_form():
    return render_template('jogo_form.html')

@form.route('/adicionar_form', methods = ['GET', 'POST'])
def adicionar_form():

    nome = request.form.get('jogador')
    
    jogador = {
        'id': len(jogadores) + 1,
        "nome": nome
    }
    
    jogadores.append(jogador)
    print(jogadores)
    
    
    
    # data = request.get_json()
    
    # with open('database/dados.py', 'w') as f:
    #     f.write(f"jogador = {data['aux_bd']}\n")
        
    return redirect('/biblioteca')
