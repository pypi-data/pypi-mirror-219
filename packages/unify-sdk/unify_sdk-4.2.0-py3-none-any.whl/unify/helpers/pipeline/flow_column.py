import json


class FlowColumn:

    def __init__(self, name=None, dataType=None, isOpt=None, columnType=None):
        self.name: str = name
        self.dataType: str = dataType
        self.isOpt: bool = isOpt
        self.columnType: str = columnType

    def build(self):
        return {
            "name": self.name,
            "dataType": self.dataType,
            "isOpt": self.isOpt,
            "columnType": self.columnType
        }
