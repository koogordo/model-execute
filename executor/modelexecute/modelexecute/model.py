from __future__ import annotations
from dataclasses import dataclass
from io import BytesIO
import logging
import json
import sys
from typing import Dict
import uuid
import cloudpickle
import pandas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from modelexecute.aws import s3_client, split_s3_path
from modelexecute.models import Model


log_format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    format=log_format,
                    level=logging.INFO)

logger = logging.getLogger()


class ModelServiceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class __ModelService:
    def __init__(self) -> None:
        self.s3_client = s3_client
        self.model_meta: Model = None
        self.model = None
        pass

    def set_session(self, session: Session) -> None:
        self.session = session

    def register_from_metadata_path(self, path: str) -> None:
        bucket, key = split_s3_path(path)

        model_meta: Dict = json.loads(s3_client.get_object(
            Bucket=bucket, Key=key)['Body'].read())

        self.__register_model(Model(
            name=model_meta['name'],
            artifacts=model_meta['artifacts'],
            file_name=model_meta['file_name'],
            predict_method=model_meta['predict_method'],
            status='ONLINE'
        ))

    def load_model_meta(self, model_name: str) -> None:
        self.model_meta = self.session.execute(self.session.query(
            Model).where(Model.name == model_name)).first()[0]
        self.model_meta.status = 'ONLINE'
        self.__commit(True)

    def register_from_metadata(self, model: Model) -> None:
        self.__register_model(model)

    def unregister_model(self, commit=True) -> None:
        self.__assert_session()

        # self.model_meta = self.session.execute(self.session.query(
        #     Model).where(Model.id == self.model_meta.id)).fetchone()[0]

        # self.session.query(Model).filter(
        #     Model.id == self.model_meta.id).update({'status': 'OFFLINE'})
        self.model_meta.status = 'OFFLINE'

        self.__commit(commit)

    def load_model(self) -> None:
        pkl_bucket, pkl_key = split_s3_path(
            self.model_meta.artifacts + self.model_meta.file_name)
        model_pkl: bytes = s3_client.get_object(
            Bucket=pkl_bucket, Key=pkl_key)['Body'].read()
        if self.model is None:
            logger.info(">>>>>>>>>>> Model is None. Deserializing model.")
            self.model = cloudpickle.load(model_pkl)

    def predict(self, raw_input: bytes) -> str:
        input: pandas.DataFrame = pandas.read_json(BytesIO(raw_input))
        raw_prediction = getattr(
            self.model, self.model_meta.predict_method)(None, input)
        for i, row in input.iterrows():
            input.at[i, 'output'] = raw_prediction[i]
        return input.to_json(lines=True, orient='records')

    def write_prediction(self, location: str, prediction: str) -> None:
        bucket, key = split_s3_path(location)
        self.s3_client.put_object(
            Bucket=bucket, Key=key, Body=prediction)

    def model_loaded(self) -> bool:
        return self.model is not None

    def __commit(self, do_commit: bool) -> None:
        if do_commit is True:
            self.session.commit()

    def __assert_session(self) -> None:
        if self.session is None:
            raise ModelServiceException(
                'Database session not set for the service. Operation could not be completed.')

    def __register_model(self, model: Model, commit=True) -> None:
        self.__assert_session()

        if self.model_meta is None:
            try:
                self.session.add(model)
                self.__commit(commit)
                self.model_meta = model
            except IntegrityError as e:
                if isinstance(e.__cause__, UniqueViolation) is True:
                    self.session.rollback()
                    pass
                else:
                    raise ModelServiceException(e)


model_service: __ModelService = __ModelService()
