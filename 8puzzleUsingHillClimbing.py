import copy

def get_input(prompt):
    print(prompt)
    return [int(x) for x in input().split()]

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def misplaced_tiles(state, goal):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    moves = []

    if idx % 3 != 0:  # left
        moves.append(idx - 1)
    if idx % 3 != 2:  # right
        moves.append(idx + 1)
    if idx > 2:       # up
        moves.append(idx - 3)
    if idx < 6:       # down
        moves.append(idx + 3)

    for move in moves:
        new_state = state[:]
        new_state[idx], new_state[move] = new_state[move], new_state[idx]
        neighbors.append(new_state)

    return neighbors

def hill_climb(start, goal):
    current = start
    while True:
        print_state(current)
        if current == goal:
            print("Reached goal!")
            return
        neighbors = get_neighbors(current)
        current_h = misplaced_tiles(current, goal)
        next_state = current
        for n in neighbors:
            if misplaced_tiles(n, goal) < current_h:
                next_state = n
                current_h = misplaced_tiles(n, goal)
        if next_state == current:
            print("Stuck in local optimum!")
            return
        current = next_state

# Main
start = get_input("Enter start state (9 numbers, use 0 for blank):")
goal = get_input("Enter goal state (9 numbers, use 0 for blank):")

hill_climb(start, goal)
