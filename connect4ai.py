# state = [[],[],[],[],[],[],[]]
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


def count_consecutive_chips(col_idx: int, row_idx: int, filled_state: list, chip: str) -> int:
    x_score = 0
    y_score = 0
    diag_score_up_right = 0
    diag_score_down_right = 0

    for d_col in range(MAX_CONSECUTIVE):
        if not out_of_bound_x(col_idx + d_col) and filled_state[col_idx + d_col][row_idx] == chip:
            x_score += 1
        else:
            break

    for d_row in range(MAX_CONSECUTIVE):
        if not out_of_bound_y(row_idx + d_col) and filled_state[d_col][row_idx + d_row] == chip:
            y_score += 1
        else:
            break

    for d_col_row in range(MAX_CONSECUTIVE):
        if not out_of_bound_x(col_idx + d_col_row) and not out_of_bound_y(row_idx + d_col_row) and filled_state[col_idx + d_col_row][row_idx + d_col_row] == chip:
            diag_score_up_right += 1
        else:
            break

    for d_col_row in range(MAX_CONSECUTIVE):
        if not out_of_bound_x(col_idx + d_col_row) and not out_of_bound_y(row_idx - d_col_row) and filled_state[col_idx + d_col_row][row_idx - d_col_row] == chip:
            diag_score_down_right += 1
        else:
            break

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
    return sum([len(column) for column in state]) == STATE_WIDTH * STATE_HEIGHT


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


'''Initial State'''
state = [[], [], [], [], [], [], []]
turn = True
while not is_fullboard(state):
    print_state(state)
    col = int(input('{chip} turn enter column: '.format(chip=get_chip(turn))))
    state, able_to_insert = insert_chip(turn, col, state)
    if not able_to_insert:
        print('You cannot insert at that')
    else:
        winner = get_winner(state)
        if winner:
            print('Winner is {winner}'.format(winner=winner))
            break
        turn = not turn