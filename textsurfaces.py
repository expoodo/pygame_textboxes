import pygame


class TextLine(pygame.sprite.Sprite):
    """
    Class for managing a single line of text.

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
        self._request_update = False
        self._is_focused = True

        self.cursor_width = 2
        self.cursor_blink_interval = 0.33

        super().__init__()

    def request_update(self):
        """request for surface to be updated"""
        self._request_update = True

    def _update_surface(self):
        """update surface and make surface larger to fit in the cursor"""
        if self._request_update:
            self._surface = self._font.render(self._text, self._antialias, self._colour)
            self._rect = self._surface.get_rect()
            self._request_update = False

    def update(self, events):
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

