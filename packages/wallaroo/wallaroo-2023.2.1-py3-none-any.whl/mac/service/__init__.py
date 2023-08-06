"""Service package for model auto conversion.
This package contains the interfaces, classes and functions for creating inference services.

Currently, this package supports the following services:
- MLFlow inference services.
    
In the future, more inference services will be added.
"""

from .inference_service import InferenceService
from .wsgi_server_options import WSGIServerOptions
