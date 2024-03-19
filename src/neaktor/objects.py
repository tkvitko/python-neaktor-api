"""
Neaktor objects
"""


class NeaktorObject:
    """Base class for Neaktor object"""
    def __init__(self, data: dict):
        for key, value in data.items():
            self.__dict__[key] = value


class User(NeaktorObject):
    """Neaktor user"""
    def __init__(self, data):
        super(User, self).__init__(data=data)


class Task(NeaktorObject):
    """Neaktor task"""
    def __init__(self, data):
        super(Task, self).__init__(data=data)


class TaskModel(NeaktorObject):
    """Neaktor task model"""
    def __init__(self, data):
        super(TaskModel, self).__init__(data=data)


class Comment(NeaktorObject):
    """Neaktor comment"""
    def __init__(self, data):
        super(Comment, self).__init__(data=data)
