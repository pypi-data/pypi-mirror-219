from abc import ABC
from typing import Dict


class DataSource(ABC):

    def __init__(self, data_source_name: str, data_source_properties: Dict):
        self.data_source_name: str = data_source_name
        self.data_source_properties: Dict = data_source_properties


class SearchIndexDataSource(DataSource):
    pass


class SQLDatasource(DataSource):
    pass
