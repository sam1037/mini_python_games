# todo ai
# todo window resizable
# todo better join snake
import pygame
import random
import time
from tic_tac_toe_game import msg_to_screen
from Useful_stuff import Button

grey = (169, 169, 169)
bright_grey = (189, 189, 189)
window_length = 500
snake_length = 1
cube_num = 0
grid_length = 20
red = (183, 28, 28)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)
bright_grey = (189, 189, 189)
green = (46, 149, 87)
s_direction = [0, 0, 0, 0]  # [up, left, down, right]
s_head_coords = [random.randrange(0, (window_length - grid_length) + 1, grid_length),
                 random.randrange(0, (window_length - grid_length) + 1, grid_length),
                 grid_length,
                 grid_length]  # randomly generate snake's coordinates(x,y,width,depth)
s_full_coords_list = [s_head_coords.copy()]  # this list consists all snake blocks' coords.

# window
window = pygame.display.set_mode((window_length, window_length))
pygame.display.set_caption("Snake Game")
window.fill(white)
pygame.draw.line(window, black, (0, 0), (window_length, 0))
pygame.display.flip()


def reset_all():
    # set variable
    global s_direction, s_head_coords, s_full_coords_list, snake_length, cube_num
    s_direction = [0, 0, 0, 0]  # [up, left, down, right]
    s_head_coords = [random.randrange(0, (window_length - grid_length) + 1, grid_length),
                     random.randrange(0, (window_length - grid_length) + 1, grid_length),
                     grid_length,
                     grid_length]  # randomly generate snake's coordinates(x,y,width,depth)
    s_full_coords_list = [s_head_coords.copy()]
    snake_length = 1
    cube_num = 0

    draw_all()


def anotherround():
    global event
    run = True

    window.fill(white)

    def setrun():
        global run
        run = False

    butt_rect = [int(window_length/10), int(window_length*3/10), int(window_length*8/10), int(window_length*2/10)]
    play_button = Button([setrun, main], butt_rect, bright_grey, grey, black, ["Play Again", black, int(window_length/8)], window, hotkey=' ')

    play_button.draw_button()
    while run:
        pygame.time.delay(50)
        play_button.button_react()


def draw_all():
    window.fill(white)  # draw window
    pygame.draw.line(window, black, (0, 0), (window_length, 0))
    generate_snake()
    generate_cube(True)
    return


def snake_hit_snake():
    for cycle in range(3):
        pygame.draw.rect(window, white, s_head_coords)
        pygame.display.update()

        pygame.time.delay(300)

        pygame.draw.rect(window, red, s_head_coords)
        pygame.draw.rect(window, white, s_head_coords, 1)
        pygame.display.update()

        pygame.time.delay(300)

    window.fill(white)
    pygame.display.update()
    pygame.time.delay(50)
    msg_to_screen("You hit yourself!", black, int(window_length / 10), window, window_length, window_length)
    time.sleep(2)
    anotherround()


def change_direction():
    global s_direction
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        s_direction = [0, 0, 0, 0]  # reset direction
        s_direction[0] = True
        return
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        s_direction = [0, 0, 0, 0]
        s_direction[1] = True
        return
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        s_direction = [0, 0, 0, 0]
        s_direction[2] = True
        return
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        s_direction = [0, 0, 0, 0]
        s_direction[3] = True
        return


def change_s_coords():
    if s_direction[0]:  # up
        s_head_coords[1] -= grid_length
        if s_head_coords not in s_full_coords_list:
            s_full_coords_list.append(s_head_coords.copy())  # add snake_head_coords to the snake_full_coords_list
        else:
            snake_hit_snake()

    if s_direction[1]:  # left
        s_head_coords[0] -= grid_length
        if s_head_coords not in s_full_coords_list:
            s_full_coords_list.append(s_head_coords.copy())  # add snake part to list
        else:
            snake_hit_snake()

    if s_direction[2]:  # down
        s_head_coords[1] += grid_length
        if s_head_coords not in s_full_coords_list:
            s_full_coords_list.append(s_head_coords.copy())  # add snake part to list
        else:
            snake_hit_snake()

    if s_direction[3]:  # right
        s_head_coords[0] += grid_length
        if s_head_coords not in s_full_coords_list:
            s_full_coords_list.append(s_head_coords.copy())  # add snake part to list
        else:
            snake_hit_snake()


def check_touch_wall():
    def touch_wall_action():
        # the whole snake blinks 3 times
        for cycle in range(3):
            for s_part in s_full_coords_list:
                pygame.draw.rect(window, white, s_part)
                pygame.display.update()

            pygame.time.delay(300)

            generate_snake()
            pygame.display.update()
            pygame.time.delay(300)

        window.fill(white)
        msg_to_screen("You touched the wall!", black, int(window_length / 10), window, window_length, window_length)
        time.sleep(2)
        anotherround()

    # hit wall snake die
    if s_head_coords[0] < 0 or s_head_coords[0] >= window_length:
        touch_wall_action()
    if s_head_coords[1] < 0 or s_head_coords[1] >= window_length:
        touch_wall_action()


# generate snake
def generate_snake():  # generate the whole snake
    for s_p in s_full_coords_list:
        if s_p == s_full_coords_list[-1]:  # draw head in different color
            pygame.draw.rect(window, red, s_p)
            pygame.draw.rect(window, black, [s_p[0]+1,s_p[1]+1,s_p[2]-2,s_p[3]-2], 1)
            pygame.draw.rect(window, white, s_p, 1)

        else:
            try:
                s_leftright = [s_p[0],
                               s_p[1] + 1,
                               s_p[2],
                               s_p[3] - 2]
                s_updown = [s_p[0] + 1,
                            s_p[1],
                            s_p[2] - 2,
                            s_p[3]]
                not_corner = True
                sm1 = s_full_coords_list[(s_full_coords_list.index(s_p) - 1)]
                s1 = s_full_coords_list[(s_full_coords_list.index(s_p) + 1)]
                # snake part is in corner turn
                for xy in [0, 1]:
                    if s_p[xy] == sm1[xy] and s_p[xy] != s1[xy]:  # if corner
                        pygame.draw.rect(window,red,s_p)
                        pygame.draw.rect(window,white,s_p,1)
                        not_corner = False

                # if snake part is connected with another snake part, join them togather
                if not_corner:
                    if s_p[0] == sm1[0]:
                        pygame.draw.rect(window, red, s_updown)
                    if s_p[1] == sm1[1]:
                        pygame.draw.rect(window, red, s_leftright)

            except:
                pass
    pygame.display.update()


# generate cube
def generate_cube(must_generate=False):
    global cube_num, cube_coords
    if cube_num == 0:
        while True:
            cube_coords = [random.randrange(0, (window_length - grid_length) + 1, grid_length),
                           random.randrange(0, (window_length - grid_length) + 1, grid_length),
                           grid_length,
                           grid_length]
            if cube_coords not in s_full_coords_list:
                break
    if random.randrange(101) in range(51) or must_generate:
        pygame.draw.rect(window, green, cube_coords)  # draw cube
        pygame.draw.rect(window, white, cube_coords, 1)
        if cube_coords[1] == 0:  # cube touch the upper line
            pygame.draw.line(window, black, (0, 0), (window_length, 0))
        pygame.display.update()
        cube_num = 1


def check_eat_cube():
    global snake_length, cube_num, cube_coords
    if s_head_coords == cube_coords:  # snake head touch the cube
        pygame.draw.rect(window, red, cube_coords)
        pygame.draw.rect(window, white, cube_coords, 1)
        pygame.display.update()
        snake_length += 10
        cube_num = 0


def delete_snake_tail():
    # remove extra snake parts
    while snake_length < len(s_full_coords_list):
        pygame.draw.rect(window, white, (s_full_coords_list[0]).copy())
        if (s_full_coords_list[0].copy())[1] == 0:
            pygame.draw.line(window, black, (0, 0), (window_length, 0))
        s_full_coords_list.remove(s_full_coords_list[0].copy())
        pygame.display.update()


def check_win():
    if snake_length == (window_length / grid_length) ** 2:
        msg_to_screen("You Win!", black, int(window_length / 10), window, window_length, window_length)
        pygame.time.delay(1000)
        anotherround()


def check_pause():
    if event.key == pygame.K_SPACE:
        window.fill(white)
        msg_to_screen("THE WORLD", black, int(window_length / 5), window, window_length, window_length)
        pygame.time.delay(150)

        draw_all()

        while True:
            for p_event in pygame.event.get():
                if p_event.type == pygame.KEYDOWN:
                    print("END")
                    return


# game mechanic
def main():
    reset_all()
    global event, s_full_coords_list  # for other functions that needs calling event
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(8)
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                exit()
            # wasd key, chande direction
            if event.type == pygame.KEYDOWN:
                change_direction()
                check_pause()
        change_s_coords()
        generate_snake()
        generate_cube()
        check_touch_wall()
        check_eat_cube()
        delete_snake_tail()
        check_win()

if __name__ == "__main__":
    main()
