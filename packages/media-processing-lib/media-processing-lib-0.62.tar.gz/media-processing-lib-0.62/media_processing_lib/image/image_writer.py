"""Image writer module"""
import numpy as np

from .utils import build_image_writer_fn
from ..logger import logger


# pylint: disable=broad-exception-raised
def image_write(file: np.ndarray, path: str, img_lib: str = None, count: int = 5) -> None:
    """Write an image to a path"""
    path = str(path) if not isinstance(path, str) else path
    f_write = build_image_writer_fn(img_lib)

    i = 0
    while True:
        try:
            return f_write(file, path)
        except Exception as e:
            logger.debug(f"Path: {path}. Exception: {e}")
            i += 1

            if i == count:
                raise Exception
