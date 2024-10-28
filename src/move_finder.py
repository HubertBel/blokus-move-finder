import numpy as np
from enum import Enum
from copy import deepcopy


class Direction(Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x=}, {self.y=}"

def check_diagonal(board, piece, position):
    board_height, board_width = len(board), len(board[0])

    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 0:
                continue

            board_x = position.x + x
            board_y = position.y + y

            diagonals = [
                [board_y-1, board_x-1],
                [board_y-1, board_x+1],
                [board_y+1, board_x-1],
                [board_y+1, board_x+1],
            ]

            for diag in diagonals:
                if diag[0] < 0 or diag[1] < 0:
                    continue
                if diag[0] >= board_height or diag[1] >= board_width:
                    continue

                if board[diag[0]][diag[1]] == 1:
                    return True

    return False


def check_adjacent(board, piece, position):
    board_height, board_width = len(board), len(board[0])

    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 0:
                continue

            board_x = position.x + x
            board_y = position.y + y

            adjacents = [
                [board_y-1, board_x],
                [board_y, board_x-1],
                [board_y+1, board_x],
                [board_y, board_x+1],
            ]

            for adj in adjacents:
                if adj[0] < 0 or adj[1] < 0:
                    continue
                if adj[0] >= board_height or adj[1] >= board_width:
                    continue

                if board[adj[0]][adj[1]] == 1:
                    return False

    return True

def check_collision(board, piece, position):
    board_height, board_width = len(board), len(board[0])

    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 0:
                continue

            board_x = position.x + x
            board_y = position.y + y

            if board_x >= board_width:
                return False
            if board_y >= board_height:
                return False

            if board[board_y][board_x] != 0:
                return False

    return True

def validate_position(board, piece, position):
    is_diagonal = check_diagonal(board, piece, position)
    is_not_adjacent = check_adjacent(board, piece, position)
    is_not_collision = check_collision(board, piece, position)

    if is_diagonal and is_not_collision and is_not_adjacent:
        return True

    return False


def find_valid_positions(board, piece):
    moves = []

    for y in range(len(board)):
        for x in range(len(board[0])):

            for dir in Direction:
                piece_rot = rotate_piece(piece, dir)
                position = Position(x, y)

                if validate_position(board, piece_rot, position):
                    moves.append([position, dir])

    return moves

def add_piece_to_board(board, piece, position, direction):
    new_board = deepcopy(board)
    piece_rot = rotate_piece(piece, direction)

    if piece_rot is None:
        return

    for y in range(len(piece_rot)):
        for x in range(len(piece_rot[0])):
            if piece_rot[y][x] == 0:
                continue

            board_x = position.x + x
            board_y = position.y + y

            new_board[board_y][board_x] = 'X'

    return new_board

def rotate_piece(piece, direction):
    piece_mat = np.array(piece)

    match direction:
        case Direction.UP:
            return piece
        case Direction.RIGHT:
            return np.rot90(piece_mat, k=-1).tolist()
        case Direction.LEFT:
            return np.rot90(piece_mat, k=1).tolist()
        case Direction.DOWN:
            return np.rot90(piece_mat, k=2).tolist()
