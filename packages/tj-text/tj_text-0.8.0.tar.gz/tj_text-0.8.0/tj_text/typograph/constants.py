from .chars import NBHYPHEN

RU_LONG_PREPOSITIONS = (
    'без',
    'перед',
    'при',
    'через',
    'над',
    'под',
    'про',
    'для',
    'около',
    'среди',
    'из-под',
    'из-за',
    'по-над',
)
RU_VERBOSE_PREPOSITIONS = ('несмотря на', 'в отличие от', 'в связи с')
RU_PARTICLES = ('же', 'ли', 'бы', 'б', 'уж')
RU_CUSTOM_REPLACEMENTS = (('когда-нибудь', f'когда{NBHYPHEN}нибудь'),)

CURRENCY_SYMBOLS = [
    '₽',
    '$',
    '€',
    '£',
    '₴',
    '¥',
    '₪',
    '₨',
    '₩',
    '₦',
    '฿',
    '₫',
    '₭',
    '៛',
    '₮',
    '₱',
    '₡',
    '₲',
    '₸',
    '₺',
    '₼',
    '₾',
    '¢',
    '₿',
    '﷼',
    'Ξ',
    'Ł',
]

CURRENCY_SYMBOLS_USED_IN_FORMULAS = ['Ξ', 'Ł']

# move polish zloty in standalone constant, because it uses two symbols for
# currency describing
POLISH_ZLOTY = 'Zł'
