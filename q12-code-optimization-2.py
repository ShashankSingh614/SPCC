# Code Optimization - Dead Code Elimination and Constant Propagation

def parse_code(code):
    lines = code.strip().split('\n')
    statements = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('//'):  # Skip empty lines and comments
            statements.append(line)
    
    return statements

def constant_propagation(statements):
    constants = {}  # Maps variable names to their constant values
    optimized = []
    
    for stmt in statements:
        # Skip statements without assignment
        if '=' not in stmt:
            # Replace variables with constants in non-assignment statements
            for var, value in constants.items():
                stmt = stmt.replace(var, str(value))
            optimized.append(stmt)
            continue
        
        lhs, rhs = stmt.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        # Replace variables with constants in the right-hand side
        for var, value in constants.items():
            # Replace the variable with its value, ensuring we don't replace substrings
            parts = rhs.split()
            for i, part in enumerate(parts):
                if part == var:
                    parts[i] = str(value)
            rhs = ' '.join(parts)
        
        # Try to evaluate the right-hand side if it's a constant expression
        try:
            # Only evaluate simple arithmetic expressions without function calls
            if all(c.isdigit() or c.isspace() or c in '+-*/()' for c in rhs):
                value = eval(rhs)
                constants[lhs] = value
                optimized.append(f"{lhs} = {value}  // Constant propagated")
            else:
                optimized.append(f"{lhs} = {rhs}")
        except:
            optimized.append(f"{lhs} = {rhs}")
    
    return optimized, constants

def dead_code_elimination(statements, constants):
    # Identify variables that are used
    used_vars = set()
    
    # First pass: identify all used variables in expressions
    for stmt in statements:
        if '=' in stmt:
            lhs, rhs = stmt.split('=', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            # Variables in the right-hand side are used
            words = rhs.split()
            for word in words:
                # Remove operators and punctuation
                var = ''.join(c for c in word if c.isalnum() or c == '_')
                if var and var not in constants and not var.isdigit():
                    used_vars.add(var)
        else:
            # All variables in statements without assignments are used
            words = stmt.split()
            for word in words:
                var = ''.join(c for c in word if c.isalnum() or c == '_')
                if var and var not in constants and not var.isdigit():
                    used_vars.add(var)
    
    # Second pass: eliminate assignments to unused variables
    optimized = []
    for stmt in statements:
        if '=' in stmt:
            lhs, rhs = stmt.split('=', 1)
            lhs = lhs.strip()
            
            # Keep the statement if the variable is used or if it has side effects
            if lhs in used_vars or 'func(' in rhs or 'print(' in rhs:
                optimized.append(stmt)
            else:
                # Skip this statement (dead code)
                continue
        else:
            # Keep non-assignment statements
            optimized.append(stmt)
    
    return optimized

def display_optimization(original, after_const_prop, after_dead_code):
    print("\nOriginal Code:")
    print("-" * 50)
    for stmt in original:
        print(stmt)
    
    print("\nAfter Constant Propagation:")
    print("-" * 50)
    for stmt in after_const_prop:
        print(stmt)
    
    print("\nAfter Dead Code Elimination:")
    print("-" * 50)
    for stmt in after_dead_code:
        print(stmt)

def main():
    print("Code Optimization - Dead Code Elimination and Constant Propagation")
    print("Enter your code (end with a blank line):")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    code = '\n'.join(code_lines)
    statements = parse_code(code)
    
    # Apply optimizations
    const_prop_result, constants = constant_propagation(statements)
    dead_code_result = dead_code_elimination(const_prop_result, constants)
    
    # Display results
    display_optimization(statements, const_prop_result, dead_code_result)

if __name__ == "__main__":
    main()
