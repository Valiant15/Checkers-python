import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from game import Game
from minimax import minimax
#frame rate per second (no of update of the screen per second)
FPS = 60
#windows
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#name that will be displayed on the top bar of the game.
pygame.display.set_caption('CHECKERS (Created by UV)')
#when we click on the screen we get the position of the mouse and we want to convert that position into row and column.
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
#define a main function
def main():
    run = True
    #clock will make sure that our game does not run too fast or too slow
    #Tick is just a measure of time in PyGame. clock. tick(40) means that for every second at most 40 frames should pass.
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

        if game.winner() is not None:
            print(game.winner())
            run = False
            
        #display
        #loop through all the events that are happening in the game. checks if any event is happening at a particular time.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #the red button on the top right corner of the game.
            #if we click on the screen we get the position of the mouse and we want to convert that position into row and column.
            if event.type == pygame.MOUSEBUTTONDOWN:
                #get mouse position
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()
    pygame.quit()
#call the main function 
main()