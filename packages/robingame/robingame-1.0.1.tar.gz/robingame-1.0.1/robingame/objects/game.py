import sys

import pygame
from pygame.color import Color
from pygame.surface import Surface

from robingame.input import EventQueue
from robingame.objects.entity import Entity
from robingame.objects.helpers import FpsTracker


class Game(Entity):
    """
    Special case of Entity; it is at the very top of the object tree.

    Handles much of the pygame boilerplate setup, including:

    - initialising the display
    - setting up and running the main game loop.
    - doing `clock.tick()` every iteration and enforcing the framerate
    - filling the screen with `self.screen_color` every iteration
    - updating the EventQueue with new events
    - maintaining the FPS tracker (and drawing it in debug mode)
    """

    fps: int = 60
    window_width: int = 500
    window_height: int = 500
    window_caption: str = "Game"
    screen_color = Color("black")
    debug: bool = False  # draw / print debug info?
    running: bool  # is the main game loop running

    def __init__(self):
        """
        Handles a lot of the boilerplate pygame setup.
        Creates the display (`self.window`).
        """
        super().__init__()
        pygame.init()
        self.fps_tracker = FpsTracker()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()

    def main(self):
        """
        Contains the main game loop.
        Calls `self._update()` and `self._draw()` on every iteration of the game loop.
        """
        self.running = True
        while self.running:
            self._update()
            self._draw(self.window, debug=self.debug)
        pygame.quit()
        sys.exit()

    def read_inputs(self):
        """
        Called by `self._update()`, before `super().update()` updates the children.

        Any code that polls external joysticks/controllers should go here.
        """

        # I've put this in a separate method because I don't like the idea of putting the inputs
        # in the same list as other child groups. The order might get ruined, or a subclass might
        # overwrite the list. It's crucial that the inputs are read before updating.
        EventQueue.update()
        for event in EventQueue.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                self.debug = not self.debug

    def print_debug_info(self):
        """
        Override this if you want to print any debug info.
        """
        pass

    def _update(self):
        """
        1. read inputs
        2. update
        """
        self.read_inputs()
        if self.debug:
            self.print_debug_info()
        self.update()
        self.fps_tracker.update()
        if self.fps:
            self.clock.tick(self.fps)

    def _draw(self, surface: Surface, debug: bool = False):
        surface.fill(self.screen_color)  # clear the screen
        self.draw(surface, debug)
        self.fps_tracker.draw(surface, debug)
        pygame.display.update()  # print to screen
