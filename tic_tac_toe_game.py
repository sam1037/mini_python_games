"""
23/08/19 finished.
30/8:
    added msg to screen and another round function.
2/9:
    added button class for another_round. Figured out how to exit code(hint: use exit())
4/9:
    Finished start menu and choosing figure to play. Working on ai(single player mode).
5/9:
    Added ai, pretty much not work.
6/9:
    Optimized ai. Done.
7/9:
    Made you can play after two round (removed set_next_round_false()).
    Made after another_round(), you can choose mode. TIL mousebuttondown in pygame can active two buttons at once if
the time gap between the buttons is not big enough.

Criticize:
    I should maintain the same logic. I shouldn't use position which is [x, y] in one function and use (x, y) in another
function.
    I should use another way to do all that set_xxx_false().
"""
# todo <long> add number draw figures function.
import pygame
import time
import random

# init
pygame.init()

# constant
co = 0
block_state = ['empty'] * 9  # blockstate is a list that represents the state of the nine block in the game.
turn = 0  # 0 is circle, 1 is cross
white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)
bright_grey = (189, 189, 189)
run, checking, next_round, choosing_mode = True, True, True, True
win_height = 300
p1_figure = 0
win_list = [(0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)]

# draw window
window = pygame.display.set_mode((win_height, win_height))
pygame.display.set_caption("ttt game")


class Button:
    def __init__(self, func_list, rect, color1, color2=None, outline_color=None, msg_list=None):
        """

        :rtype: object
        """
        self.func_list = func_list
        self.rect = rect
        self.color1 = color1
        self.color2 = color2
        self.outline_color = outline_color
        self.msg_list = msg_list

    def draw_text(self):
        if self.msg_list is not None:
            font = pygame.font.SysFont(None, self.msg_list[2])
            screen_text = font.render(self.msg_list[0], True, self.msg_list[1])
            msg_x = (self.rect[0] * 2 + self.rect[2]) / 2 - screen_text.get_width() / 2
            msg_y = (self.rect[1] * 2 + self.rect[3]) / 2 - screen_text.get_height() / 2
            window.blit(screen_text, [msg_x, msg_y])
            pygame.display.update()

    def draw_button(self):
        pygame.draw.rect(window, self.color1, self.rect)
        self.draw_text()
        pygame.display.update()


    def button_react(self):  # must inside pygame.event.get loop
        mouse = pygame.mouse.get_pos()
        if mouse[0] in range(self.rect[0], self.rect[0] + self.rect[2]) and mouse[1] in range(self.rect[1],
                                                                                              self.rect[1] +
                                                                                              self.rect[3]):
            # if mouse on top of a button, button change color
            if self.color2 is not None:
                pygame.draw.rect(window, self.color2, self.rect)
                if self.outline_color is not None:
                    pygame.draw.rect(window, self.outline_color, self.rect, 1)
                self.draw_text()
            # if click button, fo functions
            if event.type == pygame.MOUSEBUTTONDOWN:
                for func in self.func_list:
                    func()
                return
        else:
            self.draw_button()
        pygame.display.update()
        return

    def exec_func(self):
        for func in self.func_list:
            func()
        return


def set_constant():
    global block_state, turn, white, black, grey, bright_grey, run, checking, next_round, choosing_mode, win_height, p1_figure, win_list
    block_state = ['empty'] * 9  # blockstate is a list that represents the state of the nine block in the game.
    turn = 0  # 0 is circle, 1 is cross
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (169, 169, 169)
    bright_grey = (189, 189, 189)
    run, checking, next_round, choosing_mode = True, True, True, True
    win_height = 300
    p1_figure = 0
    win_list = [(0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6)]
    return


def draw_grid():
    window.fill(white)
    pygame.draw.line(window, (0, 0, 0), [0, 0], [300, 0])
    pygame.draw.line(window, (0, 0, 0), [100, 0], [100, 300])
    pygame.draw.line(window, (0, 0, 0), [200, 0], [200, 300])
    pygame.draw.line(window, (0, 0, 0), [0, 100], [300, 100])
    pygame.draw.line(window, (0, 0, 0), [0, 200], [300, 200])

    pygame.display.flip()


def another_round():
    global run, block_state, turn, checking, event, next_round
    window.fill(white)
    pygame.draw.line(window, black, [0, 0], [300, 0])

    def set_next_round_false():
        global next_round
        next_round = False

    # button
    button_play_again = Button([set_constant, choose_mode],
                               [50, 80, 200, 60],
                               bright_grey, grey, black,
                               ["Play Again", black, 40])
    button_exit = Button([exit],
                         [50, 180, 200, 60],
                         bright_grey, grey,
                         black,
                         ["Exit", black, 40])

    button_play_again.draw_button()
    button_exit.draw_button()

    while next_round:
        pygame.time.delay(50)

        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                exit()
            button_play_again.button_react()
            button_exit.button_react()


# text on screen
def msg_to_screen(msg, color, size, screen = window, screen_width = win_height, screen_deepth = win_height, position=None):
    """
    :param msg: the msg you want to send
    :param color: msg's color
    :param size: msg's size
    :param position: default position is the center of the window
    :return:
    """
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(msg, True, color)
    if position is None:
        screen.blit(screen_text,
                    [screen_width / 2 - screen_text.get_width() / 2, screen_deepth / 2 - screen_text.get_height() / 2])
    else:
        window.blit(screen_text, position)
    pygame.display.update()


# check if win
def check_win():
    global checking, win_list
    if checking:
        for turn in range(0,2):
            figures_pos_list = [i for i, e in enumerate(block_state) if e == turn]  # this list consists of the figures' pos.
            for winning_combination in win_list:
                if winning_combination[0] in figures_pos_list and winning_combination[1] in figures_pos_list and \
                        winning_combination[2] in figures_pos_list:
                    time.sleep(0.3)
                    window.fill(white)
                    pygame.draw.line(window, (0, 0, 0), [0, 0], [300, 0])
                    if turn == 0:
                        msg_to_screen("Circle wins!", black, 50)
                    if turn == 1:
                        msg_to_screen("Cross wins!", black, 50)
                    time.sleep(1)
                    checking = False
                    another_round()
                    return


# block: turn position(must center) into block number
def block(x, y):
    if y == 50:
        if x == 50:
            return 0
        if x == 150:
            return 1
        if x == 250:
            return 2
    if y == 150:
        if x == 50:
            return 3
        if x == 150:
            return 4
        if x == 250:
            return 5
    if y == 250:
        if x == 50:
            return 6
        if x == 150:
            return 7
        if x == 250:
            return 8


def block_to_center(block):  # turn block number into center position of the block
    if block == 0:
        return (50,50)
    if block == 1:
        return (150,50)
    if block == 2:
        return (250,50)
    if block == 3:
        return (50,150)
    if block == 4:
        return (150,150)
    if block == 5:
        return (250,150)
    if block == 6:
        return (50,250)
    if block == 7:
        return (150,250)
    if block == 8:
        return (250,250)


# check tie
def check_tie():
    global run, checking
    count = 0
    for block in block_state:
        if block != 'empty':
            count += 1
        if count == 9:
            time.sleep(0.3)
            window.fill(white)
            pygame.draw.line(window, (0, 0, 0), [0, 0], [300, 0])
            msg_to_screen("Tie game!", black, 50)
            time.sleep(1)
            checking = False
            another_round()
            return


# Turn coordinates into the coordinates of the center of a block
def reposition(x, y):
    if y <= 100:
        y = 50
    else:
        y -= 1
        y = str(y)
        y = y[:1] + "50"
        y = int(y)
    if x <= 100:
        x = 50
    else:
        x -= 1
        x = str(x)
        x = x[:1] + "50"
        x = int(x)
    return x, y


# def draw
def draw(position):  # position must be center
    # circle
    if turn == 0:
        pygame.draw.circle(window, black, position, 45, 3)
    # cross
    if turn == 1:
        pygame.draw.line(window, black, (position[0] + 40, position[1] - 40), (position[0] - 40, position[1] + 40), 3)
        pygame.draw.line(window, black, (position[0] - 40, position[1] - 40), (position[0] + 40, position[1] + 40), 3)
    pygame.display.update()
    block_state[block(position[0], position[1])] = turn


# choose figure page
def choose_circle_or_cross():
    window.fill(white)
    pygame.draw.line(window, black, [0, 0], [300, 0])
    pygame.display.flip()

    def choose_cross():
        global turn, p1_figure
        turn = 1
        p1_figure = 1  # 1 is cross. 0 is circle

    def set_choosing_false():
        global choosing_figure
        choosing_figure = False

    button_choose_circle = Button([set_choosing_false, start_game],
                                  [50, 80, 200, 60],
                                  bright_grey,
                                  grey,
                                  black,
                                  ["Choose circle to play", black, 25])
    button_choose_cross = Button([choose_cross, start_game],
                                 [50, 180, 200, 60],
                                 bright_grey,
                                 grey,
                                 black,
                                 ["Choose cross to play", black, 25])

    button_choose_cross.draw_button()
    button_choose_circle.draw_button()

    choosing_figure = True
    global event  # why add this and button works?????
    while choosing_figure:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            button_choose_circle.button_react()
            if choosing_figure:
                button_choose_cross.button_react()
                # else return


def choose_mode():
    def single_player_mode():
        global single_player
        single_player = True

    def duo_player_mode():
        global single_player
        single_player = False

    def set_choosing_mode_false():
        global choosing_mode
        choosing_mode = False

    # draw win
    window.fill(white)
    pygame.draw.line(window, black, [0, 0], [300, 0])
    pygame.display.flip()

    button_single_player_mode = Button([single_player_mode, set_choosing_mode_false, choose_circle_or_cross],
                                       [50, 80, 200, 60],
                                       bright_grey,
                                       grey,
                                       black,
                                       ["Single player mode", black, 30])
    button_duo_player_mode = Button([duo_player_mode, set_choosing_mode_false, choose_circle_or_cross],
                                    [50, 180, 200, 60],
                                    bright_grey,
                                    grey,
                                    black,
                                    ["Duo player mode", black, 30])

    button_single_player_mode.draw_button()
    button_duo_player_mode.draw_button()
    pygame.time.delay(100) # if this time is too short, the mouse will click two buttons at once
    global event

    while choosing_mode:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        button_duo_player_mode.button_react()
        if choosing_mode:
            button_single_player_mode.button_react()


def ai():
    global turn
    ai_run = True
    ai_figure = (p1_figure + 1) % 2
    ai_figure_pos_list = [i for i, e in enumerate(block_state) if e == ai_figure]  # this list consists of the ai
    # figures' pos.
    p1_figure_pos_list = [i for i, e in enumerate(block_state) if e == p1_figure]  # this list consists of the ai
    # figures' pos.
    e = 0
    # check if ai one step form winning, do it
    for winning_combination in win_list:
        if ai_run:
            for cycle in range(3):
                one_step_left_list = [item for item in winning_combination if item != winning_combination[e]]
                if [item for item in ai_figure_pos_list if item in one_step_left_list] == one_step_left_list:
                    if block_state[winning_combination[e]] == 'empty':
                        draw(block_to_center(winning_combination[e]))
                        ai_run = False
                        break
                e += 1
                e %= 3
    # check if p1 one step form winning, stop it
    for winning_combination in win_list:
        if ai_run:
            for cycle in range(3):
                one_step_left_list = [item for item in winning_combination if item != winning_combination[e]]
                if [item for item in p1_figure_pos_list if item in one_step_left_list] == one_step_left_list:
                    if block_state[winning_combination[e]] == 'empty':
                        draw(block_to_center(winning_combination[e]))
                        ai_run = False
                        break
                e += 1
                e %= 3
    # random do one step
    if ai_run:
        while True:
            random_block = random.randint(0, 8)
            if block_state[random_block] == 'empty':
                draw(block_to_center(random_block))
                break
    # check win, check tie, reset turn
    turn += 1
    turn %= 2
    check_win()
    if checking:
        check_tie()
    return


def start_game():
    draw_grid()
    global run, turn, x, y, event, single_player
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                exit()
            # click then draw stuff & set turn & check win, tie
            if not single_player or turn == p1_figure:  # player turn
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    x, y = reposition(mx, my)
                    if block_state[block(x, y)] == "empty":
                        draw((x, y))
                        pygame.time.delay(50)  # to show the figure
                        turn += 1
                        turn %= 2
                        check_win()
                        if checking:
                            check_tie()
            else:  # ai turn
                pygame.time.delay(50)
                ai()
                pygame.time.delay(50)


def main():
    choose_mode()


if __name__ == '__main__':
    main()
