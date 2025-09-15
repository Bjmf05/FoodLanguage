import re;
from tokens import tokens_compiled, Token

class Lexer:
    def __init__(self,text):
        self.text = text
    
    def tokenize(self):
        tokens = []
        in_comment = False
        for line_number, line in enumerate(self.text.splitlines(),start=1):
            line_pos = 0
            while line_pos < len(line):
                for name, pattern in tokens_compiled.items():
                    match = pattern.match(line,line_pos)
                    if match:
                        value = match.group(0)
                        if name == 'COMMENT_START':
                            in_comment = True
                        elif name == 'COMMENT_END':
                            in_comment = False
                        elif not in_comment and name != 'WHITESPACE':
                            tokens.append(Token(name, value, line_number, line_pos))
                        line_pos += len(value)
                        break
                else:
                    raise ValueError(f"Unexpected character '{line[line_pos]}' on the line {line_number}")
        return tokens
    
if __name__ == '__main__':
    code = 'recipe (quantity ++ 1 == 2)\ncook_while (x ** 2 > 0)'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(tokens)