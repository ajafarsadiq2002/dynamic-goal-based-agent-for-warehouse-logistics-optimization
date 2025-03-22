from queue import PriorityQueue

def explore_ucs(warehouse_map, entry_point, target_location, trip_type='P'):
    """UCS with obstacle penalty handling for delivery only."""
    total_rows, total_cols = warehouse_map.shape
    visited = set()
    cost_so_far = {entry_point: 0}
    penalty_so_far = {entry_point: 0}
    penalty_count_so_far = {entry_point: 0}

    pq = PriorityQueue()
    pq.put((0, entry_point, [entry_point], 0, 0))  # cost, position, path, penalty, count

    while not pq.empty():
        cost, current, path, penalty, penalty_count = pq.get()

        if current == target_location:
            return path, cost, penalty, penalty_count

        if current in visited:
            continue

        visited.add(current)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_x, new_y = current[0] + dx, current[1] + dy
            next_pos = (new_x, new_y)

            if 0 <= new_x < total_rows and 0 <= new_y < total_cols:
                cell = warehouse_map[new_x, new_y]
                new_cost = cost + 1
                new_penalty = penalty
                new_penalty_count = penalty_count

                if trip_type == 'P' and cell == 'O':
                    continue

                if trip_type == 'D' and cell == 'O':
                    new_penalty += 5
                    new_penalty_count += 1

                if next_pos not in visited:
                    pq.put((new_cost, next_pos, path + [next_pos], new_penalty, new_penalty_count))

    return None, float('inf'), penalty, penalty_count
