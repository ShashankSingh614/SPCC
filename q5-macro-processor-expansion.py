# Single Pass Macro Processor - Display Macro Expansion with Predefined Tables

def initialize_predefined_tables():
    # Predefined Macro Name Table (MNT)
    mnt = {
        'ADD': {'index': 0, 'num_args': 2},
        'INCR': {'index': 3, 'num_args': 1},
        'PRINT': {'index': 5, 'num_args': 1}
    }
    
    # Predefined Macro Definition Table (MDT)
    mdt = [
        "LOAD &ARG1",        # Index 0 (ADD)
        "ADD &ARG2",         # Index 1
        "STORE &ARG1",       # Index 2
        "LOAD &ARG1",        # Index 3 (INCR)
        "ADD ONE",           # Index 4
        "PRINT &ARG1"        # Index 5 (PRINT)
    ]
    
    return mnt, mdt

def expand_macros(macro_code):
    lines = macro_code.strip().split('\n')
    expanded_code = []
    
    # Initialize predefined tables
    mnt, mdt = initialize_predefined_tables()
    
    for line in lines:
        parts = line.strip().split()
        if not parts:  # Skip empty lines
            expanded_code.append("")
            continue
            
        # Check if the line calls a macro
        if parts[0] in mnt:
            macro_name = parts[0]
            macro_args = [arg.strip(',') for arg in parts[1:]]
            
            # Check if correct number of arguments is provided
            expected_args = mnt[macro_name]['num_args']
            if len(macro_args) != expected_args:
                expanded_code.append(f"ERROR: Macro {macro_name} expects {expected_args} args, but {len(macro_args)} provided")
                continue
            
            # Get macro definition from MDT
            start_idx = mnt[macro_name]['index']
            end_idx = start_idx + 2  # Assuming each macro has at most 3 lines in this example
            if macro_name == "INCR":  # Special case for INCR which has 2 lines
                end_idx = start_idx + 1
            if macro_name == "PRINT":  # Special case for PRINT which has 1 line
                end_idx = start_idx
            
            # Expand the macro
            expansion = []
            for i in range(start_idx, end_idx + 1):
                if i < len(mdt):
                    expanded_line = mdt[i]
                    
                    # Replace parameters with arguments
                    for j, arg in enumerate(macro_args):
                        expanded_line = expanded_line.replace(f"&ARG{j+1}", arg)
                    
                    expansion.append(f"    {expanded_line}  ; Expanded from {macro_name}")
            
            expanded_code.extend(expansion)
        else:
            # Non-macro line remains the same
            expanded_code.append(line)
    
    return expanded_code, mnt, mdt

def display_results(expanded_code, mnt, mdt):
    print("\nPredefined Macro Name Table (MNT):")
    print("-" * 50)
    print("Macro Name\tMDT Index\tNumber of Args")
    print("-" * 50)
    for name, details in mnt.items():
        print(f"{name}\t\t{details['index']}\t\t{details['num_args']}")
    
    print("\nPredefined Macro Definition Table (MDT):")
    print("-" * 50)
    print("Index\tDefinition")
    print("-" * 50)
    for i, definition in enumerate(mdt):
        print(f"{i}\t{definition}")
    
    print("\nMacro Expansion:")
    print("-" * 50)
    for line in expanded_code:
        print(line)

def main():
    print("Single Pass Macro Processor - Macro Expansion with Predefined Tables")
    print("Enter your code with macro calls (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    macro_code = '\n'.join(code_lines)
    expanded_code, mnt, mdt = expand_macros(macro_code)
    display_results(expanded_code, mnt, mdt)

if __name__ == "__main__":
    main()
