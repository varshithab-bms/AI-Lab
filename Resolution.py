def is_variable(x):
    return isinstance(x, str) and len(x) > 0 and x[0].islower()

def substitute(theta, clause):
    new_clause = []
    for pred in clause:
        name, terms = pred[0], pred[1]
        new_terms = []
        for t in terms:
   
            new_terms.append(theta.get(t, t))
        new_clause.append((name, new_terms))
    return new_clause

def unify(x, y, theta=None):
    if theta is None:
        return None
    if x == y:
        return theta
    if is_variable(x):
        return unify_var(x, y, theta)
    if is_variable(y):
        return unify_var(y, x, theta)

    if isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
            if theta is None:
                return None
        return theta
    return None

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    if x in theta:
        return unify(var, theta[x], theta)

    new_theta = theta.copy()
    new_theta[var] = x
    return new_theta

def resolve(ci, cj):
    resolvents = []
    for pi in ci:
        for pj in cj:
            name_i = pi[0].lstrip("¬")
            name_j = pj[0].lstrip("¬")
 
            if name_i == name_j and (pi[0].startswith("¬") != pj[0].startswith("¬")):
                theta = unify(pi[1], pj[1], {})
                if theta is not None:
                    new_ci = substitute(theta, [x for x in ci if x != pi])
                    new_cj = substitute(theta, [x for x in cj if x != pj])
                    combined = []
                    for lit in (new_ci + new_cj):
                        if lit not in combined:
                            combined.append(lit)
                    resolvents.append(combined)
    return resolvents

def resolution(kb, query):
    neg_query = [("¬" + query[0], query[1])]
    clauses = [list(c) for c in kb] + [neg_query]

    new = []
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            for r in resolve(ci, cj):
                if r == []:
                    return True
                if r not in new and r not in clauses:
                    new.append(r)
        if not new:
            return False
        added_any = False
        for c in new:
            if c not in clauses:
                clauses.append(c)
                added_any = True
        if not added_any:
            return False
        new = []


KB = [
    [("¬Food", ["x"]), ("Likes", ["John", "x"])],

    [("Food", ["Apple"])],
    [("Food", ["Vegetable"])],

    [("¬Eats", ["a", "b"]), ("¬NotKilled", ["a"]), ("Food", ["b"])],

    [("Eats", ["Anil", "Peanuts"])],
    [("Alive", ["Anil"])],

    [("¬Eats", ["Anil", "x"]), ("Eats", ["Harry", "x"])],

    [("¬Alive", ["x"]), ("NotKilled", ["x"])],

    [("¬NotKilled", ["x"]), ("Alive", ["x"])]
]

query = ("Likes", ["John", "Peanuts"])

print("Proving:", query)
res = resolution(KB, query)
print("Proved?" , res)


OUTPUT:
Proving: ('Likes', ['John', 'Peanuts'])
Proved? True 
