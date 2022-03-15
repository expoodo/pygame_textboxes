import pygame


class TextLine(pygame.sprite.Sprite):
    """
    Class for managing a single line of text.

    cursor position is a number for each character in text, and 0 makes the cursor on the left.

    :param text: Text to be shown
    :param font: The font file
    :param size: Size of the font (in pixels)
    :param colour: Colour of the text
    :param antialias: Antialiasing for the text (default is True)
    """

    def __init__(self, text, font, size, colour, antialias=True):
        self._text = text
        self._antialias = antialias
        self._colour = colour

        self._font = pygame.font.SysFont(font, size)
        self._surface = self._font.render(self._text, self._antialias, self._colour)
        self._rect = self._surface.get_rect()
        self._update_requested = False
        self._is_focused = True

        self.cursor = CursorManager(self._colour)

        self.request_update()
        super().__init__()

    def request_update(self):
        """request for surface to be updated"""
        self._update_requested = True

    def _update_surface(self):
        """update surface and make surface larger to fit in the cursor"""
        if self._update_requested:
            text_surface = self._font.render(self._text, self._antialias, self._colour)
            background_surface = pygame.Surface((text_surface.get_width() + self.cursor.width,
                                                 text_surface.get_height()))

            self._surface = background_surface
            self._surface.blit(text_surface, text_surface.get_rect())
            self._rect = self._surface.get_rect()

            if self.cursor.visible:
                cursor_size = (self.cursor.width, self._surface.get_height())
                cursor_pos = (self._surface.get_width() - self.cursor.width, self._rect.top)
                self._surface.fill(self.cursor.colour, (cursor_pos, cursor_size))

            self._update_requested = False
            print(f"updating surface {pygame.time.get_ticks()}")

    def check_for_cursor_changes(self):
        """check if `self.cursor` properties have been changed"""
        if self.cursor.property_changed:
            self.cursor.property_changed = False
            self.request_update()

    def update(self, events):
        self.check_for_cursor_changes()

        if self._is_focused:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[pygame.K_BACKSPACE]:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
        self._update_surface()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.request_update()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
        self.request_update()


class CursorManager:
    """
    Class for holding cursor settings and manipulation methods.

    :param colour: colour of the text
    :param position: position of the cursor corresponding to the position of characters in the text.
    position 0 means the cursor is on the left of the leftmost cursor (default value is also 0)
    """

    def __init__(self, colour: (int, int, int), position: int = 0):
        self._colour = colour
        self._position = position
        self._width = 2
        self._blink_interval_ms = 333
        self._visible = True
        self.property_changed = False

        self._left_text = ""

    def alert_change(self):
        """change _property_changed variable to True when a property is changed"""
        self.property_changed = True

    def move_cursor_left(self):
        """move cursor to the left only if cursor position is not 0"""
        if self._position > 0:
            self._position -= 1

    def move_cursor_right(self, text: str):
        """move cursor to the right only if cursor pos is not at the end of the provided text"""
        if self._position != len(text):
            self._position += 1

    def get_split_text(self, text: str):
        """return the left and right substrings around the cursor position"""
        left_text = text[:self._position]
        right_text = text[self._position:]

        return left_text, right_text

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.alert_change()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        self._colour = value
        self.alert_change()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.alert_change()

    @property
    def blink_interval_ms(self):
        return self._blink_interval_ms

    @blink_interval_ms.setter
    def blink_interval_ms(self, value):
        self._blink_interval_ms = value
        self.alert_change()


if __name__ == "__main__":
    foo = CursorManager((255, 255, 255))

    print("lolguys"[:2])
