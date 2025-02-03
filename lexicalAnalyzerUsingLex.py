import ply.lex as lex

tokens = (
    'KEYWORD', 
    'IDENTIFIER', 
    'NUMBER',  
    'OPERATOR',  
    'SPECIAL', 
)

keywords = {
    'int', 'float', 'if', 'else', 'while', 'return', 'for'
}

t_KEYWORD = r'\b(int|float|if|else|while|return|for)\b' 
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*' 
t_NUMBER = r'\d+(\.\d*)?'  
t_OPERATOR = r'[\+\-\*/]' 
t_SPECIAL = r'[;=,()\[\]{}]'
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def display_tokens(data):
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'KEYWORD':
            print(f"Keyword: {token.value}")
        elif token.type == 'IDENTIFIER':
            print(f"Identifier: {token.value}")
        elif token.type == 'NUMBER':
            print(f"Number: {token.value}")
        elif token.type == 'OPERATOR':
            print(f"Operator: {token.value}")
        elif token.type == 'SPECIAL':
            print(f"Special Character: {token.value}")
        else:
            print(f"Other: {token.value}")

def number_tokens(data):
    lexer.input(data)
    keyword, identifier, number, operator, specialSymbol, other = 0,0,0,0,0,0
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == 'KEYWORD':
            keyword = keyword + 1
        elif token.type == 'IDENTIFIER':
            identifier = identifier + 1
        elif token.type == 'NUMBER':
            number = number + 1
        elif token.type == 'OPERATOR':
            operator = operator + 1
        elif token.type == 'SPECIAL':
            specialSymbol = specialSymbol + 1
        else:
            other = other + 1
    
    print(f'''
No. of Keywords : {keyword}
No. of Identifier : {identifier}
No. of Number : {number}
No. of Operator : {operator}
No. of Special Symbols : {specialSymbol}
          ''')
print(f'''Input Statement : int a = b + c * d;
       int e = 10 / f;\n''')
input_statement = """int a = b + c * d;
int e = 10 / f ;"""

display_tokens(input_statement)
number_tokens(input_statement)
