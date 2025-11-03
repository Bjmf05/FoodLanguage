import re

token_patterns = [
    ('FUNCTION', r'(?i)\b(recipe)\b'),                # function
    ('RETURN', r'(?i)\b(serve)\b'),                  # return
    ('FOR', r'(?i)\b(stir)\b'),                      # for
    ('PRINT', r'(?i)\b(taste)\b'),                   # print
    ('WHILE', r'(?i)\b(cook_while)\b'),              # while
    ('IF', r'(?i)\b(if|if_has)\b'),                  # if
    ('ELSE', r'(?i)\b(otherwise)\b'),                # else
    ('SWITCH', r'(?i)\b(season)\b'),                 # switch
    ('CASE', r'(?i)\b(with)\b'),                     # case
    ('DEFAULT', r'(?i)\b(default_flavor)\b'),        # default
    ('INPUT', r'(?i)\b(add)\b'),                     # input
    ('TRUE', r'(?i)\b(ready)\b'),                    # true
    ('FALSE', r'(?i)\b(raw)\b'),                     # false
    ('NULL', r'(?i)\b(flavorless)\b'),               # null
    ('FLOAT', r'(?i)\b(portion)\b'),                 # float
    ('INT', r'(?i)\b(quantity)\b'),                  # int
    ('STRING', r'(?i)\b(ingredient)\b'),             # string
    ('LIST', r'(?i)\b(menu)\b'),                     # list
    ('BREAK', r'(?i)\b(stop_stirring)\b'),           # break
    ('CONTINUE', r'(?i)\b(keep_stirring)\b'),        # continue
    # Operadores lógicos
    ('NOT', r'(?i)\b(unseasoned)\b'),                # not
    ('AND', r'(?i)\b(spoon)\b'),                     # and
    ('OR', r'(?i)\b(fork)\b'),                       # or
    # Operadores aritméticos y de comparación
    ('PLUS', r'\+\+'),                               # +
    ('MINUS', r'--'),                                # -
    ('EQUAL', r'==='),                               # ===
    ('ASSIGN', r'=='),                               # =                               # ==
    ('MULTIPLY', r'\*\*'),                           # *
    ('DIVIDE', r'\\\\'),                             # \
    ('NOT_EQUAL', r'!='),                           # !=
    ('GREATER_EQUAL', r'>='),      # >=
    ('LESS_EQUAL', r'<='),         # <=
    ('GREATER', r'>'),             # >
    ('LESS', r'<'),                # <
    # Comentarios
    ('COMMENT', r'//.*'),                            # Comentarios de una línea
    # Identificadores, números, cadenas, etc.
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NUMBER', r'[+-]?(\d*\.\d+|\d+\.\d*|\d+)'),
    ('CHAR', r"'.'"),
    ('STRING_LITERAL', r'"[^"]*"|""'),
    # Delimitadores y otros
    ('DELIMETER', r'[(),:{}\[\];]'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.'),
]

tokens_compiled = {name:re.compile(pattern) for name, pattern in token_patterns}

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, Pos({self.line}:{self.column}))"

