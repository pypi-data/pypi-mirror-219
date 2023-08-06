from wallaroo.engine_config import EngineConfig

import unittest


class TestEngineConfig(unittest.TestCase):
    def test_to_yaml_all_fields(self):
        expected_yaml = """audit_logging:
  enabled: false
cpus: 4
directories:
  model: /quux
  model_config: /foo
  pipeline_config: /bar
gpus: 0
inference_channel_size: 5000
input_protocol: http
input_type: json
k8s:
  namespace: wallaroo-standalone
model_server:
  model_concurrency: 1
  model_dir: /models
onnx:
  intra_op_parallelism_threads: 4
sink:
  type: http_response
"""
        engine_config = EngineConfig.as_standalone(
            cpus=4,
            gpus=0,
            inference_channel_size=5000,
            model_concurrency=1,
            model_config_directory="/foo",
            pipeline_config_directory="/bar",
            model_directory="/quux",
        )
        assert engine_config.to_yaml() == expected_yaml

    def test_to_yaml_no_optional_fields(self):
        expected_yaml = """audit_logging:
  enabled: false
cpus: 4
directories:
  model: /model
  model_config: /modelconfig
  pipeline_config: /pipelineconfig
gpus: 0
inference_channel_size: 10000
input_protocol: http
input_type: json
k8s:
  namespace: wallaroo-standalone
model_server:
  model_concurrency: 2
  model_dir: /models
onnx:
  intra_op_parallelism_threads: 4
sink:
  type: http_response
"""
        engine_config = EngineConfig.as_standalone(cpus=4)
        assert engine_config.to_yaml() == expected_yaml
