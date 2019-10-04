#!/usr/bin/env python3

from app import db
from app.models import Response

for response in Response.query.all():
    db.session.delete(response)
db.session.commit()
