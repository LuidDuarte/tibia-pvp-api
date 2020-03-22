import os
from flask import Flask
from flask import (
    render_template,
    redirect,
    url_for,
    session,
    abort,
    flash,
    request,
    current_app,
    make_response)
from models import verify_by_name, verify_by_text, Last_Death
app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')
app.secret_key = 'asdasdasd2318317932ujih'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify_by_char/submit', methods=['POST'])
def verify_by_char():
    try:
        session['last_death'] = verify_by_name(request.form['character_name']).__dict__
        return render_template('show_skulls.html', last_death=session['last_death'])
    except:
        flash('Error!')
        return redirect(url_for('index'))

@app.route('/verify_by_death_text/submit', methods=['POST'])
def verify_by_death_text():
    # try:
    session['last_death'] = verify_by_text(request.form['death_text']).__dict__
    return render_template('show_skulls.html', last_death=session['last_death'])
    # except:
    #     flash('Error!')
    #     return redirect(url_for('index'))

@app.route('/refresh')
def refresh():
    last_death = Last_Death(dictionary=session['last_death'])
    last_death.refresh
    session['last_death'] = last_death.__dict__
    return render_template('show_skulls.html', last_death=session['last_death'])