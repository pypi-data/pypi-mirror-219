import json
from unify.helpers.pipeline.flow_column import FlowColumn

"""
  {
    "header": "name",
    "column": {
      "type": "text",
      "properties": {
        "optional": false,
        "datasets.v1.columnType": "Normal"
      }
    }
  }
"""

col_type_translation = {
    "id": "Normal",
    "normal": "Normal",
    "Normal": "Normal",
    "template": "Template",
    "sensor": "Sensor",
    "equipmentid": "EquipmentId",
    "empty": "Empty",
    "attributeid": "AttributeId",
    "primaryid": "PrimaryId",
    "unitofmeasure": "UnitOfMeasure",
    "sourceserver": "SourceServer"
}

# https://github.com/Voltir/datum/blob/master/core/src/main/scala/datum/patterns/schemas/Type.scala#L18
col_data_translation = {
    "STRING": "text",
    "BOOLEAN": "boolean",
    "LONG": "long",
    "DOUBLE": "double",
    "INT": "int",
    "FLOAT": "float"
}


class DatasetColumn:

    def __init__(self, data_type: str = None, optional: bool = False, column_type: str = None):
        self.data_type: str = data_type
        self.optional: bool = optional
        self.column_type: str = column_type

    def build(self):
        return {
            "type": self.data_type,
            "properties": {
                "optional": self.optional,
                "datasets.v1.columnType": self.column_type
            }
        }


class DatasetHeader:

    @staticmethod
    def from_pipline_flow_column(flow_column: FlowColumn):
        dataset_column = DatasetColumn(
            data_type=col_data_translation[flow_column.dataType],
            optional=flow_column.isOpt,
            column_type=col_type_translation[flow_column.columnType.lower()]
        )

        return DatasetHeader(
            name=flow_column.name,
            column=dataset_column
        ).build()

    def __init__(self, name: str = None, column: DatasetColumn = None):
        self.header: str = name
        self.column = column if column is not None else DatasetColumn()

    def build(self):
        return {
            "header": self.header,
            "column": self.column.build()
        }
