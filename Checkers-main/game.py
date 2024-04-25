import pygame
from constants import RED, WHITE, GREEN, SQUARE_SIZE,red,white
from board import Board

class Game:
    #initializing the game on windows
    def __init__(self, win):
        #calling the private init method
        self._init()
        self.win = win
    #updating the move after every move
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    #private method
    #initializing the game
    def _init(self):
        #selected piece. to decide which piece to move
        self.selected = None
        #board object. game will ctrl board for us
        self.board = Board()
        #turn. to decide which player's turn it is
        self.turn = RED
        #valid moves. to decide which moves are valid (currently)
        self.valid_moves = {}

    #make winner function without nonetype error
    def winner(self):
        if self.board.winner() == red:
            return "RED WON"
        elif self.board.winner() == white:
            return "WHITE WON"
        elif self.board.winner() is None:
            return "TIE"
    
    #after reseting the game, we need to reset the game object
    def reset(self):
        self._init()
    #selected row and column
    def select(self, row, col):
        #selected is not none
        if self.selected:
            #move the selected piece to the row and col
            result = self._move(row, col)
            #if the move is not valid
            if not result:
                self.selected = None
                #select the piece
                #select the row and col
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        #any selected piece 
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            #else return false    
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        #if the row and col selected is not the piece but is a valid move
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #move the piece
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True
    #draw the valid moves
    #move the piece at the middle
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
    #change the turn 
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        #return the new board after the moves and turns
        self.board = board
        self.change_turn()