def unify_and_substitute(premise_tuple, facts, rule_conclusion, target_var_map):
    current_subst = {}
   
    for premise in premise_tuple:
        found_match = False
       
        pred_name, args = premise.split('(')[0], premise.split('(')[1].replace(')', '').split(', ')

        for fact in facts:
            fact_name, fact_args = fact.split('(')[0], fact.split('(')[1].replace(')', '').split(', ')
           
            if pred_name == fact_name and len(args) == len(fact_args):
                temp_subst = current_subst.copy()
                is_consistent = True
               
                for i in range(len(args)):
                    var = args[i]
                    const = fact_args[i]
                   
                    if var in temp_subst:
                        if temp_subst[var] != const:
                            is_consistent = False
                            break
                    else:
                        temp_subst[var] = const
               
                if is_consistent:
                    current_subst = temp_subst
                    found_match = True
                    break
       
        if not found_match:
            return None

    if current_subst:
        conclusion_pred, conclusion_args = rule_conclusion.split('(')[0], rule_conclusion.split('(')[1].replace(')', '').split(', ')
       
        final_args = [current_subst.get(arg, arg) for arg in conclusion_args]
        inferred_fact = f"{conclusion_pred}({', '.join(final_args)})"
       
        return inferred_fact
       
    return None


def forward_chaining_criminal(facts, rule, query):
    derived = set(facts)
    premises, conclusion = rule
   
    print("\n--- Starting Forward Chaining ---")

    while True:
        new_inference = False
       
        inferred = unify_and_substitute(premises, derived, conclusion, {})
       
        if inferred and inferred not in derived:
            print(f"Applying Rule: { ' ^ '.join(premises)} => {conclusion}")
            print(f"Inferred: {inferred}")
            derived.add(inferred)
            new_inference = True
           
            if inferred == query:
                return True, derived
               
        if not new_inference:
            break

    return (query in derived), derived

facts_criminal = {
    "American(Robert)",
    "Weapons(T1)",
    "Sells(Robert, T1, A)",
    "Hostile(A)"
}

criminal_rule_premises = [
    "American(p)",
    "Weapons(q)",
    "Sells(p, q, r)",
    "Hostile(r)"
]
criminal_rule_conclusion = "Criminal(p)"

rules_criminal = (criminal_rule_premises, criminal_rule_conclusion)

query_criminal = "Criminal(Robert)"

result_criminal, derived_facts_criminal = forward_chaining_criminal(facts_criminal, rules_criminal, query_criminal)

print("\n--- Final Facts Derived ---")
for f in derived_facts_criminal:
    print(f)

print("\nQuery:", query_criminal)
print("Result:", "TRUE  (Robert is a Criminal)" if result_criminal else "FALSE  (Not provable)")
Applying Rule: American(p) ^ Weapons(q) ^ Sells(p, q, r) ^ Hostile(r) => Criminal(p)
Inferred: Criminal(Robert)


OUTPUT:
--- Final Facts Derived ---
Hostile(A)
Weapons(T1)
American(Robert)
Criminal(Robert)
Sells(Robert, T1, A)

Query: Criminal(Robert)
Result: TRUE  (Robert is a Criminal) 
