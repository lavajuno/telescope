import zmq
import base64
import json
from time import sleep
import logging

from telescope import Stats

INTERVAL_S = 60
ZMQ_CTX = zmq.Context()
CONFIG_PATH = "config.json"

_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)
_logger_console_handler = logging.StreamHandler()
_logger_console_handler.setLevel(logging.DEBUG)
_logger_console_handler.setFormatter(
    logging.Formatter("{asctime} {levelname:<8} : {message}", style="{")
)
_logger.addHandler(_logger_console_handler)


class Config:
    _instance = None

    def _setup(self):
        with open(CONFIG_PATH, "rb") as f:
            config: dict = json.loads(f.read())
            # self.host = config.get("host")
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance



class Publisher:
    _instance = None

    def _setup(self):
        self.__socket = ZMQ_CTX.socket(zmq.PUB)
        # TODO connect

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Publisher, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    def publish_stats(self, stats: dict, crypto: Crypto):
        stats_b64 = base64.b64encode(json.dumps(stats).encode("utf-8"))
        print(stats_b64)
        print(base64.b64decode(stats_b64).decode("utf-8"))
        # TODO encode, sign, and publish stats
        pass

def main() -> int:
    # TODO set up socket

    # TODO read config file for smart devices
    smart_devices = []

    # while True:
    #     sleep(INTERVAL_S)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        exit(130)
