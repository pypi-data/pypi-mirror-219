from __future__ import annotations
from image_analyst.exceptions import DownloadFailedException
from image_analyst.utils import download_file, ReportFunction
from image_analyst.cv2.utils import NmsCV2
from image_analyst.exceptions import (
    ModelLoadingFailedException,
    InvalidDtypeException,
    DetectionFailedException,
)
from image_analyst.image import ImageFormat, BoundingBox, verify_image
from image_analyst.models import ODModel, Detection
from image_analyst.utils import NmsFunction
from typing import Optional
import numpy as np
import logging
import cv2

logger = logging.getLogger(__name__)


class YoloV3OpenCV(ODModel):
    """This type represents a OpenCV YoloV3 model."""

    @staticmethod
    def coco(
        score_threshold: float = 0.5,
        nms_function: Optional[NmsFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV3OpenCV:
        """Creates a new YoloV3OpenCV pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.5.
            nms_function (Optional[NmsFunction], optional): the nms function
                to use. Defaults to a new NmsCV2.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV3OpenCV: the new YoloV3OpenCV.
        """
        try:
            weights_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-coco.weights",  # noqa: E501
                "cv2-yolov3-coco.weights",
                report_callback,
            )
            config_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-coco.cfg",  # noqa: E501
                "cv2-yolov3-coco.cfg",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-coco.names",  # noqa: E501
                "cv2-yolov3-coco.names",
                report_callback,
            )
        except DownloadFailedException as e:
            raise ModelLoadingFailedException(
                "Cannot download the YoloV3 model."
            ) from e

        if nms_function is None:
            nms_function = NmsCV2()

        return YoloV3OpenCV(
            weights_path,
            config_path,
            labels_path,
            (416, 416),
            score_threshold,
            nms_function,
        )

    @staticmethod
    def tiny_coco(
        score_threshold: float = 0.25,
        nms_function: Optional[NmsFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV3OpenCV:
        """Creates a new tiny YoloV3OpenCV pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.25.
            nms_function (Optional[NmsFunction], optional): the nms function to use.
                Defaults to a new NmsCV2.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV3OpenCV: the new YoloV3OpenCV.
        """
        try:
            weights_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-tiny-coco.weights",  # noqa: E501
                "cv2-yolov3-tiny-coco.weights",
                report_callback,
            )
            config_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-tiny-coco.cfg",  # noqa: E501
                "cv2-yolov3-tiny-coco.cfg",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystCV2/releases/download/v0.1.1/cv2-yolov3-tiny-coco.names",  # noqa: E501
                "cv2-yolov3-tiny-coco.names",
                report_callback,
            )
        except DownloadFailedException as e:
            raise ModelLoadingFailedException(
                "Cannot download the YoloV3 model."
            ) from e

        if nms_function is None:
            nms_function = NmsCV2()

        return YoloV3OpenCV(
            weights_path,
            config_path,
            labels_path,
            (416, 416),
            score_threshold,
            nms_function,
        )

    def __init__(
        self,
        weights_path: str,
        config_path: str,
        labels_path: str,
        model_size: tuple[int, int],
        score_threshold: float,
        nms_function: NmsFunction,
    ) -> None:
        """Initialises `self` to a new YoloV3OpenCV.

        Args:
            weights_path (str): the path to the weights file.
            config_path (str): the path to the config file.
            labels_path (str): the path to the labels file.
            model_size (tuple[int, int]): the size of the model.
            score_threshold (float): the score threshold to use.
            nms_function (NmsFunction): the NMS function to use.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.
        """
        if score_threshold < 0 or score_threshold > 1:
            raise ValueError("score_threshold must be between 0 and 1.")

        try:
            with open(labels_path, "rt") as f:
                self.__supported_classes = tuple(f.read().splitlines())
        except OSError:
            raise ModelLoadingFailedException("Cannot load the supported classes.")

        try:
            self.__net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        except Exception:
            raise ModelLoadingFailedException("Cannot load the YoloV3 model.")

        self.__net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.__net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        layers_names = self.__net.getLayerNames()
        self.__outputs_names = [
            layers_names[i - 1] for i in self.__net.getUnconnectedOutLayers()
        ]
        self.__model_size = model_size
        self.__nms_function = nms_function
        self.__score_threshold = score_threshold

    @property
    def supported_classes(self) -> tuple[str, ...]:  # noqa: D102
        return self.__supported_classes

    @property
    def supported_dtype(self) -> type:  # noqa: D102
        return np.uint8

    @property
    def supported_format(self) -> ImageFormat:  # noqa: D102
        return ImageFormat.RGB

    def __call__(self, image: np.ndarray) -> list[Detection]:  # noqa: D102
        if image.dtype != self.supported_dtype:
            raise InvalidDtypeException("The image dtype is not supported.")

        logger.info("Started Image preprocessing")
        verify_image(image)
        self.__net.setInput(
            cv2.dnn.blobFromImage(
                image, 1 / 255, self.__model_size, [0, 0, 0], True, crop=False
            )
        )
        logger.info("Completed Image preprocessing")

        logger.info("Started Image detection")
        try:
            outputs = self.__net.forward(self.__outputs_names)
        except Exception as e:
            raise DetectionFailedException("Failed to detect objects.") from e
        logger.info("Completed Image detection")

        logger.info("Started Bounding boxes creation")
        frameHeight, frameWidth, _ = image.shape

        detections = []
        for out in outputs:
            for detection in out:
                objectness = detection[4]
                class_probabilities = detection[5:]
                class_id = int(np.argmax(class_probabilities))
                score = float(class_probabilities[class_id] * objectness)

                if score < self.__score_threshold:
                    continue

                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)

                detections.append(
                    Detection(
                        class_name=self.supported_classes[class_id],
                        score=score,
                        bounding_box=BoundingBox(
                            xmin=left, ymin=top, xmax=left + width, ymax=top + height
                        ),
                    )
                )
        logger.info("Completed Bounding boxes creation")

        logger.info("Started NMS")
        result = self.__nms_function(detections)
        logger.info("Completed NMS")

        return result
