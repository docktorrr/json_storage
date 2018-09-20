import os
import json
import copy


class JSONStorage:
    """
    Implements read / write operations to files.
    """

    _managers = {}

    def __init__(self, path):
        self.path = path

    def set_data(self, filename, data):
        with open(os.path.join(self.path, filename), 'w+') as f:
            # TODO: concurrency control
            json.dump(data, f)

    def get_data(self, filename):
        try:
            with open(os.path.join(self.path, filename), 'r') as f:
                # TODO: concurrency control
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_manager(self, model):
        manager = self._managers.get(model)
        if not manager:
            manager = JSONManager(self, model)
            self._managers[model] = manager
        return manager


class JSONManager:
    """
    Manager for performing operations with JSON data.
    """

    def __init__(self, storage, model):
        self.storage = storage
        self.model = model

    def update(self, obj_data):
        obj_copy = copy.deepcopy(obj_data)
        id_ = obj_copy.pop(self.model.id_field)
        data = self.storage.get_data(self.model.filename)
        data[id_] = obj_copy
        self.storage.set_data(self.model.filename, data)

    def delete(self, id_):
        data = self.storage.get_data(self.model.filename)
        data.pop(id_, None)
        self.storage.set_data(self.model.filename, data)

    def get(self, id_):
        data = self.storage.get_data(self.model.filename)
        obj_data = data.get(id_)
        obj_data[self.model.id_field] = id_
        return obj_data
