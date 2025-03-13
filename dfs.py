from queue import LifoQueue

def dfs(grid, start, goal):
    rows, cols = grid.shape
    visited = set()
    stack = LifoQueue()
    stack.put((start, [start]))  # position, path

    while not stack.empty():
        current, path = stack.get()

        if current == goal:
            return path, len(path) - 1

        if current in visited:
            continue

        visited.add(current)

        # Explore neighbors (up/down/left/right)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] != 'O':
                next_pos = (nx, ny)
                if next_pos not in visited:
                    stack.put((next_pos, path+[next_pos]))

    return None, float('inf')  # No path found