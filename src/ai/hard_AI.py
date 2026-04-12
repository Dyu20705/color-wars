from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves

INF = 10**9
MAX_DEPTH = 3
MOVE_ORDER_TOP_K = 6


def _simulate_move(board, dots, move, player):
    row, col = move
    board_copy = [line[:] for line in board]
    dots_copy = [line[:] for line in dots]

    inc = get_move_dot_increment(board_copy, row, col)
    board_copy[row][col] = player
    dots_copy[row][col] += inc
    resolve_explosions(board_copy, dots_copy, row, col)
    return board_copy, dots_copy


def _normalized_features(board, dots):
    size = len(board)
    total = max(1, size * size)

    red_cells = 0
    blue_cells = 0
    red_dots = 0
    blue_dots = 0
    red_threat = 0
    blue_threat = 0
    red_stable = 0
    blue_stable = 0

    for r in range(size):
        for c in range(size):
            cell = board[r][c]
            dot = dots[r][c]
            if cell == PLAYER_RED:
                red_cells += 1
                red_dots += dot
                if dot >= 3:
                    red_threat += 1
                if dot <= 1:
                    red_stable += 1
            elif cell == PLAYER_BLUE:
                blue_cells += 1
                blue_dots += dot
                if dot >= 3:
                    blue_threat += 1
                if dot <= 1:
                    blue_stable += 1

    material_norm = (red_cells - blue_cells) / total
    mobility_norm = (len(get_valid_moves(board, PLAYER_RED)) - len(get_valid_moves(board, PLAYER_BLUE))) / total
    threat_norm = (red_threat - blue_threat) / total
    danger_norm = blue_threat / total
    stability_norm = (red_stable - blue_stable) / total
    dot_norm = (red_dots - blue_dots) / (total * 4.0)

    return material_norm, mobility_norm, threat_norm, danger_norm, stability_norm, dot_norm


def evaluate_board(board, dots):
    material_norm, mobility_norm, threat_norm, danger_norm, stability_norm, dot_norm = _normalized_features(
        board, dots
    )
    return (
        1.50 * material_norm
        + 0.70 * mobility_norm
        + 0.80 * threat_norm
        - 0.90 * danger_norm
        + 0.45 * stability_norm
        + 0.20 * dot_norm
    )


def _score_move(board, dots, move, player):
    next_board, next_dots = _simulate_move(board, dots, move, player)
    score = evaluate_board(next_board, next_dots)
    return score if player == PLAYER_RED else -score


def _ordered_moves(board, dots, player, top_k):
    moves = get_valid_moves(board, player)
    if not moves:
        return []

    scored = [(move, _score_move(board, dots, move, player)) for move in moves]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [move for move, _ in scored[: min(top_k, len(scored))]]


def _alphabeta(board, dots, depth, alpha, beta, player):
    moves = get_valid_moves(board, player)
    if depth == 0 or not moves:
        return evaluate_board(board, dots), None

    next_player = PLAYER_BLUE if player == PLAYER_RED else PLAYER_RED
    ordered = _ordered_moves(board, dots, player, MOVE_ORDER_TOP_K)

    if player == PLAYER_RED:
        best_score = -INF
        best_move = None
        for move in ordered:
            nboard, ndots = _simulate_move(board, dots, move, player)
            score, _ = _alphabeta(nboard, ndots, depth - 1, alpha, beta, next_player)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_move

    best_score = INF
    best_move = None
    for move in ordered:
        nboard, ndots = _simulate_move(board, dots, move, player)
        score, _ = _alphabeta(nboard, ndots, depth - 1, alpha, beta, next_player)
        if score < best_score:
            best_score = score
            best_move = move
        beta = min(beta, best_score)
        if alpha >= beta:
            break
    return best_score, best_move


def get_hard_move(board, dots):
    """Choose the strongest move found by a fixed-depth alpha-beta search."""
    moves = get_valid_moves(board, PLAYER_RED)
    if not moves:
        return None

    if len(moves) == 1:
        return moves[0]

    _, best_move = _alphabeta(board, dots, MAX_DEPTH, -INF, INF, PLAYER_RED)
    return best_move if best_move in moves else moves[0]
