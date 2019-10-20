import requests
from requests import ConnectTimeout, ReadTimeout

from app import app, db
from app.models import Reply, Link

app.app_context().push()

TIMEOUT = app.config['TIMEOUT']


def handle_response_from_url(url: Link) -> None:
    try:
        resp = requests.get(url.url, timeout=TIMEOUT)
        r = Reply(response=resp.text,
                  duration=resp.elapsed.total_seconds(),
                  link_id=url.id)
    except (ConnectTimeout, ReadTimeout):
        r = Reply(response=None,
                  duration=TIMEOUT,
                  link_id=url.id)
    db.session.add(r)
    db.session.commit()
