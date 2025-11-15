tree = {
    'A': 10, 'B': 11, 'C': 9,  'D': 12,
    'E': 14, 'F': 15, 'G': 13, 'H': 14,
    'I': 5,  'J': 2,  'K': 4,  'L': 1,
    'M': 3,  'N': 22, 'O': 20, 'P': 21
}

tree_structure = [
    ['A', 'B', 'C', 'D'],
    ['E', 'F', 'G', 'H'],
    ['I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P']
]

pruned_nodes = []

def alpha_beta_min(values, alpha, beta):
    min_val = float('inf')
    for name in values:
        val = tree[name]
        print(f"    MIN checks {name}={val}, α={alpha}, β={beta}")
        if val < min_val:
            min_val = val
        if min_val <= alpha:
            remaining = values[values.index(name)+1:]
            pruned_nodes.extend(remaining)
            print(f"    Pruning at MIN node after {name}: {remaining}")
            break
        beta = min(beta, min_val)
    print(f"    → MIN returns {min_val}")
    return min_val

def alpha_beta_max(structure, alpha, beta):
    max_val = float('-inf')
    best_branch = None
    for group in structure:
        print(f"\nExploring branch: {group}")
        val = alpha_beta_min(group, alpha, beta)
        if val > max_val:
            max_val = val
            best_branch = group
        alpha = max(alpha, max_val)
        if alpha >= beta:
            remaining = structure[structure.index(group)+1:]
            for g in remaining:
                pruned_nodes.extend(g)
            print(f"Pruning at MAX after {group}")
            break
        print(f"MAX updated α={alpha}, β={beta}")
    print(f"\n→ MAX returns {max_val}")
    return max_val, best_branch

root_value, path = alpha_beta_max(tree_structure, float('-inf'), float('inf'))

print("\n===========================")
print("Root Node Value (MAX):", root_value)
print("Best Path (Branch):", path)
print("Pruned Nodes:", pruned_nodes)


OUTPUT:
Exploring branch: ['A', 'B', 'C', 'D']
    MIN checks A=10, α=-inf, β=inf
    MIN checks B=11, α=-inf, β=10
    MIN checks C=9, α=-inf, β=10
    Pruning at MIN node after C: ['D']
    → MIN returns 9
MAX updated α=9, β=inf

Exploring branch: ['E', 'F', 'G', 'H']
    MIN checks E=14, α=9, β=inf
    Pruning at MIN node after E: ['F', 'G', 'H']
    → MIN returns 14
Pruning at MAX after ['E', 'F', 'G', 'H']

→ MAX returns 10

===========================
Root Node Value (MAX): 10
Best Path (Branch): ['A', 'B', 'C', 'D']
Pruned Nodes: ['D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
