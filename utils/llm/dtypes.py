from typing import Union

import numpy as np
from PIL import Image

from ..dtypes import PathLike

ImgLike = Union[Image.Image, np.ndarray, PathLike]
