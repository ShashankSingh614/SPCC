# Code Optimization - Algebraic Simplification and Common Subexpression Elimination

def parse_code(code):
    lines = code.strip().split('\n')
    statements = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('//'):  # Skip empty lines and comments
            statements.append(line)
    
    return statements

def algebraic_simplification(statements):
    optimized = []
    
    for stmt in statements:
        # Skip statements without assignment
        if '=' not in stmt:
            optimized.append(stmt)
            continue
        
        lhs, rhs = stmt.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        # Rule 1: X + 0 = X, X - 0 = X
        rhs = rhs.replace(' + 0', '').replace(' - 0', '')
        
        # Rule 2: X * 1 = X, X / 1 = X
        rhs = rhs.replace(' * 1', '').replace(' / 1', '')
        
        # Rule 3: X * 0 = 0
        if ' * 0' in rhs or '0 * ' in rhs:
            if '+' not in rhs and '-' not in rhs and '/' not in rhs:
                rhs = '0'
        
        # Rule 4: X + X = 2 * X, X - X = 0
        parts = rhs.split(' + ')
        if len(parts) == 2 and parts[0] == parts[1]:
            rhs = f"2 * {parts[0]}"
        
        parts = rhs.split(' - ')
        if len(parts) == 2 and parts[0] == parts[1]:
            rhs = '0'
        
        # Rule 5: X / X = 1 (if X != 0)
        parts = rhs.split(' / ')
        if len(parts) == 2 and parts[0] == parts[1]:
            rhs = f"1  // Assuming {parts[0]} != 0"
        
        optimized.append(f"{lhs} = {rhs}")
    
    return optimized

def common_subexpression_elimination(statements):
    optimized = []
    expr_vars = {}  # Maps expressions to variables that hold their value
    
    for stmt in statements:
        # Skip statements without assignment
        if '=' not in stmt:
            optimized.append(stmt)
            continue
        
        lhs, rhs = stmt.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        # Check if this expression has been calculated before
        if rhs in expr_vars:
            optimized.append(f"{lhs} = {expr_vars[rhs]}  // Common subexpression")
        else:
            # This is a new expression, add it normally
            optimized.append(stmt)
            expr_vars[rhs] = lhs
    
    return optimized

def display_optimization(original, after_algebraic, after_cse):
    print("\nOriginal Code:")
    print("-" * 50)
    for stmt in original:
        print(stmt)
    
    print("\nAfter Algebraic Simplification:")
    print("-" * 50)
    for stmt in after_algebraic:
        print(stmt)
    
    print("\nAfter Common Subexpression Elimination:")
    print("-" * 50)
    for stmt in after_cse:
        print(stmt)

def main():
    print("Code Optimization - Algebraic Simplification and Common Subexpression Elimination")
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
    algebraic_result = algebraic_simplification(statements)
    cse_result = common_subexpression_elimination(algebraic_result)
    
    # Display results
    display_optimization(statements, algebraic_result, cse_result)

if __name__ == "__main__":
    main()
