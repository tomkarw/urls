from app import app, db
from app.models import Link, Reply


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Link': Link, 'Reply': Reply}


if __name__ == '__main__':
    app.run(port=8080)
