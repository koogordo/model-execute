import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask


class Config(object):
    def __init__(self) -> None:
        self.ENVIRONMENT = os.environ['ENVIRONMENT']
        self.MODEL_METADATA: str = f's3://model-execute/models/{os.environ["MODEL_NAME"]}/model.json'
        self.MODEL_NAME = os.environ["MODEL_NAME"]
        self.DB_USER = 'postgres'
        self.DB_PORT = 5432
        self.DB_NAME = 'modelexecute'


class LocalConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.DB_PASSWORD = os.environ['DB_PASSWORD']
        self.DB_HOST = 'localhost'
        self.AWS_HOST = 'localhost'
        self.DATABASE_URI: str = f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class DevConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.DB_PASSWORD = os.environ['DB_PASSWORD']
        self.DB_HOST = 'host.docker.internal'
        self.AWS_HOST = 'host.docker.internal'
        self.DATABASE_URI: str = f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


def configure(app: Flask, conf_class):
    app.config.from_object(conf_class())
    app.config['DB_ENGINE'] = create_engine(app.config.get('DATABASE_URI'))


def do_setup_hook(app: Flask, setup_hook):
    db_session: Session = Session(app.config['DB_ENGINE'])
    setup_hook(app, db_session)


def do_teardown_hook(app: Flask, teardown_hook):
    db_session: Session = Session(app.config['DB_ENGINE'])
    teardown_hook(app, db_session)
