from flask import Flask, render_template, flash, redirect, url_for, request
from routes.home import home

app = Flask(__name__)

#Liga os arquivos de routes ao programa principal, colocando um prefixo na url
app.register_blueprint(home, url_prefix='/')

