
import re

from fun_with_ast.placeholders.text import TextPlaceholder

class WhiteSpaceTextPlaceholder(TextPlaceholder):
    """Placeholder for text (non-field). For example, 'def (' in FunctionDef."""

    def __init__(self):
        super(WhiteSpaceTextPlaceholder, self).__init__(r'[ \t]*', default='', longest_match=False)

