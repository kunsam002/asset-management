from factories import initialize_api, create_app
from flask_migrate import MigrateCommand
import os

app = create_app('smart', 'config.Config')
manager = app.manager


@manager.command
def runserver():

    from asset.views.admin import main

    with app.app_context():

        initialize_api(app, app.api)

        app.register_blueprint(main)

        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    manager.run()