"""This module contains the CustomInferenceConfig class.
This class defines configuration parameters for a custom Inference object.
"""

from logging import getLogger
from pathlib import Path
from typing import List, Optional

from pydantic import Extra, root_validator

from mac.config.inference.inference_config import InferenceConfig
from mac.types import SupportedFrameworks

logger = getLogger(__name__)


class CustomInferenceConfig(InferenceConfig):
    """This class defines configuration parameters for a custom Inference object."""

    # Python modules to include
    matching_files: Optional[List[Path]] = None
    modules_to_include: List[Path]

    @root_validator(pre=True)
    @classmethod
    def raise_error_if_framework_invalid(cls, values):
        """Checks that the framework is supported."""
        if values["framework"] != SupportedFrameworks.CUSTOM:
            message = (
                "`framework` should be of type `SupportedFrameworks.CUSTOM`."
            )
            logger.error(message)
            raise ValueError(message)
        return values

    @root_validator(pre=True)
    @classmethod
    def raise_error_if_model_path_not_dir(cls, values):
        """Checks that the model_path is a directory.
        model_path should be a folder containing custom Python modules,
        model files and (optionally) pip requirements."""
        if not values["model_path"].is_dir():
            message = "`model_path` should be a directory."
            logger.error(message)
            raise ValueError(message)
        return values

    @root_validator
    @classmethod
    def raise_error_if_modules_not_py_files(cls, values):
        """Checks that all the module files are .py files."""
        values["matching_files"] = [
            file
            for path in values["modules_to_include"]
            for file in list(
                values["model_path"].glob(path.as_posix())
            )  # modules are always included in the model_path
        ]

        if not values["matching_files"]:
            message = "No matching files found inside `model_path`."
            logger.error(message)
            raise FileNotFoundError(message)

        if any(file.suffix != ".py" for file in values["matching_files"]):
            message = "`modules_to_include` must only match .py files."
            logger.error(message)
            raise ValueError(message)

        return values

    class Config:
        """Config class for Pydantic.
        At the moment, we are allowing arbitrary types to be passed to the config.
        extra = Extra.forbid is used to prevent any extra fields from being passed in the model.
        """

        # Arbitrary types are allowed to be passed.
        arbitrary_types_allowed = True

        # Extra fields are not allowed to be passed.
        extra = Extra.forbid
