import os
from flask import Flask
import json
from sqlalchemy.orm import Session

from modelexecute.appfactory import create_app
from modelexecute.model import model_service
from executor.views import executor_blueprint
from executor.config import LocalExecutorConfig, DevExecutorConfig


env: str = os.getenv('ENVIRONMENT', None)

if env == 'local':
    conf_class = LocalExecutorConfig
elif env == 'dev':
    conf_class = DevExecutorConfig
else:
    conf_class = LocalExecutorConfig


def setup_hook(app: Flask, session: Session) -> None:
    model_service.set_session(session)
    model_service.register_from_metadata_path(app.config.get('MODEL_METADATA'))
    model_service.load_model_meta(app.config.get('MODEL_NAME'))
    model_service.load_model()
    session.close()


handler: Flask = create_app(name=__name__,
                            blueprints=[executor_blueprint], conf_class=conf_class, setup_hook=setup_hook)
