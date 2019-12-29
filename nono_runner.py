import argparse
import os
import json
import time
import NonogramProblem


def read_board_from_file(file_path):
    if not os.path.exists(file_path):

        print("Error : Path -{}- not exist".format(file_path))
        return None
    with open(file_path) as json_file:
        data = json.load(json_file)
        row_cond = data.get("row")
        col_cond = data.get("col")
        if row_cond is None or col_cond is None:
            print("Error : Bad file format")
            return None
        else:
            return len(row_cond), len(col_cond), row_cond, col_cond


def parse_args():
    p = argparse.ArgumentParser()
    g = p.add_argument_group('I/O')
    g.add_argument('--path', '-p', help='Path to board file (Json format)', type=str, required=True)
    g = p.add_argument_group('Game')
    g.add_argument('--mrv', '-mrv', help='Activate MRV method' , action="store_true", default=False)
    g.add_argument('--forward', '-forward', help='Activate Forward checking method', action="store_true", default=False)
    g.add_argument('--arc', '-arc', help='Activate Arc checking method', action="store_true", default=False)
    args = p.parse_args()
    args.__dict__["board_cfg"] = read_board_from_file(args.__dict__["path"])
    return args


def run_game(args):
    w, h, r_cond, c_cond = args.__dict__["board_cfg"]
    non = NonogramProblem.NonogramCSP(w, h, r_cond, c_cond)
    actions = []
    print("Search for solution...")
    start = time.time()
    if args.__dict__["mrv"]:
        if args.__dict__["arc"]:
            actions = NonogramProblem.arc_mrv_dfs(non)
        elif args.__dict__["forward"]:
            actions = NonogramProblem.forward_checking_mrv_dfs(non)
        else:
            actions = NonogramProblem.mrv_dfs(non)
    else:
        if args.__dict__["arc"]:
            actions = NonogramProblem.arc_dfs(non)
        elif args.__dict__["forward"]:
            actions = NonogramProblem.forward_checking_dfs(non)

    end = time.time()
    if actions:
        non.fill_cells(actions)
        print("=================== FINISH =========================")
        print("Found solution in {}s | expended {} nodes".format(end - start, non.expanded))
    else:
        print("No solution...")


if __name__ == '__main__':
    run_game(parse_args())





