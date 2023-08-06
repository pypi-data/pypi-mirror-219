from fun_with_ast.placeholders.list_placeholder import SeparatedListFieldPlaceholder
from fun_with_ast.source_matchers.matcher_resolver import GetDynamicMatcher

from fun_with_ast.manipulate_node.call_args_node import CallArgs
from fun_with_ast.source_matchers.base_matcher import SourceMatcher

from fun_with_ast.placeholders.composite import CompositePlaceholder
from fun_with_ast.placeholders.node import NodePlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder


class ArgsDefaultsPlaceholder(CompositePlaceholder):
    """Placeholder to handle args and defaults for _ast.argument.

    These fields behave differently than most other fields and therefore
    don't fall into any of the other placeholders. Therefore, we have to define
    a custom placeholder.
    """

    def __init__(self, arg_separator_placeholder, kwarg_separator_placeholder):
        super(ArgsDefaultsPlaceholder, self).__init__()
        self.arg_separator_placeholder = arg_separator_placeholder
        self.kwarg_separator_placeholder = kwarg_separator_placeholder
        self.arg_separators = []
        self.kwarg_separators = []

    def _GetArgSeparator(self, index):
        if index < len(self.arg_separators):
            return self.arg_separators[index]
        new_placeholder = self.arg_separator_placeholder.Copy()
        self.arg_separators.append(new_placeholder)
        return new_placeholder

    def _GetKwargSeparator(self, index):
        if index < len(self.kwarg_separators):
            return self.kwarg_separators[index]
        new_placeholder = self.kwarg_separator_placeholder.Copy()
        self.kwarg_separators.append(new_placeholder)
        return new_placeholder

    def _GetArgsKwargs(self, node):
        kwargs = list(zip(node.args[len(node.args) - len(node.defaults):], node.defaults))
        args = node.args[:-len(kwargs)] if kwargs else node.args
        return args, kwargs

    def GetElements(self, node):
        """Gets the basic elements of this composite placeholder."""
        args, kwargs = self._GetArgsKwargs(node)
        elements = []
        arg_index = 0
        kwarg_index = 0
        for index, arg in enumerate(args):
            elements.append(NodePlaceholder(arg))
            if index is not len(args) - 1 or kwargs:
                elements.append(self._GetArgSeparator(arg_index))
                arg_index += 1
        for index, (key, val) in enumerate(kwargs):
            elements.append(NodePlaceholder(key))
            elements.append(self._GetKwargSeparator(kwarg_index))
            kwarg_index += 1
            elements.append(NodePlaceholder(val))
            if index is not len(kwargs) - 1:
                elements.append(self._GetArgSeparator(arg_index))
                arg_index += 1
        return elements

    def __repr__(self):
        return ('ArgsDefaultsPlaceholder separating args with "{}" '
                'and kwargs with "{}"'
                .format(self.arg_separator_placeholder,
                        self.kwarg_separator_placeholder))


class KeysValuesPlaceholder(ArgsDefaultsPlaceholder):

    def _GetArgsKwargs(self, node):
        return [], list(zip(node.keys, node.values))


class ArgsKeywordsPlaceholder(ArgsDefaultsPlaceholder):

    def __init__(self, arg_separator_placeholder, kwarg_separator_placeholder):
        super(ArgsKeywordsPlaceholder, self).__init__(
            arg_separator_placeholder, kwarg_separator_placeholder)
        self.stararg_separator = TextPlaceholder(r'\s*,?\s*\*', ', *')
        self.start_paren_matchers = []
        self.args_matcher = None
        self.use_default_matcher = True # TODO: remove this feature flag

    def _match(self, node, string):

        if self.use_default_matcher == True:
            default_matcher_result = self._use_default_matcher(node, string)
            return default_matcher_result
        else:
            remaing_string = super()._match(node, string)
            return remaing_string
    def GetElements(self, node):
        if self.use_default_matcher == True and self.args_matcher:
            elements = []
            elements.extend(self.args_matcher.start_paren_matchers)
            elements.extend(self.args_matcher.expected_parts)
            elements.extend(self.args_matcher.end_paren_matchers)
            return elements
        elif self.use_default_matcher == True and not self.args_matcher:
            parts = self._get_parts_for_default_matcher(0, node)
            start_paren = TextPlaceholder(r'\(\s*', '(')
            end_paren = TextPlaceholder(r'\s*,?\s*\)', ')')
            parts.insert(0, start_paren)
            parts.append(end_paren)
            return parts
        else:
            raise ValueError('old implementation not supported anymore')
# We leave this code for reference only -- will be deleted in the near future
    # def _original_GetElements(self, node):
    #     """Gets the basic elements of this composite placeholder."""
    #     args = node.args or []
    #     keywords = node.keywords or []
    #     elements = []
    #     arg_index = 0
    #     for index, arg in enumerate(args):
    #         elements.append(NodePlaceholder(arg))
    #         if index != len(args) - 1 or keywords:
    #             elements.append(self._GetArgSeparator(arg_index))
    #             arg_index += 1
    #     if getattr(node, 'starargs', False):
    #         elements.append(self.stararg_separator)
    #         elements.append(NodePlaceholder(node.starargs))
    #         if keywords:
    #             arg_seperator = self._GetArgSeparator(arg_index)
    #             elements.append(arg_seperator)
    #             arg_index += 1
    #     for index, arg in enumerate(keywords):
    #         elements.append(NodePlaceholder(arg))
    #         if index != len(keywords) - 1:
    #             elements.append(self._GetArgSeparator(arg_index))
    #             arg_index += 1
    #     start_paren = TextPlaceholder(r'\(\s*', '(')
    #     end_paren = TextPlaceholder(r'\s*,?\s*\)', ')')
    #     elements.insert(0,start_paren)
    #     elements.append(end_paren)
    #
    #     return elements

    def _use_default_matcher(self, node, string):
        arg_index = len(node.args)
        args_node = CallArgs(node.args)
        parts = self._get_parts_for_default_matcher(arg_index, node)
        self.args_matcher = GetDynamicMatcher(args_node, parts_in=parts)
        matched_string = self.args_matcher._match(string)
        return matched_string

    def _get_parts_for_default_matcher(self, arg_index, node):
        parts = []
        parts.append(SeparatedListFieldPlaceholder(
            r'args', TextPlaceholder(r'\s*,\s*', ', ')))
        if getattr(node, 'starargs', False):
            parts.append(self.stararg_separator)
            parts.append(NodePlaceholder(node.starargs))
            if node.keywords:
                arg_seperator = self._GetArgSeparator(arg_index)
                parts.append(arg_seperator)
                arg_index += 1
            for index, arg in enumerate(node.keywords):
                parts.append(NodePlaceholder(arg))
                if index != len(node.keywords) - 1:
                    parts.append(self._GetArgSeparator(arg_index))
                    arg_index += 1
        return parts


class OpsComparatorsPlaceholder(ArgsDefaultsPlaceholder):

    def _GetArgsKwargs(self, node):
        return [], list(zip(node.ops, node.comparators))
