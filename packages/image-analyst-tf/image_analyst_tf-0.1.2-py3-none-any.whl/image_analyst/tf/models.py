from __future__ import annotations
from image_analyst.exceptions import DownloadFailedException
from image_analyst.utils import download_file, ReportFunction
from image_analyst.exceptions import (
    ModelLoadingFailedException,
    InvalidDtypeException,
    DetectionFailedException,
)
from image_analyst.image import (
    ImageFormat,
    BoundingBox,
    ImageEmbedder,
    EmbeddingFunction,
)
from image_analyst.utils import NmsFunction, NmsPython
from image_analyst.models import ODModel, Detection
from typing import Optional
import tensorflow as tf
import numpy as np
import logging


logger = logging.getLogger(__name__)


class YoloV7Tflite(ODModel):
    """This type represents a Tensorflow Lite YoloV7 model."""

    @staticmethod
    def coco(
        score_threshold: float = 0.5,
        nms_function: Optional[NmsFunction] = None,
        embedding_function: Optional[EmbeddingFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV7Tflite:
        """Creates a new YoloV7Tflite pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.5.
            nms_function (Optional[NmsFunction], optional): the nms function to use.
                Defaults to None.
            embedding_function (Optional[EmbeddingFunction], optional): the embedding
                function to use. Defaults to an ImageEmbedder.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV7Tflite: the new YoloV7Tflite.
        """
        try:
            model_path = download_file(
                "https://github.com/BergLucas/ImageAnalystTF/releases/download/v0.1.2/tf-yolov7-coco.tflite",  # noqa: E501
                "tf-yolov7-coco.tflite",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystTF/releases/download/v0.1.2/tf-yolov7-coco.names",  # noqa: E501
                "tf-yolov7-coco.names",
                report_callback,
            )
        except DownloadFailedException as e:
            raise ModelLoadingFailedException(
                "Cannot download the YoloV7 model."
            ) from e

        if nms_function is None:
            nms_function = NmsPython()

        if embedding_function is None:
            embedding_function = ImageEmbedder()

        return YoloV7Tflite(
            model_path,
            labels_path,
            (640, 640),
            score_threshold,
            nms_function,
            embedding_function,
        )

    @staticmethod
    def tiny_coco(
        score_threshold: float = 0.25,
        nms_function: Optional[NmsFunction] = None,
        embedding_function: Optional[EmbeddingFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV7Tflite:
        """Creates a new tiny YoloV7Tflite pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.25.
            nms_function (Optional[NmsFunction], optional): the nms function
                to use. Defaults to None.
            embedding_function (Optional[EmbeddingFunction], optional): the embedding
                function to use. Defaults to an ImageEmbedder.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV7Tflite: the new YoloV7Tflite.
        """
        try:
            model_path = download_file(
                "https://github.com/BergLucas/ImageAnalystTF/releases/download/v0.1.2/tf-yolov7-tiny-coco.tflite",  # noqa: E501
                "tf-yolov7-tiny-coco.tflite",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystTF/releases/download/v0.1.2/tf-yolov7-tiny-coco.names",  # noqa: E501
                "tf-yolov7-tiny-coco.names",
                report_callback,
            )
        except DownloadFailedException as e:
            raise ModelLoadingFailedException(
                "Cannot download the YoloV7 model."
            ) from e

        if nms_function is None:
            nms_function = NmsPython()

        if embedding_function is None:
            embedding_function = ImageEmbedder()

        return YoloV7Tflite(
            model_path,
            labels_path,
            (640, 640),
            score_threshold,
            nms_function,
            embedding_function,
        )

    def __init__(
        self,
        model_path: str,
        labels_path: str,
        model_size: tuple[int, int],
        score_threshold: float,
        nms_function: NmsFunction,
        embedding_function: EmbeddingFunction,
    ) -> None:
        """Initialises `self` to a new YoloV7Tflite.

        Args:
            model_path (str): the path to the model file.
            labels_path (str): the path to the labels file.
            model_size (tuple[int, int]): the size of the model.
            score_threshold (float): the score threshold to use.
            nms_function (NmsFunction): the nms function to use.
            embedding_function (EmbeddingFunction): the embedding function to use.

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
            self.__interpreter = tf.lite.Interpreter(model_path=model_path)
            self.__interpreter.allocate_tensors()
        except ValueError:
            raise ModelLoadingFailedException("Cannot load the YoloV7 model.")

        self.__score_threshold = score_threshold
        self.__input_details = self.__interpreter.get_input_details()
        self.__output_details = self.__interpreter.get_output_details()
        self.__model_size = model_size
        self.__nms_function = nms_function
        self.__embedding_function = embedding_function

    @property
    def supported_classes(self) -> tuple[str, ...]:  # noqa: D102
        return self.__supported_classes

    @property
    def supported_dtype(self) -> type:  # noqa: D102
        return np.float32

    @property
    def supported_format(self) -> ImageFormat:  # noqa: D102
        return ImageFormat.RGB

    def __call__(self, image: np.ndarray) -> list[Detection]:  # noqa: D102
        if image.dtype != self.supported_dtype:
            raise InvalidDtypeException("The image dtype is not supported.")

        logger.info("Started Image preprocessing")
        embedded_image, bounding_box = self.__embedding_function(
            image, *self.__model_size
        )
        image_array = np.ascontiguousarray(
            np.expand_dims(embedded_image.transpose((2, 0, 1)), 0)
        )
        logger.info("Completed Image preprocessing")

        logger.info("Started Image detection")
        self.__interpreter.set_tensor(self.__input_details[0]["index"], image_array)
        try:
            self.__interpreter.invoke()
        except ValueError as e:
            raise DetectionFailedException("Failed to detect objects.") from e
        outputs = self.__interpreter.get_tensor(self.__output_details[0]["index"])
        logger.info("Completed Image detection")

        logger.info("Started Bounding boxes creation")
        detections = []

        height, width, _ = image.shape

        x_scale = width / bounding_box.width
        y_scale = height / bounding_box.height

        for _, xmin, ymin, xmax, ymax, class_id, score in outputs:
            if score < self.__score_threshold:
                continue

            detections.append(
                Detection(
                    class_name=self.__supported_classes[int(class_id)],
                    score=float(score),
                    bounding_box=BoundingBox(
                        int((xmin - bounding_box.xmin) * x_scale),
                        int((ymin - bounding_box.ymin) * y_scale),
                        int((xmax - bounding_box.xmin) * x_scale),
                        int((ymax - bounding_box.ymin) * y_scale),
                    ),
                )
            )
        logger.info("Completed Bounding boxes creation")

        logger.info("Started NMS")
        result = self.__nms_function(detections)
        logger.info("Completed NMS")

        return result


class YoloV7Tf(ODModel):
    """This type represents a Tensorflow YoloV7 model."""

    def __init__(
        self,
        model_path: str,
        labels_path: str,
        model_size: tuple[int, int],
        score_threshold: float,
        nms_function: NmsFunction,
        embedding_function: EmbeddingFunction,
    ) -> None:
        """Initialises `self` to a new YoloV7Tf.

        Args:
            model_path (str): the path to the model file.
            labels_path (str): the path to the labels file.
            model_size (tuple[int, int]): the size of the model.
            score_threshold (float): the score threshold to use.
            nms_function (NmsFunction): the nms function to use.
            embedding_function (EmbeddingFunction): the embedding function to use.

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
            self.__infer = tf.saved_model.load(model_path).signatures["serving_default"]
        except ValueError:
            raise ModelLoadingFailedException("Cannot load the YoloV7 model.")

        self.__score_threshold = score_threshold
        self.__model_size = model_size
        self.__nms_function = nms_function
        self.__embedding_function = embedding_function

    @property
    def supported_classes(self) -> tuple[str, ...]:  # noqa: D102
        return self.__supported_classes

    @property
    def supported_dtype(self) -> type:  # noqa: D102
        return np.float32

    @property
    def supported_format(self) -> ImageFormat:  # noqa: D102
        return ImageFormat.RGB

    def __call__(self, image: np.ndarray) -> list[Detection]:  # noqa: D102
        if image.dtype != self.supported_dtype:
            raise InvalidDtypeException("The image dtype is not supported.")

        logger.info("Started Image preprocessing")
        embedded_image, bounding_box = self.__embedding_function(
            image, *self.__model_size
        )
        expanded_image = np.expand_dims(embedded_image.transpose((2, 0, 1)), 0)
        logger.info("Completed Image preprocessing")

        logger.info("Started Image detection")
        try:
            outputs = self.__infer(tf.constant(expanded_image))["output"]
        except ValueError as e:
            raise DetectionFailedException("Failed to detect objects.") from e
        logger.info("Completed Image detection")

        logger.info("Started Bounding boxes creation")
        detections = []

        height, width, _ = image.shape

        x_scale = width / bounding_box.width
        y_scale = height / bounding_box.height

        for _, xmin, ymin, xmax, ymax, class_id, score in outputs:
            if score < self.__score_threshold:
                continue

            detections.append(
                Detection(
                    class_name=self.__supported_classes[int(class_id)],
                    score=float(score),
                    bounding_box=BoundingBox(
                        int((xmin - bounding_box.xmin) * x_scale),
                        int((ymin - bounding_box.ymin) * y_scale),
                        int((xmax - bounding_box.xmin) * x_scale),
                        int((ymax - bounding_box.ymin) * y_scale),
                    ),
                )
            )
        logger.info("Completed Bounding boxes creation")

        logger.info("Started NMS")
        result = self.__nms_function(detections)
        logger.info("Completed NMS")

        return result
