"""
    Snake game following Chapter 6 – Wormy (page 131)
    of Making Games with Python & Pygame by Al Sweigart
"""


import pygame
import random
import sys
from pygame.locals import *

FPS = 15

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)

BGCOLOR = BLACK
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

pygame.display.set_caption('Snake')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()
    runGame()
    showGameOverScreen()
    while True:
        if checkForKeyPress():
            return

def showStartScreen():
    titleFont =  pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)
    degrees1 = 0
    degrees2 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)

def runGame():
    get_random_location = lambda: (int(random.random() * CELLWIDTH), int(random.random() * CELLHEIGHT))

    apple_location = get_random_location()
    snake_head_x, snake_head_y = get_random_location()

    direction = RIGHT if snake_head_x < CELLWIDTH / 2 else LEFT
    snake_coordinates = [
        (snake_head_x, snake_head_y),
        (snake_head_x - 1 if direction == RIGHT else +1, snake_head_y),
        (snake_head_x - 2 if direction == RIGHT else +2, snake_head_y)
    ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT and not direction == RIGHT:
                    direction = LEFT
                elif event.key == K_RIGHT and not direction == LEFT:
                    direction = RIGHT
                elif event.key == K_UP and not direction == DOWN:
                    direction = UP
                elif event.key == K_DOWN and not direction == UP:
                    direction = DOWN
                
        if snake_coordinates[HEAD] == apple_location:
            when_eats_apple(snake_coordinates, apple_location, direction)
            apple_location = get_random_location()
        else:
            move_snake(snake_coordinates, direction)

        if is_dead(snake_coordinates):            
            return

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(snake_coordinates)
        drawApple(apple_location)
        drawScore(len(snake_coordinates) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def is_dead(snake_coordinates):
    return snake_coordinates[HEAD][0] < 0 or snake_coordinates[HEAD][0] > CELLWIDTH\
        or snake_coordinates[HEAD][1] < 0 or snake_coordinates[HEAD][1] > CELLHEIGHT\
        or any(coordinate == snake_coordinates[HEAD] for coordinate in snake_coordinates[HEAD+1:])

def is_horizontal_direction(direction):
    return direction == LEFT or direction == RIGHT

def is_vertical_direction(direction):
    return direction == DOWN or direction == UP

def when_eats_apple(snake_coords, apple, direction):
    new_head = move_with_direction(snake_coords[HEAD], direction)
    snake_coords.insert(0, new_head)

def move_snake(snake_coords, direction):
    snake_coords.insert(0, move_with_direction(snake_coords[HEAD], direction))
    snake_coords.pop()

def move_with_direction(coordinate, direction):
    direction_mapper = {RIGHT: 1, LEFT: -1, UP: -1, DOWN: 1}
    new_segment_x, new_segment_y = coordinate

    if is_vertical_direction(direction):
        new_segment_y += direction_mapper[direction]
    elif is_horizontal_direction(direction):
        new_segment_x += direction_mapper[direction]
    
    return (new_segment_x, new_segment_y)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def drawApple(coords):
    x, y = coords
    appleRect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord[0] * CELLSIZE
        y = coord[1] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()