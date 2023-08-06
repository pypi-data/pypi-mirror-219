import pygame
from pygame import Surface, Rect, Color

from robingame.input import EventQueue
from robingame.objects import Game, Group, Entity
from robingame.text import fonts


class Follower(Entity):
    rect: Rect

    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = Rect(x, y, 200, 50)
        self.state = self.state_idle  # set initial state

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        # draw a filled white rectangle
        pygame.draw.rect(surface, Color("white"), self.rect)

        # draw some text
        fonts.cellphone_black.render(surface, "Drag me!", *self.rect.topleft, scale=3)

        # if debug is enabled (press F1 to toggle) draw a red outline and also the center of
        # self.rect
        if debug:
            pygame.draw.rect(surface, Color("red"), self.rect, width=2)
            pygame.draw.circle(surface, Color("red"), self.rect.center, radius=2)

    def state_idle(self):
        """
        Do nothing.
        If the left mouse button is pressed, switch to state_follow.
        """
        if EventQueue.get(type=pygame.MOUSEBUTTONDOWN, button=1):
            self.state = self.state_follow

    def state_follow(self):
        """
        Follow the mouse around the screen.
        If the left mouse button is released, switch to state_idle.
        """
        self.rect.center = pygame.mouse.get_pos()  # follow the mouse

        if EventQueue.get(type=pygame.MOUSEBUTTONUP, button=1):
            self.state = self.state_idle


class HelloWorld(Game):
    window_caption = "Hello, world!"
    window_width = 500
    window_height = 500

    def __init__(self):
        super().__init__()

        # create a Group to store sub-objects
        self.children = Group()

        # register the group with `self.child_groups` so that Game.update also calls the
        # `.update()` method of `self.children`
        self.child_groups = [self.children]

        # Add an object to the children group
        self.children.add(Follower(x=10, y=10))


if __name__ == "__main__":
    HelloWorld().main()
