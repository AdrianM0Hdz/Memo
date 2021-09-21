from flask import render_template, redirect, url_for, request
from . import main
from .. import db
from ..models import FieldOfStudy, Note

@main.route('/', methods=['GET', 'POST'])
def index():
    fields = FieldOfStudy.query.all()
    return render_template('index.html', fields=fields)

@main.route('/add_field_of_study', methods=['POST'])
def add_field_of_study():
    def _create_url_alias(name):
        name = name.lower()
        name = name.replace(' ', '_')
        return name

    name = request.form.get('name_of_field')
    
    if name == '':
        return redirect(url_for('main.index'))
    
    url_alias = _create_url_alias(name) 
    field = FieldOfStudy(name=name, url_alias=url_alias, currently_reviewing=True, empty=True)
    try:
        db.session.add(field)
        db.session.commit()
    except BaseException as e: 
        print(f'This Error Ocurred{e}')
    return redirect(url_for('main.index'))

@main.route('/delete_field_of_study', methods=['POST'])
def delete_field_of_study():
    name = request.form.get('name_of_field')
    try:
        field = FieldOfStudy.query.filter_by(name=name).first()
        if field.empty == True:
            db.session.delete(field)
            db.session.commit()
    except BaseException as e:
        pass
    return redirect(url_for('main.index'))

@main.route('/field_of_study/<string:url_alias>')
def field_of_study(url_alias):
    field = FieldOfStudy.query.filter_by(url_alias=url_alias).first()
    return render_template('field.html', field=field)

@main.route('/field_of_study/<string:url_alias>/add_note', methods=['GET', 'POST'])
def add_note(url_alias):
    field = FieldOfStudy.query.filter_by(url_alias=url_alias).first()
    if request.method == 'POST':
        what = request.form.get('what')
        definition = request.form.get('definition')
        try: 
            note = Note(what=what, definition=definition, field_id=field.id)
            field.notes.append(note)
            field.empty = False
            db.session.commit()
        except BaseException as e:
            pass
    return render_template('add_note.html', field=field)

@main.route('/field_of_study/<string:url_alias>/update_note/<int:note_id>', methods=['GET', 'POST'])
def update_note(url_alias, note_id):
    field  = FieldOfStudy.query.filter_by(url_alias=url_alias).first()
    note = Note.query.filter_by(field_id=field.id).first()
    if request.method == 'POST':
        what = request.form.get('what')
        definition = request.form.get('new')
        try:
            note.what = what
            note.definition = definition
            db.session.commit()
        except BaseException as e:
            pass
    return render_template('update_note.html', field=field, note=note)

@main.route('/daily_review', methods=['GET', 'POST'])
def daily_review():
    fields = FieldOfStudy.query.filter_by(currently_reviewing=True)
    notes = []
    for field in fields:
        notes += field.notes
    notes.sort(key= lambda note: note.strength)

    return render_template('daily_review.html', notes=notes)