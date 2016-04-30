from factories import create_app, initialize_api
import os

app = create_app('monitor', 'config.Config')

with app.app_context():
    from asset import api
    from asset.resources.resource import *
    from asset.views.home import main

    app.register_blueprint(main)
    initialize_api(app,api)

    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)