from copy import deepcopy

    
from gamelogic import (
    get_valid_moves,
    get_valid_walls,
    apply_move,
    check_winner,
    shortest_path_length
)



def get_easy_move(game_state):
    ai_moves = get_valid_moves(game_state, player="AI")

    best_move = None
    shortest_distance = float('inf')

    for move in ai_moves:
        temp_state = deepcopy(game_state)
        apply_move(temp_state, move)

        distance = shortest_path_length(temp_state, player="AI")

        if distance < shortest_distance:
            shortest_distance = distance
            best_move = move

    return best_move




def get_medium_move(game_state):
    ai_distance = shortest_path_length(game_state, "AI")
    human_distance = shortest_path_length(game_state, "HUMAN")

    # Try defensive wall
    if human_distance <= ai_distance and game_state["AI"]["walls"] > 0:
        walls = get_valid_walls(game_state)

        best_wall = None
        best_block_score = -float('inf')

        for wall in walls:
            temp_state = deepcopy(game_state)
            apply_move(temp_state, wall)

            new_human_distance = shortest_path_length(temp_state, "HUMAN")

            score = new_human_distance - human_distance

            if score > best_block_score:
                best_block_score = score
                best_wall = wall

        if best_wall:
            return best_wall

    
    return get_easy_move(game_state)





def get_hard_move(game_state, depth=3):
    _, best_move = minimax(
        game_state,
        depth,
        alpha=-float('inf'),
        beta=float('inf'),
        maximizing_player=True
    )

    return best_move






def minimax(game_state, depth, alpha, beta, maximizing_player):

    winner = check_winner(game_state)

    # Stop condition
    if depth == 0 or winner:

        return evaluate_state(game_state), None
    
    if maximizing_player:

        max_eval = -float('inf')

        best_move = None

        possible_actions = (
            get_valid_moves(game_state, "AI")
            + get_valid_walls(game_state)
        )

        for action in possible_actions:

            temp_state = deepcopy(game_state)

            apply_move(temp_state, action)

            evaluation, _ = minimax(
                temp_state,
                depth - 1,
                alpha,
                beta,
                False
            )

            if evaluation > max_eval:

                max_eval = evaluation

                best_move = action

            alpha = max(alpha, evaluation)

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return max_eval, best_move



    else:

        min_eval = float('inf')

        best_move = None

        possible_actions = (
            get_valid_moves(game_state, "HUMAN")
            + get_valid_walls(game_state)
        )

        for action in possible_actions:

            temp_state = deepcopy(game_state)

            apply_move(temp_state, action)

            evaluation, _ = minimax(
                temp_state,
                depth - 1,
                alpha,
                beta,
                True
            )

            if evaluation < min_eval:

                min_eval = evaluation

                best_move = action

            beta = min(beta, evaluation)

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return min_eval, best_move
    





def evaluate_state(game_state):

    ai_distance = shortest_path_length(game_state, "AI")

    human_distance = shortest_path_length(game_state, "HUMAN")

    ai_walls = game_state["AI"]["walls"]

    human_walls = game_state["HUMAN"]["walls"]

    score = 0

    # Path advantage
    score += (human_distance - ai_distance) * 10

    # Wall advantage
    score += ai_walls * 2

    score -= human_walls

    # AI winning
    if ai_distance == 0:

        score += 1000

    # Human winning
    if human_distance == 0:

        score -= 1000

    return score