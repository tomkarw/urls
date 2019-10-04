from flask import jsonify, request

from app import app, db
from app.errors import bad_request, entity_too_large
from app.models import Url


@app.route('/api/fetcher', methods=['GET'])
def get_urls():
    return jsonify([url.to_dict() for url in Url.query.all()])


@app.route('/api/fetcher', methods=['POST'])
def create_or_update_url():
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
    url = Url.query.filter_by(url=data['url']).first()
    if url:
        url.interval = interval
        #change scheduler interval
        #scheduler.cancel(url.job_id)
        #scheduler.schedule(scheduled_time=datetime.utcnow(), func=tasks_factory, interval=1)
    else:
        url = Url(url=data['url'], interval=interval)
        db.session.add(url)
        #create scheduler
        #scheduler.schedule(scheduled_time=datetime.utcnow(), func=tasks_factory, interval=1)
    db.session.commit()
    return jsonify(url.to_dict(['id']))


@app.route('/api/fetcher/<int:id>', methods=['GET'])
def get_url(id):
    return jsonify(Url.query.get_or_404(id).to_dict())


@app.route('/api/fetcher/<int:id>', methods=['DELETE'])
def delete_url(id):
    url = Url.query.get_or_404(id)
    response = jsonify(url.to_dict(['id']))
    # delete scheduler
    # scheduler.cancel(job)
    db.session.delete(url)
    db.session.commit()
    return response


@app.route('/api/fetcher/<int:id>/history', methods=['GET'])
def get_url_history(id):
    responses = Url.query.get_or_404(id).responses.all()
    return jsonify([response.to_dict() for response in responses])
