# Single Pass Macro Processor - Identify Macros and Perform Expansion

def process_macros(macro_code):
    lines = macro_code.strip().split('\n')
    
    # Initialize tables
    mnt = {}  # Macro Name Table: {macro_name: {index_in_mdt, num_args}}
    mdt = []  # Macro Definition Table: List of all macro definition lines
    ala = {}  # Argument List Array: {macro_name: [arg1, arg2, ...]}
    
    # Output code after macro processing
    expanded_code = []
    
    # First pass: Identify macros
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        parts = line.split()
        
        if not parts:  # Skip empty lines
            i += 1
            continue
        
        # Check for MACRO directive
        if parts[0] == 'MACRO':
            # Extract macro name and arguments
            if len(parts) > 1:
                macro_name = parts[1]
                args = [arg.strip(',') for arg in parts[2:]] if len(parts) > 2 else []
                
                # Add to MNT and ALA
                mnt[macro_name] = {'index': len(mdt), 'num_args': len(args)}
                ala[macro_name] = args
                
                # Collect macro body until MEND
                j = i + 1
                while j < len(lines) and 'MEND' not in lines[j].strip().split():
                    mdt.append(lines[j].strip())
                    j += 1
                
                # Skip the processed lines
                i = j + 1  # Skip MEND line as well
            else:
                i += 1
        else:
            # Check if this line is a macro call
            if parts[0] in mnt:
                macro_name = parts[0]
                call_args = [arg.strip(',') for arg in parts[1:]]
                
                # Get macro definition
                start_idx = mnt[macro_name]['index']
                macro_lines = []
                for k in range(start_idx, len(mdt)):
                    if 'MEND' in mdt[k]:
                        break
                    macro_line = mdt[k]
                    
                    # Replace formal parameters with actual arguments
                    for idx, formal_param in enumerate(ala[macro_name]):
                        if idx < len(call_args):
                            macro_line = macro_line.replace(f"&{formal_param}", call_args[idx])
                    
                    macro_lines.append(f"    {macro_line}  ; Expanded from {macro_name}")
                
                expanded_code.extend(macro_lines)
            else:
                # Not a macro definition or call
                expanded_code.append(line)
            
            i += 1
    
    # Filter out macro definitions from expanded code
    final_expanded_code = []
    in_macro_def = False
    for line in expanded_code:
        if 'MACRO' in line.split():
            in_macro_def = True
            continue
        if 'MEND' in line.split():
            in_macro_def = False
            continue
        if not in_macro_def:
            final_expanded_code.append(line)
    
    return mnt, mdt, final_expanded_code

def display_results(mnt, mdt, expanded_code):
    print("\nIdentified Macros (MNT):")
    print("-" * 50)
    print("Macro Name\tMDT Index\tNumber of Args")
    print("-" * 50)
    for name, details in mnt.items():
        print(f"{name}\t\t{details['index']}\t\t{details['num_args']}")
    
    print("\nMacro Definitions (MDT):")
    print("-" * 50)
    print("Index\tDefinition")
    print("-" * 50)
    for i, definition in enumerate(mdt):
        print(f"{i}\t{definition}")
    
    print("\nExpanded Code:")
    print("-" * 50)
    for line in expanded_code:
        print(line)

def main():
    print("Single Pass Macro Processor - Identify and Expand Macros")
    print("Enter your code with macro definitions and calls (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    macro_code = '\n'.join(code_lines)
    mnt, mdt, expanded_code = process_macros(macro_code)
    display_results(mnt, mdt, expanded_code)

if __name__ == "__main__":
    main()
