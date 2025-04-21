# Intermediate Code Generator - 3-Address Code using Triples

def generate_triples(expression):
    # Initialize data structures
    triples = []  # (op, arg1, arg2)
    variables = {}  # Maps expressions to their temporary variable
    temp_count = 1
    
    # Helper function to get a new temporary variable
    def new_temp():
        nonlocal temp_count
        temp = f"t{temp_count}"
        temp_count += 1
        return temp
    
    # Helper function to parse expressions recursively
    def parse_expression(expr):
        # Remove unnecessary parentheses
        expr = expr.strip()
        if expr.startswith('(') and expr.endswith(')'):
            # Check if these parentheses are necessary
            count = 0
            for i, c in enumerate(expr[1:-1]):
                if c == '(':
                    count += 1
                elif c == ')':
                    count -= 1
                if count < 0:  # Found a closing parenthesis without an opening one
                    break
            else:
                if count == 0:  # All inner parentheses are matched
                    expr = expr[1:-1]
        
        # Check if expression is already computed
        if expr in variables:
            return variables[expr]
        
        # Handle simple operands (variables and constants)
        if expr.isalnum() or expr in ['+', '-', '*', '/', '%']:
            return expr
        
        # Find the operator with lowest precedence
        operators = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
        min_precedence = 99
        op_pos = -1
        count = 0
        
        for i, c in enumerate(expr):
            if c == '(':
                count += 1
            elif c == ')':
                count -= 1
            elif count == 0 and c in operators and operators[c] <= min_precedence:
                min_precedence = operators[c]
                op_pos = i
        
        # If no operator found, it must be a variable or constant
        if op_pos == -1:
            return expr
        
        # Split the expression around the operator
        op = expr[op_pos]
        left = expr[:op_pos].strip()
        right = expr[op_pos+1:].strip()
        
        # Parse the operands recursively
        left_result = parse_expression(left)
        right_result = parse_expression(right)
        
        # Create a triple for this expression
        result = new_temp()
        triples.append((op, left_result, right_result))
        variables[expr] = result
        
        return result
    
    # Process each expression (assumed to be separated by semicolons)
    expressions = expression.split(';')
    results = []
    
    for expr in expressions:
        expr = expr.strip()
        if not expr:
            continue
            
        # Handle assignment
        if '=' in expr:
            lhs, rhs = expr.split('=', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            # Parse the right-hand side
            rhs_result = parse_expression(rhs)
            
            # Create an assignment triple
            triples.append(('=', rhs_result, None))
            results.append(lhs)
        else:
            # Parse a standalone expression
            parse_expression(expr)
            results.append(None)
    
    return triples, results

def display_triples(triples, results):
    print("\nIntermediate Code (Triples):")
    print("-" * 50)
    print("Index\tOperator\tArg1\tArg2")
    print("-" * 50)
    
    for i, (op, arg1, arg2) in enumerate(triples):
        if arg2 is None:
            print(f"{i}\t{op}\t\t{arg1}\t-")
        else:
            print(f"{i}\t{op}\t\t{arg1}\t{arg2}")
    
    print("\nVariable Mappings:")
    print("-" * 50)
    for i, result in enumerate(results):
        if result:
            print(f"{result} = (Index {i})")

def main():
    print("Intermediate Code Generator - 3-Address Code using Triples")
    print("Enter expressions (separated by semicolons, end with a blank line):")
    print("Example: a = b + c; d = a * 2")
    
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    code = '\n'.join(code_lines)
    triples, results = generate_triples(code)
    display_triples(triples, results)

if __name__ == "__main__":
    main()
