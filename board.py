import numpy as np
import copy


class Board:

    def __init__(self, board_w, board_h, row_cond, col_cond):
        self.board_w = board_w
        self.board_h = board_h
        self.row_cond = row_cond  # List (of lists) of the Nonogram conditions.
        self.col_cond = col_cond
        self.state = np.zeros((board_h, board_w))
        self.unassigned_rows = [i for i in range(board_h)]

    def __copy__(self):
        c_board = Board(self.board_w, self.board_h, self.row_cond, self.col_cond)
        c_board.state = np.copy(self.state)
        c_board.unassigned_rows = copy.copy(self.unassigned_rows)
        return c_board

    def add_move(self, move):
        if isinstance(move, SMove):
            self.state[move.x, move.y] = move.content

        elif isinstance(move, CMove):
            if move.col_move:
                self.state[:, move.idx] = move.content
            else: #row move:
                self.state[move.idx] = move.content

    def get_move_result(self, move):
        '''
        Creates a copy and apply the move on it.
        :return The copy.
        '''
        c_board = self.__copy__()
        c_board.add_move(move)
        return c_board

    def get_legal_moves(self):
        options = np.argwhere(self.state == 0)
        move_lst = []
        for op in options:
            move_lst.append(SMove(1, op[0], op[1]))
            move_lst.append(SMove(-1, op[0], op[1]))
        return move_lst

    def get_legal_moves_for_row(self, num, for_col=False):
        '''
        Returns list of legal moves for the row/col, (CRMove objects)
        '''
        k = len(self.row_cond[num]) + 1
        n = self.board_w - sum(self.row_cond[num]) - len(self.row_cond[num]) + 1
        cond = self.row_cond[num]
        size = self.board_w
        if for_col:
            k = len(self.col_cond[num]) + 1
            n = self.board_h - sum(self.col_cond[num]) - len(self.col_cond[num]) + 1
            cond = self.col_cond[num]
            size= self.board_h

        if n > 0:
            a = np.eye(k)
            l = [a]
            for i in range(1, n):
                temp = np.eye(k)
                new_l = []
                for m in l:
                    for j in range(k):
                        new_l.append(m + np.roll(temp, j, axis=1))
                l = new_l.copy()
            perm = np.concatenate(l, axis=0)
            perm = np.unique(perm, axis=0)
        else:
            perm = np.array([[0]*k])

        all_moves = []
        perm += np.array([0] + [1]*(k-2) + [0])
        perm += np.array([0] + cond)
        perm = perm.cumsum(axis=1)[:, :-1]
        for p in perm:
            b_pos = p.astype(int)
            v = (-np.ones(size))
            for i, b_seq in enumerate(cond):
                v[b_pos[i]: b_pos[i] + b_seq] = 1
            all_moves.append(CMove(num, v, col_move=for_col))
        return all_moves


class CSPBoard(Board):
    def __init__(self, board_w, board_h, row_cond, col_cond):
        Board.__init__(self, board_w, board_h, row_cond, col_cond)
        self.row_valid_moves = [Board.get_legal_moves_for_row(self, row) for row in range(board_h)]
        self.col_valid_moves = [Board.get_legal_moves_for_row(self, col, for_col=True) for col in range(board_w)]
        self.unassigned_cols = [i for i in range(board_w)]
        self.last_move = None

    def __copy__(self):
        c_board = CSPBoard(self.board_w, self.board_h, self.row_cond, self.col_cond)
        c_board.state = np.copy(self.state)
        c_board.unassigned_rows = copy.copy(self.unassigned_rows)
        c_board.unassigned_cols = copy.copy(self.unassigned_cols)
        c_board.row_valid_moves = copy.copy(self.row_valid_moves)
        c_board.col_valid_moves = copy.copy(self.col_valid_moves)
        c_board.last_move = self.last_move
        return c_board

    def add_move(self, move):
        if move.col_move:
            self.state[:, move.idx] = move.content
            self.col_valid_moves[move.idx] = [move]
        else: #row move:
            self.state[move.idx] = move.content
            self.row_valid_moves[move.idx] = [move]
        self.last_move = move

    def get_next_variable_to_assign(self):
        '''
        Use for MRV method
        '''
        if self.state.all():
            return -1, False
        assert (self.unassigned_cols or self.unassigned_rows), "no options for next move"
        min_row_moves_num = np.inf
        min_col_moves_num = np.inf
        new_row = -1
        new_col = -1
        for row_num in self.unassigned_rows:
            row_moves_num = len(self.row_valid_moves[row_num])
            if row_moves_num < min_row_moves_num:
                min_row_moves_num = row_moves_num
                new_row = row_num
        for col_num in self.unassigned_cols:
            col_moves_num = len(self.col_valid_moves[col_num])
            if col_moves_num < min_col_moves_num:
                min_col_moves_num = col_moves_num
                new_col = col_num
        if min_row_moves_num <= min_col_moves_num and new_row != (-1):
            is_col = False
            var = new_row
            self.unassigned_rows.remove(new_row)
        else:
            is_col = True
            var = new_col
            self.unassigned_cols.remove(new_col)
        return var, is_col

    def create_vector_for_move(self, move):
        vector = np.zeros(self.board_w)
        for i, black_part_len in enumerate(self.row_cond[move.row_num]):
            start_idx = move.content[i]
            vector[start_idx : start_idx + black_part_len] = 1
        return vector

    def has_collision(self, move, assignment, intersection_index):
        '''
        checks if a certain row move contradicts the given column move to check
        row move represented by row_num, and assignment to the intersection cell between the given column to check
        :param move: move(assignment) for column to check
        :param assignment: an integer 0/1 which indicates what was assigned to this column by a row move
        :return: True for collision and False otherwise.
        '''
        return move.content[intersection_index] != assignment

    def continuous_update_valid_moves_sets(self):
        '''
        Use for Arc checking method
        '''
        if self.last_move is None:
            return True
        col_update = self.last_move.col_move
        row_sets_len = [len(self.row_valid_moves[i]) for i in self.unassigned_rows]
        col_sets_len = [len(self.col_valid_moves[i]) for i in self.unassigned_cols]
        rows_to_check = [i for i in range(self.board_h) if i not in self.unassigned_rows]
        cols_to_check = [i for i in range(self.board_w) if i not in self.unassigned_cols]
        while(True):
            if col_update:
                for col_num in cols_to_check:
                    for col_move in self.col_valid_moves[col_num]:
                        for row_num in self.unassigned_rows:
                            row_moves = self.row_valid_moves[row_num]
                            row_assignment = col_move.content[row_num]
                            self.row_valid_moves[row_num] = [move for move in row_moves if not self.has_collision
                                (move, row_assignment, col_num)]
                            if len(self.row_valid_moves[row_num]) == 0:
                                return False
                curr_row_sets_len = [len(self.row_valid_moves[i]) for i in self.unassigned_rows]
                if curr_row_sets_len != row_sets_len:
                    rows_to_check = []
                    for j in range(len(curr_row_sets_len)):
                        if curr_row_sets_len[j] != row_sets_len[j] and curr_row_sets_len[j]==1:
                            rows_to_check.append(self.unassigned_rows[j])
                    row_sets_len = curr_row_sets_len.copy()
                    col_update = not col_update
                    if len(rows_to_check) == 0:
                        return True
                    continue
            else:
                for row_num in rows_to_check:

                    for row_move in self.row_valid_moves[row_num]:
                        for col_num in self.unassigned_cols:
                            col_moves = self.col_valid_moves[col_num]
                            col_assignment = row_move.content[col_num]
                            self.col_valid_moves[col_num] = [move for move in col_moves if not self.has_collision
                                (move, col_assignment, row_num)]
                            if len(self.col_valid_moves[col_num]) == 0:
                                return False
                curr_col_sets_len = [len(self.col_valid_moves[i]) for i in self.unassigned_cols]
                if curr_col_sets_len != col_sets_len:
                    cols_to_check = []
                    for j in range(len(curr_col_sets_len)):
                        if curr_col_sets_len[j] != col_sets_len[j] and curr_col_sets_len[j]==1:
                            cols_to_check.append(self.unassigned_cols[j])

                    col_sets_len = curr_col_sets_len.copy()
                    col_update = not col_update
                    if len(cols_to_check) == 0:
                        return True
                    continue
            break
        return True

    def update_valid_moves_sets(self):
        '''
        Use for Forward checking method.
        '''
        # updates moves for rows & cols, if any set is empty-> cut tree (return False)
        if self.last_move is None:
            return True
        vector = self.last_move.content
        if self.last_move.col_move:
            for row_num in self.unassigned_rows:
                row_moves = self.row_valid_moves[row_num]
                row_assignment = vector[row_num]
                self.row_valid_moves[row_num] = [move for move in row_moves if not self.has_collision
                (move, row_assignment, self.last_move.idx)]
                if len(self.row_valid_moves[row_num]) == 0:
                    return False
        else:
            for col_num in self.unassigned_cols:
                col_moves = self.col_valid_moves[col_num]
                col_assignment = vector[col_num]
                self.col_valid_moves[col_num] = [move for move in col_moves if not self.has_collision
                (move, col_assignment, self.last_move.idx)]
                if len(self.col_valid_moves[col_num]) == 0:
                    return False
        return True

    def get_legal_moves_for_row(self, num, for_col=False):
        return self.col_valid_moves[num] if for_col else self.row_valid_moves[num]


class SMove:
    '''
    Single move, assignment for a cell.
    '''
    def __init__(self, content, x=0, y=0):
        self.x = x
        self.y = y
        self.content = content

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class CMove:
    '''
    Complete move, a full assignment for a row/col.
    '''
    def __init__(self, idx, content, col_move=False):
        '''
        :param idx: The index of the row/col
        :param content: The content of the row/col, vector of +-1 values
        '''
        self.idx = idx
        self.content = content
        self.col_move = col_move

