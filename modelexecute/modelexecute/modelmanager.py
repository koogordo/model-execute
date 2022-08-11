from __future__ import annotations
from ast import parse
from copyreg import pickle
from dataclasses import dataclass
from io import BytesIO
import logging
import sys
import cloudpickle
import pandas
from urllib.parse import urlparse
from modelexecute.awssession import AwsSession


log_format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    format=log_format,
                    level=logging.INFO)

logger = logging.getLogger()


@dataclass
class ModelDef:
    pkl_path: str = ''
    predict_method: str = ''
    output_location: str = ''


class Model:
    def __init__(self, model_def: ModelDef) -> None:
        self.model_def: ModelDef = model_def
        self.s3_client = AwsSession().get_client('s3')
        self.model = None
        self.prediction: pandas.DataFrame = None
        pass

    def load_model(self) -> Model:
        if self.model is None:
            logger.info(">>>>>>>>>>> Model is None. Deserializing model.")
            with open(self.model_def.pkl_path, 'rb') as pkl_f:
                self.model = cloudpickle.load(pkl_f)
        return self

    def predict(self, input: pandas.DataFrame) -> Model:
        # sys.stdout.write(help(self.model))
        # sys.stdout.flush()
        raw_prediction = self.model.predict(None, input)
        # sys.stdout.write('>>>>>>>>>>>>>>>> prediction: ' +
        #                  str(self.prediction))
        # sys.stdout.flush()
        for i, row in input.iterrows():
            input.at[i, 'output'] = raw_prediction[i]
        self.prediction = input.to_json(lines=True, orient='records')
        return self

    def write_prediction(self) -> None:
        parsed_url = urlparse(self.model_def.output_location)
        self.s3_client.put_object(
            Bucket=parsed_url.netloc, Key=parsed_url.path.lstrip('/'), Body=self.prediction)
