import re

class Lexer:
    def __init__(self, file_path):
        self.tokens = []
        self.file_path = file_path
    
    def tokenize(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                self.tokens.extend(self._tokenize_line(line))
        
        return self.tokens
    
    def _tokenize_line(self, line):
        tokens = []
        
        number_pattern = re.compile(r"\d+")
        operator_pattern = re.compile(r"\+")
        
        for token in line.split():
            if match := number_pattern.match(token):
                number = match.group()
                tokens.append(('NUMBER', int(number)))
            elif match := operator_pattern.match(token):
                operator = match.group()
                tokens.append(('OPERATOR', operator))
            else:
                raise ValueError(f"Invalid character: {token} - Line: {line}")
        
        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()
    
    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None
    
    def parse(self):
        if self.current_token is None:
            raise ValueError("Unexpected end of input")
        
        result = self.parse_number()
        
        while self.current_token:
            if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '+':
                self.next_token()
                result += self.parse_number()
            else:
                raise ValueError(f"Invalid operator: {self.current_token[1]}")
        
        return result
    
    def parse_number(self):
        if self.current_token[0] == 'NUMBER':
            number = self.current_token[1]
            self.next_token()
            return number
        else:
            raise ValueError(f"Invalid token: {self.current_token[1]}")

# Usage example
lexer = Lexer("cool_program.num")  # Replace "cool_program.num" with the path to your file
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
print(result)
