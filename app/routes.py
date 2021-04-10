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
from app.controllers import Character
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify_by_char/submit', methods=['POST'])
def verify_by_char():
    try:
        session['character'] = request.form['character_name']
        char = Character(session['character'], view_involveds=True)
        return render_template('show_skulls.html', character=char.__dict__)
    except:
        flash('Error!')
        return redirect(url_for('index'))


@app.route('/refresh')
def refresh():
    char = Character(session['character'], view_involveds=True)
    return render_template('show_skulls.html', character=char.__dict__)