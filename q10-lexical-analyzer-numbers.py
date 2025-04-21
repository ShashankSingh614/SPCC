# Handwritten Lexical Analyzer - Display Numbers, Identifiers, Preprocessor Directives

def lexical_analyzer(source_code):
    # Initialize token lists
    numbers = []
    identifiers = []
    preprocessors = []
    
    # Process the source code line by line
    lines = source_code.split('\n')
    for line in lines:
        line = line.strip()
        
        # Check for preprocessor directives
        if line.startswith('#'):
            # Extract the entire preprocessor directive
            preprocessors.append(line)
            continue
        
        # Tokenize the line
        i = 0
        while i < len(line):
            char = line[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Process identifiers
            if char.isalpha() or char == '_':
                token = char
                i += 1
                
                # Continue reading until end of identifier
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    token += line[i]
                    i += 1
                
                identifiers.append(token)
                continue
            
            # Process numbers (integer or float)
            if char.isdigit() or (char == '.' and i + 1 < len(line) and line[i+1].isdigit()):
                token = char
                i += 1
                has_decimal = (char == '.')
                
                # Continue reading digits and at most one decimal point
                while i < len(line) and (line[i].isdigit() or (line[i] == '.' and not has_decimal)):
                    if line[i] == '.':
                        has_decimal = True
                    token += line[i]
                    i += 1
                
                # Handle scientific notation (e.g., 1.23e-4)
                if i < len(line) and line[i].lower() == 'e':
                    token += line[i]
                    i += 1
                    
                    # Handle sign after 'e'
                    if i < len(line) and (line[i] == '+' or line[i] == '-'):
                        token += line[i]
                        i += 1
                    
                    # Read exponent digits
                    while i < len(line) and line[i].isdigit():
                        token += line[i]
                        i += 1
                
                numbers.append(token)
                continue
            
            # Skip other characters (symbols, etc.)
            i += 1
    
    # Remove duplicates and sort
    numbers = sorted(list(set(numbers)))
    identifiers = sorted(list(set(identifiers)))
    preprocessors = sorted(list(set(preprocessors)))
    
    return numbers, identifiers, preprocessors

def display_tokens(numbers, identifiers, preprocessors):
    print("\nLexical Analysis Results:")
    print("-" * 50)
    
    print("\nNumbers:")
    print("-" * 20)
    for i, number in enumerate(numbers, 1):
        print(f"{i}. {number}")
    
    print("\nIdentifiers:")
    print("-" * 20)
    for i, identifier in enumerate(identifiers, 1):
        print(f"{i}. {identifier}")
    
    print("\nPreprocessor Directives:")
    print("-" * 20)
    for i, directive in enumerate(preprocessors, 1):
        print(f"{i}. {directive}")

def main():
    print("Handwritten Lexical Analyzer - Numbers, Identifiers, Preprocessor Directives")
    print("Enter your source code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    source_code = '\n'.join(code_lines)
    numbers, identifiers, preprocessors = lexical_analyzer(source_code)
    display_tokens(numbers, identifiers, preprocessors)

if __name__ == "__main__":
    main()
