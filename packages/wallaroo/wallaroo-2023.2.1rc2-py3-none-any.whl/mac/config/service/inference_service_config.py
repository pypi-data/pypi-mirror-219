"""This module contains the InferenceServiceConfig class.
InferenceServiceConfig is the base class for all inference service configurations
such as MLflow service.
"""

from abc import abstractmethod

from pydantic import BaseModel, Extra

from mac.config.inference import InferenceConfig
from mac.types import SupportedServices


class InferenceServiceConfig(BaseModel):
    """This class represents the configuration for an Inference Service object (e.g., MLflow
    service).
    """

    inference: InferenceConfig

    @property
    @abstractmethod
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""

    class Config:
        """Config class for Pydantic.
        At the moment, we are allowing arbitrary types to be passed to the config.
        extra = Extra.forbid is used to prevent any extra fields from being passed in the model.
        """

        # Arbitrary types are allowed to be passed to the Pydantic.
        arbitrary_types_allowed = True
        # Extra fields are not allowed to be passed to the Pydantic.
        extra = Extra.forbid
