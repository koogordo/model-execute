import os

from modelexecute.appconf import LocalConfig, DevConfig


class LocalPartitionerConfig(LocalConfig):
    def __init__(self) -> None:
        super().__init__()
        self.APP_PORT = 5002
        self.EXECUTOR_URL: str = 'http://localhost:5001/batch'
        self.CONTROLPLANE_URL: str = 'http://localhost:5000/submit-partitions'


class DevPartitionerConfig(DevConfig):
    def __init__(self) -> None:
        super().__init__()
        self.EXECUTOR_URL: str = 'http://gateway.openfaas.svc.cluster.local:8080/async-function/executor/batch'
        self.CONTROLPLANE_URL: str = 'http://gateway.openfaas.svc.cluster.local:8080/async-function/controlplane/submit-partitions'
