#!/usr/bin/env python3

import datetime

from app import app, db
from app.models import Link


def manage_tasks():
    while True:
        for url in Link.query.all():
            if url.next_runtime <= datetime.datetime.utcnow():
                app.task_queue.enqueue('app.tasks.handle_response_from_url', url)
                url.next_runtime += datetime.timedelta(seconds=url.interval)
        db.session.commit()


if __name__ == '__main__':
    manage_tasks()
