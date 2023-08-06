from image_analyst.image import verify_dimensions, verify_image
import numpy as np
import cv2


def bilinear_resize_cv2(
    image: np.ndarray, new_width: int, new_height: int
) -> np.ndarray:
    """Resizes an image to a new size using bilinear interpolation.

    Args:
        image (np.ndarray): the image to resize. It must be a valid numpy image.
        new_width (int): the new width. It must be stricly positive.
        new_height (int): the new height. It must be stricly positive.

    Raises:
        InvalidImageException: if `image` is not a valid numpy image.
        InvalidDimensionsException: if `new_width` or
            `new_height` are not stricly positive.

    Returns:
        np.ndarray: the resized image.
    """
    verify_dimensions(new_width, new_height)
    verify_image(image)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
