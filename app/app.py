from flask import Flask, render_template, flash, redirect, url_for, request
from routes.home import home
from routes.jogo import jogo

app = Flask(__name__)

#Liga os arquivos de routes ao programa principal, colocando um prefixo na url
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(jogo, url_prefix='/A_Condessa')


