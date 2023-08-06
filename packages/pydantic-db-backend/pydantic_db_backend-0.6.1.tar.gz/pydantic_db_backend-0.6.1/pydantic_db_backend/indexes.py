from typing import List, Dict

from pydantic import BaseModel


class Index(object):
    type: str
    name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class SortingIndex(Index):
    type = "sorting"
    sorting: List[Dict[str, str]]

    def __init__(self, name: str, sorting: List[Dict[str, str]]) -> None:
        super().__init__(name)
        self.sorting = sorting


class AggregationIndex(Index):
    type = "aggregation"
    spec: dict

    def __init__(self, name: str, spec: dict) -> None:
        super().__init__(name)
        self.spec = spec

    @property
    def design_document(self):
        return f"aggregation_{self.name}"

    @property
    def view_name(self):
        return self.name
