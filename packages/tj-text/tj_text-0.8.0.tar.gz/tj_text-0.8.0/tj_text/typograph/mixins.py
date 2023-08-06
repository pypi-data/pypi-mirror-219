import re

from .chars import (
    ANYSP,
    DLQUO,
    DPRIME,
    HBAR,
    HYPHEN,
    HYPHEN_MINUS,
    LAQUO,
    LDQUO,
    LSQUO,
    MDASH,
    MDASH_PAIR,
    MINUS,
    NBHYPHEN,
    NBSP,
    NDASH,
    NNBSP,
    RAQUO,
    RDQUO,
    RSQUO,
    SPRIME,
    TIMES,
    WHSP,
    WORD_JOINER,
)
from .constants import (
    CURRENCY_SYMBOLS,
    CURRENCY_SYMBOLS_USED_IN_FORMULAS,
    POLISH_ZLOTY,
    RU_CUSTOM_REPLACEMENTS,
    RU_LONG_PREPOSITIONS,
    RU_PARTICLES,
    RU_VERBOSE_PREPOSITIONS,
)
from .utils import map_choices, without

__all__ = ('EnQuotes', 'RuQuotes', 'EnRuExpressions', 'RuExpressions')


class EnQuotes:
    r"""
    Provides English quotes configutation for :class:`typus.processors.Quotes`
    processor.

    >>> en_typus('He said "\'Winnie-the-Pooh\' is my favorite book!".')
    'He said “‘Winnie-the-Pooh’ is my favorite book!”.'
    """

    # Left odd, right odd, left even, right even
    loq, roq, leq, req = LDQUO, RDQUO, LSQUO, RSQUO


class RuQuotes:
    r"""
    Provides Russian quotes configutation for :class:`typus.processors.Quotes`
    processor.

    >>> ru_typus('Он сказал: "\'Винни-Пух\' -- моя любимая книга!".')
    'Он сказал: «„Винни-Пух“ — моя любимая книга!».'
    """

    # Left odd, right odd, left even, right even
    loq, roq, leq, req = LAQUO, RAQUO, DLQUO, LDQUO


class EnRuExpressions:
    """
    This class holds most of Typus functionality for English and Russian
    languages. It works with :class:`typus.processors.Expressions`.
    """

    expressions = (
        'spaces',
        'linebreaks',
        'apostrophe',
        'complex_symbols',
        'mdash',
        'primes',
        # 'phones',
        'digit_spaces',
        'pairs',
        'vulgar_fractions',
        # 'math',
        # 'ruble',
        'rep_positional_spaces',
        'del_positional_spaces',
        'rep_hyphen_between_short_words',
        'join_digits_with_mdash',
        'join_digits_with_horizontal_bar',
        'horizontal_bar',
    )

    # Any unicode word
    words = r'[^\W\d_]'

    complex_symbols = {
        '...': '…',
        '<-': '←',
        '->': '→',
        '+-': '±',
        '+' + MINUS: '±',
        '<=': '≤',
        '>=': '≥',
        '/=': '≠',
        # Removed, as breaks tokens
        # '==': '≡',
        '(r)': '®',
        '(c)': '©',
        '(p)': '℗',
        '(tm)': '™',
        '(sm)': '℠',
        # cyrillic
        '(с)': '©',
        '(р)': '℗',
        '(тм)': '™',
    }

    vulgar_fractions = {
        '1/2': '½',
        '1/3': '⅓',
        '1/5': '⅕',
        '1/6': '⅙',
        '1/8': '⅛',
        '2/3': '⅔',
        '2/5': '⅖',
        '3/4': '¾',
        '3/5': '⅗',
        '3/8': '⅜',
        '4/5': '⅘',
        '5/6': '⅚',
        '5/8': '⅝',
        '7/8': '⅞',
    }

    math = {
        '-': MINUS,
        # '*xх': TIMES,
    }

    # Not need to put >=, +-, etc, after expr_complex_symbols
    math_operators = fr'[\-{MINUS}\*xх{TIMES}\+\=±≤≥≠÷\/]'

    rep_positional_spaces = {
        # No need to put vulgar fractions in here because of expr_digit_spaces
        # which joins digits and words afterward
        'after': f'←%±{MINUS}{TIMES}©§¶№',
        'both': '&≡≤≥≠',
        'before': f'→{MDASH}',
    }

    del_positional_spaces = {'before': '®℗™℠:,.?!…'}

    # Replace this if you don't need nbsp before ruble
    ruble = NBSP + '₽'

    def expr_spaces(self):
        """
        Trims spaces at the beginning and end of the line and remove extra
        spaces within.

        >>> en_typus('   foo bar  ')
        'foo bar'

        .. caution::
            Doesn't work correctly with nbsp (replaces with whitespace).
        """

        expr = ((fr'{ANYSP}{{2,}}', WHSP), (r'(?:^{0}+|{0}+$)'.format(ANYSP), ''))
        return expr

    def expr_linebreaks(self):
        r"""
        Converts line breaks to unix-style and removes extra breaks
        if found more than two in a row.

        >>> en_typus('foo\r\nbar\n\n\nbaz')
        'foo\nbar\n\nbaz'
        """

        expr = ((r'\r\n', '\n'), (r'\n{2,}', '\n' * 2))
        return expr

    def expr_apostrophe(self):
        """
        Replaces single quote with apostrophe.

        >>> en_typus("She'd, I'm, it's, don't, you're, he'll, 90's")
        'She’d, I’m, it’s, don’t, you’re, he’ll, 90’s'

        .. note::
            By the way it works with any omitted word. But then again, why not?
        """

        expr = ((r'(?<={0}|[0-9])\'(?={0})'.format(self.words), RSQUO),)
        return expr

    def expr_complex_symbols(self):
        """
        Replaces complex symbols with Unicode characters. Doesn't care
        about case-sensitivity and handles Cyrillic-Latin twins
        like ``c`` and ``с``.

        >>> en_typus('(c)(с)(C)(r)(R)...')
        '©©©®®…'

        .. csv-table:: Character map
            :header: …, ←, →, ±, ≤, ≥, ≠, ≡, ®, ©, ℗, ™, ℠

            ..., <-, ->, +- or +−, <=, >=, /=, ==, (r), (c), (p), (tm), (sm)
        """

        expr = (map_choices(self.complex_symbols),)
        return expr

    def expr_mdash(self):
        """
        Replaces dash with mdash.

        >>> en_typus('foo -- bar')  # adds non-breakable space after `foo`
        'foo\u00A0— bar'
        """

        expr = (
            # Double dash guarantees to be replaced with mdash
            (r'{0}--{0}'.format(WHSP), MDASH_PAIR),
            # Dash can be between anything except digits
            # because in that case it's not obvious
            (r'{0}+[\-|{1}]{0}+(?!\d\b)'.format(ANYSP, NDASH), MDASH_PAIR),
            # Same but backwards
            # It joins non-digit with digit or word
            (r'(\b\D+){0}+[\-|{1}]{0}+'.format(ANYSP, NDASH), fr'\1{MDASH_PAIR}'),
            # Line beginning adds nbsp after dash
            (fr'^\-{{1,2}}{ANYSP}+', fr'{MDASH}{NBSP}'),
            # Also mdash can be at the end of the line in poems
            (r'{0}+\-{{1,2}}{0}*(?=$|<br/?>)'.format(ANYSP), fr'{NBSP}{MDASH}'),
        )
        return expr

    def expr_primes(self):
        r"""
        Replaces quotes with prime after digits.

        >>> en_typus('3\' 5" long')
        '3′ 5″ long'

        .. caution::
            Won't break "4", but fails with " 4".
        """

        expr = (
            (fr'(^|{ANYSP})(\d+)\'', r'\1\2' + SPRIME),
            (fr'(^|{ANYSP})(\d+)"', r'\1\2' + DPRIME),
        )
        return expr

    def expr_phones(self):
        """
        Replaces dash with ndash in phone numbers which should be a trio of
        2-4 length digits.

        >>> en_typus('111-00-00'), en_typus('00-111-00'), en_typus('00-00-111')
        ('111–00–00', '00–111–00', '00–00–111')
        """

        expr = (
            (
                r'([0-9]{2,4})\-([0-9]{2,4})\-([0-9]{2,4})',
                r'\1{0}\2{0}\3'.format(NDASH),
            ),
        )
        return expr

    def expr_digit_spaces(self):
        """
        Replaces whitespace with non-breakable space after 4 (and less)
        length digits if word or digit without comma or math operators
        found afterwards:
        3 apples
        40 000 bucks
        400 + 3
        Skips:
        4000 bucks
        40 000,00 bucks
        """

        expr = (
            (
                r'\b(\d{{1,3}}){0}(?=[0-9]+\b|{1}|{2})'.format(
                    WHSP, self.words, self.math_operators
                ),
                r'\1' + NBSP,
            ),
        )
        return expr

    def expr_pairs(self):
        """
        Replaces whitespace with non-breakable space after 1-2 length words.
        """

        expr = (
            # Unions, units and all that small staff
            (fr'\b({self.words}{{1,2}}){WHSP}+', r'\1' + NBSP),
            # Fixes previous with leading dash, ellipsis or apostrophe
            (fr'([-…’]{self.words}{{1,2}}){NBSP}', r'\1' + WHSP),
        )
        return expr

    def expr_units(self):
        """
        Puts non-breakable space between digits and units.

        >>> en_typus('1mm', debug=True), en_typus('1mm')
        ('1_mm', '1 mm')
        """

        expr = (
            (
                fr'\b(\d+){WHSP}*(?!(?:nd|rd|th|d|g|px)\b)({self.words}{{1,3}})\b',
                fr'\1{NBSP}\2',
            ),
        )
        return expr

    def expr_ranges(self):
        """
        Replaces dash with mdash in ranges.
        Supports float and negative values.
        Tries to not mess with minus: skips if any math operator or word
        was found after dash: 3-2=1, 24-pin.
        **NOTE**: _range_ should not have spaces between dash: `2-3` and
        left side should be less than right side.
        """

        def ufloat(string):
            return float(string.replace(',', '.'))

        def replace(match):
            left, dash, right = match.groups()
            if ufloat(left) < ufloat(right):
                dash = MDASH
            return f'{left}{dash}{right}'

        expr = (
            (
                r'(-?(?:[0-9]+[\.,][0-9]+|[0-9]+))(-)'
                r'([0-9]+[\.,][0-9]+|[0-9]+)'
                r'(?!{}+{}|{})'.format(ANYSP, self.math_operators, self.words),
                replace,
            ),
        )
        return expr

    def expr_vulgar_fractions(self):
        """
        Replaces vulgar fractions with appropriate unicode characters.

        >>> en_typus('1/2')
        '½'
        """

        expr = (
            # \b to excludes digits which are not on map, like `11/22`
            map_choices(self.vulgar_fractions, r'\b({0})\b'),
        )
        return expr

    def expr_math(self):
        """
        Puts minus and multiplication symbols between pair and before
        single digits.

        >>> en_typus('3 - 3 = 0')
        '3 − 3 = 0'
        >>> en_typus('-3 degrees')
        '−3 degrees'
        >>> en_typus('3 x 3 = 9')
        '3 × 3 = 9'
        >>> en_typus('x3 better!')
        '×3 better!'

        .. important::

            Should run after `mdash` and `phones` expressions.
        """

        expr = (
            (r'(^|\d{0}*|{0}*)[{1}]({0}*\d)'.format(ANYSP, re.escape(x)), fr'\1{y}\2')
            for x, y in self.math.items()
        )
        return expr

    def expr_abbrs(self):
        """
        Adds narrow non-breakable space and replaces whitespaces between
        shorten words.
        """

        expr = (
            (r'\b({1}\.){0}*({1}\.)'.format(ANYSP, self.words), fr'\1{NNBSP}\2'),
            (r'\b({1}\.){0}*(?={1})'.format(WHSP, self.words), fr'\1{NBSP}'),
        )
        return expr

    def expr_ruble(self):
        """
        Replaces `руб` and `р` (with or without dot) after digits
        with ruble symbol.

        >>> en_typus('1000 р.')
        '1000 ₽'

        .. caution::

            Drops the dot at the end of sentence if match found in there.
        """

        expr = ((fr'(\d){ANYSP}*(?:руб|р)\b\.?', fr'\1{self.ruble}'),)
        return expr

    def _positional_spaces(self, data, find, replace):
        """
        Helper method for `rep_positional_spaces` and `del_positional_spaces`
        expressions.
        """

        both = data.get('both', '')
        before = re.escape(data.get('before', '') + both)
        after = re.escape(data.get('after', '') + both)
        expr = []
        if before:
            expr.append((fr'{find}+(?=[{before}])', replace))
        if after:
            expr.append((fr'(?<=[{after}]){find}+', replace))
        return expr

    def _positional_spaces_before_currency_symbols(self):
        return [
            # add non-breaking space between value and currency symbol
            (
                fr'(?<=\d)({WHSP})*(?=[{"".join(CURRENCY_SYMBOLS)}]|{POLISH_ZLOTY})',
                NBSP,
            ),
            # replace non-breaking space to usual space after polish zloty currency,
            # that added in formulas transform (after ł)
            (fr'(?<=\d{NBSP}{POLISH_ZLOTY})({NBSP})', WHSP),
            # replace non-breaking space to usual space after currency symbols,
            # that uses in formulas transformations
            (
                fr'(?<=\d{NBSP}[{"".join(CURRENCY_SYMBOLS_USED_IN_FORMULAS)}])({NBSP})',
                WHSP,
            ),
        ]

    def expr_rep_positional_spaces(self):
        """
        Replaces whitespaces after and before certain symbols
        with non-breakable space.
        """

        expr = self._positional_spaces(self.rep_positional_spaces, WHSP, NBSP)
        expr += self._positional_spaces_before_currency_symbols()
        return expr

    def expr_del_positional_spaces(self):
        """
        Removes spaces before and after certain symbols.
        """

        expr = self._positional_spaces(self.del_positional_spaces, ANYSP, '')
        return expr

    def expr_rep_hyphen_between_short_words(self):
        """
        Replaces hyphen between two words. One of words should be at most 4 character.
        """
        hyphens = f'({HYPHEN}|{HYPHEN_MINUS})'
        return [
            (fr'(\b{self.words}{{1,4}}){hyphens}({self.words}+\b)', fr'\1{NBHYPHEN}\3'),
            (fr'(\b{self.words}+){hyphens}({self.words}{{1,4}}\b)', fr'\1{NBHYPHEN}\3'),
        ]

    def expr_join_digits_with_mdash(self):
        """
        Prohibits a line break if a digit is followed by an m-dash
        >>> en_typus(f'28{MDASH}word')
        f'28{WORD_JOINER}{MDASH}word'
        >>> en_typus(f'28{MDASH}31')
        f'28{WORD_JOINER}{MDASH}{WORD_JOINER}31'
        """

        return [
            (fr'(\d){MDASH}(\d)', fr'\1{WORD_JOINER}{MDASH}{WORD_JOINER}\2'),
            (fr'(\d){MDASH}({self.words}+\b)', fr'\1{WORD_JOINER}{MDASH}\2'),
        ]

    def expr_join_digits_with_horizontal_bar(self):
        """
        Prohibits a line break if a digit is followed by a horizontal bar
        >>> en_typus(f'28{HBAR}word')
        f'28{WORD_JOINER}{HORIZONTAL_BAR}word'
        >>> en_typus(f'28{HBAR}31')
        f'28{WORD_JOINER}{HORIZONTAL_BAR}{WORD_JOINER}31'
        """

        return [
            (fr'(\d){HBAR}(\d)', fr'\1{WORD_JOINER}{HBAR}{WORD_JOINER}\2'),
            (fr'(\d){HBAR}({self.words}+\b)', fr'\1{WORD_JOINER}{HBAR}\2'),
        ]

    def expr_horizontal_bar(self):
        """
        Apply to a horizontal bar the rules of the m-dash.
        """
        expr = (
            # Horizontal can be between anything except digits
            # because in that case it's not obvious
            (fr'{ANYSP}+{HBAR}{ANYSP}', f'{NBSP}{HBAR}{WHSP}'),
            # Line beginning adds nbsp after horizontal bar
            (fr'^\{HBAR}{{1,2}}{ANYSP}+', fr'{HBAR}{NBSP}'),
            # Also horizontal bar can be at the end of the line
            (fr'{ANYSP}+\{HBAR}{{1,2}}{ANYSP}*(?=$|<br/?>)', fr'{NBSP}{HBAR}'),
        )
        return expr


class RuExpressions(EnRuExpressions):
    """
    Reorder a `rep_hyphen_between_short_words` method
    to ensure `rep_positional_spaces_after_long_prepositions` works correctly because
    some long prepositions have hyphens.
    """

    expressions = (
        *without(EnRuExpressions.expressions, 'rep_hyphen_between_short_words'),
        'rep_positional_spaces_after_long_prepositions',
        'rep_hyphen_between_short_words',  # From EnRuExpressions
        'rep_positional_spaces_before_particles',
        'rep_positional_spaces_for_verbose_prepositions',
        'rep_custom_replacements',
    )

    def expr_rep_positional_spaces_after_long_prepositions(self):
        """
        Replaces whitespaces after and before certain words with non-breakable space.
        """
        expressions = []
        for word in RU_LONG_PREPOSITIONS:
            expressions.append((fr'(^{word}|\s{word}){WHSP}+', fr'\1{NBSP}'))
        return expressions

    def expr_rep_positional_spaces_before_particles(self):
        """Replaces whitespaces before particles with non-breakable space."""
        before_particles = [(fr'\s({word}\W)', fr'{NBSP}\1') for word in RU_PARTICLES]
        # Remove effect of `expr_pairs` for short particles
        short_particles = [word for word in RU_PARTICLES if len(word) < 3]
        after_short_particles = [
            (fr'(\W{word}){NBSP}+', fr'\1{WHSP}') for word in short_particles
        ]

        return [*before_particles, *after_short_particles]

    def expr_rep_positional_spaces_for_verbose_prepositions(self):
        """Replaces whitespaces in and after verbose prepositions
        with non-breakable spaces."""
        flags = re.M | re.S  # Skip re.I
        expressions = []
        for preposition_words in map(str.split, RU_VERBOSE_PREPOSITIONS):
            re_any_spaces_between_words = fr'{ANYSP}'.join(preposition_words)
            non_breaking_spaces_between_words = NBSP.join(preposition_words)

            exp_at_the_middle_of_sentence = (
                fr'(\s){re_any_spaces_between_words}\s',
                fr'\1{non_breaking_spaces_between_words}{NBSP}',
                flags,
            )
            expressions.append(exp_at_the_middle_of_sentence)
            exp_at_the_beginning_of_sentence = (
                fr'(^|\s){re_any_spaces_between_words.capitalize()}\s',
                fr'\1{non_breaking_spaces_between_words.capitalize()}{NBSP}',
                flags,
            )
            expressions.append(exp_at_the_beginning_of_sentence)

        return expressions

    def expr_rep_custom_replacements(self):
        """Replaces custom cases."""
        expressions = [
            (fr'\b{before}\b', fr'{after}') for before, after in RU_CUSTOM_REPLACEMENTS
        ]
        return expressions
