import _ast
import ast

from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError
from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.placeholders.string_parser import StringParser
from fun_with_ast.placeholders.node import NodePlaceholder


class CompositePlaceholder(Placeholder):

    """Node which wraps one or more other nodes."""

    def _match(self, node, string):
        """Makes sure node.(self.field_name) is in string."""
        self.Validate(node)
        elements = self.GetElements(node)
        elements = self._set_parents(elements, node)
        parser = StringParser(
            string, elements, starting_parens=self.starting_parens)
        return parser.GetMatchedText()

    def _set_parents(self, elements, node):
        if isinstance(node, ast.Constant) and not isinstance(node.s, int) and not hasattr(node, 'default_quote'):
            raise ValueError('Constant nodes must of type string must have a default_quote attribute')
        for element in elements:
            element.parent = node
        return elements

    def GetSource(self, node):
        source = ''
        elements = self.GetElements(node)
        for element in elements:
            source += element.GetSource(node)
        return source
    def Validate(self, unused_node):
        return True


class FieldPlaceholder(CompositePlaceholder):
    """Placeholder for a field."""

    def __init__(
            self, field_name, before_placeholder=None):
        super(FieldPlaceholder, self).__init__()
        self.field_name = field_name
        self.before_placeholder = before_placeholder

    def GetElements(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        #if isinstance(node, _ast.Constant) and not getattr(node,'matcher',None):
        #    raise ValueError('Constant nodes must have a matcher')
#        if isinstance(node, _ast.Constant):
#            raise NotImplementedError('not implemented yet')

        else:
            field_value = getattr(node, self.field_name)

        if not field_value and field_value != 0:
            return []
        #if field_value is None:
        #    return []

        elements = []
        if self.before_placeholder:
            elements.append(self.before_placeholder)
        elements.append(NodePlaceholder(field_value))
        return elements

    def _match(self, node, string):
        return super(FieldPlaceholder, self)._match(node, string)

    def Validate(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        else:
            field_value = getattr(node, self.field_name)
        if isinstance(field_value, (list, tuple)):
            raise BadlySpecifiedTemplateError(
                'Field {} of node {} is a list. please use a ListFieldPlaceholder'
                'instead of a FieldPlaceholder'.format(self.field_name, node))

    def __repr__(self):
        return 'FieldPlaceholder for field "{}"'.format(
            self.field_name)

