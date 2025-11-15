def is_variable(x):
    return isinstance(x, str) and x.islower()

def occur_check(var, expr):
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occur_check(var, e) for e in expr)
    return False

def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    elif is_variable(x):
        if occur_check(x, y):
            print(f"Failure: occur-check failed for {x} in {y}")
            return None
        subst[x] = y
        return subst
    elif is_variable(y):
        if occur_check(y, x):
            print(f"Failure: occur-check failed for {y} in {x}")
            return None
        subst[y] = x
        return subst
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            print(f"Failure: different arity - {len(x)} vs {len(y)}")
            return None
        if x[0] != y[0]:
            print(f"Failure: different function symbols - {x[0]} vs {y[0]}")
            return None
        for xi, yi in zip(x, y):
            result = unify(xi, yi, subst)
            if result is None:
                return None
            subst = result
        return subst
    else:
        print(f"Failure: cannot unify {x} and {y}")
        return None

expr1 = ['f', 'x', 'b']
expr2 = ['f', 'a', 'y']
print("Expression 1:", expr1)
print("Expression 2:", expr2)
result = unify(expr1, expr2)
if result is not None:
    print("Unification Result:", result)
else:
    print("Unification Failure")

expr3 = ['f', 'x', 'b']
expr4 = ['g', 'a', 'y']
print("\nExpression 1:", expr3)
print("Expression 2:", expr4)
result2 = unify(expr3, expr4)
if result2 is not None:
    print("Unification Result:", result2)
else:
    print("Unification Failure")

OUTPUT:
Expression 1: ['f', 'x', 'b']
Expression 2: ['f', 'a', 'y']
Unification Result: {'x': 'a', 'b': 'y'}

Expression 1: ['f', 'x', 'b']
Expression 2: ['g', 'a', 'y']
Failure: different function symbols - f vs g
Unification Failure
