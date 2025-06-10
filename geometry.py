import pygame
import sys


pygame.init()


width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Фигуры и линии")

black = (0, 0, 0)
dark_blue = (50, 0, 130)
yellow = (255, 230, 0)
magenta = (220, 0, 130)
orange_red = (255, 70, 0)
lime_green = (140, 255, 0)
white = (255, 255, 255)


black_square_pos = (150, 150)
blue_circle_pos = (450, 150)
yellow_circle_pos = (150, 450)
magenta_square_pos = (450, 450)

radius = 50
side = 100


running = True
while running:
    screen.fill(white)

    pygame.draw.rect(screen, black, (*black_square_pos, side, side))
    pygame.draw.circle(screen, dark_blue, (blue_circle_pos[0] + radius, blue_circle_pos[1] + radius), radius)
    pygame.draw.circle(screen, yellow, (yellow_circle_pos[0] + radius, yellow_circle_pos[1] + radius), radius)
    pygame.draw.rect(screen, magenta, (*magenta_square_pos, side, side))

    pygame.draw.line(
        screen, lime_green,
        (black_square_pos[0] + side // 2, black_square_pos[1] + side // 2),
        (magenta_square_pos[0] + side // 2, magenta_square_pos[1] + side // 2), 5
    )
    pygame.draw.line(
        screen, orange_red,
        (yellow_circle_pos[0] + radius, yellow_circle_pos[1] + radius),
        (blue_circle_pos[0] + radius, blue_circle_pos[1] + radius), 5
    )

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
