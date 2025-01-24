from flask import Blueprint, render_template, redirect, url_for, request, session
from models.character import Player
import random


jogo = Blueprint('jogo', __name__)

@jogo.route('/iniciar', methods=['POST'])
def iniciar_jogo():
    if 'jogadores' in session:
        papeis = ['Condessa', 'Vampiro', 'Campones', 'Açougueiro', 'Bruxa', 'Caçador', 'Guarda-Costa']  
        random.shuffle(papeis)
        session['papeis_jogadores'] = {}
        
        for i, jogador in enumerate(session['jogadores']):
            session['papeis_jogadores'][jogador] = papeis[i % len(papeis)]  
        session.modified = True
        return redirect(url_for('jogo.mostrar_selecao'))  

    return redirect(url_for('home'))

@jogo.route('/ver_papel/<nome>')
def ver_papel(nome):
    if 'papeis_jogadores' in session and nome in session['papeis_jogadores']:
        papel = session['papeis_jogadores'][nome]
            
        return render_template('ver_papel.html', nome=nome, papel=papel)
    return redirect(url_for('home'))


#Deverá ser explicado a equipe
@jogo.route('/papeis')
def mostrar_selecao():
    if 'jogadores' in session:
        papeis = session.get('papeis_jogadores', {})
        papeis_serializaveis = {k: str(v) for k, v in papeis.items()}
        
        jogadores = session['jogadores']
        papeis = session['papeis_jogadores']
        
        if not all(jogador in papeis for jogador in jogadores):
            return "Erro: Nem todos os jogadores têm papéis atribuídos.", 400
        papeis_serializaveis = {k: str(v) for k, v in papeis.items()}
        
        return render_template('selecao_papeis.html', jogadores=session['jogadores'], papeis=papeis_serializaveis)
    return redirect(url_for('home'))


@jogo.route('/iniciar_acoes', methods=['POST', 'GET'])
def iniciar_acoes():
    if 'papeis_jogadores' in session:
        jogadores_com_acao = [
            jogador for jogador, papel in session['papeis_jogadores'].items()
            if papel in ['Condessa', 'Vampiro', 'Açougueiro', 'Bruxa', 'Caçador', 'Guarda-Costa'] 
        ]

        session['jogador_atual'] = 0  
        session['acoes'] = []  
        session['fila_acoes'] = jogadores_com_acao  
        session.modified = True

        return redirect(url_for('jogo.realizar_acao'))
    return redirect(url_for('home'))

@jogo.route('/realizar_acao', methods=['GET', 'POST'])
def realizar_acao():
    if 'fila_acoes' not in session or 'jogador_atual' not in session:
        return redirect(url_for('home'))

    fila_acoes = session['fila_acoes']
    jogador_atual_idx = session['jogador_atual']

    if jogador_atual_idx >= len(fila_acoes):
        return redirect(url_for('jogo.finalizar_fase'))

    jogador_atual = fila_acoes[jogador_atual_idx]
    papel = session['papeis_jogadores'][jogador_atual]

    if request.method == 'POST':

        acao = request.form.get('acao')
        if acao:
            session['acoes'].append({'jogador': jogador_atual, 'papel': papel, 'acao': acao})
            session['jogador_atual'] += 1  
            session.modified = True
            return redirect(url_for('jogo.realizar_acao'))

    return render_template('realizar_acao.html', jogador=jogador_atual, papel=papel)




