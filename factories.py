from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.restful import Api
from flask_bcrypt import Bcrypt


def create_app(app_name, config_obj):
    app = Flask(app_name)
    app.config.from_object(config_obj)
    app.db = SQLAlchemy(app)

    app.api = Api(app, prefix='/api/v1')
    app.api_registry = []
    app.migrate = Migrate(app, app.db)
    app.bcrypt = Bcrypt(app)

    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler("/var/log/monitor/%s.log" % app.config.get("LOGFILE_NAME", app_name), maxBytes=500*1024)
        file_handler.setLevel(logging.ERROR)
        from logging import Formatter
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)

    return app


def initialize_api(app, api):
    """ Register all resources for the API """
    api.init_app(app=app)  # Initialize api first
    _resources = getattr(app, "api_registry", None)
    if _resources and isinstance(_resources, (list, tuple,)):
        for cls, args, kwargs in _resources:
            api.add_resource(cls, *args, **kwargs)
