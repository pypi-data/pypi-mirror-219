"""This module features helper functions for the mac package."""

import functools
import importlib
import inspect
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Set, Type

import numpy as np
import numpy.typing as npt
import pandas as pd

from mac.exceptions import (
    DirectoryNotExistError,
    FileFormatError,
    PathNotExistError,
)
from mac.inference.creation.inference_builder import InferenceBuilder

logger = logging.getLogger(__name__)


def convert_dataframe_to_numpy(data: pd.DataFrame) -> npt.NDArray:
    """Converts a Pandas DataFrame to a numpy array.

    :param data: The data to convert.

    :return: The data converted to a numpy array.
    """
    return data.to_numpy()


def convert_dataframe_to_dict_of_numpy_arrays(
    data: pd.DataFrame,
) -> Dict[str, npt.NDArray]:
    """Converts a Pandas DataFrame to a dict of numpy arrays.

    :param data: The data to convert.
    :raises ValueError: If the conversion fails.

    :return: The data converted to a dict of numpy arrays.
    """
    output = {}
    for col in data.columns:
        try:
            output[col] = np.array(data[col].tolist())
        except ValueError:
            message = (
                f"Could not convert column `{col}` to numpy array, due to ValueError. "
                "Converting to numpy array of lists instead."
            )
            logger.debug(message, exc_info=True)
            output[col] = np.array(data[col].tolist(), dtype=object)
    return output


def convert_dict_of_arrays_to_list_of_arrays(
    data: Dict[str, Iterable]
) -> List[Iterable]:
    """Converts a dict of arrays to a list of arrays preserving
    the key order.

    Example:

    {
        "output_1": np.array([1, 2, 3]),
        "output_2": np.array([4, 5, 6]),
    }

    converts to:
    [np.array([1, 2, 3]), np.array([4, 5, 6])]

    :param data: The data to convert.

    :return: The converted data.
    """
    return [data[key] for key in data.keys()]


def convert_list_of_arrays_to_dict_of_arrays(
    data: List[Iterable], expected_skeleton: str
) -> Dict[str, Iterable]:
    """Converts a list of arrays to a dict of arrays with sorted
    keys in ascending order.

    Example:
    {
        "output_1": np.array([1, 2, 3]),
        "output_2": np.array([4, 5, 6]),
    }

    :param data: The data to convert.
    :param expected_skeleton: The expected skeleton of the keys.

    :return: The converted data to a dict of iterables.
    """
    return {f"{expected_skeleton}_{i+1}": data for i, data in enumerate(data)}


def convert_list_of_dicts_to_dict_of_numpy_arrays(
    data: List[Dict[str, Any]], expected_keys: List[str]
) -> Dict[str, npt.NDArray]:
    """Converts a list of dicts to a dict of numpy arrays.

    :param data: The data to convert.
    :param expected_keys: The expected keys of the dicts.

    :return: The converted data to a dict of numpy arrays.
    """
    return {
        key: np.array([item[key] for item in data]) for key in expected_keys
    }


def is_class_member(obj: Callable) -> bool:
    """Checks if the given object is a class member.

    :param obj: The object to check.

    :return: True if the given object is a class member, False otherwise.
    """
    return inspect.isclass(obj)


def is_key_order_incorrect(data: Dict[str, Any], expected_keys: list) -> bool:
    """Checks if the keys of the given dictionary are in the correct order.

    :param data: The dictionary to check.
    :param expected_keys: The expected keys of the dictionary.

    :return: True if the keys of the given dictionary are in the correct order,
    False otherwise.
    """
    return list(data.keys()) != expected_keys


def is_object_derived_from_class(obj: Any, cls: Any) -> bool:
    """Checks if the given object is derived from the given class.

    :param obj: The object to check.
    :param cls: The class to check.

    :return: True if the given object is derived from the given class, False otherwise.
    """
    return issubclass(obj, cls) and obj.__name__ != cls.__name__


def load_custom_inference_builder(
    matching_files: List[Path],
) -> InferenceBuilder:
    """Load custom inference builder from the python modules specified in a
    given custom inference config.

    :param matching_files: A list of paths to the python files that contain the
    custom InferenceBuilder and its related components.

    :return: An InferenceBuilder subclass instance.
    """
    logger.info("Loading custom InferenceBuilder from Python files...")

    inference_builder = None

    for py_file in matching_files:  # type: ignore
        module = import_py_module_from_path(py_file, "custom_inference")
        for _, obj in inspect.getmembers(module, is_class_member):
            if is_object_derived_from_class(obj, InferenceBuilder):
                if inference_builder is None:
                    inference_builder = obj()
                else:
                    message = "Multiple InferenceBuilder subclasses found in the given files."
                    logger.error(message)
                    raise ValueError(message)

    if inference_builder is None:
        message = "No InferenceBuilder subclass found in the given files."
        logger.error(message)
        raise AttributeError(message)

    logger.info("Loading successful.")

    return inference_builder


def import_py_module_from_path(file_path: Path, spec_name: str) -> Any:
    """Import a python module from a given file path.

    :param file_path: The path of the file to import the module from.
    :param spec_name: The name to import the module as.

    :return: The imported module.
    """
    spec = importlib.util.spec_from_file_location(spec_name, file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore

    try:
        spec.loader.exec_module(module)  # type: ignore
    except FileNotFoundError as exc:
        message = f"Could not load module from file: {file_path.as_posix()}."
        logger.error(message, exc_info=True)
        raise exc

    return module


def raise_file_format_error_if_file_format_incorrect(
    file_path: Path, supported_file_formats: Set[str]
) -> None:
    """Raise a FileFormatError if the format of the given file is not supported, i.e.,
        the format of the given file is not in the supported_file_formats.

    :param file_path: The path of the file which we want to check the validity of its format.
    The file must exist.
    :param supported_file_formats: A list of supported file formats. The concreate classes that
    deal with files should define this attribute.

    :raises FileFormatError: If the format of the given file is not in the supported_file_formats
    list, then a FileFormatError is raised.
    """
    file_format = file_path.suffix[1:]
    if file_format not in supported_file_formats:
        message = (
            f"File format {file_format} is not supported. "
            f"Supported file formats are: {supported_file_formats}."
        )
        logger.error(message)
        raise FileFormatError(message)


def log_error(exception_type: Type[Exception], message: str) -> Any:
    """This helper function logs the error and raises the given exception type.

    :param exception_type: The type of the exception to raise.
    :param message: The message to log.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.error(message, exc_info=True)
                raise exception_type(message) from exc

        return wrapper

    return decorator


def raise_path_not_exist_error_if_no_path(
    path: Path,
) -> None:
    """This helper function raises an error if the path passed doesn't exist.

    :param path: Path of a file.

    :raises PathDoesNotExistError: If there is no file at the given path, then
    PathDoesNotExistError is raised.
    """
    if not path.exists():
        message = f"There is no file or directory at: '{path.as_posix()}'."
        logger.error(message)
        raise PathNotExistError(message)


def raise_directory_not_exists_if_no_dir(
    directory: Path,
) -> None:
    """Raise an error if the directory doesn't exist.

    :param directory: Path to the directory.

    :raises DirectoryNotExistError: If there is no directory at the given path, then
        DirectoryNotExistError is raised.
    """
    if not directory.is_dir():
        message = f"There is no directory at: '{directory.as_posix()}'."
        logger.error(message)
        raise DirectoryNotExistError(message)
