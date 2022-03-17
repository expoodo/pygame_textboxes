import pygame
import re
import pyperclip


def separate_words(text: str, return_len_values: bool = False, custom_separators: tuple | list = ("':", ";,.")):
    """
    Returns a list of the separated words in a string. A word is defined as a substring surrounded by separator. All
    non-alphanumeric characters are separators except `;,.` for substrings that end with digits, and `':` for words.
    :param text: String to be modified
    :param custom_separators: Custom separators. 1st element are for words, 2nd are for digits. Each element is a string
    with all the characters inside. Custom characters will overwrite the default values of `':` and `;,.`
    :param return_len_values: Changes each element (word) into its length of characters (default value is False)
    :return: Returns list of every word with its separators on the right if there are any
    """

    # make element have all non-alphanumeric characters as separators if it is None or ''
    custom_separators = ["^\w\W" if s is None or s == "" else s for s in custom_separators]

    split_string = re.findall(fr"\w+(?:(?<=\d)[{custom_separators[1]}]?\d+|[{custom_separators[0]}]?\w*)+\W*|\W+", text)

    if return_len_values:
        split_string = [len(element) for element in split_string]

    return split_string


class TextLine(pygame.sprite.Sprite):
    """
    Class for managing a single line of text.

    cursor position is a number for each character in text, and 0 makes the cursor on the left.

    :param text: Text to be shown
    :param font: The font file
    :param size: Size of the font (in pixels)
    :param colour: Colour of the text
    :param antialias: Antialiasing for the text (default is True)
    :param text_background: colour of the text background (default is None)
    :param bold: Bool if font is bold or not
    :param italic: Bool if font is italicized or not
    """

    def __init__(self, text, font, size, colour, antialias=True, text_background=None, bold=False, italic=False):
        self._text = text
        self._antialias = antialias
        self._colour = colour
        self._font_file = font
        self._font_size = size
        self._text_background = text_background
        self._bold = bold
        self._italic = italic

        self._font = pygame.font.SysFont(self._font_file, self._font_size, self._bold, self._italic)
        self._surface = self._font.render(self._text, self._antialias, self._colour, self._text_background)
        self._rect = self._surface.get_rect()
        self._update_requested = False

        self.cursor = CursorManager(self._text, self._colour)
        self._left_text, self._right_text = self.cursor.get_split_text()
        self._left_text_size = self._font.size(self._left_text)
        self._right_text_size = self._font.size(self._right_text)  # GOAL: MAKE CURSOR ITALICIZED (TILTED) WHEN FONT IS
        # also try to prevent surface update spamming when attributes are changed
        self.is_focused = True

        self._request_update()
        super().__init__()

    def _request_update(self):
        """request for surface to be updated"""
        self._update_requested = True

    def _update_surface(self):
        """update surface and make surface larger to fit in the cursor (only if it is requested)"""
        if self._update_requested:
            text_surface = self._font.render(self._text, self._antialias, self._colour, self._text_background)
            background_surface = pygame.Surface((text_surface.get_width() + self.cursor.width,
                                                 text_surface.get_height()))

            self._surface = background_surface
            self._surface.blit(text_surface, (1, 0))
            self._rect = self._surface.get_rect()

            if self.cursor.visible and self.cursor.enabled:
                # update left and right substrings around cursor and fill the cursor into the surface
                self._left_text, self._right_text = self.cursor.get_split_text()
                self._left_text_size = self._font.size(self._left_text)
                self._right_text_size = self._font.size(self._right_text)

                cursor_size = (self.cursor.width, self._surface.get_height())
                cursor_pos = (self._left_text_size[0], self._rect.top)
                self._surface.fill(self.cursor.colour, (cursor_pos, cursor_size))

            self._update_requested = False
            print(f"updating surface {pygame.time.get_ticks()}")

    def _check_for_cursor_changes(self):
        """check if `self.cursor` properties have been changed"""
        if self.cursor.property_changed:
            self.cursor._property_changed = False
            self._request_update()

    def update(self, events):
        """check for key events and update surface/cursor if it is requested"""
        self._update_surface()

        if self.is_focused:
            self._check_for_cursor_changes()
            self.cursor.blink()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[pygame.K_BACKSPACE]:
                        if len(self.left_text) != 0:
                            if pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]:  # delete words
                                split_string = separate_words(self.left_text, True)

                                self.left_text = self.left_text[:-split_string[-1]]
                            else:
                                self.left_text = self.left_text[:-1]
                            self.cursor.override_cursor_visibility(True)

                    elif pressed_keys[pygame.K_RIGHT]:
                        self.cursor.move_cursor_right()
                        self.cursor.override_cursor_visibility(True)

                    elif pressed_keys[pygame.K_LEFT]:
                        self.cursor.move_cursor_left()
                        self.cursor.override_cursor_visibility(True)

                    else:
                        if len(event.unicode) != 0:  # prevent non character inputs from updating surface
                            self.left_text += event.unicode
                            self.cursor.override_cursor_visibility(True)

    def _update_text(self):
        """update `self.text` property by combining the left and right text of the cursor"""
        self.text = self.left_text + self.right_text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        """update screen to display changed text and also update CursorManager's version of the text"""
        self._text = value
        self.cursor._text = value
        self._request_update()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface):
        self._surface = value
        self._request_update()

    @property
    def left_text(self):
        return self._left_text

    @left_text.setter
    def left_text(self, value: str):
        """when text is added to the left of the cursor move cursor by the amount of characters added"""
        self._left_text = value
        self.cursor.position = len(value)
        self._update_text()

    @property
    def right_text(self):
        return self._right_text

    @right_text.setter
    def right_text(self, value: str):
        self._right_text = value
        self._update_text()

    @property
    def is_focused(self):
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value: bool):
        """
        disable cursor and input to object when False, (though still listen for property changes). Make cursor
        visible when object is focused
        """
        self._is_focused = value
        self.cursor.enabled = value
        self.cursor.override_cursor_visibility(value)
        self._request_update()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._request_update()

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self, value: bool):
        self._antialias = value
        self._request_update()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value: (int, int, int)):
        self._colour = value
        self._request_update()

    @property
    def text_background(self):
        return self._text_background

    @text_background.setter
    def text_background(self, value: (int, int, int)):
        self._text_background = value
        self._request_update()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: pygame.Rect):
        self._rect = value
        self._request_update()

    @property
    def font_file(self):
        return self._font_file

    @font_file.setter
    def font_file(self, value: str):
        self._font_file = value
        self.font = pygame.font.SysFont(self._font_file, self._font_size)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        self._font_size = value
        self.font = pygame.font.SysFont(self._font_file, self._font_size, self._bold, self._italic)

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value: bool):
        self._bold = value
        self.font.set_bold(value)

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, value: bool):
        self._italic = value
        self.font.set_italic(value)


class CursorManager:
    """
    Class for holding cursor settings and manipulation methods.

    :param text: the text that the cursor will be based on
    :param colour: colour of the text
    :param position: position of the cursor corresponding to the position of characters in the text (default value is
    the length of the text). position 0 means the cursor is on the left of the leftmost cursor.
    """

    def __init__(self, text, colour: (int, int, int), position: int = None):
        self._colour = colour
        self._text = text
        self._position = len(self._text) if position is None else position
        self._width = 1
        self._blink_interval = 500
        self._time_visible = 500
        self._visible = True
        self._elapsed_time = 0
        self._property_changed = False
        self._previous_tick_visible = pygame.time.get_ticks()
        self._enabled = True

    def alert_change(self):
        """change _property_changed variable to True when a property is changed"""
        self._property_changed = True

    def move_cursor_left(self):
        """move cursor to the left only if cursor position is not 0"""
        if self.position > 0:
            self.position -= 1

    def move_cursor_right(self):
        """move cursor to the right only if cursor pos is not at the end of the provided text"""
        if self.position != len(self._text):
            self.position += 1

    def get_split_text(self):
        """return the left and right substrings around the cursor position"""
        left_text = self._text[:self.position]
        right_text = self._text[self.position:]

        return left_text, right_text

    def override_cursor_visibility(self, visible: bool):
        """override `blink()` to make cursor visible (which will be visible for the time specified in `_time_visible`"""
        if visible:
            self._previous_tick_visible = pygame.time.get_ticks() - self._blink_interval
        else:
            self._previous_tick_visible = pygame.time.get_ticks()

    def blink(self):
        """
        check if the specified interval has been passed since the cursor was last visible, and if so, make the cursor
        visible.
         """
        if self.enabled:
            self._elapsed_time = pygame.time.get_ticks() - self._previous_tick_visible

            # if elapsed time is between `_blink_interval` and `time_visible + _blink_interval`
            if self._blink_interval <= self._elapsed_time <= self._time_visible + self._blink_interval:
                if not self.visible:
                    self.visible = True
            else:
                if self.visible:
                    self._previous_tick_visible = pygame.time.get_ticks()
                    self.visible = False
        else:
            self._visible = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.alert_change()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value: (int, int, int)):
        self._colour = value
        self.alert_change()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        self.alert_change()

    @property
    def blink_interval(self):
        return self._blink_interval

    @blink_interval.setter
    def blink_interval(self, value: int):
        """in milliseconds"""
        self._blink_interval = value
        self.alert_change()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value
        self.alert_change()

    @property
    def time_visible(self):
        return self._time_visible

    @time_visible.setter
    def time_visible(self, value: int):
        """in milliseconds"""
        self._time_visible = value
        self.alert_change()

    @property
    def property_changed(self):
        return self._property_changed

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self.alert_change()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.alert_change()


if __name__ == "__main__":
    print(separate_words("lol"))
