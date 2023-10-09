import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/a')
    def hello():
        return 'holaaa!'

    from . import db
    
    from . import can
    app.register_blueprint(can.bp)
    
    from . import alb
    app.register_blueprint(alb.bp)

    from . import art
    app.register_blueprint(art.bp)
    
    @app.route("/")
    def principal():
        return render_template("base.html")

    return app