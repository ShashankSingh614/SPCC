def calculate_follow(grammar, first_sets):
    # Initialize FOLLOW sets for all non-terminals
    follow = {}
    for non_terminal in grammar:
        follow[non_terminal] = set()
    
    # Add $ to FOLLOW(S) where S is the start symbol (first key in grammar)
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$')
    
    # Keep updating until no changes
    changed = True
    while changed:
        changed = False
        
        # Check each production rule
        for NT, productions in grammar.items():
            for prod in productions:
                # Skip epsilon productions
                if prod == 'ε':
                    continue
                
                # Check each symbol in the production
                for i in range(len(prod)):
                    symbol = prod[i]
                    
                    # We only care about non-terminals
                    if symbol in grammar:
                        # Case 1: Symbol is followed by another symbol
                        if i < len(prod) - 1:
                            next_symbol = prod[i+1]
                            
                            # If next symbol is terminal, add it to FOLLOW(symbol)
                            if next_symbol not in grammar:
                                if next_symbol != 'ε' and next_symbol not in follow[symbol]:
                                    follow[symbol].add(next_symbol)
                                    changed = True
                            
                            # If next symbol is non-terminal, add FIRST(next_symbol) to FOLLOW(symbol)
                            else:
                                for terminal in first_sets[next_symbol] - {'ε'}:
                                    if terminal not in follow[symbol]:
                                        follow[symbol].add(terminal)
                                        changed = True
                                
                                # If next symbol can derive epsilon, also add FOLLOW(NT) to FOLLOW(symbol)
                                if 'ε' in first_sets[next_symbol]:
                                    for terminal in follow[NT]:
                                        if terminal not in follow[symbol]:
                                            follow[symbol].add(terminal)
                                            changed = True
                        
                        # Case 2: Symbol is at the end of production or can derive epsilon
                        # Add FOLLOW(NT) to FOLLOW(symbol)
                        elif i == len(prod) - 1:
                            for terminal in follow[NT]:
                                if terminal not in follow[symbol]:
                                    follow[symbol].add(terminal)
                                    changed = True

    return follow

# Function to calculate FIRST sets (simplified from previous example)
def calculate_first(grammar):
    first = {}
    for symbol in "abcdefghijklmnopqrstuvwxyz$":
        first[symbol] = {symbol}
    first['ε'] = {'ε'}
    
    for non_terminal in grammar:
        first[non_terminal] = set()
    
    changed = True
    while changed:
        changed = False
        for NT, productions in grammar.items():
            for prod in productions:
                if prod == 'ε':
                    if 'ε' not in first[NT]:
                        first[NT].add('ε')
                        changed = True
                    continue
                
                # Get first symbol
                symbol = prod[0]
                if symbol not in grammar and symbol != 'ε':
                    if symbol not in first[NT]:
                        first[NT].add(symbol)
                        changed = True
                elif symbol in grammar:
                    for term in first[symbol] - {'ε'}:
                        if term not in first[NT]:
                            first[NT].add(term)
                            changed = True
                    
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
    'S': ['ABC'],
    'A': ['a', 'ε'],
    'B': ['b'],
    'C': ['c']
}

first_sets = calculate_first(grammar)
follow_sets = calculate_follow(grammar, first_sets)

print("FIRST sets:")
for nt in grammar:
    print(f"FIRST({nt}) = {first_sets[nt]}")

print("\nFOLLOW sets:")
for nt in grammar:
    print(f"FOLLOW({nt}) = {follow_sets[nt]}")
