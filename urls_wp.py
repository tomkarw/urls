from app import app, db
from app.models import Url, Response


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Url': Url, 'Response': Response}


if __name__ == '__main__':
    app.run(port=8080)
