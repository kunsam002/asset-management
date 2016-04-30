from factories import initialize_api, create_app
from flask_migrate import MigrateCommand
from flask_script import Manager
import os

app = create_app('monitor', 'config.Config')

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def runserver():

    with app.app_context():

        from asset import app, db, api

        initialize_api(app, api)

        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    manager.run()