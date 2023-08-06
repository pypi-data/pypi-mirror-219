import pygame
from pygame import Color

from robingame.objects import Game, Group, Particle
from robingame.utils import random_float


class ParticleExample(Game):
    window_caption = "Particle example"
    screen_color = (50, 50, 50)
    window_width = 500
    window_height = 500

    def __init__(self):
        super().__init__()
        self.particles = Group()
        self.child_groups = [self.particles]

    def print_debug_info(self):
        print(f"{len(self.particles)=}")

    def update(self):
        super().update()
        left, middle, right = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        if left:
            self.particles.add(
                Particle(
                    x=x,
                    y=y,
                    radius=30,
                    color=Color("white"),
                    decay=0.1,
                )
            )
        if middle:
            self.particles.add(
                Particle(
                    x=x,
                    y=y,
                    v=random_float(-15, -10),
                    radius=random_float(20, 30),
                    decay=random_float(0.2, 0.5),
                    gravity=0.5,
                    color=Color("blue"),
                )
                for _ in range(10)
            )
        if right:
            self.particles.add(
                Particle(
                    x=x,
                    y=y,
                    radius=random_float(5, 30),
                    decay=random_float(0.2, 0.5),
                    gravity=random_float(0.1, 1),
                    color=Color("yellow"),
                )
            )


if __name__ == "__main__":
    ParticleExample().main()
