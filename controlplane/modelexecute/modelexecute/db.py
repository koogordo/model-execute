from flask import current_app, g
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import Session


class DBMetaCtx():
    def __init__(self) -> None:
        self.engine = current_app.config.get('DB_ENGINE')
        self.metadata_obj = MetaData()
        self.metadata_obj.reflect(bind=self.engine)

    def get_table(self, name: str) -> Table:
        return self.metadata_obj.tables[name]


def get_db() -> Connection:
    if 'db' not in g:
        g.db = current_app.config.get('DB_ENGINE').connect()
    return g.db


def get_session() -> Session:
    if 'db_session' not in g:
        g.db_session = Session(current_app.config.get('DB_ENGINE'))
    return g.db_session


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def close_session(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.commit()
        db_session.close()


