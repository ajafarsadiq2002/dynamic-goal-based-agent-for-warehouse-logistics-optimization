from queue import Queue

def explore_bfs(warehouse_map, entry_point, target_location, trip_type='P'):
    """BFS for warehouse navigation with obstacle penalty handling."""
    total_rows, total_cols = warehouse_map.shape
    explored = set()
    penalty = 0
    penalty_count = 0
    q = Queue()
    q.put((entry_point, [entry_point]))
    explored.add(entry_point)

    while not q.empty():
        current_pos, path = q.get()
        if current_pos == target_location:
            return path, len(path) - 1, penalty, penalty_count

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            next_pos = (new_x, new_y)

            if 0 <= new_x < total_rows and 0 <= new_y < total_cols and next_pos not in explored:
                cell = warehouse_map[new_x, new_y]

                if trip_type == 'P' and cell == 'O':
                    continue  # Avoid obstacles during pickup

                if trip_type == 'D' and cell == 'O':
                    penalty += 5
                    penalty_count += 1

                explored.add(next_pos)
                q.put((next_pos, path + [next_pos]))

    return None, float('inf'), penalty, penalty_count
