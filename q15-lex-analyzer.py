# Install PLY library if not installed:
# pip install ply

import ply.lex as lex

# List of token names
tokens = (
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'LESSTHAN',
    'GREATERTHAN',
    'STRING',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'

# Regular expression rules with actions
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

# Define a rule for comments (to be ignored)
def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass  # No return value. Token discarded

# Define a rule for newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Characters to ignore (whitespace)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
def build_lexer():
    return lex.lex()

def analyze_code(input_code):
    lexer = build_lexer()
    lexer.input(input_code)
    
    # Collect and display tokens
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno))
    
    return tokens

def display_tokens(tokens):
    print("\nTokens (Type, Value, Line):")
    print("-" * 60)
    print("| {:<15} | {:<25} | {:<8} |".format("Token Type", "Value", "Line"))
    print("-" * 60)
    
    for token_type, value, line in tokens:
        # Truncate value display if too long
        value_str = str(value)
        if len(value_str) > 25:
            value_str = value_str[:22] + "..."
        print("| {:<15} | {:<25} | {:<8} |".format(token_type, value_str, line))
    
    print("-" * 60)

def main():
    print("Automated Lexical Analyzer using PLY (Python Lex-Yacc)")
    print("Enter your code below. Enter 'EXIT' on a new line to finish input.")
    print("Example: int main() { return 0; }")
    
    while True:
        print("\nEnter your code (or type 'EXIT' to quit):")
        
        lines = []
        while True:
            line = input()
            if line == "EXIT":
                if not lines:  # If EXIT is the first input, quit the program
                    return
                break
            lines.append(line)
        
        input_code = "\n".join(lines)
        
        tokens = analyze_code(input_code)
        display_tokens(tokens)
        
        choice = input("\nAnalyze another code? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main()
