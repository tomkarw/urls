from app import app


@app.errorhandler(400)
def bad_request(error=None):
    return "Bad Request", 400


@app.errorhandler(404)
def not_found(error=None):
    return "Not Found", 404


@app.errorhandler(413)
def entity_too_large(error=None):
    return "Entity Too Large", 413
