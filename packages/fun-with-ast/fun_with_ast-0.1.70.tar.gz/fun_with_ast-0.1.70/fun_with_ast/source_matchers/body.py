from fun_with_ast.placeholders.list_placeholder import ListFieldPlaceholder
from fun_with_ast.manipulate_node.syntax_free_line_node import SyntaxFreeLine
from fun_with_ast.get_source import GetSource
from fun_with_ast.placeholders.base_match import MatchPlaceholder, MatchPlaceholderList


class BodyPlaceholder(ListFieldPlaceholder):
    """Placeholder for a "body" field. Handles adding SyntaxFreeLine nodes."""

    def __init__(self, *args, **kwargs):
        self.match_after = kwargs.pop('match_after', False)
        super(BodyPlaceholder, self).__init__(*args, **kwargs)

    def MatchSyntaxFreeLine(self, remaining_string):
        line, remaining_string = remaining_string.split('\n', 1)
        syntax_free_node = SyntaxFreeLine()
        line += '\n'
        syntax_free_node.SetFromSrcLine(line)
        GetSource(syntax_free_node, text=line)
        return remaining_string, syntax_free_node

    def _match(self, node, string):
        remaining_string = string
        new_node = []
        if not getattr(node, self.field_name):
            return ''
        if self.prefix_placeholder:
            remaining_string = MatchPlaceholder(
                remaining_string, node, self.prefix_placeholder)
        field_value = getattr(node, self.field_name)
        for index, child in enumerate(field_value):
            remaining_string = self._skip_syntax_free_lines(new_node, remaining_string)
            new_node.append(child)
            number_of_indents = (len(remaining_string) -
                                  len(remaining_string.lstrip()))
            indent_level = ' ' * number_of_indents
            value_at_index=self.GetValueAtIndex(field_value, index)
            self._set_parents(value_at_index, node)
            remaining_string = MatchPlaceholderList(
                remaining_string, node, value_at_index)

        while (SyntaxFreeLine.MatchesStart(remaining_string) and
               (remaining_string.startswith(indent_level) or self.match_after)):
            remaining_string, syntax_free_node = self.MatchSyntaxFreeLine(
                remaining_string)
            new_node.append(syntax_free_node)
        setattr(node, self.field_name, new_node)
        matched_string = string
        if remaining_string:
            matched_string = string[:-len(remaining_string)]
        return matched_string

    def _skip_syntax_free_lines(self, new_node, remaining_string):
        while SyntaxFreeLine.MatchesStart(remaining_string):
            remaining_string, syntax_free_node = self.MatchSyntaxFreeLine(
                remaining_string)
            new_node.append(syntax_free_node)
        return remaining_string

    def GetElements(self, node):
        field_value = getattr(node, self.field_name)
        elements = []
        if not field_value:
            return elements
        if self.prefix_placeholder:
            elements.append(self.prefix_placeholder)
        for index, unused_child in enumerate(field_value):
            elements.extend(self.GetValueAtIndex(field_value, index))
        return elements
