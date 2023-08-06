import wallaroo
from wallaroo.model_config import ModelConfig
from wallaroo.model import Model

import datetime
import responses
import unittest

from . import testutil


class TestModelConfig(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth"
        )

    @responses.activate
    def test_init_full_dict(self):

        model_config = ModelConfig(
            client=self.test_client,
            data={
                "id": 1,
                "filter_threshold": 0.1234,
                "model": {
                    "id": 2,
                },
                "runtime": "onnx",
                "tensor_fields": ["foo", "bar", "baz"],
            },
        )

        self.assertEqual(1, model_config.id())
        self.assertEqual(0.1234, model_config.filter_threshold())
        self.assertEqual(2, model_config.model().id())
        self.assertEqual("onnx", model_config.runtime())
        self.assertEqual(["foo", "bar", "baz"], model_config.tensor_fields())

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("filter_threshold", 0.1234),
            ("runtime", "onnx"),
            ("tensor_fields", ["foo", "bar"]),
            # TODO: Test model_variant()
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    "http://api-lb/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("ModelConfigById")],
                    json={
                        "data": {
                            "model_config_by_pk": {
                                "id": 1,
                                "filter_threshold": 0.1234,
                                "model": {
                                    "id": 2,
                                },
                                "runtime": "onnx",
                                "tensor_fields": ["foo", "bar"],
                            },
                        },
                    },
                )

                model_config = ModelConfig(client=self.test_client, data={"id": 1})

                self.assertEqual(want_value, getattr(model_config, method_name)())
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                self.assertEqual(want_value, getattr(model_config, method_name)())
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    def test_to_yaml_all_fields(self):
        expected_yaml = """filter_threshold: 0.4
model_id: model_class
model_version: model_name
runtime: onnx
tensor_fields:
- tensor
"""
        model = Model.as_standalone("model_class", "model_name", "hubert.onnx")
        model_config = ModelConfig.as_standalone(
            model=model, filter_threshold=0.4, runtime="onnx", tensor_fields=["tensor"]
        )
        self.assertEqual(expected_yaml, model_config.to_yaml())

    def test_to_yaml_no_optional_fields(self):
        expected_yaml = """model_id: model_class
model_version: model_name
"""
        model = Model.as_standalone("model_class", "model_name", "hubert.onnx")
        model_config = ModelConfig.as_standalone(model=model)
        self.assertEqual(expected_yaml, model_config.to_yaml())
