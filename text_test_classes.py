import pygame
from pygame.locals import (K_a, K_w, K_d, K_s, KEYDOWN, K_ESCAPE, QUIT)
import re
import pyperclip


# enable stuff like moving cursor
class TextSurface(pygame.sprite.Sprite):
    def __init__(self, screen, text, text_color=(255, 255, 255), aa=True, font_size=40, font_file=None,
                 add_cursor=True, cursor_width=2, cursor_colour=(255, 255, 255), curse_blink_interval=333.33):
        super().__init__()

        self.text = text
        self.aa = aa
        self.text_color = text_color
        self.font_file = font_file
        self.font_size = font_size
        self.screen = screen
        self.add_cursor = add_cursor
        self.cursor_width = cursor_width
        self.cursor_colour = cursor_colour
        self.curse_blink_interval = curse_blink_interval

        self.font = pygame.font.SysFont(self.font_file, self.font_size)
        self.surface = self.font.render(self.text, self.aa, self.text_color)
        self.rect = self.surface.get_rect()
        self.enable_full_word_deletion = True
        self.enable_copy_pasting = True

    def update(self, events):
        pressed_keys = pygame.key.get_pressed()

        if self.add_cursor:
            if pygame.time.get_ticks() % 1000 > self.curse_blink_interval:
                pygame.draw.line(
                    self.screen, self.cursor_colour, self.rect.topright, self.rect.bottomright, self.cursor_width)

        for event in events:
            if event.type == KEYDOWN:

                if (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and pressed_keys[pygame.K_v] \
                        and self.enable_copy_pasting:

                    self.text = self.text + pyperclip.paste()

                if pressed_keys[pygame.K_BACKSPACE]:
                    # delete full words
                    if (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and not len(self.text) == 0 \
                            and self.enable_full_word_deletion:

                        split_string = re.findall(r"\w+(?:(?<=\d)[;,.]?\d+|[':]?\w*)+[^\w]*", self.text)
                        converted_list = [len(element) for element in split_string]

                        self.text = self.text[:-converted_list[-1]]
                    else:
                        self.text = self.text[:-1]

                else:
                    self.text = self.text + event.unicode

                # update screen
                self.surface = self.font.render(self.text, self.aa, self.text_color)
                self.rect = self.surface.get_rect()


if __name__ == "__main__":
    print("changed")  # hey  # test
