def two_pass_assembler(assembly_code):
    """
    Implement a simple two-pass assembler for a subset of assembly language
    Generates symbol table and literal table
    """
    # Initialize tables
    symbol_table = {}  # {symbol: address}
    literal_table = {}  # {literal: address}
    
    # Define op codes for a subset of instructions
    op_codes = {
        'ADD': '01',
        'SUB': '02',
        'MUL': '03',
        'DIV': '04',
        'MOV': '05',
        'LOAD': '06',
        'STORE': '07',
        'JMP': '08',
        'JZ': '09',
        'JNZ': '10',
        'HALT': '11'
    }
    
    # Define pseudo-operations
    pseudo_ops = ['START', 'END', 'DC', 'DS']
    
    # Split the assembly code into lines and remove comments
    lines = []
    for line in assembly_code.strip().split('\n'):
        # Remove comments (anything after semicolon)
        cleaned_line = line.split(';')[0].strip()
        if cleaned_line:  # Skip empty lines
            lines.append(cleaned_line)
    
    # First pass: Build the symbol table
    location_counter = 0
    start_address = 0
    
    for line in lines:
        # Parse the line into components: [label] operation operand1, operand2
        parts = line.split()
        
        # Check if line starts with a label
        if parts and parts[0] not in op_codes and parts[0] not in pseudo_ops:
            label = parts[0]
            if ':' in label:
                label = label.rstrip(':')
                parts = parts[1:]  # Remove label from parts
            
            # Add label to symbol table
            if label not in symbol_table:
                symbol_table[label] = location_counter
        
        # If no label or after processing the label
        if parts:
            operation = parts[0] if parts else ''
            
            # Handle pseudo-operations
            if operation == 'START':
                if len(parts) > 1:
                    start_address = int(parts[1], 16)
                    location_counter = start_address
                continue
            elif operation == 'END':
                break
            elif operation == 'DC':
                # Define constant - allocate space for a value
                location_counter += 1
            elif operation == 'DS':
                # Define storage - allocate specified number of words
                if len(parts) > 1:
                    location_counter += int(parts[1])
                else:
                    location_counter += 1
            else:
                # Regular instruction - each takes 1 memory word in this simple model
                location_counter += 1
                
                # Identify literals (constants prefixed with '=')
                for operand in parts[1:]:
                    if operand.startswith('='):
                        literal = operand
                        if literal not in literal_table:
                            literal_table[literal] = None  # Address will be assigned in second pass
    
    # Assign addresses to literals (at the end of the program)
    for literal in literal_table:
        literal_table[literal] = location_counter
        location_counter += 1
    
    # Second pass: Generate the object code (simplified for this assignment)
    # We're focusing on symbol and literal table generation as per the requirement
    
    return {
        'symbol_table': symbol_table,
        'literal_table': literal_table
    }

def display_tables(symbol_table, literal_table):
    """Display the symbol table and literal table"""
    print("\nSymbol Table:")
    print("-" * 30)
    print("| {:<15} | {:<10} |".format("Symbol", "Address"))
    print("-" * 30)
    
    for symbol, address in symbol_table.items():
        print("| {:<15} | {:<10X} |".format(symbol, address))
    
    print("-" * 30)
    
    if literal_table:
        print("\nLiteral Table:")
        print("-" * 30)
        print("| {:<15} | {:<10} |".format("Literal", "Address"))
        print("-" * 30)
        
        for literal, address in literal_table.items():
            print("| {:<15} | {:<10X} |".format(literal, address))
        
        print("-" * 30)

def main():
    print("Two-Pass Assembler")
    print("Enter your assembly code below. Enter 'EXIT' on a new line to finish input.")
    print("Example assembly code format:")
    print("START 100")
    print("LABEL: ADD A, B")
    print("MOV X, =5")
    print("END")
    
    while True:
        print("\nEnter your assembly code (or type 'EXIT' to quit):")
        
        lines = []
        while True:
            line = input()
            if line == "EXIT":
                if not lines:  # If EXIT is the first input, quit the program
                    return
                break
            lines.append(line)
        
        assembly_code = "\n".join(lines)
        
        result = two_pass_assembler(assembly_code)
        
        display_tables(result['symbol_table'], result['literal_table'])
        
        choice = input("\nProcess another assembly code? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main()
