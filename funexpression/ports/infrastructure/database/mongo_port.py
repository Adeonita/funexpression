from typing import Protocol


class MongoAdapterPort(Protocol):

    def insert(self, data: dict): ...

    def find(self, query: dict): ...

    def update(self, query: dict, data: dict): ...

    def delete(self, query: dict): ...
