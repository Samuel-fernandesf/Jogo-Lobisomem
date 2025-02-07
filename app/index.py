from app import app
from flask import Flask, session

#tinha um session clear aqui, mas como tava dando erro eu movi ele pro fim do jogo

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)