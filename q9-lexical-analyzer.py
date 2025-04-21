# Handwritten Lexical Analyzer - Display Keywords, Identifiers, Symbols

def lexical_analyzer(source_code):
    # Define token types
    KEYWORDS = [
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 
        'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 
        'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 
        'volatile', 'while'
    ]
    
    SYMBOLS = '{}[]()+-*/=<>!&|;,.:%^#"\'?\\~'
    
    # Initialize token lists
    keywords = []
    identifiers = []
    symbols = []
    
    # Tokenize the input
    i = 0
    while i < len(source_code):
        char = source_code[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
        
        # Process identifiers and keywords
        if char.isalpha() or char == '_':
            token = char
            i += 1
            
            # Continue reading until end of identifier
            while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == '_'):
                token += source_code[i]
                i += 1
            
            # Check if it's a keyword or identifier
            if token in KEYWORDS:
                keywords.append(token)
            else:
                identifiers.append(token)
            
            continue
        
        # Process symbols
        if char in SYMBOLS:
            # Handle multi-character symbols
            if i + 1 < len(source_code):
                double_char = char + source_code[i+1]
                if double_char in ['==', '!=', '<=', '>=', '++', '--', '&&', '||', '<<', '>>']:
                    symbols.append(double_char)
                    i += 2
                    continue
            
            # Single character symbol
            symbols.append(char)
            i += 1
            continue
        
        # Skip comments
        if char == '/' and i + 1 < len(source_code):
            # Single line comment
            if source_code[i+1] == '/':
                i += 2
                while i < len(source_code) and source_code[i] != '\n':
                    i += 1
                continue
            
            # Multi-line comment
            elif source_code[i+1] == '*':
                i += 2
                while i + 1 < len(source_code) and not (source_code[i] == '*' and source_code[i+1] == '/'):
                    i += 1
                i += 2  # Skip the closing */
                continue
        
        # Skip unrecognized characters
        i += 1
    
    return keywords, identifiers, symbols

def display_tokens(keywords, identifiers, symbols):
    print("\nLexical Analysis Results:")
    print("-" * 50)
    
    print("\nKeywords:")
    print("-" * 20)
    for i, keyword in enumerate(keywords, 1):
        print(f"{i}. {keyword}")
    
    print("\nIdentifiers:")
    print("-" * 20)
    for i, identifier in enumerate(identifiers, 1):
        print(f"{i}. {identifier}")
    
    print("\nSymbols:")
    print("-" * 20)
    for i, symbol in enumerate(symbols, 1):
        print(f"{i}. {symbol}")

def main():
    print("Handwritten Lexical Analyzer - Keywords, Identifiers, Symbols")
    print("Enter your source code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    source_code = '\n'.join(code_lines)
    keywords, identifiers, symbols = lexical_analyzer(source_code)
    display_tokens(keywords, identifiers, symbols)

if __name__ == "__main__":
    main()
