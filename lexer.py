import re;
from tokens import tokens_compiled, Token

class Lexer:
    def __init__(self,text):
        self.text = text
    
    def tokenize(self):
        tokens = []
        for line_number, line in enumerate(self.text.splitlines(),start=1):
            line_pos = 0
            while line_pos < len(line):
                for name, pattern in tokens_compiled.items():
                    match = pattern.match(line,line_pos)
                    if match:
                        value = match.group(0)
                        if name not in ['COMMENT', 'WHITESPACE']:
                            tokens.append(Token(name, value, line_number, line_pos))
                        line_pos += len(value)
                        break
                else:
                    raise ValueError(f"Línea {line_number}: Carácter inesperado '{line[line_pos]}'")
        return tokens
    
if __name__ == '__main__':
    code = 'recipe (quantity ++ 1 == 2)\ncook_while (x ** 2 > 0)'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(tokens)