import pprint

from fun_with_ast.placeholders.base_match import MatchPlaceholderList
from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class DefaultSourceMatcher(SourceMatcher):
    """Class to generate the source for a node."""

    def __init__(self, node, expected_parts, starting_parens=None, parent_node=None):
        super(DefaultSourceMatcher, self).__init__(node, starting_parens)
        previous_was_string = False
        # We validate that the expected parts does not contain two strings in
        # a row.
        for part in expected_parts:
            if not isinstance(part, Placeholder):
                raise ValueError('All expected parts must be Placeholder objects')
            if isinstance(part, TextPlaceholder) and not previous_was_string:
                previous_was_string = True
            else:
                previous_was_string = False
        self.expected_parts = expected_parts


    def _match(self, string):
        """Matches the string against self.expected_parts.

        Note that this is slightly peculiar in that it first matches fields,
        then goes back to match text before them. This is because currently we
        don't have matchers for every node, so by default, we separate each
        field with a '.*' TextSeparator, which is basically the current behavior
        of ast_annotate. This can change after we no longer have any need for
        '.*' TextSeparators.

        Args:
          string: {str} The string to match.

        Returns:
          The matched text.

        Raises:
          BadlySpecifiedTemplateError: If there is a mismatch between the
            expected_parts and the string.
          ValueError: If there is more than one TextPlaceholder in a rwo
        """
        remaining_string = self.MatchWhiteSpaces(string)
        remaining_string = self.MatchStartParens(remaining_string)


        try:
            remaining_string = MatchPlaceholderList(
                remaining_string, self.node, self.expected_parts,
                self.start_paren_matchers)
            remaining_string = self.MatchEndParen(remaining_string)

        except BadlySpecifiedTemplateError as e:
            raise BadlySpecifiedTemplateError(
                'When attempting to match string "{}" with {}, this '
                'error resulted:\n\n{}'
                    .format(string, self, e.message))
        matched_string = DefaultSourceMatcher.GetSource(self)
        self.end_of_line_comment = self.MatchCommentEOL(remaining_string)
        end_ws = self.GetWhiteSpaceText(self.end_whitespace_matchers)
        result =  (matched_string + end_ws + self.end_of_line_comment)
        self.matched = True
        self.matched_source = result
        return result


    def GetSource(self):
        self.validated_call_to_match()
        if self.matched:
            return self.matched_source
        source_list = []
        for part in self.expected_parts:
            part_source = part.GetSource(self.node)
            source_list.append(part_source)
        source = ''.join(source_list)
        source = '{}{}{}'.format(
            self.GetStartParenText(),
            source,
            self.GetEndParenText())

        if self.start_whitespace_matchers:
            source = '{}{}'.format(self.GetWhiteSpaceText(self.start_whitespace_matchers), source)
        if self.end_whitespace_matchers:
            source = '{}{}'.format(source, self.GetWhiteSpaceText(self.end_whitespace_matchers))
        if self.end_of_line_comment:
            source = '{}{}'.format(source, self.end_of_line_comment)
        return source

    def __repr__(self):
        return ('DefaultSourceMatcher "{}" for node "{}" expecting to match "{}"'
                .format(super(DefaultSourceMatcher, self).__repr__(),
                        self.node,
                        pprint.pformat(self.expected_parts)))

    def MatchWhiteSpaces(self, remaining_string):
        ws_placeholder = self.start_whitespace_matchers[0]
        match_ws = ws_placeholder._match(None, remaining_string)
        remaining_string = remaining_string[len(match_ws):]
        return remaining_string

