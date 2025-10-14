from itertools import product
import re

# Evaluate propositional expression in a given model
def pl_true(expr, model):
    expr = expr.replace("<=>", "==")       # biconditional
    expr = expr.replace("=>", " or not ")  # implication

    # Replace symbols with True/False values
    for sym, val in model.items():
        expr = re.sub(rf'\b{sym}\b', str(val), expr)

    # Ensure logical operators are correct Python keywords
    expr = expr.replace("and", " and ").replace("or", " or ").replace("not", " not ")

    return eval(expr)

# Extract all unique propositional symbols (excluding 'and', 'or', 'not')
def extract_symbols(kb, query):
    text = " ".join(kb + [query])
    symbols = set(re.findall(r"[A-Za-z_]+", text))
    symbols -= {"and", "or", "not"}  # Remove logical operators
    return sorted(symbols)

# Truth-table entailment algorithm
def tt_entails(kb, query):
    symbols = extract_symbols(kb, query)
    print("\nSymbols:", symbols)

    print("\nTruth Table:")
    print(" | ".join(symbols + ["KB", "Query"]))
    print("-" * 75)

    entails = True
    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        kb_value = all(pl_true(sentence, model) for sentence in kb)
        query_value = pl_true(query, model)
        print(" | ".join(str(model[s]) for s in symbols), "|", kb_value, "|", query_value)
        if kb_value and not query_value:
            entails = False

    print("\nDoes KB entail Query? =>", "YES ✅" if entails else "NO ❌")

# ----------------- Main Program -----------------
if __name__ == "__main__":
    print("Enter the Knowledge Base sentences (type 'done' when finished):")
    kb = []
    while True:
        sentence = input("> ").strip()
        if sentence.lower() == "done":
            break
        if sentence:
            kb.append(sentence)

    query = input("\nEnter the Query sentence: ").strip()

    tt_entails(kb, query)

Output:
Enter the Knowledge Base sentences (type 'done' when finished):
>  A or C
> B or not C
> done

Enter the Query sentence: A or B

Symbols: ['A', 'B', 'C']

Truth Table:
A | B | C | KB | Query
---------------------------------------------------------------------------
False | False | False | False | False
False | False | True | False | False
False | True | False | False | True
False | True | True | True | True
True | False | False | True | True
True | False | True | False | True
True | True | False | True | True
True | True | True | True | True

Does KB entail Query? => YES ✅
