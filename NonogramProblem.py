from board import Board, CSPBoard
import display
import time

class Nonogram():
    """Abstract  Class"""
    def __init__(self, board_w, board_h, row_cond, col_cond):
        self._board = Board(board_w, board_h, row_cond, col_cond)
        self.expanded = 0

    def get_start_state(self):
        return self._board

    def is_goal_state(self, state):
        if not state.state.all(): # in case the board is not full yet.
            return False
        for i, row in enumerate(state.state):
            if not self._check_line_conditions(row, state.row_cond[i]):
                return False
        for j, col in enumerate(state.state.T):
            if not self._check_line_conditions(col, state.col_cond[j]):
                return False
        return True

    def get_successors(self, state, **kwargs):
        pass

    def _check_line_conditions(self, line, cond):
        curr_block = 0
        blocks = []
        for i in line:
            if i == 1:
                curr_block += 1
            else:
                if curr_block != 0:
                    blocks.append(curr_block)
                    curr_block = 0
        if curr_block != 0:
            blocks.append(curr_block)
        if len(blocks) < len(cond):
            blocks = blocks + [0] * (len(cond) - len(blocks))
        return blocks == cond

    def show(self):
        display.display_board(self._board)

    def fill_cells(self, moves):
        for m in moves:
            self._board.add_move(m)
            display.print_to_cmd(self._board)
            time.sleep(0.2)


# ============================================================================================
# =============================== Nonogram Problems ==========================================
# ============================================================================================

class NonogramCellsProblem(Nonogram):
    def __init__(self, board_w, board_h, row_cond, col_cond):
        Nonogram.__init__(self, board_w, board_h, row_cond, col_cond)

    def get_successors(self, state, **kwargs):
        self.expanded += 1
        return [(state.get_move_result(move), move) for move in state.get_legal_moves()]

# ============================================================================================


class NonogramLinesProblem(Nonogram):
    def __init__(self, board_w, board_h, row_cond, col_cond):
        Nonogram.__init__(self, board_w, board_h, row_cond, col_cond)

    def get_successors(self, state, **kwargs):
        self.expanded += 1
        if state.unassigned_rows:
            next_row = state.unassigned_rows.pop(0)
            return [(state.get_move_result(move), move) for move in state.get_legal_moves_for_row(next_row)]
        else:
            return []

    def is_goal_state(self, state):
        if not state.state.all(): # in case the board is not full yet.
            return False
        for j, col in enumerate(state.state.T):
            if not self._check_line_conditions(col, state.col_cond[j]):
                return False
        return True

# ============================================================================================


class NonogramCSP(Nonogram):
    def __init__(self, board_w, board_h, row_cond, col_cond):
        Nonogram.__init__(self, board_w, board_h, row_cond, col_cond)
        self._board = CSPBoard(board_w, board_h, row_cond, col_cond)

    def get_successors(self, state, **kwargs):
        self.expanded += 1
        if state.unassigned_rows:
            next_row = state.unassigned_rows.pop(0)
            return [(state.get_move_result(move), move) for move in state.get_legal_moves_for_row(next_row)]
        else:
            return []

    def get_successors_mrv(self, state, **kwargs):
        self.expanded += 1
        var, is_col = state.get_next_variable_to_assign()
        if var == (-1):
            return []
        return [(state.get_move_result(move), move) for move in state.get_legal_moves_for_row(var, is_col)]

    def is_goal_state(self, state):
        if not state.state.all():  # in case the board is not full yet.
            return False
        for i, row in enumerate(state.state):
            if not self._check_line_conditions(row, state.row_cond[i]):
                return False
        for j, col in enumerate(state.state.T):
            if not self._check_line_conditions(col, state.col_cond[j]):
                return False
        return True

    def forward_checking(self, state):
        return state.update_valid_moves_sets()

    def arc_checking(self, state):
        return state.continuous_update_valid_moves_sets()

# ===================================================================
# ===================== SEARCH ALGORITHMS ===========================
# ===================================================================


def depth_first_search(nono):
    '''
    Search the deepest nodes in the search tree first.
    :param nono: NonogramCells or NonogramLines object.
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []


def mrv_dfs(nono):
    '''
    Search the deepest nodes in the search tree first, with mrv approach.
    :param nono: NonogramCSP object
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors_mrv(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []


def forward_checking_dfs(nono):
    '''
    Search the deepest nodes in the search tree first, with forward checking approach.
    :param nono: NonogramCSP object
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if not nono.forward_checking(current_s):
            continue
        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []


def forward_checking_mrv_dfs(nono):
    '''
    :param nono: NonogramCSP object
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if not nono.forward_checking(current_s):
            continue
        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors_mrv(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []


def arc_dfs(nono):
    '''
    Search the deepest nodes in the search tree first, with forward checking approach.
    :param nono: NonogramCSP object
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if not nono.arc_checking(current_s):
            continue
        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []


def arc_mrv_dfs(nono):
    '''
    :param nono: NonogramCSP object
    :return: actions that leads to goal state.
    '''
    visited = set()
    fringe = [(nono.get_start_state(), [])]

    while fringe:
        current_s, actions = fringe[-1]
        fringe = fringe[:-1]

        if not nono.arc_checking(current_s):
            continue
        if nono.is_goal_state(current_s):
            return actions
        elif current_s not in visited:
            visited.add(current_s)
            successors = nono.get_successors_mrv(current_s)
            for state, act in successors:
                fringe.append((state, actions + [act]))

    print("can't find solution...")
    return []