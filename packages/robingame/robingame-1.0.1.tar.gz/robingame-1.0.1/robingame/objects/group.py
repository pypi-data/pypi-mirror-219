import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from robingame.objects.entity import Entity


class Group(pygame.sprite.Group):
    """Container for multiple Entities."""

    def add(self, *entities: "Entity") -> None:
        """
        Does the same thing as pygame's `Group.add()`.
        Only overriding this because pygame's typing was making the linter complain.
        """
        super().add(*entities)

    def update(self, *args):
        """
        Call `.update()` on all member Entities.
        """
        super().update(*args)

    def draw(self, surface: pygame.Surface, debug: bool = False):
        """
        Call `.draw(surface, debug)` on all member Entities.

        This is different from pygame's `Group.draw()` in that it calls the `Entity.draw()` method
        (thus allowing the Entity to decide how to draw itself) instead of just blitting the
        Entity's `.image` onto the surface.
        """
        entities = self.sprites()
        for entity in entities:
            entity.draw(surface, debug)
        self.lostsprites = []

    def kill(self):
        """
        Call `.kill()` on all the entities in this group.
        This is different from `Group.empty()`.
        """
        for entity in self:
            entity.kill()
