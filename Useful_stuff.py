# todo hotkey for button as click button

import pygame
import keyboard as kd


# button
class Button:
    def __init__(self, func_list, rect, color1, color2=None, outline_color=None, msg_list=None, window = None, hotkey = None):
        """

        :rtype: object
        """
        self.func_list = func_list
        self.rect = rect
        self.color1 = color1
        self.color2 = color2
        self.outline_color = outline_color
        self.msg_list = msg_list
        self.window = window
        self.hotkey = hotkey

    def draw_text(self):
        if self.msg_list is not None:
            font = pygame.font.SysFont(None, self.msg_list[2])
            screen_text = font.render(self.msg_list[0], True, self.msg_list[1])
            msg_x = (self.rect[0] * 2 + self.rect[2]) / 2 - screen_text.get_width() / 2
            msg_y = (self.rect[1] * 2 + self.rect[3]) / 2 - screen_text.get_height() / 2
            self.window.blit(screen_text, [msg_x, msg_y])
            pygame.display.update()

    def draw_button(self):
        pygame.draw.rect(self.window, self.color1, self.rect)
        self.draw_text()
        pygame.display.update()

    def button_react(self):  # must inside loop
        for cevent in pygame.event.get():
            if cevent.type == pygame.QUIT:
                exit()
            mouse = pygame.mouse.get_pos()
            # if mouse is on top of a button, button change color
            if mouse[0] in range(self.rect[0], self.rect[0] + self.rect[2]) and mouse[1] in range(self.rect[1],
                                                                                                  self.rect[1] +
                                                                                                  self.rect[3]):
                if self.color2 is not None:
                    pygame.draw.rect(self.window, self.color2, self.rect)
                    if self.outline_color is not None:
                        pygame.draw.rect(self.window, self.outline_color, self.rect, 1)
                    self.draw_text()

                # if click button, run functions
                if cevent.type == pygame.MOUSEBUTTONDOWN:
                    for func in self.func_list:
                        func()
                    return

            # run func if hotkey is pressed
            for key in self.hotkey:
                if not kd.is_pressed(key):
                    return False
                else:
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
