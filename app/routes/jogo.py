from flask import Blueprint, render_template, redirect, url_for, session, request
import random

jogo = Blueprint('jogo', __name__)

@jogo.route('/iniciar', methods=['POST', 'GET'])
def iniciar_jogo():

    if 'jogadores' in session and 6 <= len(session['jogadores']) <= 10:
        num_jogadores = len(session['jogadores'])
        papeis = ['Condessa']
        papeis.append('Vampiro')
        papeis += ['Açougueiro', 'Caçador']
        papeis += ['Campones'] * (num_jogadores - len(papeis)) # Ele preenche o que sobrou dos jogadores com Camponeses.
        random.shuffle(papeis)
        session['papeis_jogadores'] = {
            jogador: {'papel': papeis[i], 'vivo': True, 'marcado_para_morrer': False}
            for i, jogador in enumerate(session['jogadores'])
        } # compreensao de dicionario, ele associa um papel da lista embaralhada para cada jogador da session.
        
        # Criar uma lista de Vampiros e Condessa
        session['vampiros'] = [
            jogador for jogador, info in session['papeis_jogadores'].items()
            if info['papel'] in ['Vampiro', 'Condessa']
        ]
        session.modified = True
        
        return redirect(url_for('jogo.mostrar_papel', indice=0))
    return redirect(url_for('form.jogo_form'))

@jogo.route('/mostrar_papel/<int:indice>', methods=['GET', 'POST'])
def mostrar_papel(indice):
    jogadores = session.get('jogadores', [])
    papeis = session.get('papeis_jogadores', {})
    vampiros = session.get('vampiros', [])
    
    if indice >= len(jogadores):
        return redirect(url_for('jogo.iniciar_acoes'))  # Após o último jogador, inicia ações
    
    jogador_atual = jogadores[indice]
    papel = papeis[jogador_atual]['papel']
    aliados = None
    
    if papel in ['Vampiro', 'Condessa']:
        aliados = [j for j in vampiros if j != jogador_atual]  # Exclui ele mesmo
        
    if request.method == 'POST':
        return redirect(url_for('jogo.mostrar_papel', indice=indice + 1))
    
    return render_template(
        'mostrar_papel.html',
        jogador=jogador_atual,
        papel=papel,
        aliados=aliados
    )
    
@jogo.route('/iniciar_acoes', methods=['GET', 'POST'])
def iniciar_acoes():
    for jogador in session['jogadores']:
        if session['papeis_jogadores'][jogador]['papel'] == 'Açougueiro':
            session.pop(f'{jogador}_inspecionou', None) # limpa a chave de inspeção.
            
    if 'papeis_jogadores' in session:
        vivos_com_acao = [
            jogador for jogador, info in session['papeis_jogadores'].items()
            if info['vivo'] and info['papel'] in ['Condessa', 'Vampiro', 'Açougueiro', 'Caçador', 'Campones']
        ]
        session['fila_acoes'] = vivos_com_acao
        session['fase_acao'] = True
        session['jogador_atual'] = 0  # Reinicia o jogador atual para a nova fase de ações
        session.modified = True
        return redirect(url_for('jogo.realizar_acao'))
    return redirect(url_for('form.jogo_form'))

@jogo.route('/realizar_acao', methods=['GET', 'POST'])
def realizar_acao():
    session['acoes'] = []
    if 'fila_acoes' not in session:
        return redirect(url_for('form.jogo_form'))
    
    if 'jogador_atual' not in session:
        session['jogador_atual'] = 0

    fila_acoes = session['fila_acoes']
    jogador_atual_idx = session['jogador_atual']

    # Enquanto o jogador na posição atual não estiver vivo, incremente o índice
    while jogador_atual_idx < len(fila_acoes) and not session['papeis_jogadores'][fila_acoes[jogador_atual_idx]]['vivo']:
        jogador_atual_idx += 1
        session['jogador_atual'] = jogador_atual_idx
        session.modified = True

    # Se não houver mais jogadores vivos na fila de ação, finaliza a fase
    if jogador_atual_idx >= len(fila_acoes):
        print(f'{fila_acoes}, {fila_acoes}')
        return redirect(url_for('jogo.finalizar_fase'))
    
    # Agora, garantimos que o jogador atual esteja vivo
    jogador_atual = fila_acoes[jogador_atual_idx]
    papel_atual = session['papeis_jogadores'][jogador_atual]['papel']
    jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]
    mensagem_inspecao = session.pop('mensagem_inspecao', None)  # garante que a mensagem de inspeção apareça apenas uma vez.

    # Resto da lógica...
    if papel_atual == 'Campones' and request.method == 'POST':
        if 'pular' in request.form:
            session['jogador_atual'] += 1  # pula a vez do camponês
            session.modified = True
            return redirect(url_for('jogo.realizar_acao'))
        
    if request.method == 'POST':
        acao = request.form.get('acao')
        alvo = request.form.get('alvo')
        
        if acao == 'matar' and alvo in jogadores_vivos:
            session['papeis_jogadores'][alvo]['marcado_para_morrer'] = True
            session['papeis_jogadores'][jogador_atual].setdefault('matou', True)
            
        elif acao == 'inspecionar' and alvo and papel_atual == 'Açougueiro':
            if session.get(f'{jogador_atual}_inspecionou', False):
                mensagem_inspecao = "Você já fez uma inspeção nesta rodada."
            else:
                alvo_info = session['papeis_jogadores'][alvo]
                if alvo_info['papel'] in ['Vampiro', 'Condessa', 'Caçador'] and alvo_info.get('matou', False):
                    mensagem_inspecao = f"{alvo} cheira a sangue!"
                else:
                    mensagem_inspecao = f"{alvo} não cheira a sangue."
                session[f'{jogador_atual}_inspecionou'] = True
                session.modified = True
                
            return render_template(
                'realizar_acao.html',
                jogador_atual=jogador_atual,
                papel_atual=papel_atual,
                jogadores_vivos=jogadores_vivos,
                mensagem_inspecao=mensagem_inspecao,
            )

        session['jogador_atual'] += 1
        session.modified = True
        
        return redirect(url_for('jogo.realizar_acao'))
    
    return render_template(
        'realizar_acao.html',
        jogador_atual=jogador_atual,
        papel_atual=papel_atual,
        jogadores_vivos=jogadores_vivos,
        mensagem_inspecao=mensagem_inspecao,
    )

@jogo.route('/finalizar_fase')
def finalizar_fase():
    jogadores = session.get('jogadores', [])
    papeis = session.get('papeis_jogadores', {})
    mortos = []
    
    # Atualiza os jogadores marcados para morrer
    for jogador, info in papeis.items():
        if info.get('marcado_para_morrer'):
            info['vivo'] = False
            mortos.append(jogador)
            info['marcado_para_morrer'] = False
    
    vivos = [j for j, info in papeis.items() if info['vivo']]

    # Limpa a chave de inspeção para o Açougueiro
    for jogador in vivos:
        if papeis[jogador]['papel'] == 'Açougueiro':
            session.pop(f'{jogador}_inspecionou', None)

    # Define que a fase de ação acabou
    session['fase_acao'] = False
    
    monstros = sum(1 for jogador in vivos if papeis[jogador]['papel'] in ['Vampiro', 'Condessa'])

    
    if monstros == 0:
        return redirect(url_for('jogo.fim_jogo', vitoria='aldeoes'))
    else:
        session['jogador_votando'] = 0
        session['votos'] = {jogador: 0 for jogador in vivos}
        session.modified = True

        return redirect(url_for('jogo.votacao'))

@jogo.route('/fim_jogo/<vitoria>')
def fim_jogo(vitoria):
    session.clear()
    return render_template('fim_jogo.html', vitoria=vitoria)

@jogo.route('/votacao', methods=['GET', 'POST'])
def votacao():
    if 'jogador_votando' not in session:
        session['jogador_votando'] = 0
        session['votos'] = {jogador: 0 for jogador in session['jogadores'] if session['papeis_jogadores'][jogador]['vivo']}
    
    # Garantindo que 'votos_pular' esteja na sessão
    if 'votos_pular' not in session:
        session['votos_pular'] = 0  

    jogador_votando_idx = session['jogador_votando']
    jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]
    jogadores_mortos = [j for j in session['jogadores'] if not session['papeis_jogadores'][j]['vivo']]

    # verifica se todos os jogadores vivos já votaram.
    if jogador_votando_idx >= len(jogadores_vivos):
        vivos_votantes = {jogador: votos for jogador, votos in session['votos'].items() if session['papeis_jogadores'][jogador]['vivo']}

        if not vivos_votantes:
            return redirect(url_for('jogo.fim_jogo', vitoria='empate'))

        # se sobrar ao menos 2 jogadores, o jogo verifica quem ganhou.
        if len(vivos_votantes) <= 3:
            jogadores_restantes = list(vivos_votantes.keys())
            papeis_restantes = [session['papeis_jogadores'][jogador]['papel'] for jogador in jogadores_restantes]

            if all(papel in ['Campones', 'Açougueiro', 'Caçador'] for papel in papeis_restantes):
                return redirect(url_for('jogo.fim_jogo', vitoria='aldeoes'))

            if any(papel in ['Vampiro', 'Condessa'] for papel in papeis_restantes):
                return redirect(url_for('jogo.fim_jogo', vitoria='monstros'))

        # verifica quem recebeu o maior número de votos.
        max_votos = max(vivos_votantes.values(), default=0)

        # Se a opção "pular" teve mais votos que qualquer jogador, ninguém é eliminado
        if session['votos_pular'] >= max_votos:
            return render_template(
                'resultado_votacao.html',
                eliminado="Ninguém",
                mensagem="A maioria escolheu não eliminar ninguém nesta rodada.",
                vivos=jogadores_vivos,
                mortos=jogadores_mortos
            )

        jogadores_com_max_votos = [j for j, v in vivos_votantes.items() if v == max_votos]

        if len(jogadores_com_max_votos) > 1:
            return render_template(
                'resultado_votacao.html',
                mensagem="A votação empatou! Ninguém foi eliminado.",
                vivos=jogadores_vivos,
            )

        eliminado = jogadores_com_max_votos[0]
        session['papeis_jogadores'][eliminado]['vivo'] = False
        session.modified = True
        jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]

        return render_template(
            'resultado_votacao.html',
            eliminado=eliminado,
            papel=session['papeis_jogadores'][eliminado]['papel'],
            vivos=jogadores_vivos,
            mortos=jogadores_mortos
        )

    jogador_atual = jogadores_vivos[jogador_votando_idx]

    if request.method == 'POST':
        voto = request.form.get('voto')
        if voto == 'pular':
            session['votos_pular'] += 1  # Adiciona um voto nulo
        elif voto:
            session['votos'][voto] += 1  # Adiciona um voto a um jogador

        session['jogador_votando'] += 1
        session.modified = True
        return redirect(url_for('jogo.votacao'))

    return render_template(
        'votacao.html', jogador_atual=jogador_atual, vivos=jogadores_vivos, mortos=jogadores_mortos
    )
