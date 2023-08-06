##
#   Copyright 2021 Alibaba, Inc. and its affiliates. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##

# -*- coding: utf-8 -*-

import re
from dashvector.common.constants import DASHVECTOR_VECTOR_NAME
from dashvector.common.types import *
from dashvector.common.error import DashVectorCode, DashVectorException
from dashvector.common.types import DataParser
from dashvector.common.handler import RPCRequest
from dashvector.core.proto import centaur_pb2


class CreateCollectionRequest(RPCRequest):
    def __init__(self, *,
                 name: str,
                 dimension: int,
                 dtype: VectorDataType = float,
                 fields_schema: Optional[FieldDataType] = None,
                 metric: str = "euclidean",
                 extra_params: Optional[Dict[str, Any]] = None):

        """
        name: str
        """
        self._name = ""
        if not isinstance(name, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest name Type({name}) is Invalid")

        if len(name) < 3 or len(name) > 32:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest name Length({len(name)}) is Invalid and must be in [3, 32]")

        if re.search('^[a-zA-Z][a-zA-Z0-9_]{0,32}$', name) is None:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest name Characters({name}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")
        self._name = name

        """
        dim: int
        """
        self._dimension = 0
        if not isinstance(dimension, int):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dimension Type({type(dimension)}) is Invalid")

        if dimension <= 1 or dimension > 20000:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dimension Value({dimension}) is Invalid and must be in (1, 20000]")
        self._dimension = dimension

        """
        metric: str
        """
        self._metric = ""
        if not isinstance(metric, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest metric Type({type(metric)}) is Invalid")

        if metric == "euclidean":
            self._metric = "SquaredEuclidean"
        elif metric == "dotproduct":
            self._metric = "InnerProduct"
        elif metric == "cosine":
            self._metric = "Cosine"
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dim Value({metric}) is Invalid and must be in ['euclidean', 'dotproduct']")

        """
        dtype: VectorDataType 
        """
        self._dtype = float
        if not isinstance(dtype, type):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dtype Type({type(dtype)}) is Invalid")

        if dtype is not int \
                and dtype is not float:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dtype Value({dtype}) is Invalid and must be in [int, float]")
        if dtype is not float \
                and metric == "cosine":
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK CreateCollectionRequest dtype Value({dtype}) is Invalid and must be [float] when metric is cosine")

        self._dtype = dtype

        """
        fields_schema: Optional[FieldDataType] 
        """
        self._fields_schema = None
        if fields_schema is not None:
            if not isinstance(fields_schema, dict):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK CreateCollectionRequest fields_schema Type({type(fields_schema)}) is Invalid")

            if len(fields_schema) > 1024:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK CreateCollectionRequest fields_schema Length({len(fields_schema)}) is Invalid and must be in [0, 1024]")

            fields_is_empty = True
            for field_name, field_dtype in fields_schema.items():
                fields_is_empty = False

                if not isinstance(field_name, str):
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest field_name in fields_schema Type({type(field_name)}) is Invalid")

                if len(field_name) < 1 or len(field_name) > 32:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest field_name in fields_schema Length({len(field_name)}) is Invalid and must be in [1, 32]")

                if re.search('^[a-zA-Z][a-zA-Z0-9_-]{0,32}$', field_name) is None:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest field_name in fields_schema Characters({field_name}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")

                if field_name == DASHVECTOR_VECTOR_NAME:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f'DashVectorSDK CreateCollectionRequest field_name in fields_schema Value({DashVector_VECTOR_NAME}) is Reserved')

                if not isinstance(field_dtype, type):
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest field_dtype in fields_schema Type({type(field_dtype)}) is Invalid")

                if field_dtype is not str \
                        and field_dtype is not int \
                        and field_dtype is not float \
                        and field_dtype is not bool:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest field_dtype in fields_schema Value({field_dtype}) is Invalid and must be in [str, int, float, bool]")

            if not fields_is_empty:
                self._fields_schema = fields_schema

        """
        extra_params: Optional[Dict[str, Any]]
        """
        self._extra_params = {}
        if extra_params is not None:
            if not isinstance(extra_params, dict):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK CreateCollectionRequest extra_params Type({type(extra_params)}) is Invalid")

            extra_params_is_empty = True
            for extra_param_key, extra_param_value in extra_params.items():
                extra_params_is_empty = False

                if not isinstance(extra_param_key, str):
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest extra_param key Type({type(extra_param_key)}) is Invalid")

                if len(extra_param_key) <= 0:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK CreateCollectionRequest extra_param key is Empty")

            if not extra_params_is_empty:
                self._extra_params = extra_params

        """
        CreateCollectionRequest: google.protobuf.Message
        """
        create_request = centaur_pb2.CreateCollectionRequest()
        schema = create_request.schema
        schema.collection_name = self._name

        # DASHVECTOR_VECTOR_NAME field
        vector_field = schema.fields.add()
        vector_field.field_name = DASHVECTOR_VECTOR_NAME
        vector_field.data_type = DataParser.parse_vector_data_type(self._dtype)
        vector_field.index_type = centaur_pb2.IndexType.IT_HNSW
        vector_field.dimension = self._dimension

        # metric
        if len(self._metric) > 0:
            metric_extra_param = vector_field.extra_params.add()
            metric_extra_param.key = 'metric_type'
            metric_extra_param.value = self._metric

        # fields
        if self._fields_schema is not None:
            for field_name, field_dtype in self._fields_schema.items():
                new_field = schema.fields.add()
                new_field.field_name = field_name
                new_field.data_type = DataParser.parse_attr_data_type(field_dtype)

        # extra_params
        schema.channel_count = self._extra_params['channel_count'] if 'channel_count' in self._extra_params else 1
        schema.replica_count = self._extra_params['replica_count'] if 'replica_count' in self._extra_params else 2
        schema.max_docs_per_mutable_segment = self._extra_params['max_docs_per_mutable_segment'] if \
            'max_docs_per_mutable_segment' in self._extra_params else 500000
        schema.max_docs_per_immutable_segment = self._extra_params['max_docs_per_immutable_segment'] if \
            'max_docs_per_immutable_segment' in self._extra_params else 5000000

        super().__init__(request=create_request)
