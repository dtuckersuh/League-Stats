# Routes module contains different URLs app implements
from flask import render_template, request, flash, redirect, url_for
from app import app
from .summoner import Summoner
from app.form import SearchForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
# Homepage view
def index():
    form = SearchForm()
    if form.validate_on_submit():
        name = form.username.data
        # TODO: Handle errors and sanitize
        return redirect(url_for('user', username=name))
    else:
        flash('All fields required')
    return render_template('index.html', title='Home', form=form)

@app.route('/user/')
@app.route('/user/<username>')
def user(username=None):
    if not username:
        return redirect(url_for('user', username=request.args['q']))
    user = Summoner(username)
    return render_template('user.html', title=username, user=user)


