import collections

def is_valid(state):
    """
    Checks if a state is valid.
    A state is a tuple of two frozensets: (left_bank, right_bank).
    """
    left_bank, right_bank = state
    # Check for invalid combinations on the left bank when farmer is not there
    if 'F' not in left_bank:
        if 'W' in left_bank and 'G' in left_bank:
            return False
        if 'G' in left_bank and 'C' in left_bank:
            return False
    # Check for invalid combinations on the right bank when farmer is not there
    if 'F' not in right_bank:
        if 'W' in right_bank and 'G' in right_bank:
            return False
        if 'G' in right_bank and 'C' in right_bank:
            return False
    return True

def get_next_states(state):
    """
    Generates all possible next valid states from the current state.
    """
    next_states = []
    left_bank, right_bank = state
    
    if 'F' in left_bank:
        # Farmer moves from left to right
        # Move farmer alone
        new_left = left_bank - {'F'}
        new_right = right_bank | {'F'}
        if is_valid((new_left, new_right)):
            next_states.append((('F', 'R'), (new_left, new_right)))
            
        # Move farmer with one item
        for item in left_bank - {'F'}:
            new_left = left_bank - {'F', item}
            new_right = right_bank | {'F', item}
            if is_valid((new_left, new_right)):
                next_states.append(((item, 'R'), (new_left, new_right)))
    else: # Farmer is on the right bank
        # Farmer moves from right to left
        # Move farmer alone
        new_left = left_bank | {'F'}
        new_right = right_bank - {'F'}
        if is_valid((new_left, new_right)):
            next_states.append((('F', 'L'), (new_left, new_right)))
            
        # Move farmer with one item
        for item in right_bank - {'F'}:
            new_left = left_bank | {'F', item}
            new_right = right_bank - {'F', item}
            if is_valid((new_left, new_right)):
                next_states.append(((item, 'L'), (new_left, new_right)))
                
    return next_states

def solve():
    """
    Solves the river crossing puzzle using BFS.
    """
    initial_state = (frozenset(['F', 'W', 'G', 'C']), frozenset())
    goal_state = (frozenset(), frozenset(['F', 'W', 'G', 'C']))
    
    queue = collections.deque([([], initial_state)]) # (path, state)
    visited = {initial_state}
    
    while queue:
        path, current_state = queue.popleft()
        
        if current_state == goal_state:
            return path
            
        for move, next_state in get_next_states(current_state):
            frozen_next_state = (frozenset(next_state[0]), frozenset(next_state[1]))
            if frozen_next_state not in visited:
                visited.add(frozen_next_state)
                new_path = path + [move]
                queue.append((new_path, frozen_next_state))
                
    return None

def main():
    solution = solve()
    if solution:
        with open('solution.txt', 'w') as f:
            for move, direction in solution:
                f.write(f"{move}\n")

if __name__ == "__main__":
    main()
