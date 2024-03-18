from neaktor.api import NeaktorApiClient


if __name__ == '__main__':
    my_public_key = 'my_public_key'
    api = NeaktorApiClient(public_key=my_public_key)
    my_tasks = api.get_tasks()
    print(len(my_tasks))
    my_users = api.get_users()
    print(len(my_users))
