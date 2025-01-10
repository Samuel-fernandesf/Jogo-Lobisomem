from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Olá'