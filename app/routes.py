# Routes module contains different URLs app implements
from flask import render_template
from app import app
from .summoner import Summoner

@app.route('/')
@app.route('/index')
def index():
    user = Summoner('suh hyungwon')
    champions = user.getTopFiveChamps()  # Dictionary
    match_history = user.getMatchHistory()
    return render_template('index.html', title='Home', user=user, champions=champions, match_history=match_history)



