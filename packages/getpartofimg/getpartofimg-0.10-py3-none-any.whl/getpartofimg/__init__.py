import cv2
import random
from a_cv2_easy_resize import add_easy_resize_to_cv2
from a_cv_imwrite_imread_plus import add_imwrite_plus_imread_plus_to_cv2
from typing import Any
import numpy as np

add_imwrite_plus_imread_plus_to_cv2()
add_easy_resize_to_cv2()


def get_part_of_image(
    image: Any, width: int, height: int, allow_resize: bool = True
) -> np.ndarray:
    r"""
    Extracts a part of the image specified by width and height from the given image file path using OpenCV.

    Parameters:
    -----------
    image : Any
        The file path of the image from which a part will be extracted.

    width : int
        The desired width of the extracted part.

    height : int
        The desired height of the extracted part.

    allow_resize : bool, optional (default=True)
        If True, allows resizing of the input image when the specified width or height is greater
        than the original image's dimensions.

    Returns:
    --------
    numpy.ndarray
        The extracted part of the image as a NumPy array.

    Raises:
    -------
    ValueError
        If the 'allow_resize' parameter is set to False and the specified width or height is greater than
        the original image's dimensions, a ValueError is raised with a message indicating that the image is too small.

    Notes:
    ------
    The function uses the 'cv2.imread_plus' function ( https://github.com/hansalemaos/a_cv_imwrite_imread_plus )
    to read the image from the given file path. It then calculates
    the possible ranges for extracting the desired part based on the image's dimensions and the specified width
    and height. If the 'allow_resize' parameter is True, the function resizes the image using 'cv2.easy_resize_image'
    ( https://github.com/hansalemaos/a_cv2_easy_resize )
    with the 'cv2.INTER_AREA' interpolation method to fit the desired part. Otherwise, it raises a ValueError.

    Random starting coordinates within the allowable range are generated to extract the part of the image specified
    by the given width and height.

    Example:
    --------
    import cv2
    from getpartofimg import get_part_of_image
    im = get_part_of_image(image=r"https://raw.githubusercontent.com/hansalemaos/screenshots/main/pic5.png", width=600, height=500, allow_resize=True)
    cv2.imwrite('c:\\testimage.png', im)
    """
    image = cv2.imread_plus(image)
    possible_width_range = image.shape[1] - width - 1
    possible_height_range = image.shape[0] - height - 1
    if possible_height_range <= 0 or possible_width_range <= 0:
        if allow_resize:
            if possible_width_range <= 0:
                image = cv2.easy_resize_image(
                    image,
                    width=width * 2,
                    height=None,
                    percent=None,
                    interpolation=cv2.INTER_AREA,
                )
            possible_height_range = image.shape[0] - height - 1
            if possible_height_range <= 0:
                image = cv2.easy_resize_image(
                    image,
                    width=None,
                    height=height * 2,
                    percent=None,
                    interpolation=cv2.INTER_AREA,
                )
        else:
            raise ValueError(
                f"Picture width:{image.shape[1]} height:{image.shape[0]} is too small for width:{width}, height:{height}"
            )
        possible_width_range = image.shape[1] - width - 1
        possible_height_range = image.shape[0] - height - 1
    start_x = random.randint(0, possible_width_range)
    start_y = random.randint(0, possible_height_range)
    return image[start_y : start_y + height, start_x : start_x + width]
