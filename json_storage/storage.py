import os
import json
import copy
from typing import Iterable, Type

from .model import BaseModel


class JSONStorage:
    """
    Implements read / write operations to files.
    """

    _managers = {}

    def __init__(self, path: str):
        self.path = path

    def set_data(self, filename: str, data: dict) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, filename), 'w+') as f:
            # TODO: concurrency control
            json.dump(data, f)

    def get_data(self, filename: str) -> dict:
        try:
            with open(os.path.join(self.path, filename), 'r') as f:
                # TODO: concurrency control
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_manager(self, model: Type[BaseModel]):
        manager = self._managers.get(model)
        if not manager:
            manager = JSONManager(self, model)
            self._managers[model] = manager
        return manager


class JSONManager:
    """
    Manager for performing operations with JSON data.
    """

    def __init__(self, storage: JSONStorage, model: Type[BaseModel]):
        self.storage = storage
        self.model = model

    def update(self, obj_data: dict) -> None:
        obj_copy = copy.deepcopy(obj_data)
        id_ = obj_copy.pop(self.model.id_field)
        data = self.storage.get_data(self.model.filename)
        data[id_] = obj_copy
        self.storage.set_data(self.model.filename, data)

    def delete(self, id_: str) -> None:
        data = self.storage.get_data(self.model.filename)
        data.pop(id_, None)
        self.storage.set_data(self.model.filename, data)

    def get(self, ids: Iterable[str]) -> dict:
        data = self.storage.get_data(self.model.filename)
        result = []
        for id_ in ids:
            obj_data = data.get(id_)
            if obj_data:
                obj_data[self.model.id_field] = id_
                result.append(obj_data)
        return result

    def all(self) -> list:
        result = []
        data = self.storage.get_data(self.model.filename)
        for id_, val in data.items():
            val.update({self.model.id_field: id_})
            result.append(val)
        return result

    def clear_all(self) -> None:
        self.storage.set_data(self.model.filename, {})

