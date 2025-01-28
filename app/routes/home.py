from flask import Blueprint, render_template, session

home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    return render_template('index.html')

@home.route('/biblioteca', methods=['GET', 'POST'])
def biblioteca():
    return render_template('biblioteca.html', jogadores=session.get('jogadores', []))

@home.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@home.route('/historia')
def historia():
    return render_template('historia.html')

@home.route('/creditos')
def creditos():
    return render_template('creditos.html')