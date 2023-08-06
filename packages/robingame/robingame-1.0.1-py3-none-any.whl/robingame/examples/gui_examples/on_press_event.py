from dataclasses import dataclass

import pygame.mouse

from robingame.examples.gui_examples.coloured_button_effects import MyButton
from robingame.gui import Menu
from robingame.input import EventQueue
from robingame.objects import Game, Group


class OnPressEventExample(Game):
    """
    This is an example where the hooks increment/decrement a value stored on the outer Game class.
    """

    screen_color = (50, 50, 50)

    def __init__(self):
        super().__init__()
        self.value = 0
        self.scenes = Group()
        self.particles = Group()
        self.child_groups += [self.scenes, self.particles]
        menu = Menu()
        self.scenes.add(menu)
        menu.buttons.add(
            MyButton(
                x=200,
                y=100,
                width=200,
                height=50,
                text="change value",
                on_press=lambda button: EventQueue.add(ChangeValue(amount=5)),
                on_release=lambda button: EventQueue.add(ChangeValue(amount=-5)),
                on_focus=lambda button: EventQueue.add(ChangeValue(amount=1)),
                on_unfocus=lambda button: EventQueue.add(ChangeValue(amount=-1)),
            )
        )

    def update(self):
        super().update()
        self.listen_events()

    def listen_events(self):
        if event := EventQueue.get(type=ChangeValue.type):
            self.value += event.amount
            print(f"{self.value=}")


@dataclass
class ChangeValue:
    type = pygame.event.custom_type()
    amount: int = 1


if __name__ == "__main__":
    OnPressEventExample().main()
