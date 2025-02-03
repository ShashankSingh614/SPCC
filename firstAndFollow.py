import re

def cal_first(s, productions):
    first = set()
    if s not in productions:  # If 's' is a terminal, return itself as FIRST
        return {s}

    for production in productions[s]:  # Iterate over all production rules for s
        for terminal in production:  # Iterate over symbols in the production
            if terminal.isupper():  # If it's a non-terminal
                f = cal_first(terminal, productions)  
                first.update(f - {'ε'})  # Add everything except 'ε'
                if 'ε' not in f:  # Stop if 'ε' is not present
                    break
            else:  # If it's a terminal
                first.add(terminal)
                break  
    return first

def cal_follow(s, productions, first):
    follow = set()
    if s == list(productions.keys())[0]:  # Rule 1: Add '$' to the start symbol
        follow.add('$')
    
    for lhs in productions:  # Iterate through all production rules
        for production in productions[lhs]:
            for i, symbol in enumerate(production):
                if symbol == s:  # If we found the non-terminal we are calculating FOLLOW for
                    if i + 1 < len(production):  # Check if there's a symbol after it
                        next_symbol = production[i + 1]
                        if next_symbol in productions:  # Check if next_symbol is a non-terminal
                            follow.update(first[next_symbol] - {'ε'})  # Add FIRST(next_symbol) except 'ε'
                            if 'ε' in first[next_symbol]:  # If FIRST(next_symbol) contains 'ε', continue
                                follow.update(cal_follow(lhs, productions, first))
                        else:  # If the next symbol is a terminal, just add it
                            follow.add(next_symbol)
                    else:  # If there is no symbol after it, add FOLLOW(lhs)
                        follow.update(cal_follow(lhs, productions, first))
    
    return follow

def main():
    productions = {}
    
    # Get number of rules from the user
    num_rules = int(input("Enter the number of production rules: "))
    
    # Accept production rules from the user
    for _ in range(num_rules):
        lhs = input("Enter the left-hand side (non-terminal): ").strip()
        rhs = input("Enter the right-hand side (productions, separated by '|'): ").strip()
        
        # Split the RHS by '|'
        rhs_prod = [re.findall(r'[A-Z]|[^A-Z\s]', prod.strip()) for prod in rhs.split('|')]
        
        # Store the production
        productions[lhs] = rhs_prod
    
    first = {}
    follow = {}
    
    # Calculate the FIRST set for each non-terminal
    for s in productions.keys():
        first[s] = cal_first(s, productions)
    
    print("*****FIRST*****")
    for lhs, rhs in first.items():
        print(lhs, ":", rhs)
    
    print("")
    
    # Initialize FOLLOW set for each non-terminal
    for lhs in productions:
        follow[lhs] = set()
    
    # Calculate the FOLLOW set for each non-terminal
    for s in productions.keys():
        follow[s] = cal_follow(s, productions, first)
    
    print("*****FOLLOW*****")
    for lhs, rhs in follow.items():
        print(lhs, ":", rhs)

if __name__ == "__main__":
    main()
