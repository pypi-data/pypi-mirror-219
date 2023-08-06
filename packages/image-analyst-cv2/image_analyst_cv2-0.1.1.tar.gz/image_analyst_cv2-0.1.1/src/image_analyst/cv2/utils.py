from __future__ import annotations
from image_analyst.utils import NmsFunction
from image_analyst.image import ImageFormat
from image_analyst.models import Detection
from typing import Optional, Generator
from contextlib import contextmanager
import numpy as np
import cv2


class NmsCV2(NmsFunction):
    """A CV2 implementation of the Non-maximum Suppression (NMS) algorithm."""

    def __init__(self, nms_threshold: float = 0.25, score_threshold: float = 0) -> None:
        """Initializes `self` to a new NmsPython.

        Args:
            nms_threshold (float, optional): the threshold
                to use for the NMS algorithm. Defaults to 0.25.
            score_threshold (float, optional): the threshold
                to use for the NMS algorithm. Defaults to 0.

        Raises:
            ValueError: if `nms_threshold` is not between 0 and 1.
            ValueError: if `score_threshold` is not between 0 and 1.
        """
        if nms_threshold < 0 or nms_threshold > 1:
            raise ValueError("nms_threshold must be between 0 and 1.")

        if score_threshold < 0 or score_threshold > 1:
            raise ValueError("score_threshold must be between 0 and 1.")

        self.__nms_threshold = nms_threshold
        self.__score_threshold = score_threshold

    def __call__(self, detections: list[Detection]) -> list[Detection]:  # noqa: D102
        bboxes: list[tuple[int, int, int, int]] = []
        scores: list[float] = []
        for detection in detections:
            bboxes.append(detection.bounding_box.as_box())
            scores.append(detection.score)

        return [
            detections[i]
            for i in cv2.dnn.NMSBoxes(
                bboxes, scores, self.__score_threshold, self.__nms_threshold
            )
        ]


def convert_image(
    image: np.ndarray, target_format: ImageFormat, target_dtype: type
) -> np.ndarray:
    """Converts an image from BGR uint8 to the target format and dtype.

    Args:
        image (np.ndarray): the image to convert.
        target_format (ImageFormat): the format to convert the image to.
        target_dtype (type): the type to convert the image to.

    Raises:
        ValueError: if `target_format` or `target_dtype` is not supported.

    Returns:
        np.ndarray: the converted image.
    """
    if target_format == ImageFormat.RGB:
        formatted_image = image
    elif target_format == ImageFormat.BGR:
        formatted_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError(f"Unsupported image format: {target_format}")

    if target_dtype == np.uint8:
        return formatted_image
    elif target_dtype == np.float32:
        return formatted_image.astype(np.float32) / 255
    else:
        raise ValueError(f"Unsupported image dtype: {target_dtype}")


@contextmanager
def create_frame_generator(
    path_or_id: str | int,
    api_preference: cv2.VideoCaptureAPIs = cv2.CAP_ANY,
    video_options: Optional[dict[cv2.VideoCaptureProperties, float]] = None,
) -> Generator[Generator[np.ndarray, None, None], None, None]:
    """Creates a generator that yields the frames a video.

    Args:
        path_or_id (str | int): the path or id of the video.
        api_preference (cv2.VideoCaptureAPIs, optional): the API preference.
            Defaults to cv2.CAP_ANY.
        video_options (Optional[dict[cv2.VideoCaptureProperties, float]], optional):
            the video options. Defaults to None.

    Yields:
        Generator[Generator[np.ndarray, None, None], None, None]: a generator
            that yields the frames from the video.
    """
    video = cv2.VideoCapture(path_or_id, api_preference)

    if video_options is not None:
        for key, value in video_options.items():
            video.set(key, value)

    def frame_generator() -> Generator[np.ndarray, None, None]:
        while True:
            success, image = video.read()

            if not success:
                break

            yield image

    try:
        yield frame_generator()
    finally:
        video.release()
