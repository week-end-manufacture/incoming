import json
from dataclasses import dataclass, field
from enum import Enum, unique


class PreProcessing:
    def __init__(self) -> None:
        pass

    def open_ic_settings(self):
        with open('./config/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_default(self):
        with open('./config/ic-preset/ic_default.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset
    

@unique
class IcType(Enum):
    VIDEO = 1
    IMANGE = 2

@dataclass
class IcFile:
    path: str
    filename: str
    extension: str
    type: IcType