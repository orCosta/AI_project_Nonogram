import board
import display
import NonogramProblem
import time


def main():
    # ================= 15 X 15 Example ===================
    r_cond20 = [[5],[5],[7],[11],[13], [1,12],[17],[7,6],[8,4],[3,2,4], [3,2,4],[2,1,4],[1,4],[1,3],[3,5], [3,5],[6],[4],[3],[3]]
    c_cond20 = [[1],[2],[2],[4],[2,3],[6],[6],[5,2,1,1],[5,3,2,2],[5,3,6],[6,1,2,4],[7,1,1,2],[7,1,3],[8,2,3],[2,5,7],[1,5,2],[11],[9],[7],[4]]
    # ================= 15 X 15 Example ===================
    r_cond15 = [[2, 2], [7],[7],[7],[3,5,3], [5,3,5],[6,1,6],[6,6],[6,1,6],[5,1,5],[3,1,3],[2],[2],[4],[2]]
    c_cond15 = [[2,2],[7],[7,2],[7,2],[3,5,1],[5,3,2],[6,1,2],[6,4],[6,1],[5,3],[3,5],[7],[7],[7],[2,2]]

    # ================= 10 X 10 Example ===================
    r_cond10 = [[2, 2], [2, 2], [2, 2], [2, 2], [8], [10], [10], [2, 4, 2], [3, 3], [6]]
    c_cond10 = [[3], [5], [7, 2], [10], [4, 1], [4, 1], [10], [7,2], [5], [3]]

    # ================= 5 X 5 Example ===================
    r_cond5 = [[1, 1], [2, 2], [3], [2], [2]]
    c_cond5 = [[2, 2], [4], [1], [2], [2]]

    # ================= 3 X 3 Example ===================
    r_cond3 = [[1], [2], [2]]
    c_cond3 = [[2], [2], [1]]
    # r_cond3 = [[0], [1], [3]]
    # c_cond3 = [[1], [1], [2]]
    # ================= 4 X 4 Example ===================
    r_cond4 = [[1], [3], [1,1],[1]]
    c_cond4 = [[1], [1], [4], [1]]

    # ================= 2 X 2 Example ===================
    r_cond2 = [[1], [2]]
    c_cond2 = [[1], [2]]
    # ================= 6 X 6 Example ===================
    # r_cond6 = [[0], [1], [1,1],[1],[2,2],[0]]
    # c_cond6 = [[1], [1,1],[0], [1,1], [1,1], [1]]

    # r_cond6 = [[0], [2], [4], [6], [2], [2]]
    # c_cond6 = [[1], [2], [5], [5], [2], [1]]

    # r_cond6 = [[0], [0], [2], [2], [0], [0]]
    # c_cond6 = [[0], [0], [2], [2], [0], [0]]

    # r_cond6 = [[2], [4], [6], [6], [4], [2]]
    # c_cond6 = [[2], [4], [6], [6], [4], [2]]

    r_cond6 = [[0], [2], [4], [4], [2], [0]]
    c_cond6 = [[0], [2], [4], [4], [2], [0]]

    # r_cond6 = [[0], [1], [1], [1], [1], [0]]
    # c_cond6 = [[0], [1,1], [0], [0], [1,1], [0]]

    # r_cond6 = [[2], [0], [1,2,1], [1,3], [0], [1,1]]
    # c_cond6 = [[1], [1, 1], [1,1], [1,2], [1, 1], [2]]

    # r_cond6 = [[1,1], [2,1,1], [6], [6], [1,1,2], [1, 1]]
    # c_cond6 = [[4], [4, 1], [3], [3, 1], [1, 3], [4]]
    start = time.time()
    # ===================== Lines =======================================
    # non2 = NonogramProblem.NonogramCellsProblem(3, 3, r_cond3, c_cond3)
    # non2 = NonogramProblem.NonogramCellsProblem(4, 4, r_cond4, c_cond4)
    # non2 = NonogramProblem.NonogramCellsProblem(2, 2, r_cond2, c_cond2)
    # actions = NonogramProblem.depth_first_search(non2)
    # ===================== Lines =======================================
    # non2 = NonogramProblem.NonogramLinesProblem(3, 3, r_cond3, c_cond3)
    # non2 = NonogramProblem.NonogramLinesProblem(6, 6, r_cond6, c_cond6)
    # non2 = NonogramProblem.NonogramLinesProblem(4, 4, r_cond4, c_cond4)
    # non2 = NonogramProblem.NonogramLinesProblem(2, 2, r_cond2, c_cond2)
    # non2 = NonogramProblem.NonogramLinesProblem(5, 5, r_cond5, c_cond5)
    # non2 = NonogramProblem.NonogramLinesProblem(10, 10, r_cond10, c_cond10)
    # actions = NonogramProblem.depth_first_search(non2)
    # ===================== CSP =========================================
    # non2 = NonogramProblem.NonogramCSP(5, 5, r_cond5, c_cond5)
    # non2 = NonogramProblem.NonogramCSP(10, 10, r_cond10, c_cond10)
    non2 = NonogramProblem.NonogramCSP(15, 15, r_cond15, c_cond15)
    # non2 = NonogramProblem.NonogramCSP(20, 20, r_cond20, c_cond20)
    actions = NonogramProblem.arc_dfs(non2)
    # actions = NonogramProblem.forward_checking_dfs(non2)
    # actions = NonogramProblem.mrv_dfs(non2)
    # ===================================================================
    non2.fill_cells(actions)
    end = time.time()
    print("test1, tested with {}, took {} seconds, expended {} nodes".format(type(non2), end - start, non2.expanded))
    non2.show()


if __name__ == '__main__':
    main()