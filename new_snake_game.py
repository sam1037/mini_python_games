import pygame
import color
import random
pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 500
CUBE_SIZE = 24 # grid also contains a pixel
last_key = "None"

run = True

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("New Snake Game")


class Cube():
    def __init__(self, x, y, color, is_head, direction):
        self.x = x
        self.y = y
        self.is_head = is_head
        self.color = color
        self.direction = direction

    def show(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, CUBE_SIZE, CUBE_SIZE))
        pygame.display.update()

    def move(self):
        self.x += self.direction[0] * (CUBE_SIZE+1)
        self.y += self.direction[1] * (CUBE_SIZE+1)

    def spawn_randomly(self):
        _xlist = [x for x in range(1, 500) if x % 25 == 1]
        self.x = random.choice(_xlist)
        self.y = random.choice(_xlist) # since the width and height of the window is the same
        self.show()
    
    def change_direction(self, key):
        if key == pygame.K_UP:
            self.direction = [0, -1]
        if key == pygame.K_DOWN:
            self.direction = [0, 1]
        if key == pygame.K_LEFT:
            self.direction = [-1, 0]
        if key == pygame.K_RIGHT:
            self.direction = [1, 0]

class Snake:
    def __init__(self, cube_list, direction):
        self.cube_list = cube_list
        self.head = cube_list[0]
        self.direction = direction
        self.length = len(cube_list)
        self.color = cube_list[0].color

        for cube in self.cube_list:
            cube.direction = direction

    def move(self):
        for cube in self.cube_list:
            cube.move()

    def change_dir(self, key):
        if key == pygame.K_UP:
            self.direction = [0, -1]
        if key == pygame.K_DOWN:
            self.direction = [0, 1]
        if key == pygame.K_LEFT:
            self.direction = [-1, 0]
        if key == pygame.K_RIGHT:
            self.direction = [1, 0]

        for i, cube in enumerate(self.cube_list[::-1]):
            if i == len(self.cube_list)-1:
                cube.direction = self.direction
            else:
                cube.direction = self.cube_list[i+1].direction
                print(self.cube_list[i+1].direction)


    def show(self):
        for cube in self.cube_list:
            cube.show()

def draw_grid():
    window.fill(color.white)
    pygame.draw.line(window, color.black, (0,0), (WIN_WIDTH, 0), 1)
    
    for x in [x for x in range(0,WIN_WIDTH) if x % (CUBE_SIZE+1) == 0]:
        pygame.draw.line(window, color.black, (x,0), (x, WIN_HEIGHT), 1)
    for y in [x for x in range(0,WIN_HEIGHT) if x % (CUBE_SIZE+1) == 0]:
        pygame.draw.line(window, color.black, (0,y), (WIN_WIDTH, y), 1)
    pygame.display.update()

def generate_snack():
    pass

def check_eat_snack():
    pass


test_cube = Cube((CUBE_SIZE+1)*10+1, (CUBE_SIZE+1)*14+1, color.red, False, [1, 0])
test_cube1 = Cube((CUBE_SIZE+1)*11+1, (CUBE_SIZE+1)*14+1, color.red, False, [0, 0])
test_snake = Snake([test_cube, test_cube1], [-1,0])
while run:
    draw_grid()
    test_snake.change_dir(0)
    test_snake.move()
    test_snake.show()
    pygame.time.delay(200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            test_snake.change_dir(event.key)
    
    
pygame.quit()