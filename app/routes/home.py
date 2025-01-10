from flask import Blueprint, render_template, redirect, url_for

home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    return render_template('index.html')

