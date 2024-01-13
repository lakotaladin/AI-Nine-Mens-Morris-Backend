SET_STONE = 'set'
MOVE_STONE = 'move'
REMOVE_STONE = 'remove'

WHITE = 1
BLACK = -1

MOVE_TYPE = 0
MOVE_COLOR = 1
MOVE_X = 2
MOVE_Y = 3
MOVE_Z = 4


def is_end(state):
    return state['white_remaining'] == 0 and state['black_remaining'] == 0 and (state['white_count'] <= 2 or state['black_count'] <= 2)


def evaluate(state):
    stones = state['stones']
    
    value = 0
    
    for square in range(3):
        for line in [0, 2]:
            line_sum = 0
            for spot in range(3):
                line_sum += stones[square][line][spot]
            
            if abs(line_sum) > 1:
                value += line_sum * 10
                
    for square in range(3):
        for line in [0, 2]:
            line_sum = 0
            for spot in range(3):
                line_sum += stones[square][spot][line]

            if abs(line_sum) > 1:
                value += line_sum * 10
    
    value += state['white_count'] * 5
    value -= state['black_count'] * 5
    return value


def get_neighboaring_empty_spots(state, x, y, z):
    stones = state['stones']
    
    # left
    if y != 1 and z - 1 >= 0 and stones[x][y][z - 1] == 0:
        yield x, y, z - 1
    
    # right
    if y != 1 and z + 1 <= 2 and stones[x][y][z + 1] == 0:
        yield x, y, z + 1
    
    # up
    if z != 1 and y - 1 >= 0 and stones[x][y - 1][z] == 0:
        yield x, y - 1, z
    
    # down
    if z != 1 and y + 1 <= 2 and stones[x][y + 1][z] == 0:
        yield x, y + 1, z
    
    # cross-square out
    if (y == 1 or z == 1) and x - 1 >= 0 and stones[x - 1][y][z] == 0:
        yield x - 1, y, z
    
    # cross-square in
    if (y == 1 or z == 1) and x + 1 <= 2 and stones[x + 1][y][z] == 0:
        yield x + 1, y, z


def get_moves(state, player, line_made):
    # REMOVE_STATE moves
    if line_made:
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    if element == player * -1:
                        yield REMOVE_STONE, player, s, i, j
                        
        return
    
    # SET_STONE moves
    if state['white_remaining' if player == 1 else 'black_remaining'] > 0:
        for s, square in enumerate(state['stones']):
            for i, row in enumerate(square):
                for j, element in enumerate(row):
                    if i == 1 and j == 1:
                        continue
                    if element == 0:
                        yield SET_STONE, player, s, i, j
                    
        return
    
    # MOVE_STONE moves
    for s, square in enumerate(state['stones']):
        for i, row in enumerate(square):
            for j, element in enumerate(row):
                if element == player:
                    for x, y, z in get_neighboaring_empty_spots(state, s, i, j):
                        yield MOVE_STONE, player, x, y, z, s, i, j


def is_making_line(state, move):
    stones = state['stones']
    _, _, x, y, z, *_ = move
    
    # check if this move makes new horizontal line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[x][y][i]
        
    if abs(stones_sum) == 3:
        return True
    
    # check if this move makes new vertical line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[x][i][z]
        
    if abs(stones_sum) == 3:
        return True
    
    # check if this move makes new cross-sqare top line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[i][0][1]
    
    if abs(stones_sum) == 3:
        return True
    
    # check if this move makes new cross-sqare bottom line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[i][2][1]
        
    if abs(stones_sum) == 3:
        return True
    
    # check if this move makes new cross-sqare left line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[i][1][0]

    if abs(stones_sum) == 3:
        return True

    # check if this move makes new cross-sqare right line
    stones_sum = 0
    for i in range(3):
        stones_sum += stones[i][1][2]

    if abs(stones_sum) == 3:
        return True
    
    return False


def apply_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:
        _, color, x, y, z = move
        stones[x][y][z] = color
        state['white_remaining' if color == WHITE else 'black_remaining'] -= 1
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == REMOVE_STONE:
        _, color, x, y, z = move
        stones[x][y][z] = 0
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == MOVE_STONE:
        _, color, to_x, to_y, to_z, from_x, from_y, from_z = move
        stones[from_x][from_y][from_z] = 0
        stones[to_x][to_y][to_z] = color
        
    state['turn'] += 1


def undo_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:
        _, color, x, y, z = move
        stones[x][y][z] = 0
        state['white_remaining' if color == WHITE else 'black_remaining'] += 1
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == REMOVE_STONE:
        _, color, x, y, z = move
        stones[x][y][z] = color * -1
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == MOVE_STONE:
        _, color, to_x, to_y, to_z, from_x, from_y, from_z = move
        stones[from_x][from_y][from_z] = color
        stones[to_x][to_y][to_z] = 0
    
    state['turn'] += 1


# def minimax(state, depth, player, line_made = False):
#     if depth == 0 or is_end(state):
#         return evaluate(state), None

#     next_player = player * -1
    
#     if player == WHITE:
#         value = -1000000
#         best_move = None
#         for move in get_moves(state, player, line_made):
#             apply_move(state, move)
#             if is_making_line(state, move):
#                 next_player *= -1
#                 line_made = True
#             value = max(value, minimax(state, depth - 1, next_player, line_made)[0])
#             best_move = move
#             line_made = False
#             undo_move(state, move)
#         return value, best_move
#     else:
#         value = 1000000
#         best_move = None
#         for move in get_moves(state, player, line_made):
#             apply_move(state, move)
#             if is_making_line(state, move):
#                 next_player *= -1
#                 line_made = True
#             value = min(value, minimax(state, depth - 1, next_player, line_made)[0])
#             best_move = move
#             line_made = False
#             undo_move(state, move)
#         return value, best_move

def minimax(state, depth, player, line_made=False, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or is_end(state):
        return evaluate(state), None

    next_player = player * -1

    if player == WHITE:
        value = float('-inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            new_value = minimax(state, depth - 1, next_player, line_made, alpha, beta)[0]
            if new_value > value:
                value = new_value
                best_move = move
            line_made = False
            undo_move(state, move)
            alpha = max(alpha, value)
            if value >= beta:
                break
        return value, best_move
    else:
        value = float('inf')
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            new_value = minimax(state, depth - 1, next_player, line_made, alpha, beta)[0]
            if new_value < value:
                value = new_value
                best_move = move
            line_made = False
            undo_move(state, move)
            beta = min(beta, value)
            if value <= alpha:
                break
        return value, best_move    

def alphabeta(state, depth, a, b, player, line_made = False):
    if depth == 0 or is_end(state):
        return evaluate(state), None

    next_player = player * -1
    
    if player == WHITE:
        value = -1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            value = max(value, alphabeta(state, depth - 1, a, b, next_player, line_made)[0])
            best_move = move
            line_made = False
            undo_move(state, move)
            if value > b:
                break
            a = max(a, value)
        return value, best_move
    else:
        value = 1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            value = min(value, alphabeta(state, depth - 1, a, b, next_player, line_made)[0])
            best_move = move
            line_made = False
            undo_move(state, move)
            if value < a:
                break
            b = min(b, value)
        return value, best_move
