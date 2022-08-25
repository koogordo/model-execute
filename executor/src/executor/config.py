from modelexecute.appconf import LocalConfig, DevConfig


class LocalExecutorConfig(LocalConfig):
    def __init__(self) -> None:
        super().__init__()
        self.APP_PORT = 5001


class DevExecutorConfig(DevConfig):
    pass
