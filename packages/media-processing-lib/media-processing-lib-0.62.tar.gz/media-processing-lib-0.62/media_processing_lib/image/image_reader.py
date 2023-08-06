"""Image reader module"""
from pathlib import Path
import numpy as np

from ..logger import logger
from .utils import build_image_reader_fn

# TODO: support for grayscale or RGBA perhaps?

# pylint: disable=broad-exception-raised
def image_read(path: str, img_lib: str = None, count: int = 5) -> np.ndarray:
    """Read an image from a path given a library"""
    f_read = build_image_reader_fn(img_lib)
    path = str(path) if isinstance(path, Path) else path

    i = 0
    while True:
        try:
            return f_read(path)
        except Exception as e:
            logger.debug(f"Path: {path}. Exception: {e}")
            i += 1

            if i == count:
                raise Exception(e)
