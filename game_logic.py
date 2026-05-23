# game_logic.py
class GameLogic:
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.reset_state()

    def reset_state(self):
        self.player1_pos = (8, 4)  # Red starts at center baseline
        self.player2_pos = (0, 4)  # Blue starts at center baseline
        self.player1_walls_left = 10
        self.player2_walls_left = 10
        self.walls_h = set()       # Stores (row, col) of horizontal walls
        self.walls_v = set()       # Stores (row, col) of vertical walls
        self.current_player = 1
        self.game_over = False

    def is_move_blocked_by_wall(self, r1, c1, r2, c2):
        """Checks if a direct orthogonal step between two cells is blocked by a wall."""
        if r2 == r1 + 1 and c1 == c2:    # Down
            return (r1, c1) in self.walls_h or (r1, c1 - 1) in self.walls_h
        if r2 == r1 - 1 and c1 == c2:    # Up
            return (r2, c1) in self.walls_h or (r2, c1 - 1) in self.walls_h
        if c2 == c1 + 1 and r1 == r2:    # Right
            return (r1, c1) in self.walls_v or (r1 - 1, c1) in self.walls_v
        if c2 == c1 - 1 and r1 == r2:    # Left
            return (r1, c2) in self.walls_v or (r1 - 1, c2) in self.walls_v
        return False

    def get_valid_moves(self, current_pos, opponent_pos):
        """Calculates legal 1-step orthogonal moves, pawn jumps, and diagonal escapes."""
        r, c = current_pos
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            if 0 <= next_r < self.board_size and 0 <= next_c < self.board_size:
                if self.is_move_blocked_by_wall(r, c, next_r, next_c):
                    continue
                
                # If adjacent to opponent, handle jumping logic
                if (next_r, next_c) == opponent_pos:
                    jump_r, jump_c = next_r + dr, next_c + dc
                    straight_blocked = (
                        not (0 <= jump_r < self.board_size and 0 <= jump_c < self.board_size) or 
                        self.is_move_blocked_by_wall(next_r, next_c, jump_r, jump_c)
                    )
                    if not straight_blocked:
                        valid_moves.append((jump_r, jump_c))  # Standard straight jump
                    else:
                        # Special Case: Jump is blocked by wall/edge -> diagonal escapes
                        side_dirs = [(0, -1), (0, 1)] if dr != 0 else [(-1, 0), (1, 0)]
                        for s_dr, s_dc in side_dirs:
                            diag_r, diag_c = next_r + s_dr, next_c + s_dc
                            if 0 <= diag_r < self.board_size and 0 <= diag_c < self.board_size:
                                if not self.is_move_blocked_by_wall(next_r, next_c, diag_r, diag_c):
                                    valid_moves.append((diag_r, diag_c))
                else:
                    valid_moves.append((next_r, next_c))  # Open tile move
        return valid_moves

    def check_geometric_validity(self, r, c, orientation):
        """Ensures walls stay on the board boundaries, don't overlap, and don't cross."""
        if r >= self.board_size - 1 or c >= self.board_size - 1 or r < 0 or c < 0:
            return False
        if orientation == 'H':
            if (r, c) in self.walls_h or (r, c + 1) in self.walls_h or (r, c - 1) in self.walls_h or (r, c) in self.walls_v:
                return False
        else:
            if (r, c) in self.walls_v or (r + 1, c) in self.walls_v or (r - 1, c) in self.walls_v or (r, c) in self.walls_h:
                return False
        return True

    def bfs_has_path(self, start_pos, goal_row):
        """Mandatory pathfinding check to ensure a route to the goal always exists."""
        queue = [start_pos]
        visited = {start_pos}
        while queue:
            curr_r, curr_c = queue.pop(0)
            if curr_r == goal_row:
                return True
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    if (nr, nc) not in visited and not self.is_move_blocked_by_wall(curr_r, curr_c, nr, nc):
                        visited.add((nr, nc))
                        queue.append((nr, nc))
        return False

    def is_wall_placement_valid(self, r, c, orientation):
        """Verifies wall validation by speculatively adding it and running BFS."""
        walls_left = self.player1_walls_left if self.current_player == 1 else self.player2_walls_left
        if walls_left <= 0 or not self.check_geometric_validity(r, c, orientation):
            return False

        if orientation == 'H': self.walls_h.add((r, c))
        else: self.walls_v.add((r, c))

        # Check if BOTH players still have a valid path to their respective baseline goals
        path_valid = self.bfs_has_path(self.player1_pos, 0) and self.bfs_has_path(self.player2_pos, 8)

        if orientation == 'H': self.walls_h.remove((r, c))
        else: self.walls_v.remove((r, c))
        
        return path_valid

    def place_wall(self, r, c, orientation):
        if orientation == 'H':
            self.walls_h.add((r, c))
        else:
            self.walls_v.add((r, c))
        if self.current_player == 1:
            self.player1_walls_left -= 1
            self.current_player = 2
        else:
            self.player2_walls_left -= 1
            self.current_player = 1

    def move_pawn(self, row, col):
        if self.current_player == 1:
            self.player1_pos = (row, col)
            self.current_player = 2
        else:
            self.player2_pos = (row, col)
            self.current_player = 1

    def check_win_condition(self):
        """Returns winner ID if a player has reached the opposite side baseline."""
        if self.player1_pos[0] == 0: return 1
        if self.player2_pos[0] == 8: return 2
        return 0