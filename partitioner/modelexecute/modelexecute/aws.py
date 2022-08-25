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
        return self.session.client(name, endpoint_url=f"http://{os.environ['AWS_HOST']}:4566")


__aws_session = AwsSession()
s3_client = __aws_session.get_client('s3')


def split_s3_path(s3_path):
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key
