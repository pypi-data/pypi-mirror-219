import _ast


class CallArgs(_ast.stmt):
    """A node for handling arguments for a function call"""

    def __init__(self, args_list):
        self._fields = ['args']
        self.args = args_list
