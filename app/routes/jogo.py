from flask import Blueprint, render_template, redirect, url_for, request


jogo = Blueprint('jogo', __name__)

@jogo.route('/')
def jogo_01():
    return render_template('jogo_01.html')