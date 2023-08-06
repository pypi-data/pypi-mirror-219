from collections import deque

from robingame.utils import count_edges

# Represents the current state of 1 input channel.
# E.g. 1 for key pressed, 0 for key not pressed.
# But could also be float values for joystick axes.
InputChannel = int | float

# Array of InputChannels representing the state of an entire input device e.g. keyboard, joystick
# The index of each channel maps to its value (e.g. 0th elem = button A, 1st elem = button B, ...)
ChannelTuple = tuple[InputChannel, ...]


class Empty(tuple):
    """
    Mock tuple of 0/1s that always returns a 0 no matter the index. This is used to
    spoof an empty pygame.key.get_pressed() tuple.
    """

    def __getitem__(self, *args, **kwargs) -> int:
        return 0


class InputQueue(deque):
    """
    Provides additional functionality beyond pygame.key.get_pressed().
    Contains a series of ChannelTuples which represent the state history of the input device
    that this queue is tracking.
    This input history allows us to track which keys have been pressed and released this tick.

    Subclasses should implement `get_new_values`.
    """

    def __init__(self, queue_length=5):
        super().__init__(maxlen=queue_length)

    def get_new_values(self) -> ChannelTuple:
        """
        Subclasses should implement this.
        It should be something like pygame.key.get_pressed().

        Returns:
            a tuple of integers representing the states of the input channels
        """
        raise NotImplementedError

    def read_new_inputs(self):
        self.append(self.get_new_values())

    def get_down(self) -> ChannelTuple:
        """
        Return the keys which are currently held down.

        Returns:
            a tuple of values for each input channel. 0 = not down. Nonzero = down.
        """
        return self[-1] if len(self) > 0 else Empty()

    def get_pressed(self) -> ChannelTuple:
        """
        Return the keys that have just been pressed
        i.e. those that are down this tick but not the previous tick

        Returns:
            a tuple of integers for each input channel. 1 = pressed, 0 = not pressed.
        """
        try:
            current = self[-1]
            previous = self[-2]
            # we HAVE to use the __getattr__ method of the ScancodeWrapper
            # here. Using for/in to iterate over it gives erroneous results!
            # That's why I'm using the index to get the values.
            return tuple(
                int(current[i] and not previous[i])
                for (i, c), p in zip(enumerate(current), previous)
            )
        except IndexError:
            return Empty()

    def get_released(self) -> ChannelTuple:
        """
        Return the keys that have just been released
        i.e. those that are not down this tick, but were down the previous tick.

        Returns:
            a tuple of integers for each input channel. 1 = released, 0 = not released.
        """
        try:
            current = self[-1]
            previous = self[-2]
            return tuple(
                int(previous[i] and not current[i])
                for (i, c), p in zip(enumerate(current), previous)
            )
        except IndexError:
            return Empty()

    def is_pressed(self, key) -> int:
        """
        Check if a key has been pressed this tick

        Returns:
            1 if pressed; 0 otherwise
        """
        keys = self.get_pressed()
        return keys[key]

    def is_down(self, key) -> int:
        """
        Check if a key is currently held down

        Returns:
            1 if down; 0 otherwise
        """
        keys = self.get_down()
        return keys[key]

    def is_released(self, key) -> int:
        """
        Check if a key has been released this tick

        Returns:
            1 if released; 0 otherwise
        """
        keys = self.get_released()
        return keys[key]

    def buffered_inputs(self, key: int, buffer_length: int) -> tuple[int, int]:
        """
        Count the rising and falling edges. Can be used to detect past inputs.

        Args:
            key: identifier of the input channel
            buffer_length: how many past iterations to consider

        Returns:
            number of times the input channel has been pressed and released over the `buffer_length`
        """
        buffer = list(self)[-buffer_length:]
        values = [layer[key] for layer in buffer]
        return count_edges(values)

    def buffered_presses(self, key, buffer_length):
        rising, falling = self.buffered_inputs(key, buffer_length)
        return rising

    def buffered_releases(self, key, buffer_length):
        rising, falling = self.buffered_inputs(key, buffer_length)
        return falling
