# Program to find the FOLLOW set of a given grammar (continued)

def calculate_first_and_follow(grammar, start_symbol):
    # Initialize FIRST and FOLLOW sets
    first = {non_terminal: set() for non_terminal in grammar}
    follow = {non_terminal: set() for non_terminal in grammar}
    
    # Add $ to FOLLOW of start symbol
    follow[start_symbol].add('$')
    
    # Calculate FIRST sets
    def find_first(symbol):
        # Terminal symbols are their own FIRST sets
        if symbol not in grammar:
            return {symbol}
        
        result = set()
        
        # Process each production for this non-terminal
        for production in grammar[symbol]:
            # For empty production (epsilon)
            if not production or production[0] == "ε":
                result.add("ε")
                continue
            
            # Process the first symbol of the production
            first_symbol = production[0]
            
            # If it's a terminal, add it to FIRST
            if first_symbol not in grammar:
                result.add(first_symbol)
                continue
            
            # If it's a non-terminal, add its FIRST set (except epsilon)
            for item in find_first(first_symbol):
                if item != "ε":
                    result.add(item)
            
            # Check if all symbols can derive epsilon
            all_derive_epsilon = True
            for sym in production:
                if sym not in grammar or "ε" not in find_first(sym):
                    all_derive_epsilon = False
                    break
            
            if all_derive_epsilon:
                result.add("ε")
        
        # Cache result
        first[symbol] = result
        return result
    
    # Calculate FIRST for all non-terminals
    for non_terminal in grammar:
        find_first(non_terminal)
    
    # Calculate first of a string of symbols
    def first_of_string(string):
        if not string:
            return {"ε"}
        
        result = set()
        
        # Add FIRST of first symbol
        for item in find_first(string[0]):
            if item != "ε":
                result.add(item)
        
        # If first symbol can derive epsilon, consider next symbols
        i = 0
        while i < len(string) and "ε" in find_first(string[i]):
            i += 1
            if i < len(string):
                for item in find_first(string[i]):
                    if item != "ε":
                        result.add(item)
            else:
                result.add("ε")  # All symbols can derive epsilon
        
        return result
    
    # Calculate FOLLOW sets
    changed = True
    while changed:
        changed = False
        
        for non_terminal in grammar:
            for production in grammar:
                for rule in grammar[production]:
                    for i, symbol in enumerate(rule):
                        if symbol in grammar:  # If it's a non-terminal
                            # Case 1: A -> αBβ, then FIRST(β) - {ε} is added to FOLLOW(B)
                            if i + 1 < len(rule):
                                rest = rule[i+1:]
                                first_of_rest = first_of_string(rest)
                                
                                # Add everything except epsilon
                                old_len = len(follow[symbol])
                                for item in first_of_rest:
                                    if item != "ε":
                                        follow[symbol].add(item)
                                
                                if len(follow[symbol]) > old_len:
                                    changed = True
                                
                                # Case 2: A -> αBβ and ε is in FIRST(β), then FOLLOW(A) is added to FOLLOW(B)
                                if "ε" in first_of_rest:
                                    old_len = len(follow[symbol])
                                    follow[symbol].update(follow[production])
                                    if len(follow[symbol]) > old_len:
                                        changed = True
                            
                            # Case 3: A -> αB, then FOLLOW(A) is added to FOLLOW(B)
                            elif i == len(rule) - 1:
                                old_len = len(follow[symbol])
                                follow[symbol].update(follow[production])
                                if len(follow[symbol]) > old_len:
                                    changed = True
    
    return first, follow

def parse_grammar_input():
    print("Enter the grammar productions (one per line, format: A -> B C | D)")
    print("Enter a blank line to finish input.")
    print("Note: Use 'ε' for epsilon (empty string)")
    
    grammar = {}
    start_symbol = None
    
    while True:
        line = input().strip()
        if not line:
            break
        
        # Parse the production
        if "->" in line:
            non_terminal, productions = line.split("->")
            non_terminal = non_terminal.strip()
            
            # Set the first non-terminal as the start symbol
            if start_symbol is None:
                start_symbol = non_terminal
            
            # Handle multiple productions separated by |
            production_list = [p.strip() for p in productions.split("|")]
            
            # Initialize the list if it doesn't exist
            if non_terminal not in grammar:
                grammar[non_terminal] = []
            
            # Add all productions
            for prod in production_list:
                if prod.lower() in ["ε", "epsilon", ""]:
                    grammar[non_terminal].append([])  # Empty list for epsilon
                else:
                    # Split production into individual symbols
                    symbols = prod.split()
                    grammar[non_terminal].append(symbols)
    
    return grammar, start_symbol

def display_follow_sets(follow_sets):
    print("\nFOLLOW Sets:")
    print("-" * 40)
    for non_terminal, follow_set in follow_sets.items():
        print(f"FOLLOW({non_terminal}) = {{{ ', '.join(sorted(follow_set)) }}}")

def main():
    print("Program to find FOLLOW set for a grammar")
    grammar, start_symbol = parse_grammar_input()
    
    # Verify grammar
    if not grammar:
        print("No valid grammar productions entered.")
        return
        
    print(f"Using '{start_symbol}' as the start symbol")
    
    # Calculate FOLLOW sets
    _, follow_sets = calculate_first_and_follow(grammar, start_symbol)
    
    # Display results
    display_follow_sets(follow_sets)

if __name__ == "__main__":
    main()
