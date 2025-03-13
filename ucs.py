from queue import PriorityQueue

def ucs(grid, start, goal):
    rows, cols = grid.shape
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start, [start]))  # cost, position, path

    while not queue.empty():
        cost, current, path = queue.get()

        if current == goal:
            return path, cost

        if current in visited:
            continue

        visited.add(current)

        # Explore neighbors (up/down/left/right)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] != 'O':
                next_pos = (nx, ny)
                if next_pos not in visited:
                    queue.put((cost+1, next_pos, path+[next_pos]))

    return None, float('inf')  # No path found