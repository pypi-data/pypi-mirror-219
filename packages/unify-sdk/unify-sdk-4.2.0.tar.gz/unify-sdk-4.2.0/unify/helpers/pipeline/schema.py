import json
from unify.helpers.datasets.column import DatasetHeader
from unify.helpers.pipeline.flow_column import FlowColumn


class FlowSchema:

    def __init__(self, columns: list = None):
        self.columns: list = []
        if columns is not None:
            self.columns = columns.copy()

    def to_dataset_schema(self):
        dataset_schema = []

        for col in self.columns:
            flow_col = FlowColumn(**col)
            dataset_schema.append(DatasetHeader.from_pipline_flow_column(flow_col))

        return dataset_schema
