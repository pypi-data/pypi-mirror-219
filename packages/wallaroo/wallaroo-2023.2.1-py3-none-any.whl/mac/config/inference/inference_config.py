"""This module contains the InferenceConfig class.
This class defines configuration parameters for an Inference object.
"""

from typing import Union

from pydantic import BaseModel, DirectoryPath, Extra, FilePath

from mac.types import SupportedFrameworks


class InferenceConfig(BaseModel):
    """This class defines configuration parameters for an Inference object."""

    # The framework of the model to be loaded. See SupportedFrameworks for more info.
    framework: SupportedFrameworks

    # The path to the model.
    model_path: Union[FilePath, DirectoryPath]

    class Config:
        """Config class for Pydantic.
        At the moment, we are allowing arbitrary types to be passed to the config.
        extra = Extra.forbid is used to prevent any extra fields from being passed in the model.
        """

        # Arbitrary types are allowed to be passed to the Pydantic.
        arbitrary_types_allowed = True

        # Extra fields are not allowed to be passed to the Pydantic.
        extra = Extra.forbid
