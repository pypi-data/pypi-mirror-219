class Placeholder(object):
    """Base class for other placeholder objects."""

    def __init__(self):
        self.starting_parens = []

    def _match(self, node, string):
        raise NotImplementedError

    def GetSource(self, node):
        raise NotImplementedError

    def IdentSource(self, node):
        raise NotImplementedError

    def SetStartingParens(self, starting_parens):
        self.starting_parens = starting_parens
