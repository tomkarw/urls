from flask import jsonify, request

from app import app, db
from app.errors import bad_request, entity_too_large
from app.models import Link


@app.route('/api/fetcher', methods=['GET'])
def get_links():
    return jsonify([link.to_dict() for link in Link.query.all()])


@app.route('/api/fetcher', methods=['POST'])
def create_or_update_link():
    if len(request.get_data()) > app.config['PAYLOAD_MAX_SIZE']:
        return entity_too_large()
    data = request.get_json() or {}
    if 'url' not in data or 'interval' not in data:
        return bad_request()
    try:
        interval = int(data['interval'])
    except ValueError:
        return bad_request()
    if interval < app.config['MIN_INTERVAL']:
        return bad_request()
    link = Link.query.filter_by(url=data['url']).first()
    if link:
        link.interval = interval
    else:
        link = Link(url=data['url'], interval=interval)
        db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict(['id']))


@app.route('/api/fetcher/<int:id>', methods=['GET'])
def get_link(id):
    return jsonify(Link.query.get_or_404(id).to_dict())


@app.route('/api/fetcher/<int:id>', methods=['DELETE'])
def delete_link(id):
    link = Link.query.get_or_404(id)
    response = jsonify(link.to_dict(['id']))
    db.session.delete(link)
    db.session.commit()
    return response


@app.route('/api/fetcher/<int:id>/history', methods=['GET'])
def get_link_history(id):
    replies = Link.query.get_or_404(id).replies.all()
    return jsonify([reply.to_dict() for reply in replies])
