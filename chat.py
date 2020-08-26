from app import create_app, db
from app.models import User, Message, Friend, Dialog

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message, 'Friend': Friend, 'Dialog': Dialog}
