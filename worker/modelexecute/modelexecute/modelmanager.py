from __future__ import annotations
from ast import parse
from copyreg import pickle
from dataclasses import dataclass
import logging
import sys
import cloudpickle
import pandas
from urllib.parse import urlparse
from modelexecute.awssession import AwsSession


log_format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream = sys.stdout, 
                    format = log_format, 
                    level = logging.INFO)

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
        pass
    
    def load_model(self) -> Model:
        if self.model is None:
            logger.info(">>>>>>>>>>> Model is None. Deserializing model.")
            with open(self.model_def.pkl_path, 'rb') as pkl_f:
                self.model = cloudpickle.load(pkl_f)
        return self
    
    def predict(self, input: pandas.DataFrame) -> Model:
        sys.stdout.write(help(self.model))
        sys.stdout.flush()
        self.prediction = self.model.predict(input)
        sys.stdout.write('>>>>>>>>>>>>>>>> prediction: ' + str(self.prediction))
        sys.stdout.flush()
        return self
    
    def write_prediction(self) -> None:
        parsed_url = urlparse(self.model_def.output_location)
        self.s3_client.put_object(Bucket=parsed_url.netloc, Key=parsed_url.path.lstrip('/'), Body=self.prediction)