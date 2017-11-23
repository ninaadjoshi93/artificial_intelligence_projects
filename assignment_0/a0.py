#!/usr/bin/python2.7 -tt
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# modified by : Ninaad Joshi
#  n queens problem
import sys
import time

#################################global variables###############################

global start_time
global end_time
global fringe

#################################Common##########################################

# Count # of pieces in given row
def count_on_row(board, row):
    return sum(board[row])


# Count # of pieces in given column
def count_on_col(board, col):
    return sum([row[col] for row in board])


# count # of pieces in left diagonal
def count_on_left_diagonal(board, r_pos, c_pos):
    # y = m * x + c for m = 1
    # y = x + c
    return sum(board[r_num][c_num] for c_num in range(len(board)) \
               for r_num in range(len(board)) if c_num - r_num == c_pos - r_pos)


# count # of pieces in right diagonal
def count_on_right_diagonal(board, r_pos, c_pos):
    # y = m * x + c for m = -1
    # y = -x + c OR y + x = c
    return sum(board[r_num][c_num] for c_num in range(len(board)) \
               for r_num in range(len(board)) if r_num + c_num == c_pos + r_pos)


# Count total # of pieces on board
def count_pieces(board):
    return sum([sum(row) for row in board])


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    # print board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]
    return board[0:row] + [board[row][0:col] + [1, ] + board[row][col + 1:]] + board[row + 1:]


#####################################nqueen###########################################

# Return a string with the board rendered in a human-friendly format
def printable_board_nqueens(board):
    return "\n".join([" ".join(["Q" if col else "X" \
        if 0 <= blocked_position_r < N and 0 <= blocked_position_c < N \
           and r_num == blocked_position_r and c_num == blocked_position_c \
        else "_" for c_num, col in enumerate(row)]) for r_num, row in enumerate(board)])


# check if nqueen board is a goal state
def is_goal_nqueens(board):
    if 0 <= blocked_position_c < N and 0 <= blocked_position_r < N:
        return not board[blocked_position_r][blocked_position_c] and \
               all([count_on_row(board, r) == 1 for r in range(0, N)]) and \
               all([count_on_col(board, c) == 1 for c in range(0, N)]) and \
               all([count_on_left_diagonal(board, r, c) <= 1 for r in range(0, N) for c in range(0, N)]) and \
               all([count_on_right_diagonal(board, r, c) <= 1 for r in range(N) for c in range(N)]) and \
               count_pieces(board) == N
    else:
        return count_pieces(board) == N and \
               all([count_on_row(board, r) == 1 for r in range(0, N)]) and \
               all([count_on_col(board, c) == 1 for c in range(0, N)]) and \
               all([count_on_left_diagonal(board, r, c) <= 1 for r in range(0, N) for c in range(0, N)]) and \
               all([count_on_right_diagonal(board, r, c) <= 1 for r in range(N) for c in range(N)])

# Get list of nqueen successors of given board state
def successors_nqueens(board):
    return [add_piece(board, r, (count_pieces(board) + N/2) % N) for r in range(0, N)
            if (not count_on_row(board, r)
                and not count_on_col(board, (count_pieces(board) + N/2) % N)
                and not count_on_left_diagonal(board, r, (count_pieces(board) + N/2) % N)
                and not count_on_right_diagonal(board, r, (count_pieces(board) + N/2) % N))]


# Solve n-queens by dfs!
def solve_nqueens_by_dfs(initial_board):
    global fringe
    fringe = [initial_board]
    global start_time
    start_time = time.time()
    while len(fringe) > 0:
        for s in successors_nqueens(fringe.pop()):
            if is_goal_nqueens(s):
                global end_time
                end_time = time.time()
                return (s)
            fringe.append(s)
    return False

############################################nrooks############################################

# Return a string with the board rendered in a human-friendly format
def printable_board_nrooks(board):
    return "\n".join([" ".join(["R" if col else "X" \
        if 0 <= blocked_position_r < N and 0 <= blocked_position_c < N \
           and r_num == blocked_position_r and c_num == blocked_position_c \
        else "_" for c_num, col in enumerate(row)]) for r_num, row in enumerate(board)])


# check if nrook board is a goal state
def is_goal_nrooks(board):
    if 0 <= blocked_position_c < N and 0 <= blocked_position_r < N:
        return not board[blocked_position_r][blocked_position_c] and \
               all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
               all([count_on_col(board, c) <= 1 for c in range(0, N)]) and \
               count_pieces(board) == N
    else:
        return count_pieces(board) == N and \
               all([count_on_col(board, r) <= 1 for r in range(0, N)]) and \
               all([count_on_col(board, c) <= 1 for c in range(0, N)])


# Get list of nrook successors of given board state
def successors_nrooks(board):
    return [add_piece(board, r, (count_pieces(board) + N/2) % N) for r in range(0, N) \
            if (count_on_row(board, r) < 1 and count_on_col(board, (count_pieces(board) + N/2) % N) < 1)]


# Solve n-rooks by dfs!
def solve_nrooks_by_dfs(initial_board):
    global fringe
    fringe = [initial_board]
    global start_time
    start_time = time.time()
    while len(fringe) > 0:
        for s in successors_nrooks(fringe.pop()):
            if is_goal_nrooks(s):
                global end_time
                end_time = time.time()
                return (s)
            fringe.append(s)
    return False

####################################start program##############################

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])
if len(sys.argv) == 5:
    blocked_position_r = int(sys.argv[3]) - 1
    blocked_position_c = int(sys.argv[4]) - 1
else:
    blocked_position_r = -1
    blocked_position_c = -1
# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0] * N] * N
# print ("Starting from initial board:\n" + printable_board_nrooks(initial_board) + "\n\nLooking for solution...\n")
if sys.argv[1] == "nqueen" or sys.argv[1] == "nqueens":
    solution = solve_nqueens_by_dfs(initial_board)
    print (printable_board_nqueens(solution) if solution else "Sorry, no solution found. :(")
else:
    solution = solve_nrooks_by_dfs(initial_board)
    print (printable_board_nrooks(solution) if solution else "Sorry, no solution found. :(")

#print "%.9f" % (end_time - start_time) if solution else " "
