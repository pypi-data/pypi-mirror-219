import _ast

from fun_with_ast.source_matchers.body import BodyPlaceholder
from fun_with_ast.get_source import GetSource
from fun_with_ast.source_matchers.base_matcher import SourceMatcher
from fun_with_ast.placeholders.base_match import MatchPlaceholderList
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.placeholders.list_placeholder import SeparatedListFieldPlaceholder


class WithSourceMatcher(SourceMatcher):
    """Class to generate the source for an _ast.With node."""

    def __init__(self, node, starting_parens=None, Parent=None):
        super(WithSourceMatcher, self).__init__(node, starting_parens)
        self.with_placeholder = TextPlaceholder(r' *(with)? *', 'with ')
        self.withitems_placeholder = SeparatedListFieldPlaceholder('items', before_separator_placeholder=TextPlaceholder(r', *', ', '))
        self.colon_placeholder = TextPlaceholder(r':\n?', ':\n')
        self.body_placeholder = BodyPlaceholder('body')
        self.is_compound_with = False
        self.starting_with = True

    def _match(self, string):
        if string.lstrip().startswith('with'):
            self.starting_with = True
        placeholder_list = [self.with_placeholder,
                            self.withitems_placeholder]
        remaining_string = MatchPlaceholderList(
            string, self.node, placeholder_list)
        if remaining_string.lstrip().startswith(','):
            self.is_compound_with = True
            placeholder_list = [self.compound_separator,
                                self.body_placeholder]
            remaining_string = MatchPlaceholderList(
                remaining_string, self.node, placeholder_list)
        else:
            placeholder_list = [self.colon_placeholder,
                                self.body_placeholder]
            remaining_string = MatchPlaceholderList(
                remaining_string, self.node, placeholder_list)

        if not remaining_string:
            return string
        return string[:len(remaining_string)]

    def GetSource(self):
        placeholder_list = []
        if self.starting_with:
            placeholder_list.append(self.with_placeholder)
        placeholder_list.append(self.withitems_placeholder)
#        placeholder_list.append(self.optional_vars)
        if (self.is_compound_with and
                isinstance(self.node.body[0], _ast.With)):
            if not hasattr(self.node.body[0], 'matcher'):
                # Triggers attaching a matcher. We don't act like an stmt,
                # so we can assume no indent.
                GetSource(self.node.body[0], assume_no_indent=True)
            # If we're part of a compound with, we want to make
            # sure the initial "with" of the body isn't included
            self.node.body[0].matcher.starting_with = False
            placeholder_list.append(self.compound_separator)
        else:
            # If we're not a compound with, we expect the colon
            placeholder_list.append(self.colon_placeholder)
        placeholder_list.append(self.body_placeholder)

        source_list = [p.GetSource(self.node) for p in placeholder_list]
        return ''.join(source_list)
