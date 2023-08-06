"""This module features entrypoints for serving a model using MLflow."""

import logging
from pathlib import Path
from typing import Callable

from mac.config.inference import CustomInferenceConfig, InferenceConfig
from mac.config.service import MLflowServiceConfig
from mac.inference.creation import InferenceBuilder
from mac.io.file_loading.json_loader import JSONLoader
from mac.service.creation import InferenceServiceFactory
from mac.utils.helpers import load_custom_inference_builder

logger = logging.getLogger(__name__)


def create_mlflow_service_config_for_auto_inference(
    config_dict: dict,
) -> MLflowServiceConfig:
    """Creates an MLflowServiceConfig for auto inference
    from a parsed model JSON file.

    The config_dict must have the following structure:
    {
        "metadata": {
            "conversion": {
                "framework": "<SupportedFrameworks>"
            },
            "file_info": {
                "file_name": "<file_name>"
            }
        }
    }

    :param config_dict: Dictionary loaded from a model JSON config.

    :raises KeyError: If the config_dict is not valid, then a KeyError is raised.

    :return: An MLflowServiceConfig instance.
    """
    logger.debug("Creating MLflowServiceConfig for auto inference...")

    framework = config_dict["data"]["model"]["conversion"]["framework"]
    model_path = config_dict["data"]["model"]["file_info"]["file_name"]

    inference_config = InferenceConfig(
        framework=framework, model_path=model_path
    )

    return MLflowServiceConfig(inference=inference_config)


def create_mlflow_service_config_for_custom_inference(
    config_dict: dict,
) -> MLflowServiceConfig:
    """Creates an MLflowServiceConfig for custom inference
    from a parsed model JSON file.

    The config_dict must have the following structure:
    {
        "metadata": {
            "conversion": {
                "framework": "<SupportedFrameworks.CUSTOM>"
            },
            "file_info": {
                "file_name": "<file_name>"
            }
        }
    }

    :param config_dict: Dictionary loaded from a model JSON config.

    :raises KeyError: If the config_dict is not valid, then a KeyError is raised.

    :return: An MLflowServiceConfig instance.
    """
    logger.debug("Creating MLflowServiceConfig for custom Inference...")

    framework = config_dict["data"]["model"]["conversion"]["framework"]
    model_path = config_dict["data"]["model"]["file_info"]["file_name"]

    inference_config = CustomInferenceConfig(
        framework=framework,
        model_path=Path(model_path),
        modules_to_include=[Path("*.py")],
    )

    return MLflowServiceConfig(inference=inference_config)


def serve_inference_with_mlflow(
    mlflow_service_config: MLflowServiceConfig,
    inference_builder: InferenceBuilder,
) -> None:
    """Entrypoint for serving a model using MLflow.

    :param mlflow_service_config_creator: Function that creates an MLflowServiceConfig instance.
    :param inference_builder: InferenceBuilder instance.

    Example of the config file:

    {
            "id": "uuid",
            "metadata": {
                "name": "model_name",
                "visibility": "string",
                "workspace_id": 1234,
                "conversion": {
                    "python_version": "3.8",
                    "framework": "keras",
                    "requirements": [],
                },
                "file_info": {
                    "version": "uuid",
                    "sha": "0000000000000000...",
                    "file_name": "model_file.h5"
                }
            }
        }
    """
    logger.info("Serving model with MLflow...")

    inference = inference_builder.create(mlflow_service_config.inference)

    inference_service = InferenceServiceFactory().create(
        mlflow_service_config.service_type.value,
        config=mlflow_service_config,
        inference=inference,
    )
    inference_service.serve()

    logger.info("Model served successfully.")


def serve_auto_inference_with_mlflow_from_json_config(
    config_path: Path,
    inference_builder: InferenceBuilder,
    mlflow_service_config_creator: Callable[
        [dict], MLflowServiceConfig
    ] = create_mlflow_service_config_for_auto_inference,
) -> None:
    """Entrypoint for serving an auto Inference from a model JSON file using MLflow.

    :param config_path: Path to the model JSON file coming from the pipeline.
    """
    logger.info("Serving auto Inference with MLflow from JSON config...")

    config = JSONLoader().load(config_path)
    mlflow_service_config = mlflow_service_config_creator(config)
    serve_inference_with_mlflow(
        mlflow_service_config=mlflow_service_config,
        inference_builder=inference_builder,
    )

    logger.info("Serving successful.")


def serve_custom_inference_with_mlflow_from_json_config(
    config_path: Path,
) -> None:
    """Entrypoint for serving a custom Inference from a model JSON file using MLflow.

    :param config_path: Path to the model JSON file coming from the pipeline.
    """
    logger.info("Serving custom Inference with MLflow from JSON config...")

    config = JSONLoader().load(config_path)
    mlflow_service_config = create_mlflow_service_config_for_custom_inference(
        config
    )
    custom_inference_builder = load_custom_inference_builder(
        mlflow_service_config.inference.matching_files  # type: ignore
    )
    serve_inference_with_mlflow(
        mlflow_service_config=mlflow_service_config,
        inference_builder=custom_inference_builder,
    )

    logger.info("Serving successful.")
