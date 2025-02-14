
from flask import Flask
from routes.home import home
from routes.jogo import jogo
from routes.form import form

app = Flask(__name__)
app.secret_key = 'ABABIBABABABABABABABIBABABABA'

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(form, url_prefix='/form')
app.register_blueprint(jogo, url_prefix='/A_Condessa')