# ai.py
from copy import deepcopy
from collections import deque


# ---------------------------------------------------------------------------
# BFS shortest path - works directly on GameLogic object
# ---------------------------------------------------------------------------

def shortest_path_length(logic, player):
    """Returns BFS distance for a player to reach their goal row."""
    if player == "AI":
        start    = logic.player2_pos
        goal_row = 8
    else:
        start    = logic.player1_pos
        goal_row = 0

    queue   = deque([(start, 0)])
    visited = {start}

    while queue:
        (r, c), dist = queue.popleft()
        if r == goal_row:
            return dist
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < logic.board_size and 0 <= nc < logic.board_size:
                if (nr, nc) not in visited and not logic.is_move_blocked_by_wall(r, c, nr, nc):
                    visited.add((nr, nc))
                    queue.append(((nr, nc), dist + 1))
    return 999


# ---------------------------------------------------------------------------
# Get valid wall placements - works directly on GameLogic object
# ---------------------------------------------------------------------------

def get_valid_walls(logic):
    """Returns list of (r, c, orient) tuples for all valid wall placements."""
    walls = []
    if logic.player2_walls_left <= 0:
        return walls
    for r in range(logic.board_size - 1):
        for c in range(logic.board_size - 1):
            for orient in ('H', 'V'):
                if logic.is_wall_placement_valid(r, c, orient):
                    walls.append((r, c, orient))
    return walls


# ---------------------------------------------------------------------------
# Easy AI - greedy: just move the pawn closer to the goal
# ---------------------------------------------------------------------------

def get_easy_move(logic):
    valid_moves = logic.get_valid_moves(logic.player2_pos, logic.player1_pos)

    best_move = None
    best_dist = float('inf')

    for move in valid_moves:
        temp = deepcopy(logic)
        temp.move_pawn(move[0], move[1])
        dist = shortest_path_length(temp, "AI")
        if dist < best_dist:
            best_dist = dist
            best_move = ("move", move)

    return best_move


# ---------------------------------------------------------------------------
# Medium AI - greedy advance + try blocking walls when human is close
# ---------------------------------------------------------------------------

def get_medium_move(logic):
    ai_dist  = shortest_path_length(logic, "AI")
    hum_dist = shortest_path_length(logic, "HUMAN")

    # If human is at least as close, try to place a blocking wall
    if hum_dist <= ai_dist and logic.player2_walls_left > 0:
        walls = get_valid_walls(logic)

        best_wall  = None
        best_score = -float('inf')

        for (r, c, orient) in walls:
            temp = deepcopy(logic)
            temp.place_wall(r, c, orient)
            new_hum_dist = shortest_path_length(temp, "HUMAN")
            score = new_hum_dist - hum_dist
            if score > best_score:
                best_score = score
                best_wall  = (r, c, orient)

        if best_wall and best_score > 0:
            return ("wall", best_wall)

    return get_easy_move(logic)


# ---------------------------------------------------------------------------
# Hard AI - Minimax with Alpha-Beta pruning (depth 3)
# ---------------------------------------------------------------------------

def get_hard_move(logic, depth=3):
    _, best_move = minimax(logic, depth, -float('inf'), float('inf'), True)
    return best_move or get_easy_move(logic)


def evaluate_state(logic):
    ai_dist  = shortest_path_length(logic, "AI")
    hum_dist = shortest_path_length(logic, "HUMAN")

    score  = (hum_dist - ai_dist) * 10
    score += logic.player2_walls_left * 2
    score -= logic.player1_walls_left

    if ai_dist  == 0: score += 1000
    if hum_dist == 0: score -= 1000

    return score


def minimax(logic, depth, alpha, beta, maximizing_player):
    # Stop condition
    winner = logic.check_win_condition()
    if depth == 0 or winner != 0:
        return evaluate_state(logic), None

    if maximizing_player:
        max_eval  = -float('inf')
        best_move = None

        # AI moves (player 2)
        possible_moves = [("move", m) for m in logic.get_valid_moves(logic.player2_pos, logic.player1_pos)]
        possible_moves += [("wall", w) for w in get_valid_walls(logic)]

        for action in possible_moves:
            temp = deepcopy(logic)

            if action[0] == "move":
                temp.move_pawn(action[1][0], action[1][1])
            else:
                r, c, orient = action[1]
                temp.place_wall(r, c, orient)

            evaluation, _ = minimax(temp, depth - 1, alpha, beta, False)

            if evaluation > max_eval:
                max_eval  = evaluation
                best_move = action

            alpha = max(alpha, evaluation)

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return max_eval, best_move

    else:
        min_eval  = float('inf')
        best_move = None

        # Human moves (player 1)
        possible_moves = [("move", m) for m in logic.get_valid_moves(logic.player1_pos, logic.player2_pos)]
        possible_moves += [("wall", w) for w in get_valid_walls(logic)]

        for action in possible_moves:
            temp = deepcopy(logic)

            if action[0] == "move":
                temp.move_pawn(action[1][0], action[1][1])
            else:
                r, c, orient = action[1]
                temp.place_wall(r, c, orient)

            evaluation, _ = minimax(temp, depth - 1, alpha, beta, True)

            if evaluation < min_eval:
                min_eval  = evaluation
                best_move = action

            beta = min(beta, evaluation)

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return min_eval, best_move


# ---------------------------------------------------------------------------
# Public dispatcher - called by board_ui.py
# ---------------------------------------------------------------------------

def get_ai_move(logic, difficulty="medium"):
    if difficulty == "easy":
        return get_easy_move(logic)
    elif difficulty == "hard":
        return get_hard_move(logic)
    else:
        return get_medium_move(logic)
