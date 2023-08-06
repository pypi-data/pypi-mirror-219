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
from typing import Optional, Literal
import onnxruntime as ort
import numpy as np
import logging


logger = logging.getLogger(__name__)


Provider = Literal[
    "CPUExecutionProvider",
    "CUDAExecutionProvider",
    "TensorrtExecutionProvider",
    "MIGraphXExecutionProvider",
    "ROCMExecutionProvider",
]


class YoloV7Onnx(ODModel):
    """This type represents a ONNX YoloV7 model."""

    @staticmethod
    def coco(
        score_threshold: float = 0.5,
        providers: Optional[list[Provider]] = None,
        nms_function: Optional[NmsFunction] = None,
        embedding_function: Optional[EmbeddingFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV7Onnx:
        """Creates a new YoloV7Onnx pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.5.
            providers (Optional[list[Provider]], optional): the providers to use.
                Defaults to None.
            nms_function (Optional[NmsFunction], optional): the nms function to use.
                Defaults to a new NmsPython.
            embedding_function (Optional[EmbeddingFunction], optional): the embedding
                function to use. Defaults to an ImageEmbedder.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV7Onnx: the new YoloV7Onnx.
        """
        try:
            model_path = download_file(
                "https://github.com/BergLucas/ImageAnalystONNX/releases/download/v0.1.1/onnx-yolov7-coco.onnx",  # noqa: E501
                "onnx-yolov7-coco.onnx",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystONNX/releases/download/v0.1.1/onnx-yolov7-coco.names",  # noqa: E501
                "onnx-yolov7-coco.names",
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

        return YoloV7Onnx(
            model_path,
            labels_path,
            (640, 640),
            score_threshold,
            providers,
            nms_function,
            embedding_function,
        )

    @staticmethod
    def tiny_coco(
        score_threshold: float = 0.25,
        providers: Optional[list[Provider]] = None,
        nms_function: Optional[NmsFunction] = None,
        embedding_function: Optional[EmbeddingFunction] = None,
        report_callback: Optional[ReportFunction] = None,
    ) -> YoloV7Onnx:
        """Creates a new tiny YoloV7Onnx pretrained with the coco dataset.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.25.
            providers (Optional[list[Provider]], optional): the providers to use.
                Defaults to None.
            nm_function (Optional[NmsFunction], optional): the nms function to use.
                Defaults to NmsPython.
            embedding_function (Optional[EmbeddingFunction], optional): the embedding
                function to use. Defaults to an ImageEmbedder.
            report_callback (Optional[ReportFunction], optional): the report function
                that is called while downloading the files. Defaults to None.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            YoloV7Onnx: the new YoloV7Onnx.
        """
        try:
            model_path = download_file(
                "https://github.com/BergLucas/ImageAnalystONNX/releases/download/v0.1.1/onnx-yolov7-tiny-coco.onnx",  # noqa: E501
                "onnx-yolov7-tiny-coco.onnx",
                report_callback,
            )
            labels_path = download_file(
                "https://github.com/BergLucas/ImageAnalystONNX/releases/download/v0.1.1/onnx-yolov7-tiny-coco.names",  # noqa: E501
                "onnx-yolov7-tiny-coco.names",
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

        return YoloV7Onnx(
            model_path,
            labels_path,
            (640, 640),
            score_threshold,
            providers,
            nms_function,
            embedding_function,
        )

    def __init__(
        self,
        model_path: str,
        labels_path: str,
        model_size: tuple[int, int],
        score_threshold: float,
        providers: Optional[list[Provider]],
        nms_function: NmsFunction,
        embedding_function: EmbeddingFunction,
    ) -> None:
        """Initialises `self` to a new YoloV7Onnx.

        Args:
            model_path (str): the path to the model file.
            labels_path (str): the path to the labels file.
            model_size (tuple[int, int]): the size of the model.
            score_threshold (float): the score threshold to use.
            providers (Optional[list[Provider]]): the providers to use.
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
            self.__session = ort.InferenceSession(model_path, providers=providers)
        except ValueError:
            raise ModelLoadingFailedException("Cannot load the YoloV3 model.")

        self.__score_threshold = score_threshold
        self.__input_names = [i.name for i in self.__session.get_inputs()]
        self.__output_names = [i.name for i in self.__session.get_outputs()]
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
        try:
            outputs = self.__session.run(
                self.__output_names, {self.__input_names[0]: image_array}
            )[0]
        except Exception as e:
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
