"""
Usage example
"""

from typing import List

from src.neaktor import NeaktorApiClient
from src.neaktor import User, Task, TaskModel, Comment

if __name__ == '__main__':
    my_public_key = 'test'
    api = NeaktorApiClient(public_key=my_public_key)

    my_tasks: List[Task] = api.get_tasks()
    my_users: List[User] = api.get_users(user_ids={1, 2})
    my_task_models: List[TaskModel] = api.get_task_models()
    new_task: Task = api.add_task(model_id='my_model_id', fields={'subject': 'my new task'}, assignee_id=1234)
    new_comment: Comment = api.add_comment(task_id='my_task_id', text='my comment')
    deletion_status: dict = api.delete_task(task_id=1)
