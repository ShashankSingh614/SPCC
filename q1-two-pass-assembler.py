# Two-Pass Assembler - Generate Symbol Table and Literal Table

def first_pass(assembly_code):
    lines = assembly_code.strip().split('\n')
    symbol_table = {}
    literal_table = {}
    location_counter = 0
    
    # Define opcodes and their sizes
    opcodes = {
        'ADD': 1, 'SUB': 1, 'MUL': 1, 'DIV': 1,
        'LOAD': 1, 'STORE': 1, 'JMP': 1, 'JNZ': 1,
        'HALT': 1, 'DATA': 1, 'START': 0, 'END': 0
    }
    
    for line in lines:
        parts = line.strip().split()
        if not parts:  # Skip empty lines
            continue
            
        # Check if line starts with START directive
        if parts[0] == 'START':
            if len(parts) > 1:
                location_counter = int(parts[1])
            continue
            
        # Check if line has a label
        if parts[0] not in opcodes:
            symbol = parts[0]
            symbol_table[symbol] = location_counter
            parts = parts[1:]  # Remove label
            
        # Check for END directive
        if parts and parts[0] == 'END':
            break
            
        # Check for literals
        if parts and len(parts) > 1:
            for operand in parts[1:]:
                if operand.startswith('='):  # Literal
                    if operand not in literal_table:
                        literal_table[operand] = None
        
        # Increment location counter if there's an opcode
        if parts and parts[0] in opcodes:
            location_counter += opcodes[parts[0]]
    
    # Assign addresses to literals at the end
    for literal in literal_table:
        literal_table[literal] = location_counter
        location_counter += 1
        
    return symbol_table, literal_table

def display_tables(symbol_table, literal_table):
    print("\nSymbol Table:")
    print("-" * 25)
    print("Symbol\t\tAddress")
    print("-" * 25)
    for symbol, address in symbol_table.items():
        print(f"{symbol}\t\t{address}")
        
    print("\nLiteral Table:")
    print("-" * 25)
    print("Literal\t\tAddress")
    print("-" * 25)
    for literal, address in literal_table.items():
        print(f"{literal}\t\t{address}")

def main():
    print("Two-Pass Assembler - Symbol and Literal Tables")
    print("Enter your assembly code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    assembly_code = '\n'.join(code_lines)
    symbol_table, literal_table = first_pass(assembly_code)
    display_tables(symbol_table, literal_table)

if __name__ == "__main__":
    main()
