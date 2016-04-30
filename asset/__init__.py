from flask import current_app as app

with app.app_context():
    db = app.db
    api = app.api
    migrate = app.migrate
    logger = app.logger
    bcrypt = app.bcrypt


def register_api(cls, *urls, **kwargs):
    """ A simple pass through class to add entities to the api registry """
    kwargs["endpoint"] = getattr(cls, 'resource_name', kwargs.get("endpoint", None))
    app.api_registry.append((cls, urls, kwargs))