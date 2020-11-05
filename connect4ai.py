STATE_WIDTH = 7
STATE_HEIGHT = 6
MAX_CONSECUTIVE = 4

'''
Game play functions
'''


def print_state(state) -> None:
    filled_state = fill_empty_entry(state)
    for row in range(STATE_HEIGHT - 1, -1, -1):
        str_row = ''
        for col in range(STATE_WIDTH):
            str_row += filled_state[col][row] + '\t'
        print(str_row)
    index_row = '\t'.join([str(col) for col in range(STATE_WIDTH)])
    print(index_row)


def fill_empty_entry(state: list) -> list:
    return [col + ['O'] * (7-len(col)) for col in state]


def out_of_bound_x(col_idx: int) -> bool:
    return col_idx >= STATE_WIDTH or col_idx < 0


def out_of_bound_y(row_idx: int) -> bool:
    return row_idx >= STATE_HEIGHT or row_idx < 0


def count_consecutive_chips_direction(col_idx: int, row_idx: int, filled_state: list, chip: str, direction: int) -> int:
    '''
    direction
    0 -> x
    1 -> y
    2 -> up right
    3 -> down right
    '''
    x_score = 0
    y_score = 0
    diag_score_up_right = 0
    diag_score_down_right = 0

    if direction == 0:
        for d_col in range(MAX_CONSECUTIVE):
            if not out_of_bound_x(col_idx + d_col) and filled_state[col_idx + d_col][row_idx] == chip:
                x_score += 1
            else:
                break
        return x_score
    elif direction == 1:
        for d_row in range(MAX_CONSECUTIVE):
            if not out_of_bound_y(row_idx + d_row) and filled_state[col_idx][row_idx + d_row] == chip:
                y_score += 1
            else:
                break
        return y_score
    elif direction == 2:
        for d_col_row in range(MAX_CONSECUTIVE):
            if not out_of_bound_x(col_idx + d_col_row) and not out_of_bound_y(row_idx + d_col_row) and filled_state[col_idx + d_col_row][row_idx + d_col_row] == chip:
                diag_score_up_right += 1
            else:
                break
        return diag_score_up_right
    else:
        for d_col_row in range(MAX_CONSECUTIVE):
            if not out_of_bound_x(col_idx + d_col_row) and not out_of_bound_y(row_idx - d_col_row) and filled_state[col_idx + d_col_row][row_idx - d_col_row] == chip:
                diag_score_down_right += 1
            else:
                break
        return diag_score_down_right


def count_consecutive_chips(col_idx: int, row_idx: int, filled_state: list, chip: str) -> int:
    x_score = count_consecutive_chips_direction(
        col_idx, row_idx, filled_state, chip, 0)
    y_score = count_consecutive_chips_direction(
        col_idx, row_idx, filled_state, chip, 1)
    diag_score_up_right = count_consecutive_chips_direction(
        col_idx, row_idx, filled_state, chip, 2)
    diag_score_down_right = count_consecutive_chips_direction(
        col_idx, row_idx, filled_state, chip, 3)

    return max(x_score, y_score, diag_score_up_right, diag_score_down_right)


def get_winner(state: list) -> str:
    max_A_score = -1
    max_B_score = -1
    filled_state = fill_empty_entry(state)
    for col_idx in range(STATE_WIDTH):
        for row_idx in range(STATE_HEIGHT):
            max_A_score = max(max_A_score, count_consecutive_chips(
                col_idx, row_idx, filled_state, 'A'))
            max_B_score = max(max_B_score, count_consecutive_chips(
                col_idx, row_idx, filled_state, 'B'))
            if max_A_score == MAX_CONSECUTIVE:
                return 'A'
            elif max_B_score == MAX_CONSECUTIVE:
                return 'B'
    return ''


def is_fullboard(state: list) -> bool:
    return count_depth(state) == STATE_WIDTH * STATE_HEIGHT


def get_chip(turn: bool) -> str:
    return 'A' if turn else 'B'


def clone_state(state: list) -> list:
    new_state = [col.copy() for col in state]
    return new_state


def insert_chip(turn: bool, col: int, state: list) -> (list, bool):
    chip = get_chip(turn)
    new_state = clone_state(state)
    if (len(new_state[col]) >= STATE_HEIGHT) or (col >= STATE_WIDTH):  # 0-based indexing
        return state, False

    new_state[col].append(chip)
    return new_state, True


'''
AI functions
'''


def count_depth(state: list) -> int:
    return sum([len(column) for column in state])


def is_terminal_state(state: list, turn: str) -> bool:
    '''
    returns whether turn wins or not
    '''
    max_score = -1
    chip = get_chip(turn)
    filled_state = fill_empty_entry(state)
    for col_idx in range(STATE_WIDTH):
        for row_idx in range(STATE_HEIGHT):
            max_score = max(max_score, count_consecutive_chips(
                col_idx, row_idx, filled_state, chip))
            if max_score == MAX_CONSECUTIVE:
                return True
    return False


def update_max_depth(state: list) -> int:
    global max_depth
    depth = count_depth(state)
    if depth < 5:
        max_depth = 4
    elif depth < 12:
        max_depth = 6
    elif depth < 24:
        max_depth = 8
    else:
        max_depth = 10


def minimax(state: list):
    update_max_depth(state)
    turn = False  # Let's B be the bot.
    alpha, beta = -2e9, 2e9
    max_val = -2e9
    best_action = -1
    # All actions
    for action in range(STATE_WIDTH):
        result_state, able_to_insert = insert_chip(turn, action, state)
        if able_to_insert:
            min_val = min_value_function(result_state, alpha, beta, 0)
            if min_val > max_val:
                best_action = action
                max_val = min_val
                alpha = max(alpha, max_val)
        else:
            continue

    return best_action


def min_value_function(state: list, alpha: int, beta: int, curr_depth: int) -> int:
    turn = True  # Player's turn
    if is_terminal_state(state, not turn):  # If AI win return score of 4
        return 1e9
    if curr_depth == max_depth:
        return magic_score(state)
    max_val = -1e9
    min_val = 1e9
    # All actions
    for action in range(STATE_WIDTH):
        result_state, able_to_insert = insert_chip(turn, action, state)
        if able_to_insert:
            max_val = max_value_function(
                result_state, alpha, beta, curr_depth + 1)
            min_val = min(min_val, max_val)
            if min_val < alpha:
                return min_val
            beta = min(beta, min_val)
        else:
            continue
    return min_val


def max_value_function(state: list, alpha: int, beta: int, curr_depth: int) -> int:
    turn = False  # AI's turn
    if is_terminal_state(state, not turn):  # If Player win return score of -4
        return -1e9
    if curr_depth == max_depth:
        return -magic_score(state)
    max_val = -1e9
    min_val = 1e9
    # All actions
    for action in range(STATE_WIDTH):
        result_state, able_to_insert = insert_chip(turn, action, state)
        if able_to_insert:
            min_val = min_value_function(
                result_state, alpha, beta, curr_depth + 1)
            max_val = max(min_val, max_val)
            if max_val > beta:
                return max_val
            alpha = max(alpha, max_val)
        else:
            continue
    return min_val


def magic_score(state: list):
    x_score = {'A': 0, 'B': 0}
    y_score = {'A': 0, 'B': 0}
    diag_score_up_right = {'A': 0, 'B': 0}
    diag_score_down_right = {'A': 0, 'B': 0}

    filled_state = fill_empty_entry(state)
    for col_idx in range(STATE_WIDTH):
        for row_idx in range(STATE_HEIGHT):
            for chip in ['A', 'B']:
                x_score[chip] = count_consecutive_chips_direction(
                    col_idx, row_idx, filled_state, chip, 0)
                y_score[chip] = count_consecutive_chips_direction(
                    col_idx, row_idx, filled_state, chip, 1)
                diag_score_up_right[chip] = count_consecutive_chips_direction(
                    col_idx, row_idx, filled_state, chip, 2)
                diag_score_down_right[chip] = count_consecutive_chips_direction(
                    col_idx, row_idx, filled_state, chip, 3)
    adjusted_score = 0
    for score in [x_score, y_score, diag_score_up_right, diag_score_down_right]:
        adjusted_score += score['B']/(score['A'] + 1e-9)

    return adjusted_score


'''Initial State'''
state = [[], [], [], [], [], [], []]
turn = True  # Player's turn
while not is_fullboard(state):
    print_state(state)
    if turn:
        col = int(
            input('{chip}\'s turn enter column: '.format(chip=get_chip(turn))))
    else:
        print('Bot\'s turn')
        col = minimax(state)
        print('column: {col}'.format(col=col))
    state, able_to_insert = insert_chip(turn, col, state)
    if not able_to_insert:
        print('You cannot insert at that')
    else:
        winner = get_winner(state)
        if winner:
            print('Winner is {winner}'.format(winner=winner))
            break
        turn = not turn
