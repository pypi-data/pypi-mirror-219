from pathlib import Path

from pygame.color import Color
from pygame.surface import Surface

from robingame.image import load_spritesheet, scale_image, empty_image
from robingame.text.exceptions import TextError


class Font:
    """
    Handles loading custom fonts from a spritesheet, and rendering text onto a surface.
    """

    letters: dict[str:Surface]
    image_size: tuple[int, int]
    xpad: int
    ypad: int

    def __init__(
        self,
        filename: str | Path,
        image_size: tuple[int, int],
        letters: str,
        xpad: int = 0,
        ypad: int = 0,
        trim: bool = False,
        space_width: int = None,
        **kwargs: dict,
    ):
        """
        Loads the font from a spritesheet of letters using `load_spritesheet`.

        Args:
            filename: path to the spritesheet of letters
            image_size: the xy size of a character image in the spritesheet (we assume the
                characters are evenly spaced in the spritesheet)
            letters: describes the order in which the characters appear in the spritesheet
            xpad: extra x space between characters (in pixels). Can be negative
            ypad: extra y space between characters (in pixels). Can be negative
            trim: if `True`, trim any empty x space from the characters so that the width of
                each character depends on the letter ("l" will be narrower than "m"). If `False`,
                leave the characters equal width (results in a monospaced font)
            space_width: desired width of the space character (in pixels). If omitted, the space
                will be made as wide as a character
            kwargs: any extra kwargs will be passed on to `load_spritesheet`

        Example:
            ```
            test_font = Font(
                filename="test_font.png",
                image_size=(16, 16),
                letters=(
                    string.ascii_uppercase
                    + string.ascii_lowercase
                    + r"1234567890-=!@#$%^&*()_+[];',./{}|:<>?~`"
                ),
                trim=True,
                xpad=1,
                space_width=8,
            )
            ```
        """
        self.image_size = width, height = image_size
        self.xpad = xpad
        self.ypad = ypad
        self.letters = dict()
        self.letters[" "] = empty_image((space_width or width, height))
        self.not_found = Surface(image_size)
        self.not_found.fill(Color("red"))
        images = load_spritesheet(filename, image_size=image_size, **kwargs)
        if trim:
            images = self._trim_images(images)
        self.letters.update({letter: image for letter, image in zip(letters, images)})

    def render(
        self,
        surf: Surface,
        text: str,
        x: int = 0,
        y: int = 0,
        scale: int = 1,
        wrap: int = 0,
        align: int = None,
    ) -> int:
        """
        Render text onto a surface.

        Args:
            surf: surface on which to render the text
            text: the string of characters to render in this font
            x: x-position on the surface
            y: y-position on the surface
            scale: factor by which to scale the text (1 = no scaling)
            wrap: x width at which to wrap text
            align: -1=left, 0=center, 1=right

        Example:
            ```
            test_font.render(
                surface,
                text="Hello world!",
                scale=2,
                wrap=50,
                x=10,
                y=20,
                align=-1,
            )
            ```
        """
        _, ysize = self.image_size
        cursor = x
        for line in text.splitlines():
            wrapped_lines = self._wrap_words(line, wrap, x, scale) if wrap else [line]
            for line in wrapped_lines:
                cursor = self._align_cursor(line, x, align, scale, wrap)
                for letter in line:
                    image = self.get(letter)
                    image = scale_image(image, scale)
                    surf.blit(image, (cursor, y))
                    w = image.get_width()
                    cursor += w + self.xpad * scale
                y += (ysize + self.ypad) * scale
        return cursor

    def get(self, letter: str) -> Surface:
        """
        Get the image associated with a letter.

        If this font does not have a character for the letter, return the error image ( usually a
        red rectangle)

        Args:
            letter:
        """
        try:
            return self.letters[letter]
        except KeyError:
            return self.not_found

    def _align_cursor(self, line: str, x: int, align: int, scale: int, wrap: int) -> int:
        """
        Used for left/right/centered text alignmnent
        """
        match align:
            case -1 | None:
                cursor = x
            case 0:
                if not wrap:
                    raise TextError("Can't center text without specifying a wrap width.")
                line_width = self._printed_width(line, scale)
                slack = wrap - line_width
                cursor = x + slack // 2
            case 1:
                line_width = self._printed_width(line, scale)
                cursor = x + wrap - line_width
            case _:
                raise TextError(f"Bad alignment value: {align}")
        return cursor

    def _wrap_words(self, text: str, wrap: int, x: int = 0, scale: int = 1) -> list[str]:
        """
        Break one long line into multiple lines based on the wrap width.
        """
        lines = []
        line = ""
        for word in text.split(" "):
            new_line = f"{line} {word}" if line else word
            if self._printed_width(new_line, scale) <= wrap:
                line = new_line
            else:
                lines.append(line)
                line = word
        lines.append(line)  # last line
        return lines

    def _printed_width(self, text: str, scale: int) -> int:
        """
        Calculate how wide a string of text will be when rendered.
        """
        return sum((self.get(letter).get_width() + self.xpad) * scale for letter in text)

    def _trim_images(self, images: list[Surface]) -> list[Surface]:
        """
        Make a monospaced font non-monospaced
        """
        trimmed = []
        for image in images:
            x, _, w, _ = image.get_bounding_rect()  # trim x to bounding rect
            _, y, _, h = image.get_rect()  # maintain original y position of character
            new = image.subsurface((x, y, w, h))
            trimmed.append(new)
        return trimmed
