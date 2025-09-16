import heapq

# Moves: up, down, left, right
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristic(board, goal):
    """Count of misplaced tiles (excluding 0)."""
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1
    return count

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
