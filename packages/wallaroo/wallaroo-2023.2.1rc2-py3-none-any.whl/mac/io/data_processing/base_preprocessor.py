"""This module features the BasePreprocessor interface that can be extended to
implement a concrete data preprocessor for InferenceData and covers the use-case
where the user sends the data with the pre-agreed contract of ascending input
keys."""

import logging
from abc import abstractmethod
from typing import Any, Dict, List, Optional

import numpy.typing as npt
import pydantic
from pydantic import StrictStr

from mac.exceptions import InferencePreprocessingError
from mac.io.data_processing.preprocessor import Preprocessor
from mac.types import InferenceData
from mac.utils.helpers import is_key_order_incorrect, log_error

logger = logging.getLogger(__name__)


class BasePreprocessor(Preprocessor, pydantic.BaseModel):
    """This class serves as an interface for creating concrete data preprocessors,
    that preprocess data sent in the pre-agreed user contract (i.e. ascending input keys)
    and returns the data in a framework-appropriate format.

    Attributes:
        - expected_keys: Expected keys of the data.
    """

    expected_keys: Optional[List[StrictStr]] = None

    @abstractmethod
    def _convert_dict_of_numpy_arrays_to_framework_format(
        self, data: Dict[str, npt.NDArray]
    ) -> Any:
        """Convert a dictionary of arrays to a framework-appropriate format."""

    @abstractmethod
    def _convert_numpy_input(self, data: npt.NDArray) -> Any:
        """Convert a numpy input to a framework-appropriate format."""

    @log_error(
        InferencePreprocessingError,
        "An error occurred during pre-processing.",
    )
    def preprocess(self, data: InferenceData) -> Any:
        """Preprocess the incoming InferenceData to a framework-appropriate format.

        :param data: Data to preprocess.

        :return: Preprocessed data.
        """
        if isinstance(data, dict):
            return self._convert_dict_input(data)
        return self._convert_numpy_input(data)

    def _convert_dict_input(self, data: Dict[str, npt.NDArray]) -> Any:
        self._raise_error_if_expected_keys_is_none()
        data_ = data.copy()

        if is_key_order_incorrect(data, self.expected_keys):  # type: ignore
            data_ = self._rearrange_input_order(data)

        return self._convert_dict_of_numpy_arrays_to_framework_format(data_)

    def _raise_error_if_expected_keys_are_wrong_type(self, value: Any) -> None:
        """Raise an error if the expected keys are of wrong type."""

        if not isinstance(value, list) or (
            isinstance(value, list)
            and not all(isinstance(key, str) for key in value)
        ):
            message = "Expected keys must be a list of strings."
            logger.error(message)
            raise TypeError(message)

    def _rearrange_input_order(
        self,
        input_data: Dict[str, npt.NDArray],
    ) -> Dict[str, npt.NDArray]:
        return {
            key: input_data[key] for key in self.expected_keys  # type: ignore
        }

    def _raise_error_if_expected_keys_is_none(self) -> None:
        if self.expected_keys is None:
            message = "Expected keys must be set."
            logger.error(message)
            raise ValueError(message)

    class Config:
        """Config class for Pydantic.
        At the moment, we are allowing arbitrary types to be passed to the config.
        extra = Extra.forbid is used to prevent any extra fields from being passed in the model.
        """

        # Arbitrary types are allowed to be passed to the Pydantic.
        arbitrary_types_allowed = True

        # Extra fields are not allowed to be passed to the Pydantic.
        extra = pydantic.Extra.forbid

        # Use validator when assigning values to the model.
        validate_assignment = True
