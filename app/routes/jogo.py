from flask import Blueprint, render_template, redirect, url_for, session, request
import random

jogo = Blueprint('jogo', __name__)

@jogo.route('/iniciar', methods=['POST', 'GET'])
def iniciar_jogo():
    if 'jogadores' in session and 4 <= len(session['jogadores']) <= 8:
        num_jogadores = len(session['jogadores'])
        papeis = ['Condessa']

        papeis += ['Açougueiro', 'Caçador']
        papeis += ['Campones'] * (num_jogadores - len(papeis))
        random.shuffle(papeis)

        session['papeis_jogadores'] = {
            jogador: {'papel': papeis[i], 'vivo': True, 'marcado_para_morrer': False}
            for i, jogador in enumerate(session['jogadores'])
        }
        session.modified = True
        return redirect(url_for('jogo.mostrar_papel', indice=0))
    return redirect(url_for('form.jogo_form'))


@jogo.route('/mostrar_papel/<int:indice>', methods=['GET', 'POST'])
def mostrar_papel(indice):
    jogadores = session.get('jogadores', [])
    papeis = session.get('papeis_jogadores', {})

    if indice >= len(jogadores):
        return redirect(url_for('jogo.iniciar_acoes'))

    jogador_atual = jogadores[indice]
    papel = papeis[jogador_atual]['papel']

    if request.method == 'POST':
        return redirect(url_for('jogo.mostrar_papel', indice=indice + 1))

    return render_template('mostrar_papel.html', jogador=jogador_atual, papel=papel)

@jogo.route('/iniciar_acoes', methods=['GET', 'POST'])
def iniciar_acoes():
    if 'papeis_jogadores' in session:
        vivos_com_acao = [
            jogador for jogador, info in session['papeis_jogadores'].items()
            if info['vivo'] and info['papel'] in ['Condessa', 'Vampiro', 'Açougueiro', 'Caçador']
        ]
        session['fila_acoes'] = vivos_com_acao
        session['acoes'] = []
        session.modified = True
        return redirect(url_for('jogo.realizar_acao'))
    return redirect(url_for('form.jogo_form'))

@jogo.route('/realizar_acao', methods=['GET', 'POST'])
def realizar_acao():
    if 'fila_acoes' not in session:
        return redirect(url_for('form.jogo_form'))

    if 'jogador_atual' not in session:
        session['jogador_atual'] = 0

    fila_acoes = session['fila_acoes']
    jogador_atual_idx = session['jogador_atual']

    if jogador_atual_idx >= len(fila_acoes):
        return redirect(url_for('jogo.finalizar_fase'))

    jogador_atual = fila_acoes[jogador_atual_idx]
    papel_atual = session['papeis_jogadores'][jogador_atual]['papel']
    jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]

    if papel_atual == 'Campones' and request.method == 'POST':
        if 'pular' in request.form:
            session['jogador_atual'] += 1
            session.modified = True
            return redirect(url_for('jogo.realizar_acao'))

    if request.method == 'POST':
        acao = request.form.get('acao')
        alvo = request.form.get('alvo')

        if acao == 'matar' and alvo in jogadores_vivos:
            session['papeis_jogadores'][alvo]['marcado_para_morrer'] = True
            session['papeis_jogadores'][jogador_atual].setdefault('matou', True)


        session['jogador_atual'] += 1
        session.modified = True
        return redirect(url_for('jogo.realizar_acao'))


    return render_template(
        'realizar_acao.html',
        jogador_atual=jogador_atual,
        papel_atual=papel_atual,
        jogadores_vivos=jogadores_vivos,
    )


@jogo.route('/finalizar_fase')
def finalizar_fase():
    papeis = session.get('papeis_jogadores', {})
    mortos = []

    for jogador, info in papeis.items():
        if info['marcado_para_morrer']:
            info['vivo'] = False
            mortos.append(jogador)
            info['marcado_para_morrer'] = False 
    vivos = [jogador for jogador, info in papeis.items() if info['vivo']]

    # Verificar condição de vitória
    matadores = sum(1 for jogador in vivos if papeis[jogador]['papel'] in ['Vampiro', 'Condessa'])
    camponeses = sum(1 for jogador in vivos if papeis[jogador]['papel'] == 'Campones')

    if len(vivos) == 1:
        if camponeses == 1:
            return redirect(url_for('jogo.fim_jogo', vitoria='camponeses'))
        else:
            return redirect(url_for('jogo.fim_jogo', vitoria='matadores'))

    if len(vivos) <= 4 and matadores >= 2:
        return redirect(url_for('jogo.fim_jogo', vitoria='matadores'))

    if session.get('fase_acao', True):
        session['fase_acao'] = False
        session['jogador_votando'] = 0
        session['votos'] = {jogador: 0 for jogador in vivos}
        session.modified = True
        return redirect(url_for('jogo.votacao'))
    else:
        session['fase_acao'] = True
        session['fila_acoes'] = vivos
        session['jogador_atual'] = 0  # Reinicia o índice do jogador atual
        session.modified = True
        return redirect(url_for('jogo.realizar_acao'))


@jogo.route('/fim_jogo/<vitoria>')
def fim_jogo(vitoria):
    session.pop('papeis_jogadores', None)
    session.pop('fila_acoes', None)
    session.pop('jogador_atual', None)
    session.pop('jogador_votando', None)
    session.pop('votos', None)
    return render_template('fim_jogo.html', vitoria=vitoria)

@jogo.route('/votacao', methods=['GET', 'POST'])
def votacao():
    if 'jogador_votando' not in session:
        session['jogador_votando'] = 0
        session['votos'] = {jogador: 0 for jogador in session['jogadores'] if session['papeis_jogadores'][jogador]['vivo']}

    jogador_votando_idx = session['jogador_votando']
    jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]

    if jogador_votando_idx >= len(jogadores_vivos):
        # Verifica jogadores vivos após a votação
        vivos_votantes = {jogador: votos for jogador, votos in session['votos'].items() if session['papeis_jogadores'][jogador]['vivo']}
        
        if not vivos_votantes:
            # Nenhum jogador vivo ou sem votos
            return redirect(url_for('jogo.fim_jogo', vitoria='empate'))

        if len(vivos_votantes) == 2 or len(vivos_votantes) < 2:
            # Verificar os papéis dos dois jogadores restantes
            jogadores_restantes = list(vivos_votantes.keys())
            papeis_restantes = [session['papeis_jogadores'][jogador]['papel'] for jogador in jogadores_restantes]

            # Se ambos forem camponeses
            if all(papel == 'Campones' for papel in papeis_restantes):
                return redirect(url_for('jogo.fim_jogo', vitoria='camponeses'))

            # Se pelo menos um for um matador (Vampiro ou Condessa)
            if any(papel in ['Vampiro', 'Condessa'] for papel in papeis_restantes):
                return redirect(url_for('jogo.fim_jogo', vitoria='matadores'))

        # Obter o máximo de votos e os jogadores com esse número de votos
        max_votos = max(vivos_votantes.values())
        jogadores_com_max_votos = [j for j, v in vivos_votantes.items() if v == max_votos]

        if len(jogadores_com_max_votos) > 1:
            # Empate na votação
            return render_template(
                'resultado_votacao.html',
                eliminado="Ninguem",
                mensagem="A votação empatou! Ninguém foi eliminado.",
                vivos=jogadores_vivos,
            )

        # Eliminar o jogador com mais votos
        eliminado = jogadores_com_max_votos[0]
        session['papeis_jogadores'][eliminado]['vivo'] = False
        session.modified = True

        # Atualiza a lista de jogadores vivos
        jogadores_vivos = [j for j in session['jogadores'] if session['papeis_jogadores'][j]['vivo']]

        return render_template(
            'resultado_votacao.html',
            eliminado=eliminado,
            papel=session['papeis_jogadores'][eliminado]['papel'],
            vivos=jogadores_vivos,
        )

    jogador_atual = jogadores_vivos[jogador_votando_idx]

    if request.method == 'POST':
        voto = request.form.get('voto')
        if voto:
            session['votos'][voto] += 1
            session['jogador_votando'] += 1
            session.modified = True
            return redirect(url_for('jogo.votacao'))

    return render_template('votacao.html', jogador_atual=jogador_atual, vivos=jogadores_vivos)

