# Two-Pass Assembler - Generate Base Table and Location Counter

def two_pass_assembler(assembly_code):
    lines = assembly_code.strip().split('\n')
    base_table = {}  # Format: {section_name: base_address}
    location_counter_log = []  # Track LC values for each instruction
    current_section = None
    location_counter = 0
    
    # Define opcodes and their sizes
    opcodes = {
        'ADD': 1, 'SUB': 1, 'MUL': 1, 'DIV': 1,
        'LOAD': 1, 'STORE': 1, 'JMP': 1, 'JNZ': 1,
        'HALT': 1, 'DATA': 1, 'START': 0, 'END': 0
    }
    
    # Add section handling directives
    directives = {
        'SECTION': 0, 'START': 0, 'END': 0
    }
    
    for line in lines:
        parts = line.strip().split()
        if not parts:  # Skip empty lines
            continue
        
        # Log current instruction with its LC
        location_counter_log.append((line.strip(), location_counter))
        
        # Check for START directive
        if parts[0] == 'START':
            if len(parts) > 1:
                location_counter = int(parts[1])
            continue
        
        # Check for SECTION directive
        if parts[0] == 'SECTION':
            if len(parts) > 1:
                current_section = parts[1]
                base_table[current_section] = location_counter
            continue
        
        # Handle labels (skip them for location counter calculation)
        if parts[0] not in opcodes and parts[0] not in directives:
            parts = parts[1:]  # Remove label
        
        # Check for END directive
        if parts and parts[0] == 'END':
            break
        
        # Increment location counter for instructions
        if parts and parts[0] in opcodes:
            location_counter += opcodes[parts[0]]
    
    return base_table, location_counter_log

def display_results(base_table, location_counter_log):
    print("\nBase Table:")
    print("-" * 30)
    print("Section\t\tBase Address")
    print("-" * 30)
    for section, address in base_table.items():
        print(f"{section}\t\t{address}")
    
    print("\nLocation Counter Log:")
    print("-" * 40)
    print("Instruction\t\tLocation Counter")
    print("-" * 40)
    for instruction, lc in location_counter_log:
        print(f"{instruction}\t\t{lc}")

def main():
    print("Two-Pass Assembler - Base Table and Location Counter")
    print("Enter your assembly code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    assembly_code = '\n'.join(code_lines)
    base_table, location_counter_log = two_pass_assembler(assembly_code)
    display_results(base_table, location_counter_log)

if __name__ == "__main__":
    main()
