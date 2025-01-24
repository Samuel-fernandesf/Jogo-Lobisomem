from flask import Blueprint, render_template, redirect, url_for, request, session
from models.character import Player, Assassino, Bruxa, GuardaCosta
import random

jogo = Blueprint('jogo', __name__)

@jogo.route('/iniciar', methods=['POST','GET'   ])
def iniciar_jogo():
    if 'jogadores' in session:
        papeis = ['Condessa', 'Vampiro', 'Campones', 'Açougueiro', 'Bruxa', 'Caçador', 'Guarda-Costa']
        random.shuffle(papeis)
        session['papeis_jogadores'] = {}
        session['players_objetos'] = {}

        for i, jogador in enumerate(session['jogadores']):
            papel = papeis[i % len(papeis)]
            session['papeis_jogadores'][jogador] = papel  

            if papel == "Vampiro":
                player_obj = Assassino(jogador)
            elif papel == "Bruxa":
                player_obj = Bruxa(jogador)
            elif papel == "Guarda-Costa":
                player_obj = GuardaCosta(jogador)
            else:
                player_obj = Player(jogador, papel)

            session['players_objetos'][jogador] = player_obj.to_dict()  # Agora serializável

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
        return redirect(url_for('jogo.resumo_rodada'))

    jogador_atual = fila_acoes[jogador_atual_idx]  # Corrigido para pegar o jogador atual do índice
    papel = session['papeis_jogadores'][jogador_atual]

    if request.method == 'POST':
        alvo_nome = request.form.get('alvo')

        if alvo_nome and alvo_nome in session['players_objetos']:
            jogador_data = session['players_objetos'][jogador_atual]
            alvo_data = session['players_objetos'][alvo_nome]

            # Convertendo os dicionários de volta para objetos
            if jogador_data["papel"] == "Vampiro":
                jogador_obj = Assassino.from_dict(jogador_data)
            elif jogador_data["papel"] == "Bruxa":
                jogador_obj = Bruxa.from_dict(jogador_data)
            elif jogador_data["papel"] == "Guarda-Costa":
                jogador_obj = GuardaCosta.from_dict(jogador_data)
            else:
                jogador_obj = Player.from_dict(jogador_data)

            if alvo_data["papel"] == "Vampiro":
                alvo_obj = Assassino.from_dict(alvo_data)
            elif alvo_data["papel"] == "Bruxa":
                alvo_obj = Bruxa.from_dict(alvo_data)
            elif alvo_data["papel"] == "Guarda-Costa":
                alvo_obj = GuardaCosta.from_dict(alvo_data)
            else:
                alvo_obj = Player.from_dict(alvo_data)

            # Executa a ação
            resultado = jogador_obj.realizar_acao(alvo_obj)

            # Atualiza os estados na sessão
            session['players_objetos'][jogador_atual] = jogador_obj.to_dict()
            session['players_objetos'][alvo_nome] = alvo_obj.to_dict()
            session['acoes'].append({'jogador': jogador_atual, 'acao': resultado})
            session['jogador_atual'] += 1
            session.modified = True

            return redirect(url_for('jogo.realizar_acao'))

    jogadores_vivos = [j for j in session['players_objetos'] if session['players_objetos'][j]["vivo"]]
    
    return render_template('realizar_acao.html', jogador=jogador_atual, papel=papel, jogadores_vivos=jogadores_vivos)


@jogo.route('/resumo_rodada')
def resumo_rodada():
    if 'acoes' not in session or 'players_objetos' not in session:
        return redirect(url_for('home'))

    mortes = 0
    vivos = 0
    acoes = session['acoes']
    jogadores_objetos = session['players_objetos']

    # Verifica quantos jogadores morreram
    for jogador in jogadores_objetos:
        if not jogadores_objetos[jogador]['vivo']:
            mortes += 1
        else:
            vivos += 1

    return render_template('resumo_rodadas.html', mortes=mortes, vivos=vivos, acoes=acoes)
