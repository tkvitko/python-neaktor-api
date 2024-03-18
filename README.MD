# Python Neaktor API wrapper
Python lib to interact with Neaktor

https://neaktor.com/

https://developers.neaktor.com/#/overview 

## Installation
``pip install -r requirements.txt``

## Usage
```python
from neaktor.api import NeaktorApiClient

my_public_key = "test"
api = NeaktorApiClient(public_key=my_public_key)

my_tasks = api.get_tasks()
my_users = api.get_users()
```

## Functionality
### Supports
- public key authorization
- getting task list
- getting users list

### Roadmap
- all other api methods
