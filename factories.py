from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext import restful
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.db = SQLAlchemy(app)
app.migrate = Migrate(app, db)

app.api = restful.Api(app, prefix='/api/v1')
app.api_registry = []

def initialize_api(app, api):
	""" Register all resources for the API """
	api.init_app(app=app) # Initialize api first
	_resources = getattr(app, "api_registry", None)
	if _resources and isinstance(_resources, (list, tuple,)):
		for cls, args, kwargs in _resources:
			api.add_resource(cls, *args, **kwargs)