str = input("Enter the Expression :")
keyword, identifier, number, specialSymbol, operator, delimeter = 0, 0, 0, 0, 0, 0
keywordList = ["False", "None", "True", "and", "break","class", "continue","def", "del", "elif", "else", "except", "for","if", "in", "is", "lambda", "not", "or", "pass", "return", "try", "while","with", "int", "float"]
tokens = str.split()
for token in tokens:
    if token in keywordList:
        keyword += 1
    elif token.isnumeric():
        number += 1
    elif token.isalpha():
        identifier += 1
    elif token in "&~'><}{][|)(?": 
        specialSymbol += 1
    elif token in "*+-/%!=":
        operator += 1
    elif token in ";,:":
        delimeter +=1
print("Identifiers:", identifier)
print("Numbers:", number)
print("Special Symbols:", specialSymbol)
print("Keywords:", keyword)
print("Operators:", operator)
print("Delimeter:", delimeter)
