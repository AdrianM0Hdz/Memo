from app import create_app, db
from app.models import FieldOfStudy, Note

app = create_app('default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, FieldOfStudy=FieldOfStudy, Note=Note)