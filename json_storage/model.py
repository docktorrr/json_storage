from jsonschema import validate, ValidationError, SchemaError


class BaseModel:
    """
    Base class for object stored as a JSON.
    """

    filename = None
    id_field = None
    schema = None
    _data = None

    def __init__(self, data):
        if not self.filename:
            raise NotImplementedError("Set filename property")
        if not self.id_field:
            raise NotImplementedError("Set id_field property")
        self._data = data

    def validate(self):
        if not self._data:
            raise ValidationError()
        if not self.schema:
            raise SchemaError()

        validate(self._data, self.schema)

    def get_data(self):
        return self._data

