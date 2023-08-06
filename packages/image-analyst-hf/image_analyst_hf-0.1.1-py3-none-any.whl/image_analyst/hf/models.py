from __future__ import annotations
from image_analyst.exceptions import (
    ModelLoadingFailedException,
    InvalidDtypeException,
    DetectionFailedException,
)
from image_analyst.image import (
    BoundingBox,
    ImageFormat,
    verify_image,
)
from image_analyst.models import ODModel, Detection
from transformers import DetrForObjectDetection, AutoImageProcessor
from PIL import Image
import numpy as np
import logging
import torch


logger = logging.getLogger(__name__)


class Detr(ODModel):
    """This type represents a Detr model."""

    @staticmethod
    def resnet50(
        score_threshold: float = 0.5,
    ) -> Detr:
        """Creates a new Detr pretrained with resnet 50.

        Args:
            score_threshold (float, optional): the score threshold to use.
                Defaults to 0.5.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.

        Returns:
            Detr: the new Detr.
        """
        try:
            model: DetrForObjectDetection = DetrForObjectDetection.from_pretrained(
                "facebook/detr-resnet-50"
            )  # type: ignore
            image_processor = AutoImageProcessor.from_pretrained(
                "facebook/detr-resnet-50"
            )
        except Exception as e:
            raise ModelLoadingFailedException("Cannot download the Detr model.") from e

        return Detr(
            model,
            image_processor,
            score_threshold,
        )

    def __init__(
        self,
        model: DetrForObjectDetection,
        image_processor: AutoImageProcessor,
        score_threshold: float,
    ) -> None:
        """Initialises `self` to a new Detr.

        Args:
            model (DetrForObjectDetection): the model to use.
            image_processor (AutoImageProcessor): the image processor to use.
            score_threshold (float): the score threshold to use.

        Raises:
            ModelLoadingFailedException: if the model cannot be loaded.
            ValueError: if the score threshold is not between 0 and 1.
        """
        if score_threshold < 0 or score_threshold > 1:
            raise ValueError("score_threshold must be between 0 and 1.")

        labels = model.config.id2label
        if labels is None:
            raise ModelLoadingFailedException("Cannot load the Detr model.")

        try:
            self.__supported_classes = tuple(labels[i] for i in range(max(labels) + 1))
        except KeyError as e:
            raise ModelLoadingFailedException("Cannot load the Detr model.") from e

        self.__score_threshold = score_threshold
        self.__device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.__model = model.to(self.__device)
        self.__image_processor = image_processor

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
        verify_image(image)

        if image.dtype != self.supported_dtype:
            raise InvalidDtypeException("The image dtype is not supported.")

        logger.info("Started Image preprocessing")
        pil_image = Image.fromarray(image, self.supported_format.name)
        inputs = self.__image_processor(
            images=pil_image,
            return_tensors="pt",
        ).to(self.__device)  # type: ignore
        logger.info("Completed Image preprocessing")

        logger.info("Started Image detection")
        try:
            outputs = self.__model(**inputs)
        except Exception as e:
            raise DetectionFailedException("Failed to detect objects.") from e
        logger.info("Completed Image detection")

        logger.info("Started Bounding boxes creation")
        results = self.__image_processor.post_process_object_detection(  # type: ignore
            outputs,
            threshold=0.9,
            target_sizes=torch.tensor([pil_image.size[::-1]]),
        )[0]

        detections = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            if score < self.__score_threshold:
                continue

            xmin, ymin, xmax, ymax = tuple(round(i) for i in box.tolist())

            detections.append(
                Detection(
                    class_name=self.__supported_classes[label.item()],  # type: ignore
                    score=score.item(),
                    bounding_box=BoundingBox(
                        xmin=xmin,
                        ymin=ymin,
                        xmax=xmax,
                        ymax=ymax,
                    ),
                )
            )
        logger.info("Completed Bounding boxes creation")

        return detections
