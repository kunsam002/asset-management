from flask import current_app as app

with app.app_context():
    db = app.db
    api = app.api
    migrate = app.migrate
