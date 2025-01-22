from flask import Blueprint, render_template, redirect, url_for, request


jogo = Blueprint('jogo', __name__)

@jogo.route('/resumo_rodada')
def resumo_rodada():
    return render_template('resumo.html')

@jogo.route('/acao/<int:id>', methods=['GET', 'POST'])
def acao():
    return render_template('acao.html') 