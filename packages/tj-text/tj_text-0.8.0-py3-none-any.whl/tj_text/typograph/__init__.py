from .core import TypusCore
from .mixins import EnQuotes, EnRuExpressions, RuExpressions, RuQuotes
from .processors import EscapeHtml, EscapePhrases, Expressions

__all__ = ('en_typus', 'ru_typus')


class EnTypus(EnQuotes, EnRuExpressions, TypusCore):
    processors = (EscapePhrases, EscapeHtml, Expressions)


class RuTypus(RuQuotes, RuExpressions, TypusCore):
    processors = (EscapePhrases, EscapeHtml, Expressions)


en_typus, ru_typus = EnTypus(), RuTypus()
