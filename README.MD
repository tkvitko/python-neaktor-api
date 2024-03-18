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
new_task = api.add_task(model_id='my_model_id',
                        fields={'subject': 'my new task'},
                        assignee_id=1234)
new_comment = api.add_comment(task_id='my_task_id', 
                              text='my comment')

```

## Functionality
### Supports
- public key authorization
- getting tasks list
- getting users list
- adding tasks
- adding comments to tasks

### Roadmap
- all other api methods
