import numpy as np
import board
import os
from matplotlib import pyplot as plt

CHAR_MAP = {-1: ".", 0: "x", 1: "@"}


def display_board(board1):
    row_c = board1.row_cond
    col_c = board1.col_cond
    nono_board = (board1.state * (-1)) +1
    fig, ax = plt.subplots()
    im = ax.imshow(nono_board, cmap="gray")
    ax.set_xticks(np.arange(-0.5, len(col_c), 1))
    ax.set_yticks(np.arange(-0.5, len(row_c), 1))
    # ax.set_xticklabels(col_c)
    # ax.set_yticklabels(row_c)

    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #          rotation_mode="anchor")

    # for i in range(len(row_c)):
    #     for j in range(len(col_c)):
    #         text = ax.text(j, i, nono_board[i, j],
    #                        ha="center", va="center", color="w")
    ax.set_title("Solution")
    ax.grid(color='b', linewidth=1)
    fig.tight_layout()
    plt.show()


def print_to_cmd(board1):
    b = " "
    b += "_"*board1.board_w + "\n"
    for i in range(board1.board_h):
        line = "|"
        for j in range(board1.board_w):
            line += CHAR_MAP[board1.state[i, j]]
        b += line + "\n"
    os.system('cls')
    print(b)


def project_graphs():

    # Cells problem vs line problem:
    # plt.figure(0)
    # line = [0.00049, 0.0024, 0.0085]
    # cell = [0.007, 85.25, 665]
    # board_size = [2, 3, 4]
    #
    # plt.plot(board_size, line, label="lines")
    # plt.plot(board_size, cell, label="cells")
    # # plt.yscale('log')
    # plt.xlabel("Board size (square)")
    # plt.ylabel("time[sec]")
    # plt.title("Naive problem structure Vs Line structure")
    # plt.legend()
    # plt.grid()
    # plt.show()

    # spreading vs density
    plt.figure(0)
    spread = [1.09, 0.52, 0.01]
    dens = [0.29, 0.35, 0.045]
    board_size = [4, 12, 24]

    plt.scatter(board_size, spread, label="spread")
    plt.scatter(board_size, dens, label="dens")
    # plt.yscale('log')
    plt.xlabel("Num of black cells")
    plt.ylabel("time[sec]")
    plt.title("Spread pattern Vs Dens pattern (6x6 board)")
    plt.legend()
    plt.grid()
    plt.show()

    # plt.figure(1)
    # MRV = [0.2, 0.3, 0.4]
    # FORW = [0.1, 0.4, 0.6]
    # ARC = [0.02, 0.6, 0.8]
    # board_size = [3, 5, 7]
    # plt.plot(board_size, MRV, label="MRV")
    # plt.plot(board_size, FORW, label="Forward")
    # plt.plot(board_size, ARC, label="ARC")
    # plt.xlabel("Board size (square)")
    # plt.ylabel("time[sec]")
    # plt.title(...)
    # plt.legend()
    # plt.show()


if __name__ == '__main__':

    project_graphs()












