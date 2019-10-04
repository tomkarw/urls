import requests
from requests import ConnectTimeout, ReadTimeout

from app import app, db
from app.models import Response, Url

app.app_context().push()

TIMEOUT = app.config['TIMEOUT']


def handle_response_from_url(url: Url) -> None:
    try:
        print(url.id, url.url)
        resp = requests.get(url.url, timeout=TIMEOUT)
        r = Response(response=resp.text,
                     duration=resp.elapsed.total_seconds(),
                     url_id=url.id)
    except (ConnectTimeout, ReadTimeout):
        r = Response(response=None,
                     duration=TIMEOUT,
                     url_id=url.id)
    db.session.add(r)
    db.session.commit()
