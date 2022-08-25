import os

from modelexecute.appconf import LocalConfig, DevConfig


class LocalControlplaneConfig(LocalConfig):
    def __init__(self) -> None:
        super().__init__()
        self.APP_PORT: int = 5000
        self.EXECUTOR_URL: str = 'http://localhost:5001/batch'
        self.PARTITIONER_URL: str = 'http://localhost:5002/partition'


class DevControlplaneConfig(DevConfig):
    def __init__(self) -> None:
        super().__init__()
        self.EXECUTOR_URL: str = 'http://gateway.openfaas.svc.cluster.local:8080/async-function/executor/batch'
        self.PARTITIONER_URL: str = 'http://gateway.openfaas.svc.cluster.local:8080/async-function/partitioner/partition'
