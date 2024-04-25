#a deepcopy will copy the reference as well the object
from copy import deepcopy
import pygame
RED = (255,0,0)
WHITE = (255, 255, 255)
#position is the current position of the piece
#depth is how far am i making this tree
#max_player is boolean val tu tell if we r minimising the val or maximising the value
#game is the game object which we will get from the main.py
def minimax(position, depth, max_player, game):
    #we dont have any valid move left and there is no winner yet then return its position evaluation and position.
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        #max evaluation is the lowest possible value
        maxEval = float('-inf')
        best_move = None
         #get all the best possible moves for the current position
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    #blank list of moves which will store the new board after the move
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)