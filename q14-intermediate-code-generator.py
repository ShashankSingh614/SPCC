def parse_expression(expr):
    """
    Basic parser for arithmetic expressions
    Returns a list of quadruples (op, arg1, arg2, result)
    """
    # Remove all spaces
    expr = expr.replace(" ", "")
    
    quadruples = []
    temp_counter = 1
    stack = []
    i = 0
    
    while i < len(expr):
        if expr[i].isalnum():
            # Process variable or number
            operand = ""
            while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
                operand += expr[i]
                i += 1
            stack.append(operand)
        elif expr[i] in "+-*/":
            # Process operators
            op = expr[i]
            i += 1
            
            # Get the next operand
            right_operand = ""
            while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
                right_operand += expr[i]
                i += 1
            
            if not right_operand:
                print("Error: Missing operand after operator")
                return []
            
            # Create a temporary variable for the result
            temp_var = f"t{temp_counter}"
            temp_counter += 1
            
            # Create a quadruple
            left_operand = stack.pop() if stack else None
            if left_operand is None:
                print("Error: Missing left operand")
                return []
            
            quadruples.append((op, left_operand, right_operand, temp_var))
            stack.append(temp_var)
        elif expr[i] == '=':
            # Handle assignment
            i += 1
            if not stack:
                print("Error: Missing left side of assignment")
                return []
            
            left_side = stack.pop()
            # Get the right side
            right_side = ""
            while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
                right_side += expr[i]
                i += 1
            
            if not right_side:
                print("Error: Missing right side of assignment")
                return []
            
            quadruples.append(('=', right_side, None, left_side))
        else:
            i += 1  # Skip other characters

    return quadruples

def display_quadruples(quadruples):
    """Display the quadruples in a tabular format"""
    print("\nQuadruples (Op, Arg1, Arg2, Result):")
    print("-" * 50)
    print("| {:<5} | {:<10} | {:<10} | {:<10} |".format("Op", "Arg1", "Arg2", "Result"))
    print("-" * 50)
    
    for quad in quadruples:
        op, arg1, arg2, result = quad
        arg2_str = str(arg2) if arg2 is not None else ""
        print("| {:<5} | {:<10} | {:<10} | {:<10} |".format(op, arg1, arg2_str, result))
    print("-" * 50)

def main():
    print("Intermediate Code Generator - 3-Address Code (Quadruples)")
    print("Example inputs: 'a=b+c', 'x=y*z+w', etc.")
    
    while True:
        expr = input("\nEnter an expression (or 'exit' to quit): ")
        if expr.lower() == 'exit':
            break
        
        quadruples = parse_expression(expr)
        if quadruples:
            display_quadruples(quadruples)
        else:
            print("Failed to generate quadruples. Please check your expression.")

if __name__ == "__main__":
    main()
