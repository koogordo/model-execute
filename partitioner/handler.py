import os
import json
from typing import Dict
from flask import Flask
from sqlalchemy.orm import Session
from modelexecute.appfactory import create_app
from modelexecute.model import model_service
from modelexecute.models import Model
from modelexecute.aws import s3_client, split_s3_path
from partitioner.views import partitioner_blueprint
from partitioner.config import LocalPartitionerConfig, DevPartitionerConfig

env: str = os.getenv('ENVIRONMENT', None)

if env == 'local':
    conf_class = LocalPartitionerConfig
elif env == 'dev':
    conf_class = DevPartitionerConfig
else:
    conf_class = LocalPartitionerConfig


# def setup_hook(app: Flask, session: Session) -> None:
#     model_service.set_session(session)
#     model_service.register_from_metadata_path(app.config.get('MODEL_METADATA'))
#     model_service.load_model_meta(app.config.get('MODEL_NAME'))
#     session.close()


# def teardown_hook(app: Flask, session: Session) -> None:
#     print('EXECUTING TEARDOWN HOOK')
#     model_service.set_session(session)
#     model_service.load_model_meta(app.config.get('MODEL_NAME'))
#     model_service.unregister_model()
#     session.close()


handler: Flask = create_app(
    name=__name__,
    blueprints=[
        partitioner_blueprint
    ],
    conf_class=conf_class)
