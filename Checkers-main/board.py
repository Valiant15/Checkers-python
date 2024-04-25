import pygame
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE,red,white
from piece import Piece
#this class will handle the differnet pieces on the board and their positions and moves. deleting , drawing and moving pieces
class Board:
    def __init__(self):
        #2d array of pieces
        #internal representation of the board
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            #for ex at (0,0), 0%2=0 so make it red then move by 2 places that us 0+2=2 so make it red and so on
            for col in range(row % 2, ROWS, 2):
                #draw a rectangle at the window with the color red. the first 2 are the size of the top left corner of the rectangle and the last 2 are the width and height of the rectangle
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    #NO OF KINGS/PIECES WE HAVE
    def evaluate(self):
        #WE WILL TRY TO MAKE THW WHITE PIECES THE KING
        #can give any pts to the kings  2 or 100 or anything
        return self.white_left - self.red_left + (self.white_kings * 2 - self.red_kings * 2)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                #if the piece is not 0 and the color is the same as the color we are looking for then we will add it to the list
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        #move the piece and also update the board
        #SWAP THE PIECES
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        #for king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 
    #select a piece
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                #place the pieces (initially)
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)#blank piece
                else:
                    self.board[row].append(0)#blank piece
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    #remove a piece from the board which we cross over
    def remove(self, pieces):
        for piece in pieces:
            #just set them to 0
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    #make winner function
    def winner(self):
        if self.red_left <= 0:
            return white
        elif self.white_left <= 0:
            return red
        return None

    #get all the valid moves for a piece
    def get_valid_moves(self, piece):
        moves = {}
        #EX = (4,5):(3,4) MOVED
        #FOR DIAGONAL MOVES
        #IF LEFT
        left = piece.col - 1
        #IF RIGHT
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            #FOR RED WE MOVE UP SO WE DO ROW-1 AND THE MAX WE CAN MOVE THE RED PIECE IS ROW-3. -1 INDICATED STOP THAT IS AT 0
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            #FOR RED WE MOVE DOWN SO WE DO ROW+1 AND THE MIN WE CAN MOVE THE RED PIECE IS ROW-3. -1 INDICATED STOP THAT IS AT 0
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
        return moves
    #FOR LEFT DIAGONAL MOVES
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        #last is the second piece that we are going to move over
        last = []
        for r in range(start, stop, step):
            #if the column is out of bounds. NOT IN THE BOARD
            if left < 0:
                break
            current = self.board[r][left]
            #found the valid move
            if current == 0:
                #if we have skipped over a piece and we dont have any more pieces to skip over
                #no double jumps
                if skipped and not last:
                    break
                #if we have skipped a piece and we are on a blank space
                #double jump
                elif skipped:
                    moves[(r, left)] = last + skipped
                #we just have empty square
                else:
                    moves[(r, left)] = last
                #recursive call to find wether we can move/skip further
                #if we find an empty square and we have skipped a piece then we can move there
                if last:
                    #if we have a piece in between and we are on a blank space
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            #if the current piece is not empty and has the same colour as the piece we r trying to move then it will not move 
            elif current.color == color:
                break
            #if it was not our colour then it was different colour so we can move over it assuming that there is an empty square
            else:
                last = [current]
            #we move left and look at other diagonal piece
            left -= 1
        return moves
    #FOR RIGHT DIAGONAL MOVES
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves