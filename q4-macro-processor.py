# Single Macro Processor - Display MNT, MDT, and ALA

def process_macro_code(macro_code):
    lines = macro_code.strip().split('\n')
    
    # Initialize tables
    macro_name_table = {}  # Format: {macro_name: {index_in_mdt, num_args}}
    macro_def_table = []    # List of all macro definition lines
    arg_list_array = {}     # Format: {macro_name: [arg1, arg2, ...]}
    
    in_macro = False
    current_macro = None
    macro_start_index = 0
    
    for i, line in enumerate(lines):
        parts = line.strip().split()
        if not parts:  # Skip empty lines
            continue
            
        # Check for MACRO directive
        if parts[0] == 'MACRO':
            in_macro = True
            if len(parts) > 1:
                current_macro = parts[1]
                macro_start_index = len(macro_def_table)
                
                # Extract arguments
                if len(parts) > 2:
                    # Get arguments (stripping commas)
                    args = [arg.strip(',') for arg in parts[2:]]
                else:
                    args = []
                    
                # Update tables
                macro_name_table[current_macro] = {
                    'index': macro_start_index,
                    'num_args': len(args)
                }
                arg_list_array[current_macro] = args
            continue
        
        # Check for MEND directive
        if in_macro and parts[0] == 'MEND':
            in_macro = False
            current_macro = None
            continue
        
        # Add line to macro definition table if inside a macro
        if in_macro:
            macro_def_table.append(line.strip())
    
    return macro_name_table, macro_def_table, arg_list_array

def display_tables(mnt, mdt, ala):
    print("\nMacro Name Table (MNT):")
    print("-" * 50)
    print("Macro Name\tMDT Index\tNumber of Args")
    print("-" * 50)
    for name, details in mnt.items():
        print(f"{name}\t\t{details['index']}\t\t{details['num_args']}")
    
    print("\nMacro Definition Table (MDT):")
    print("-" * 50)
    print("Index\tDefinition")
    print("-" * 50)
    for i, definition in enumerate(mdt):
        print(f"{i}\t{definition}")
    
    print("\nArgument List Array (ALA):")
    print("-" * 50)
    print("Macro Name\tArguments")
    print("-" * 50)
    for name, args in ala.items():
        print(f"{name}\t\t{', '.join(args)}")

def main():
    print("Single Macro Processor - MNT, MDT, and ALA")
    print("Enter your macro code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    macro_code = '\n'.join(code_lines)
    mnt, mdt, ala = process_macro_code(macro_code)
    display_tables(mnt, mdt, ala)

if __name__ == "__main__":
    main()
