import pygame

from robingame.input.queue import InputQueue


class KeyboardInputQueue(InputQueue):
    """
    Tracks the history of the keyboard input channels.

    Example:
        ```
        keyboard_handler = KeyboardInputQueue()
        if keyboard_handler.is_pressed(pygame.K_ESC):
            pygame.quit()
        ```
    """

    def get_new_values(self) -> tuple[int]:
        scancode_wrapper = pygame.key.get_pressed()
        return tuple(scancode_wrapper[ii] for ii in range(len(scancode_wrapper)))
