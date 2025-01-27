
import requests
import base64
import json
import os
from time import sleep
import logging
import secrets

from telescope_agent import Stats

INTERVAL_S = 60
CONFIG_PATH = "config.json"
STATE_PATH = ".state.json"
API_VERSION = "0.0.0"

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
            self.server_url: list[str] = config["server_url"]
            self.smart_devices: list[str] = config["smart_devices"]
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance
    
class State:
    _instance = None

    def load(self):
        with open(STATE_PATH, "rb") as f:
            config: dict = json.loads(f.read())
        self.agent_id: str = config["agent_id"]
        self.agent_secret: str = config["agent_secret"]

    def save(self):
        data = {
            "agent_id": self.agent_id,
            "agent_secret": self.agent_secret,
        }
        with open(STATE_PATH, "w") as f:
            f.write(json.dumps(data, indent=4))

    def _setup(self):
        if os.path.exists(STATE_PATH):
            self.load()
        else:
            self.agent_id = secrets.token_hex(16)
            self.agent_secret = secrets.token_hex(32)
            self.save()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance


class Publisher:
    _instance = None

    def _setup(self):
        config = Config()
        self.__server_url = config.server_url

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Publisher, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    @staticmethod
    def __post_json(url: str, post_json: dict, timeout: int = 10) -> dict | None:
        _logger.debug("POST %s", url)
        try:
            response = requests.post(url, timeout=timeout, json=post_json)
            if response.status_code != 200:
                _logger.error(
                    "POST %s failed with status %s.", url, response.status_code
                )
                _logger.debug("Response body:\n%s", response.content.decode())
                return None
            return response.json()
        except Exception as e:
            _logger.error(
                "POST %s failed with unknown error:\n%s", url, repr(e)
            )
            return None

    def publish_stats(self, stats: dict):
        state = State()
        self.__post_json(
            self.__server_url,
            {
                "version": API_VERSION,
                "agent_id": state.agent_id,
                "agent_secret": state.agent_secret,
                "body": stats,
            }
        )

def main() -> int:
    # TODO set up socket

    config = Config()
    publisher = Publisher()

    # TODO read config file for smart devices
    smart_devices = config.smart_devices

    while True:
        stats = Stats.all(smart_devices=smart_devices)
        publisher.publish_stats(stats)
        sleep(INTERVAL_S)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        exit(130)
