# Program to find the FIRST set of a given grammar

def calculate_first(grammar):
    # Initialize FIRST sets for all non-terminals
    first = {non_terminal: set() for non_terminal in grammar}
    
    # Function to find FIRST set for a symbol
    def find_first(symbol):
        # Terminal symbols are their own FIRST sets
        if symbol not in grammar:
            return {symbol}
        
        result = set()
        
        # If we've already computed FIRST for this symbol, return it
        if first[symbol] and len(first[symbol]) > 0:
            return first[symbol]
        
        # Process each production for this non-terminal
        for production in grammar[symbol]:
            # For empty production (epsilon)
            if production == "ε" or production == "":
                result.add("ε")
                continue
            
            # Process the first symbol of the production
            first_symbol = production[0]
            
            # If it's a terminal, add it to FIRST
            if first_symbol not in grammar:
                result.add(first_symbol)
                continue
            
            # If it's a non-terminal, add its FIRST set
            symbol_first = find_first(first_symbol)
            
            # Add all except epsilon
            for item in symbol_first:
                if item != "ε":
                    result.add(item)
            
            # Check if epsilon is in the FIRST of the current symbol
            # If so, we need to consider the next symbol in the production
            i = 0
            while i < len(production) and "ε" in find_first(production[i]):
                # If this is the last symbol and it can derive epsilon, add epsilon to result
                if i == len(production) - 1:
                    result.add("ε")
                    break
                
                # Add FIRST of next symbol (except epsilon)
                next_first = find_first(production[i + 1])
                for item in next_first:
                    if item != "ε":
                        result.add(item)
                
                i += 1
        
        # Update the FIRST set for this symbol
        first[symbol] = result
        return result
    
    # Calculate FIRST for all non-terminals
    for non_terminal in grammar:
        find_first(non_terminal)
    
    return first

def parse_grammar_input():
    print("Enter the grammar productions (one per line, format: A -> B C | D)")
    print("Enter a blank line to finish input.")
    
    grammar = {}
    
    while True:
        line = input().strip()
        if not line:
            break
        
        # Parse the production
        if "->" in line:
            non_terminal, productions = line.split("->")
            non_terminal = non_terminal.strip()
            
            # Handle multiple productions separated by |
            production_list = [p.strip() for p in productions.split("|")]
            
            # Initialize the list if it doesn't exist
            if non_terminal not in grammar:
                grammar[non_terminal] = []
            
            # Add all productions
            for prod in production_list:
                # Handle epsilon (empty string) production
                if prod.lower() in ["ε", "epsilon", ""]:
                    grammar[non_terminal].append("ε")
                else:
                    # Split production into individual symbols
                    symbols = prod.split()
                    grammar[non_terminal].append(symbols)
    
    return grammar

def display_first_sets(first_sets):
    print("\nFIRST Sets:")
    print("-" * 40)
    for non_terminal, first_set in first_sets.items():
        print(f"FIRST({non_terminal}) = {{{ ', '.join(sorted(first_set)) }}}")

def main():
    print("Program to find FIRST set for a grammar")
    grammar = parse_grammar_input()
    
    # Verify grammar
    if not grammar:
        print("No valid grammar productions entered.")
        return
    
    # Calculate FIRST sets
    first_sets = calculate_first(grammar)
    
    # Display results
    display_first_sets(first_sets)

if __name__ == "__main__":
    main()
