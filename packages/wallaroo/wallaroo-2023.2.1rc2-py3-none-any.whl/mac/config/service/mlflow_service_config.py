"""This module features the MLflowServiceConfig class."""

import logging
from typing import Dict, Optional, Union

from pydantic import Extra, validator

from mac.config.service.inference_service_config import InferenceServiceConfig
from mac.exceptions import MLflowModelSignatureError
from mac.types import SupportedServices

logger = logging.getLogger(__name__)


class MLflowServiceConfig(InferenceServiceConfig):
    """This class represents the configuration of MLflowService."""

    model_signature: Optional[Dict[str, str]]

    @property
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""
        return SupportedServices.MLFLOW

    @validator("model_signature")
    @classmethod
    def model_signature_check(cls, value) -> Union[Dict[str, str], None]:
        """Checks if the signature dictionary has the valid keys.
        Only ["inputs", "outputs"] are allowed as keys. If the keys are not
        valid, then MLflowModelSignatureError is raised.

        :param value: Model signature as a dictionary.

        :raises MLflowModelSignatureError: If the parameter value does not have the
            valid keys.

        :return: validated value
        """
        keys = value.keys()
        expected_keys = ["inputs", "outputs"]
        if not set(keys) == set(expected_keys):
            message = f"Found keys {keys}, but expected {expected_keys}."
            logger.error(message)
            raise MLflowModelSignatureError(message)

        return value

    class Config:
        """Config class for Pydantic.
        At the moment, we are allowing arbitrary types to be passed to the config.
        extra = Extra.forbid is used to prevent any extra fields from being passed in the model.
        """

        # Arbitrary types are allowed to be passed to the Pydantic.
        arbitrary_types_allowed = True
        # Extra fields are not allowed to be passed to the Pydantic.
        extra = Extra.forbid
