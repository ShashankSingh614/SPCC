# Two-Pass Assembler - Display MOT and POT contents

def parse_assembly_code(assembly_code):
    # Machine Operation Table (MOT)
    machine_op_table = {
        'ADD': {'opcode': '01', 'format': 2, 'type': 'Arithmetic'},
        'SUB': {'opcode': '02', 'format': 2, 'type': 'Arithmetic'},
        'MUL': {'opcode': '03', 'format': 2, 'type': 'Arithmetic'},
        'DIV': {'opcode': '04', 'format': 2, 'type': 'Arithmetic'},
        'LOAD': {'opcode': '05', 'format': 2, 'type': 'Data Transfer'},
        'STORE': {'opcode': '06', 'format': 2, 'type': 'Data Transfer'},
        'JMP': {'opcode': '07', 'format': 2, 'type': 'Control Transfer'},
        'JNZ': {'opcode': '08', 'format': 2, 'type': 'Control Transfer'},
        'HALT': {'opcode': '09', 'format': 1, 'type': 'Control'}
    }
    
    # Pseudo Operation Table (POT)
    pseudo_op_table = {
        'START': {'format': 'START [address]', 'effect': 'Set program start address'},
        'END': {'format': 'END', 'effect': 'End of program'},
        'DATA': {'format': 'DATA value', 'effect': 'Define data constant'},
        'SECTION': {'format': 'SECTION name', 'effect': 'Define a new section'}
    }
    
    # Scan assembly code to identify used MOT and POT items
    lines = assembly_code.strip().split('\n')
    used_mot = set()
    used_pot = set()
    
    for line in lines:
        parts = line.strip().split()
        if not parts:  # Skip empty lines
            continue
            
        # Check if first token is in MOT or POT
        if parts[0] in machine_op_table:
            used_mot.add(parts[0])
        elif parts[0] in pseudo_op_table:
            used_pot.add(parts[0])
        
        # If first token is a label, check second token
        elif len(parts) > 1:
            if parts[1] in machine_op_table:
                used_mot.add(parts[1])
            elif parts[1] in pseudo_op_table:
                used_pot.add(parts[1])
    
    return used_mot, used_pot, machine_op_table, pseudo_op_table

def display_tables(used_mot, used_pot, mot, pot):
    print("\nMachine Operation Table (MOT) Contents:")
    print("-" * 60)
    print("Mnemonic\tOpcode\tFormat\tType")
    print("-" * 60)
    for op in used_mot:
        details = mot[op]
        print(f"{op}\t\t{details['opcode']}\t{details['format']}\t{details['type']}")
    
    print("\nPseudo Operation Table (POT) Contents:")
    print("-" * 70)
    print("Directive\tFormat\t\t\tEffect")
    print("-" * 70)
    for op in used_pot:
        details = pot[op]
        print(f"{op}\t\t{details['format']}\t\t{details['effect']}")

def main():
    print("Two-Pass Assembler - MOT and POT Contents")
    print("Enter your assembly code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    assembly_code = '\n'.join(code_lines)
    used_mot, used_pot, mot, pot = parse_assembly_code(assembly_code)
    display_tables(used_mot, used_pot, mot, pot)

if __name__ == "__main__":
    main()
