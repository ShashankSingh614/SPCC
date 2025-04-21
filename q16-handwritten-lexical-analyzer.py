def lexical_analyzer(input_code):
    """
    A handwritten lexical analyzer that identifies identifiers, symbols,
    and removes comments from the input code.
    """
    # Initialize output lists
    identifiers = []
    symbols = []
    code_without_comments = []
    
    # Process the input line by line
    in_multi_line_comment = False
    i = 0
    
    while i < len(input_code):
        # Check for single-line comment
        if input_code[i:i+2] == '//' and not in_multi_line_comment:
            # Skip to the end of the line
            while i < len(input_code) and input_code[i] != '\n':
                i += 1
        
        # Check for multi-line comment start
        elif input_code[i:i+2] == '/*' and not in_multi_line_comment:
            in_multi_line_comment = True
            i += 2
        
        # Check for multi-line comment end
        elif input_code[i:i+2] == '*/' and in_multi_line_comment:
            in_multi_line_comment = False
            i += 2
        
        # Process code outside comments
        elif not in_multi_line_comment:
            # Check for identifiers (starting with letter or underscore)
            if input_code[i].isalpha() or input_code[i] == '_':
                identifier = input_code[i]
                i += 1
                # Continue collecting the identifier
                while i < len(input_code) and (input_code[i].isalnum() or input_code[i] == '_'):
                    identifier += input_code[i]
                    i += 1
                
                # Check if it's a keyword or not
                keywords = ['if', 'else', 'while', 'for', 'int', 'float', 'char', 'return', 'void']
                if identifier not in keywords and identifier not in identifiers:
                    identifiers.append(identifier)
                
                # Add to code without comments
                code_without_comments.append(identifier)
                continue  # Skip the increment at the end of the loop
            
            # Check for symbols
            elif input_code[i] in '+-*/=<>!&|()[]{};:,':
                # Handle multi-character operators
                if i + 1 < len(input_code):
                    double_op = input_code[i:i+2]
                    if double_op in ['==', '!=', '<=', '>=', '&&', '||', '++', '--']:
                        if double_op not in symbols:
                            symbols.append(double_op)
                        code_without_comments.append(double_op)
                        i += 2
                        continue
                
                # Single character symbol
                symbol = input_code[i]
                if symbol not in symbols:
                    symbols.append(symbol)
                code_without_comments.append(symbol)
            
            # Add any other characters (like spaces, newlines)
            else:
                code_without_comments.append(input_code[i])
            
            i += 1
        else:
            # Inside a multi-line comment, just skip
            i += 1
    
    # Combine the code_without_comments list into a string
    clean_code = ''.join(code_without_comments)
    
    return {
        'identifiers': identifiers,
        'symbols': symbols,
        'code_without_comments': clean_code
    }

def main():
    print("Handwritten Lexical Analyzer")
    print("Enter your code below. Enter 'EXIT' on a new line to finish input.")
    print("Example: int main() { /* This is a comment */ int x = 10; return 0; }")
    
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
        
        result = lexical_analyzer(input_code)
        
        print("\nIdentifiers found:")
        for ident in result['identifiers']:
            print(f"- {ident}")
        
        print("\nSymbols found:")
        for symbol in result['symbols']:
            print(f"- {symbol}")
        
        print("\nCode without comments:")
        print("-" * 40)
        print(result['code_without_comments'])
        print("-" * 40)
        
        choice = input("\nAnalyze another code? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main()
