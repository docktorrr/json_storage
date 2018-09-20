import pytest
from jsonschema import ValidationError
from json_storage import JSONStorage
from json_storage.model import BaseModel


class Product(BaseModel):
    filename = 'product.json'
    id_field = 'UUID'
    schema = {
        'type' : 'object',
        'required': [
            'UUID',
            'name',
            'price'
        ],
        'properties': {
            'UUID': {'type': 'string'},
            'name': {'type': 'string'},
            'price': {"type": 'number'},
        },
        'additionalProperties': True,
    }


def test_json_update(tmpdir):
    test_data = {'UUID': '111-111-111', 'name': 'Product 1', 'price': 220.99}
    storage = JSONStorage(tmpdir)
    manager = storage.get_manager(Product)
    manager.update(test_data)
    item = manager.get(test_data['UUID'])
    assert item['UUID'] == test_data['UUID']
    assert item['name'] == test_data['name']
    assert item['price'] == test_data['price']


def test_json_validate():
    product = Product({'UUID': '111-111-111', 'name': 'Product 1', 'price': 220.99})
    product.validate()

    product = Product({'UUID': 222, 'name': 'Product 1', 'price': 220.99})
    with pytest.raises(ValidationError):
        product.validate()

    product = Product({'UUID': 222, 'name': 'Product 1', 'price': '220.99'})
    with pytest.raises(ValidationError):
        product.validate()

    product = Product({'UUID': '111-111-111', 'name': 'Product 1'})
    with pytest.raises(ValidationError):
        product.validate()

    product = Product({'UUID': '111-111-111', 'name': 'Product 1', 'price': 220.99, 'other': 'test'})
    product.validate()
