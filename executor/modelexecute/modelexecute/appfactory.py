from typing import List, Type
from flask import Flask, Blueprint
import signal
import atexit
import sys

from modelexecute.appconf import Config, do_setup_hook, configure, do_teardown_hook
from modelexecute.db import close_db, close_session


def create_app(name: str, blueprints: List[Blueprint], conf_class: Type[Config], setup_hook=None, teardown_hook=None) -> Flask:
    app: Flask = Flask(name)

    configure(app, conf_class)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    app.teardown_appcontext(close_db)
    app.teardown_appcontext(close_session)

    if setup_hook is not None:
        do_setup_hook(app, setup_hook)

    if teardown_hook is not None:
        def signal_hook():
            sys.exit(0)

        def wrap_teardown_hook():
            do_teardown_hook(app, teardown_hook)

        signal.signal(signal.SIGTERM, signal_hook)
        atexit.register(wrap_teardown_hook)

    return app
