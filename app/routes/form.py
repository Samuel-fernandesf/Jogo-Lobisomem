from flask import Blueprint, render_template, redirect, url_for, request

form = Blueprint('form', __name__)

@form.route('/', methods = ['GET', 'POST'])
def jogo_form():
    return render_template('jogo_form.html')

@form.route('/adicionar_form', methods = ['GET', 'POST'])
def adicionar_form():

    data = request.get_json()
    
    with open('database/dados.py', 'w') as f:
        f.write(f"jogador: {data['aux_bd']}\n")
        
    return redirect('/biblioteca')
