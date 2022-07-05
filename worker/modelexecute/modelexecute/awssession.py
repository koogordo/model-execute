import os
from dataclasses import dataclass
from typing import Any, Optional
import boto3

class AwsSession():
    def __init__(self) -> None:
        self.session: boto3.Session = boto3.Session(
            aws_access_key_id='using_localstack',
            aws_secret_access_key='using_localstack',
            aws_session_token='using_localstack'
        )
        
    def get_client(self, name: str):
        return self.session.client(name, endpoint_url=f"http://{os.environ['LOCALHOST']}:4566")