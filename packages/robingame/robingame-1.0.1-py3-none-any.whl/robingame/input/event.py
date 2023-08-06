from dataclasses import dataclass, is_dataclass, asdict
from typing import Union

import pygame
from pygame.event import EventType, Event as PygameEvent

from robingame.image import init_display

init_display()


class EventQueue:
    """
    Pygame's pygame.event.get() empties the queue, which makes it impossible to listen to events
    in more than one location. This class solves that with a sort of singleton approach.
    """

    # this is intentional. I want to store the events on the class. Only one game will be active
    # at once, so we'll never need more than one instance of this class.
    events = []

    @classmethod
    def add(cls, event: Union[EventType, "dataclass"]):
        """
        Add the event to pygame's event queue, where it will stay until the .update() method
        is called to load it into cls.events.

        This prevents race conditions / order dependency where an event is added to the event
        queue and processed in the same tick.

        Args:
            event: object representing the event.
                Can be a `pygame.Event`, or a dataclass with
                attribute `type = pygame.event.custom_type()`
        """
        if is_dataclass(event):
            event = PygameEvent(event.type, **asdict(event))
        pygame.event.post(event)

    @classmethod
    def update(cls):
        """
        Read all the events from pygame's event queue into cls.events
        (also clears pygame's event queue)
        """
        cls.events = pygame.event.get()

    @classmethod
    def filter(cls, **kwargs) -> list[EventType]:
        return [
            event
            for event in cls.events
            if all(getattr(event, attribute, None) == value for attribute, value in kwargs.items())
        ]

    @classmethod
    def get(cls, **kwargs) -> EventType | None:
        try:
            return cls.filter(**kwargs)[0]
        except IndexError:
            return None
