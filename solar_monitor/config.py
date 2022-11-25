from dataclasses import dataclass
from pytils.config import Configuration


@dataclass
class PanelStatus:
    url: str = ''
    username: str = ''
    password: str = ''


@dataclass
class PanelStorage:
    url: str = ''


@dataclass
class Slack:
    url: str = ''


@dataclass
class Config(Configuration):
    panel_status: PanelStatus = PanelStatus()
    slack: Slack = Slack()
    panel_storage: PanelStorage = PanelStorage()


if __name__ == '__main__':
    config = Config.init()
    print(config)
