def optimize_code(code):
    optimized_code = []
    subexpressions = {}
    
    for line in code:
        var, expr = line.split('=', 1)
        var = var.strip()
        expr = expr.strip()

        if expr in subexpressions and var not in expr:
            optimized_code.append(f"{var} = {subexpressions[expr]}") 
        elif expr in subexpressions and var in expr:
            optimized_code.append(f"{var} = {subexpressions[expr]}")
            del subexpressions[expr]  
        else:
            subexpressions[expr] = var
            optimized_code.append(line) 
    return optimized_code

code_before_optimization = [
    "a = b + c",
    "d = b + c",
    "c = b + c",
]

optimized_code = optimize_code(code_before_optimization)
print("Code before optimization:")
for l1 in code_before_optimization:
    print(l1)
print()
print("Optimized code:")
for l2 in optimized_code:
    print(l2)
