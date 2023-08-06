from typing import Iterable

import numpy
import pygame

from robingame.animation import ease_in_out
from robingame.gui.button import Button
from robingame.objects import Entity, Group
from robingame.utils import mouse_hovering_over


class Menu(Entity):
    """Base menu class."""

    def __init__(self, groups: Iterable[Group] = ()):
        super().__init__(groups)
        self.buttons: Group[Button] = Group()
        self.child_groups = [self.buttons]

    def update(self):
        self.update_buttons()
        super().update()

    def state_idle(self):
        pass

    def update_buttons(self):
        """todo: if you wanted to make this really efficient, you could only perform updates if
        an event is detected."""
        mouse_click = pygame.mouse.get_pressed()[0]
        for button in self.buttons:
            if mouse_hovering_over(button):
                button.is_focused = True
                button.is_pressed = mouse_click
            else:
                button.is_focused = False
                button.is_pressed = False
