from copy import deepcopy

goal = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_next_states(state):
    x, y = find_zero(state)
    next_states = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            next_states.append(new_state)
    return next_states

def dfs(state, visited, path):
    if state == goal:
        return path
    visited.add(str(state))
    for next_state in get_next_states(state):
        if str(next_state) not in visited:
            result = dfs(next_state, visited, path + [next_state])
            if result:
                return result
    return None

print("Enter the initial 8-puzzle state row-wise (use 0 for blank):")
start = []
for _ in range(3):
    row = list(map(int, input().split()))
    start.append(row)

result = dfs(start, set(), [start])

if result:
    print(f"Solved in {len(result) - 1} moves:\n")
    for step in result:
        for row in step:
            print(row)
        print("-----")
else:
    print("No solution found.")
