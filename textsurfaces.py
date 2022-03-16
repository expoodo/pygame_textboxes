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
        self._font_file = font
        self._font_size = size

        self._font = pygame.font.SysFont(self._font_file, self._font_size)
        self._surface = self._font.render(self._text, self._antialias, self._colour)
        self._rect = self._surface.get_rect()
        self._update_requested = False
        self._is_focused = True

        self.cursor = CursorManager(self._colour, 1)
        self._left_text, self._right_text = self.cursor.get_split_text(self.text)
        self._left_text_size = self._font.size(self._left_text)
        self._right_text_size = self._font.size(self._right_text)

        self._request_update()
        super().__init__()

    def _request_update(self):
        """request for surface to be updated"""
        self._update_requested = True

    def _update_surface(self):
        """update surface and make surface larger to fit in the cursor (only if it is requested)"""
        if self._update_requested:
            text_surface = self._font.render(self._text, self._antialias, self._colour)
            background_surface = pygame.Surface((text_surface.get_width() + self.cursor.width,
                                                 text_surface.get_height()))

            self._surface = background_surface
            self._surface.blit(text_surface, (1, 0))
            self._rect = self._surface.get_rect()

            if self.cursor.visible:
                # update left and right substrings around cursor and fill the cursor into the surface
                self._left_text, self._right_text = self.cursor.get_split_text(self.text)
                self._left_text_size = self._font.size(self._left_text)
                self._right_text_size = self._font.size(self._right_text)
                # print("updating")

                cursor_size = (self.cursor.width, self._surface.get_height())
                cursor_pos = (self._left_text_size[0], self._rect.top)
                self._surface.fill(self.cursor.colour, (cursor_pos, cursor_size))

            self._update_requested = False
            # print(f"updating surface {pygame.time.get_ticks()}")

    def _check_for_cursor_changes(self):
        """check if `self.cursor` properties have been changed"""
        if self.cursor.property_changed:
            self.cursor.property_changed = False
            self._request_update()

    def update(self, events):
        """check for key events and update surface/cursor if it is requested"""
        self._check_for_cursor_changes()
        self._update_surface()

        if self._is_focused:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[pygame.K_BACKSPACE]:
                        self.left_text = self.left_text[:-1]

                    elif pressed_keys[pygame.K_RIGHT]:
                        self.cursor.move_cursor_right(self.text)
                    elif pressed_keys[pygame.K_LEFT]:
                        self.cursor.move_cursor_left()

                    else:
                        if len(event.unicode) != 0:  # prevent non character inputs from updating surface
                            self.left_text += event.unicode

    def _update_text(self):
        """update `self.text` property by combining the left and right text of the cursor"""
        self.text = self.left_text + self.right_text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._request_update()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
        self._request_update()

    @property
    def left_text(self):
        return self._left_text

    @left_text.setter
    def left_text(self, value):
        """when text is added to the left of the cursor move cursor by the amount of characters added"""
        self._left_text = value
        self.cursor.position = len(value)
        self._update_text()

    @property
    def right_text(self):
        return self._right_text

    @right_text.setter
    def right_text(self, value):
        self._right_text = value
        self._update_text()


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
        self._width = 1
        self._blink_interval_ms = 333
        self._visible = True
        self.property_changed = False

        self._left_text = ""

    def alert_change(self):
        """change _property_changed variable to True when a property is changed"""
        self.property_changed = True

    def move_cursor_left(self):
        """move cursor to the left only if cursor position is not 0"""
        if self.position > 0:
            self.position -= 1

    def move_cursor_right(self, text: str):
        """move cursor to the right only if cursor pos is not at the end of the provided text"""
        if self.position != len(text):
            self.position += 1

    def get_split_text(self, text: str):
        """return the left and right substrings around the cursor position"""
        left_text = text[:self.position]
        right_text = text[self.position:]

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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.alert_change()


if __name__ == "__main__":
    foo = CursorManager((255, 255, 255))

    print("lolguys"[:2])
