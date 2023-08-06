import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        import toml
        app.config.from_file("config.toml", load=toml.load, silent=True)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.setup(app)

    from . import product
    app.register_blueprint(product.bp)

    from . import client
    app.register_blueprint(client.bp)

    from . import bill
    app.register_blueprint(bill.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import me
    app.register_blueprint(me.bp)

    from . import landing
    app.register_blueprint(landing.bp)
    app.add_url_rule('/', endpoint='home')

    from . import payment
    app.register_blueprint(payment.bp)

    app.jinja_env.add_extension('jinja2.ext.i18n')

    if 'HTTP_PROXY' in app.config and app.config['HTTP_PROXY']:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    from . import database
    app.register_blueprint(database.bp)

    return app
