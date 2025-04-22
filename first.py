def calculate_first(grammar):
    # Initialize FIRST sets for all symbols
    first = {}
    
    # For terminals (lowercase letters), FIRST is just the terminal itself
    for symbol in "abcdefghijklmnopqrstuvwxyz":
        first[symbol] = {symbol}
    
    # For epsilon
    first['ε'] = {'ε'}
    
    # Initialize empty sets for non-terminals
    for non_terminal in grammar:
        first[non_terminal] = set()
    
    # Keep updating until no changes
    changed = True
    while changed:
        changed = False
        
        for NT, productions in grammar.items():
            for prod in productions:
                # If production is epsilon, add epsilon to FIRST(NT)
                if prod == 'ε':
                    if 'ε' not in first[NT]:
                        first[NT].add('ε')
                        changed = True
                    continue
                
                # Get first symbol in production
                symbol = prod[0]
                
                # If it's a terminal, add it to FIRST(NT)
                if symbol in first and symbol.islower():
                    if symbol not in first[NT]:
                        first[NT].add(symbol)
                        changed = True
                
                # If it's a non-terminal, add its FIRST set (except epsilon) to FIRST(NT)
                elif symbol in first:
                    for term in first[symbol] - {'ε'}:
                        if term not in first[NT]:
                            first[NT].add(term)
                            changed = True
                    
                    # If first symbol can derive epsilon, check next symbol
                    if 'ε' in first[symbol] and len(prod) > 1:
                        next_symbol = prod[1]
                        if next_symbol in first:
                            for term in first[next_symbol]:
                                if term not in first[NT]:
                                    first[NT].add(term)
                                    changed = True
    
    return first

# Example usage
grammar = {
    'S': ['AB', 'a'],
    'A': ['a', 'ε'],
    'B': ['b']
}

result = calculate_first(grammar)
for symbol, first_set in result.items():
    if symbol in grammar:  # Only print non-terminals
        print(f"FIRST({symbol}) = {first_set}")
