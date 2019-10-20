#!/usr/bin/env python3

from app import db
from app.models import Reply

for response in Reply.query.all():
    db.session.delete(response)
db.session.commit()
