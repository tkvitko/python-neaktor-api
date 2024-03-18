from neaktor.api import NeaktorApiClient


if __name__ == '__main__':
    my_public_key = 'test'
    api = NeaktorApiClient(public_key=my_public_key)

    my_tasks = api.get_tasks()
    print(len(my_tasks))

    my_users = api.get_users()
    print(len(my_users))

    my_task_models = api.get_task_modes()
    print(my_task_models)

    new_task = api.add_task(model_id='my_model_id',
                            fields={'subject': 'my new task'},
                            assignee_id=1234)
    print(new_task)

    new_comment = api.add_comment(task_id='my_task_id',
                                  text='my comment')
    print(new_comment)
