"""This module defines InferenceService interface. All inference services must implement this
interface, e.g., MLflowService.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from mac.exceptions import InferenceTypeError
from mac.inference.inference import Inference

logger = logging.getLogger(__name__)


class InferenceService(ABC):
    """Abstract class for an Inference service.

    Attributes:
    - inference: An inference object
    """

    def __init__(self) -> None:
        """Initialization method for the InferenceService class."""
        self._inference: Optional[Inference] = None

    @property
    def inference(self) -> Optional[Inference]:
        """Returns the inference attribute.

        :return: An Inference object.
        """
        return self._inference

    @inference.setter
    def inference(self, inference: Inference) -> None:
        """Sets the inference attribute.

        :param inference: An Inference object.

        :raises InferenceTypeError: If the inference object is not of type Inference.
        """
        self._raise_error_if_inference_is_wrong_type(inference)
        self._inference = inference

    @abstractmethod
    def serve(self) -> None:
        """This method serves an Inference object using a service."""

    @classmethod
    def _raise_error_if_inference_is_wrong_type(cls, inference: Any) -> None:
        """Raises an error if the inference object is not of type Inference."""
        if not isinstance(inference, Inference):
            message = (
                f"Expected inference to be of type Inference, but "
                f"got {type(inference).__name__} instead. An "
                "InferenceService requires an Inference instance."
            )
            logger.error(message)
            raise InferenceTypeError(message)
