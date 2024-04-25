from constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 17
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    #calculating the position of the piece
    def calc_pos(self):
        #with sq_size//2, we will be in the middle of the square
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        #pieces are circles. diplay of the pieces
        radius = SQUARE_SIZE//2 - self.PADDING
        #for outline
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        #for the piece (draw a big circle and on top of that small circle)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            #blit is used to draw an image on the respective surface (a pygame inbuilt function)
                            #for centering the crown
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    #representation of the piece
    #def __repr__(self):
        return str(self.color)