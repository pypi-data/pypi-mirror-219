import sys
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

_tmp_image = Image.new("RGB", (1, 1))
_tmp_draw = ImageDraw.Draw(_tmp_image)


@lru_cache
def get_font(path, font_size=24):
    """
    Load and return the PIL ImageFont object from the specified font file path.

    Args:
        path (str): The file path of the font.
        font_size (int, optional): The font size to load. Default is 24.

    Returns:
        ImageFont.FreeTypeFont: The loaded font object.
    """
    return ImageFont.truetype(path, font_size)


def calculate_text_size(
    text: str,
    font_path: str,
    max_width: int | None = None,
    max_height: int | None = None,
    startfont: int = 180,
) -> int:
    """
    Calculate the font size that best fits the given text within the specified constraints.

    Args:
        text (str): The text to calculate the font size for.
        font_path (str): The file path of the font to use for rendering the text.
        max_width (int, optional): The maximum allowed width for the text. None means no width constraint. Default is None.
        max_height (int, optional): The maximum allowed height for the text. None means no height constraint. Default is None.
        startfont (int, optional): The initial font size to start the calculation. Default is 180.

    Returns:
        int: The font size that best fits the text within the specified constraints.
    """
    start_width = sys.maxsize
    start_height = sys.maxsize
    allresults = []
    startfontold = startfont
    if not max_width:
        maxwidth = 0
    else:
        maxwidth = max_width
    if not max_height:
        maxheight = 0
    else:
        maxheight = max_height
    while start_height > maxheight or start_width > maxwidth:
        font = get_font(path=font_path, font_size=startfont)
        _, _, start_width, start_height = _tmp_draw.textbbox(
            (0, 0), font=font, text=text
        )
        if not max_width:
            maxwidth = start_width + 1
        if not max_height:
            maxheight = start_height + 1
        allresults.append(startfont)
        startfont -= 1
    try:
        return allresults[-2] - 1
    except IndexError:
        return calculate_text_size(
            text,
            font_path,
            max_width=max_width,
            max_height=max_height,
            startfont=startfontold + 1,
        )


