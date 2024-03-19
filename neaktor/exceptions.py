
class NoAuthParam(Exception):
    pass


class NeaktorException(Exception):

    def __init__(self, answer: dict):
        self.answer = answer

    def __str__(self):
        return str(self.answer)
