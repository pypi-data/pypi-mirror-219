import _ast
import re


class SyntaxFreeLine(_ast.stmt):
    """Class defining a new node that has no syntax (only optional comments)."""

    def __init__(self, comment=None, col_offset=0, comment_indent=1):
        super(SyntaxFreeLine, self).__init__()
        self.col_offset = col_offset
        self._fields = ['full_line']
        self.comment = comment
        self.comment_indent = comment_indent

    @property
    def full_line(self):
        if self.comment is not None:
            return '{}#{}{}'.format(' ' * self.col_offset,
                                    ' ' * self.comment_indent,
                                    self.comment)
        return ''

    @classmethod
    def MatchesStart(cls, text):
        is_syntax_free_line = re.match('^([ \t]*)(?:|(#)([ \t]*)(.*))\n', text)
        return is_syntax_free_line

    def SetFromSrcLine(self, line):
        match = self.MatchesStart(line)
        if not match:
            raise ValueError('line {} is not a valid SyntaxFreeLine'.format(line))
        self.col_offset = len(match.group(1))
        self.comment_indent = 0
        self.comment = None
        if match.group(2):
            self.comment = ''
            if match.group(3):
                self.comment_indent = len(match.group(3))
            if match.group(4):
                self.comment = match.group(4)
