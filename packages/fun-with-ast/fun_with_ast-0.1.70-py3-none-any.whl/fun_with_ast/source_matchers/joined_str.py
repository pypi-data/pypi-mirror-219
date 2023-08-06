from string import Formatter

from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher
from fun_with_ast.placeholders.list_placeholder import ListFieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder


class JoinedStrSourceMatcher(DefaultSourceMatcher):
    """Source matcher for _ast.Tuple nodes."""

    def __init__(self, node, starting_parens=None, parent=None):
        expected_parts = [
            TextPlaceholder(r'f[\'\"]', 'f\''),
            ListFieldPlaceholder(r'values'),
            TextPlaceholder(r'[\'\"]', '')
        ]
        super(JoinedStrSourceMatcher, self).__init__(
            node, expected_parts, starting_parens)
        self.padding_quote = None



    def _match(self, string):
        self._check_not_implemented(string)
        self.padding_quote = self._get_padding_quqte(string)
        string = self._convert_to_multi_part_string(string)
        matched_text = super(JoinedStrSourceMatcher, self)._match(string)
        return matched_text

    def _convert_to_multi_part_string(self, _in):
        formatted_string = list(Formatter().parse(_in[2:]))
#        if len(formatted_string) == 1 and formatted_string[0][1] == None:
#            return _in
        multi_part = _in[0:2]
        for (literal, name, format_spec, conversion) in formatted_string:
            if literal:
                multi_part += self.padding_quote + literal + self.padding_quote
            if name:
                multi_part += self.padding_quote+ '{' + name + '}'+self.padding_quote
            if format_spec:
                raise NotImplementedError
            if conversion:
                raise NotImplementedError

        return multi_part

    def MatchStartParens(self, remaining_string):
#        raise NotImplementedError('use main stack')
        return remaining_string

    def GetSource(self):
        matched_source = super(JoinedStrSourceMatcher, self).GetSource()
        matched_source = self._convert_to_single_part_string(matched_source)

        return matched_source

    def _convert_to_single_part_string(self, _in):
        if _in[-2:] == self.padding_quote * 2:
            result = _in[:-1]
        if result[0:3] == "f" + self.padding_quote*2:
            result = result.replace("f"+self.padding_quote*2, "f"+ self.padding_quote)
        result=result.replace(self.padding_quote*2+'{', '{')
        result=result.replace('}'+self.padding_quote*2, '}')
        return result

    def _get_padding_quqte(self, string):
        if string.startswith("f'"):
            return "'"
        elif string.startswith("f\""):
            return "\""
        raise BadlySpecifiedTemplateError('Formatted string must start with \' or \"')

    def _check_not_implemented(self, string):
        if '\"\"' in string:
            raise NotImplementedError('Double-quotes are not supported yet')
