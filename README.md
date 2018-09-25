# JSON Storage

## Installation

pip install git+https://github.com/docktorrr/json_storage.git

## Usage

```python
from json_storage import JSONStorage
from json_storage.model import BaseModel


# Create model
class Product(BaseModel):
    filename = 'product.json'
    id_field = 'UUID'
    schema = {
        'type': 'object',
        'required': [
            'UUID',
            'name',
            'price'
        ],
        'properties': {
            'UUID': {'type': 'string'},
            'name': {'type': 'string'},
            'price': {"type": 'number'},
        }
    }

# JSON data
data = {'UUID': '111-111-111', 'name': 'Product 1', 'price': 220.99}

# Validate data
product = Product(data)
product.validate()

# Define JSON storage and JSON manager
storage = JSONStorage('/path/to/files/')
manager = storage.get_manager(Product)

# Create / update JSON object (depends on id_field value)
manager.update(data)

# Delete JSON object
manager.delete('111-111-111')

# Get JSON objects by id_field value
items = manager.get(['111-111-111', '111-111-112'])

# Get all JSON objects
items = manager.all()

# Clear all JSON objects for this model
manager.clear_all()
```