def optimize_code(code):
    optimized_code = []
    subexpressions = {}
    
    for line in code:
        var, expr = line.split('=', 1)
        var = var.strip()
        expr = expr.strip()

        if expr in subexpressions:
            optimized_code.append(f"{var} = {subexpressions[expr]}")
            del subexpressions[expr]
        else:
            subexpressions[expr] = var
            optimized_code.append(line)
    return optimized_code

code_before_optimization = [
    "x = y + z",
    "a = y + z",
    "b = x + y",
    "c = x + y",
    "d = y + z"
]

optimized_code = optimize_code(code_before_optimization)

print("Optimized code:")
for line in optimized_code:
    print(line)
