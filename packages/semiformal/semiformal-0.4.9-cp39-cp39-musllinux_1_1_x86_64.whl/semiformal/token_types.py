import enum

class TokenType(enum.Enum):
    END = 0
    WORD = 1
    ABBREVIATION = 2
    IDEOGRAPHIC_CHAR = 3
    HANGUL_SYLLABLE = 4
    ACRONYM = 5
    PHRASE = 10
    EMAIL = 20
    URL = 21
    US_PHONE = 22
    INTL_PHONE = 23
    NUMERIC = 50
    ORDINAL = 51
    ROMAN_NUMERAL = 52
    IDEOGRAPHIC_NUMBER = 53
    PERIOD = 100
    EXCLAMATION = 101
    QUESTION_MARK = 102
    COMMA = 103
    COLON = 104
    SEMICOLON = 105
    PLUS = 106
    AMPERSAND = 107
    AT_SIGN = 108
    POUND = 109
    ELLIPSIS = 110
    DASH = 111
    BREAKING_DASH = 112
    HYPHEN = 113
    PUNCT_OPEN = 114
    PUNCT_CLOSE = 115
    DOUBLE_QUOTE = 119
    SINGLE_QUOTE = 120
    OPEN_QUOTE = 121
    CLOSE_QUOTE = 122
    SLASH = 124
    BACKSLASH = 125
    GREATER_THAN = 126
    LESS_THAN = 127
    OTHER = 200
    WHITESPACE = 300
    NEWLINE = 301
    INVALID_CHAR = 500

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
