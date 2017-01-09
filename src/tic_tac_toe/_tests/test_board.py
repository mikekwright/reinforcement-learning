import pytest

from board import Board

def test_board_start_empty():
    x = Board()
    assert len(x.open_spots()) == 9

def test_empty_board_not_won_with_X():
    x = Board()
    assert x.does_piece_win(piece='X') == False

def test_empty_board_not_won_with_O():
    x = Board()
    assert x.does_piece_win(piece='O') == False

def test_empty_board_is_not_draw():
    x = Board()
    assert x.is_draw() == False

def test_row_one_board_win_X():
    x = Board()
    x.board = ['X', 'X', 'X',
               ' ', ' ', ' ',
               ' ', ' ', ' ']
    assert x.does_piece_win(piece='X') == True

def test_row_two_board_win_X():
    x = Board()
    x.board = [' ', ' ', ' ',
               'X', 'X', 'X',
               ' ', ' ', ' ']
    assert x.does_piece_win(piece='X') == True

def test_row_three_board_win_X():
    x = Board()
    x.board = [' ', ' ', ' ',
               ' ', ' ', ' ',
               'X', 'X', 'X']
    assert x.does_piece_win(piece='X') == True

def test_row_one_board_win_O():
    x = Board()
    x.board = ['O', 'O', 'O',
               ' ', ' ', ' ',
               ' ', ' ', ' ']
    assert x.does_piece_win(piece='O') == True

def test_row_two_board_win_O():
    x = Board()
    x.board = [' ', ' ', ' ',
               'O', 'O', 'O',
               ' ', ' ', ' ']
    assert x.does_piece_win(piece='O') == True

def test_row_three_board_win_O():
    x = Board()
    x.board = [' ', ' ', ' ',
               ' ', ' ', ' ',
               'O', 'O', 'O']
    assert x.does_piece_win(piece='O') == True

def test_column_one_board_win_X():
    x = Board()
    x.board = ['X', ' ', ' ',
               'X', ' ', ' ',
               'X', ' ', ' ']
    assert x.does_piece_win(piece='X') == True

def test_column_two_board_win_X():
    x = Board()
    x.board = [' ', 'X', ' ',
               ' ', 'X', ' ',
               ' ', 'X', ' ']
    assert x.does_piece_win(piece='X') == True

def test_column_three_board_win_X():
    x = Board()
    x.board = [' ', ' ', 'X',
               ' ', ' ', 'X',
               ' ', ' ', 'X']
    assert x.does_piece_win(piece='X') == True

def test_column_one_board_win_O():
    x = Board()
    x.board = ['O', ' ', ' ',
               'O', ' ', ' ',
               'O', ' ', ' ']
    assert x.does_piece_win(piece='O') == True

def test_column_two_board_win_O():
    x = Board()
    x.board = [' ', 'O', ' ',
               ' ', 'O', ' ',
               ' ', 'O', ' ']
    assert x.does_piece_win(piece='O') == True

def test_column_three_board_win_O():
    x = Board()
    x.board = [' ', ' ', 'O',
               ' ', ' ', 'O',
               ' ', ' ', 'O']
    assert x.does_piece_win(piece='O') == True

def test_draw_with_X_win_is_false():
    x = Board()
    x.board = ['X', 'O', 'X',
               'O', 'X', 'O',
               'X', 'O', 'O'] 
    assert x.does_piece_win(piece='X') == True
    assert x.does_piece_win(piece='O') == False
    assert x.is_draw() == False

def test_draw_with_O_win_is_false():
    x = Board()
    x.board = ['X', 'O', 'X',
               'O', 'X', 'O',
               'O', 'O', 'O'] 
    assert x.does_piece_win(piece='X') == False
    assert x.does_piece_win(piece='O') == True
    assert x.is_draw() == False

def test_draw_with_no_win_is_true():
    x = Board()
    x.board = ['X', 'O', 'X',
               'O', 'X', 'O',
               'O', 'X', 'O'] 
    assert x.does_piece_win(piece='X') == False
    assert x.does_piece_win(piece='O') == False
    assert x.is_draw() == True

def test_draw_with_not_full_board_is_false():
    x = Board()
    x.board = ['X', 'O', 'X',
               'O', 'X', 'O',
               'O', 'X', ' '] 
    assert x.does_piece_win(piece='X') == False
    assert x.does_piece_win(piece='O') == False
    assert x.is_draw() == False


