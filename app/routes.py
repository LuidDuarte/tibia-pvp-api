from flask import (
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request)
from app.serializer import CharacterSerializer, InjustedSerializer
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify_by_char/submit', methods=['POST'])
def verify_by_char():
    try:
        character_name = request.form['character_name'].strip()
        char = CharacterSerializer.from_api(character_name)
        injusted = InjustedSerializer.from_api(char)
        injusted.verify_skulls()
        session['injusted'] = InjustedSerializer.object_to_dict(injusted)
        return render_template('show_skulls.html', injusted=session['injusted'])
    except Exception as e:
        print(f'{e}')
        flash('Error!')
        return redirect(url_for('index'))


@app.route('/refresh')
def refresh():
    injusted = InjustedSerializer.dict_to_object(session['injusted'])
    injusted = InjustedSerializer.refresh_skull_from_api(injusted)
    injusted.verify_skulls()
    session['injusted'] = InjustedSerializer.object_to_dict(injusted)

    return render_template('show_skulls.html', injusted=session['injusted'])