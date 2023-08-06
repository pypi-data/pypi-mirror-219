"""This module implements the MLflowService class, for serving models using MLflow.
"""

import logging
from typing import Optional

import mlflow.pyfunc.scoring_server as mlflow_service
from flask.app import Flask
from gevent.pywsgi import WSGIServer
from mlflow.models.model import Model as ModelMeta
from mlflow.models.signature import ModelSignature as MLflowSignature
from mlflow.pyfunc import PyFuncModel
from mlflow.pyfunc.model import _PythonModelPyfuncWrapper

from mac.config.service import MLflowServiceConfig
from mac.inference import Inference
from mac.service import InferenceService, WSGIServerOptions
from mac.service.mlflow.mlflow_adapter import MLflowAdapter
from mac.types import SupportedFrameworks
from mac.utils.helpers import convert_dataframe_to_dict_of_numpy_arrays

logger = logging.getLogger(__name__)

prepare_input_func_mapping = {
    SupportedFrameworks.KERAS.value: convert_dataframe_to_dict_of_numpy_arrays,
    SupportedFrameworks.SKLEARN.value: convert_dataframe_to_dict_of_numpy_arrays,
    SupportedFrameworks.PYTORCH.value: convert_dataframe_to_dict_of_numpy_arrays,
    SupportedFrameworks.XGBOOST.value: convert_dataframe_to_dict_of_numpy_arrays,
    SupportedFrameworks.HUGGING_FACE.value: convert_dataframe_to_dict_of_numpy_arrays,
    SupportedFrameworks.CUSTOM.value: convert_dataframe_to_dict_of_numpy_arrays,
}


class MLflowService(InferenceService):
    """This class implements the MLflowService, in order to serve Inference objects using MLflow.

    Attributes:
        - server_options: A WSGIServerOptions instance.
        - pyfunc_model: A PyFuncModel instance.
        - flask_app: A Flask instance.
        - wsgi_server: A WSGIServer instance.
    """

    def __init__(self, server_options: WSGIServerOptions) -> None:
        """Initialize MLflowService class."""
        self._server_options = server_options
        self._pyfunc_model: Optional[PyFuncModel] = None
        self._flask_app: Optional[Flask] = None
        self._wsgi_server: Optional[WSGIServer] = None

        super().__init__()

    @property
    def pyfunc_model(self) -> PyFuncModel:
        """Returns _pyfunc_model instance.

        :return: PyFuncModel instance.
        """
        return self._pyfunc_model

    @pyfunc_model.setter  # type: ignore
    def pyfunc_model(self, pyfunc_model: PyFuncModel) -> None:
        """Sets the _pyfunc_model instance.

        :param pyfunc_model: PyFuncModel instance.

        :raises TypeError: If pyfunc_model is not of type PyFuncModel.
        """
        self._raise_error_if_pyfunc_model_is_of_wrong_type(pyfunc_model)
        self._pyfunc_model = pyfunc_model

    def serve(self) -> None:
        """This method serves an Inference object using the MLflow service."""
        logger.info("Initializing WSGI server...")
        self._init_wsgi_server()
        logger.info("Successfully initialized WSGI server.")
        self._wsgi_server.serve_forever()  # type: ignore [union-attr]

    def _init_wsgi_server(self) -> None:
        """Initialize a Gunicorn app from a Flask app."""
        self._raise_error_if_pyfunc_model_does_not_exist()

        self._init_flask_app()
        self._wsgi_server = WSGIServer(
            (self._server_options.host, self._server_options.port),
            application=self._flask_app,
        )

    def _raise_error_if_pyfunc_model_does_not_exist(self) -> None:
        if not self._pyfunc_model:
            message = "PyFuncModel not assigned to the service."
            logger.error(message)
            raise ValueError(message)

    def _init_flask_app(self) -> None:
        """Initialize Flask app with the PyFuncModel."""
        self._flask_app = mlflow_service.init(model=self._pyfunc_model)

    def _raise_error_if_pyfunc_model_is_of_wrong_type(
        self, pyfunc_model: PyFuncModel
    ) -> None:
        if not isinstance(pyfunc_model, PyFuncModel):
            message = (
                f"Expected _pyfunc_model to be of type PyFuncModel, but "
                f"got {type(pyfunc_model).__name__} instead."
            )
            logger.error(message)
            raise TypeError(message)


def _create_pyfunc_model(
    mlflow_adapter: MLflowAdapter, model_meta: ModelMeta
) -> PyFuncModel:
    """Creates a PyFuncModel instance from a given adapter and a model metadata.

    :param mlflow_adapter: A MLFlowAdapter instance.
    :param model_meta: An MLflow Model instance that holds metadata for the model.

    :return: A PyFuncModel instance.
    """
    model_impl = _PythonModelPyfuncWrapper(mlflow_adapter, None)
    return PyFuncModel(model_meta=model_meta, model_impl=model_impl)


def _create_model_metadata(config: MLflowServiceConfig) -> ModelMeta:
    """Create a MLflow Model instance given a config.

    :param config: A MLflowServiceConfig instance, which holds the service and model signature.

    :return: An MLflow Model instance that holds metadata for the model.
    """
    model_signature = (
        MLflowSignature.from_dict(config.model_signature)
        if config.model_signature
        else None
    )
    return ModelMeta(signature=model_signature)


def create_mlflow_service(
    config: MLflowServiceConfig, inference: Inference
) -> MLflowService:
    """Initializes an MLflowService based on the given MLflowServiceConfig
    with the given Inference object.

    :param config: A MLflowServiceConfig instance.
    :param inference: An Inference instance.

    :return: A MLflowService instance.
    """
    logger.info("Creating MLflow service...")

    _mlflow_service = MLflowService(server_options=WSGIServerOptions())

    _mlflow_service.inference = inference
    prepare_inputs_func = prepare_input_func_mapping[  # type: ignore [assignment]
        config.inference.framework
    ]
    mlflow_adapter = MLflowAdapter(
        _mlflow_service.inference, prepare_inputs_func  # type: ignore [arg-type]
    )

    model_meta = _create_model_metadata(config)
    _mlflow_service.pyfunc_model = _create_pyfunc_model(
        mlflow_adapter=mlflow_adapter, model_meta=model_meta
    )

    logger.info("Successfully created MLflow service.")

    return _mlflow_service
