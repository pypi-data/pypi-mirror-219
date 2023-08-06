from pathlib import Path

from pygame import Surface, Color

from robingame.image.utils import (
    load_spritesheet,
    load_image_sequence,
    flip_images,
    recolor_images,
    scale_images,
)


class SpriteAnimation:
    """
    Animates a sequence of images.
    Can scale, flip, and recolor itself.
    """

    images: list[Surface] | None

    def __init__(
        self,
        images: list[Surface] = None,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict[Color:Color] = None,
    ):
        """
        Args:
            images: a list of Surfaces to use as frames
            scale: factor by which to scale images
            flip_x: flip all images horizontally if True
            flip_y: flip all images vertically if True
            colormap: used to recolor a sprite. It is a mapping of old colours to new colours
        """
        self.images = images
        if scale:
            self.scale(scale)
        if flip_x or flip_y:
            self.flip(flip_x, flip_y)
        if colormap:
            self.recolor(colormap)

    @classmethod
    def from_image(
        cls,
        filename: Path | str,
        colorkey=None,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        """
        Load the SpriteAnimation from a single image.
        Alias for `from_spritesheet`.
        """
        return cls.from_spritesheet(
            filename=filename,
            image_size=None,
            colorkey=colorkey,
            flip_x=flip_x,
            flip_y=flip_y,
            colormap=colormap,
            scale=scale,
        )

    @classmethod
    def from_spritesheet(
        cls,
        filename: Path | str,
        image_size: (int, int),
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        """
        Load a SpriteAnimation from a spritesheet.
        """
        images = load_spritesheet(
            filename=filename, image_size=image_size, colorkey=colorkey, num_images=num_images
        )
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    @classmethod
    def from_image_sequence(
        cls,
        pattern: Path | str,
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        """
        Load a SpriteAnimation from a sequence of images in a folder.

        Args:
            pattern: glob pattern used by `load_image_sequence`
        """
        images = load_image_sequence(pattern=pattern, colorkey=colorkey, num_images=num_images)
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    ############## playback ###############
    def play(self, n: int) -> Surface | bool:
        """
        Fetch frame with index `n`.
        This is used in the game loop (where `n` is the iteration counter) to animate the sprite.
        Return False when we've run out of frames.

        Args:
            n:

        Returns:
            the frame to display
        """
        try:
            return self.images[n]
        except IndexError:
            return False

    def loop(self, n: int) -> Surface:
        """
        Like `play()` but if `n` is greater than the number of frames, start again at the beginning.

        Args:
            n:

        Returns:
            the frame to display
        """
        return self.play(n % len(self.images))

    def play_once(self, n: int, repeat_frame: int = -1) -> Surface:
        """
        Run the animation once and then continue returning the specified frame
        (default=last frame).

        Args:
            n:
            repeat_frame: the frame to repeat after the animation has finished (default = last
                frame)

        Returns:
            the frame to display
        """
        try:
            return self.images[n]
        except IndexError:
            return self.images[repeat_frame]

    ############## edit in place ###############
    def flip(self, flip_x: bool, flip_y: bool):
        """
        Flip in place.

        Args:
            flip_x: flip horizontally
            flip_y: flip vertically
        """
        self.images = flip_images(self.images, flip_x, flip_y)

    def recolor(self, colormap: dict):
        """
        Recolor in place.

        Args:
            colormap: mapping of old colours to new colours
        """
        self.images = recolor_images(self.images, colormap)

    def scale(self, scale: float):
        """
        Scale in place.

        Args:
            scale: factor by which to scale images
        """
        self.images = scale_images(self.images, scale)

    ############## edit and copy ###############
    def flipped_copy(self, flip_x=False, flip_y=False) -> "SpriteAnimation":
        """
        Like `flip()` but returns a new instance.

        Returns:
            a new instance
        """
        return self.__class__(images=flip_images(self.images, flip_x, flip_y))

    def recolored_copy(self, colormap: dict) -> "SpriteAnimation":
        """
        Like `recolor()` but returns a new instance.

        Returns:
            a new instance
        """
        return self.__class__(images=recolor_images(self.images, colormap))

    def scaled_copy(self, scale: float) -> "SpriteAnimation":
        """
        Like `scale()` but returns a new instance.

        Returns:
            a new instance
        """
        return self.__class__(images=scale_images(self.images, scale))

    def __len__(self):
        return len(self.images)
