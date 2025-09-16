import heapq

# Moves: up, down, left, right
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristic(board, goal):
"""Manhattan distance heuristic."""
    dist = 0
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val != 0:
                # Find tile's position in goal state
                for x in range(3):
                    for y in range(3):
                        if goal[x][y] == val:
                            dist += abs(i - x) + abs(j - y)
                            break
    return dist


def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

def get_neighbors(board):
    neighbors = []
    x, y = find_blank(board)
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_board = [row[:] for row in board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append(new_board)
    return neighbors

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def a_star_search(start, goal):
    open_list = []
    start_h = heuristic(start, goal)
    heapq.heappush(open_list, (start_h, 0, start, [start]))
    closed_set = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == goal:
            return path

        closed_set.add(board_to_tuple(current))

        for neighbor in get_neighbors(current):
            neighbor_tuple = board_to_tuple(neighbor)
            if neighbor_tuple in closed_set:
                continue
            g_new = g + 1
            h_new = heuristic(neighbor, goal)
            f_new = g_new + h_new
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None

def get_user_input(prompt_text):
    print(f"\nEnter the {prompt_text} (use 0 for the blank tile).")
    board = []
    nums_seen = set()
    for i in range(3):
        while True:
            try:
                row = input(f"Enter row {i + 1} (e.g., 1 2 3): ").strip().split()
                if len(row) != 3:
                    raise ValueError
                row_int = [int(x) for x in row]
                for n in row_int:
                    if n < 0 or n > 8 or n in nums_seen:
                        raise ValueError
                    nums_seen.add(n)
                board.append(row_int)
                break
            except ValueError:
                print("Invalid input! Enter three unique integers from 0 to 8, no duplicates.")
    return board

def print_board(board):
    for row in board:
        print(' '.join(str(x) for x in row))


# Direct execution without 'if __name__ == "__main__":'

initial_state = get_user_input("initial state")
goal_state = get_user_input("goal state")

print("\nSolving the puzzle using A* search...\n")
solution = a_star_search(initial_state, goal_state)

if solution:
    print(f"Solution found in {len(solution) - 1} moves:\n")
    for step, state in enumerate(solution):
        print(f"Step {step}:")
        print_board(state)
        print()
else:
    print("No solution found.")
'''
OUTPUT:
Enter the initial state (use 0 for the blank tile).
Enter row 1 (e.g., 1 2 3): 1 2 3
Enter row 2 (e.g., 1 2 3): 4 5 6
Enter row 3 (e.g., 1 2 3): 7 0 8

Enter the goal state (use 0 for the blank tile).
Enter row 1 (e.g., 1 2 3): 1 2 3
Enter row 2 (e.g., 1 2 3): 4 5 6
Enter row 3 (e.g., 1 2 3): 7  8  0

Solving the puzzle using A* search...

Solution found in 1 moves:

Step 0:
1 2 3
4 5 6
7 0 8

Step 1:
1 2 3
4 5 6
7 8 0
'''
