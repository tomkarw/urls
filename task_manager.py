# #!/usr/bin/env python3

import datetime
import time

from app import app, db
from app.models import Url

app.app_context().push()


def manage_tasks():
    start_time = time.time()
    while True:
        for url in Url.query.all():
            utcnow = datetime.datetime.utcnow()
            print(url.next_runtime, '<=', utcnow)
            print(url.next_runtime <= utcnow)
            if url.next_runtime <= utcnow:
                app.task_queue.enqueue('app.tasks.handle_response_from_url', url)
                url.next_runtime += datetime.timedelta(seconds=url.interval)
                print(url, url.interval, url.next_runtime)
        db.session.commit()
        time.sleep(1.0 - ((time.time() - start_time) % 1.0))


if __name__ == '__main__':
    manage_tasks()
