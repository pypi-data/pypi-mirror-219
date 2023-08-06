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
from dashvector.common.types import *
from dashvector.common.error import DashVectorCode, DashVectorException
from dashvector.common.handler import RPCRequest
from dashvector.core.proto import centaur_pb2


class QueryDocRequest(RPCRequest):
    def __init__(self,
                 *,
                 collection_meta: CollectionMeta,
                 vector: VectorValueType,
                 # id: Optional[IdType] = None,
                 topk: int = 10,
                 filter: Optional[str] = None,
                 include_vector: bool = False,
                 partition: Optional[str] = None,
                 output_fields: Optional[List[str]] = None):

        self._collection_meta = collection_meta
        self._collection_name = collection_meta.name
        self._collection_field_map = {field.field_name: field for field in collection_meta.fields}
        self._collection_feature_schema = collection_meta.vector_field
        self._collection_feature_format = DataParser.data_type_to_format[self._collection_feature_schema.data_type]

        '''
        QueryRequest
        '''
        query_request = centaur_pb2.QueryRequest()
        query_request.collection_name = self._collection_name
        query_request.topk = topk

        '''
        vector: Optional[VectorValueType] = None
        '''
        self._vector = None
        if isinstance(vector, list):
            if len(vector) != self._collection_feature_schema.dimension:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest vector List Length({len(vector)}) is Invalid and must be same with Collection Dimension({self._collection_feature_schema.dimension})")
            self._vector = vector
        elif isinstance(vector, np.ndarray):
            if vector.ndim != 1:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest vector NumPy Dimension({vector.ndim}) is Invalid and must be 1")
            if vector.shape[0] != self._collection_feature_schema.dimension:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest vector NumPy Shape[0]({vector.shape[0]}) is Invalid and must be same with Collection Dimension({self._collection_feature_schema.dimension})")
            self._vector = vector
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK QueryDocRequest vector Type({type(vector)}) is Invalid")

        _vector_feature = None
        if isinstance(vector, list):
            _vector_feature = DataParser.pack_feature(self._vector,
                                                      self._collection_feature_schema.data_type,
                                                      self._collection_feature_schema.dimension)
        elif isinstance(vector, np.ndarray):
            _vector_feature = np.ascontiguousarray(self._vector,
                                                   dtype=f'<{self._collection_feature_format}').tobytes()
        query_request.vector_feature.field_name = DASHVECTOR_VECTOR_NAME
        query_request.vector_feature.data_type = self._collection_feature_schema.data_type
        query_request.vector_feature.features = _vector_feature

        '''
        id: Optional[IdType] = None
        '''
        # self._id = None
        # if id is not None:
        #     if isinstance(id, (str, int)):
        #         self._id = id
        #     else:
        #         raise DashVectorException(code=DashVectorCode.InvalidArgument,
        #                                reason=f"DashVectorSDK QueryDocRequest id Type({type(id)}) is Invalid")

        '''
        topk: int = 10
        '''
        self._topk = topk
        if not isinstance(topk, int):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK QueryDocRequest topk Type({type(topk)}) is Invalid")
        if topk < 1 or topk > 1024:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK GetDocRequest topk Value({len(topk)}) is Invalid and must be in [1, 1024]")
        query_request.topk = self._topk

        '''
        filter: Optional[str] = None,
        '''
        self._filter = None
        if filter is not None:
            if not isinstance(filter, str):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest filter Type({type(filter)}) is Invalid")

            if len(filter) > 10240:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK GetDocRequest filter Length({len(filter)}) is Invalid and must be in [0, 10240]")

            if len(filter) > 0:
                self._filter = filter
        if self._filter is not None:
            query_request.filter = self._filter

        '''
        include_vector: bool = False,
        '''
        self._include_vector = include_vector
        if not isinstance(include_vector, bool):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK QueryDocRequest include_vector Type({type(include_vector)}) is Invalid")
        query_request.include_vector = self._include_vector

        '''
        partition: Optional[str] = None
        '''
        self._partition = None
        if partition is not None:
            if not isinstance(partition, str):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest partition Type({type(partition)}) is Invalid")

            if len(partition) < 3 or len(partition) > 32:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest partition Length({len(partition)}) is Invalid and must be in [3, 32]")

            if re.search('^[a-zA-Z][a-zA-Z0-9_]{0,32}$', partition) is None:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest partition Characters({partition}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")

            self._partition = partition
        if self._partition is not None:
            query_request.partition = self._partition

        '''
        output_fields: Optional[List[str]] = None
        '''
        self.output_fields = None
        if output_fields is not None:
            if isinstance(output_fields, list):
                if len(output_fields) <= 0:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason="DashVectorSDK QueryDocRequest output_fields is Empty")
                for output_field in output_fields:
                    if not isinstance(output_field, str):
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK QueryDocRequest output_field in output_fields Type({type(output_field)}) is Invalid")
                    
                    if len(output_field) < 1 or len(output_field) > 32:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK QueryDocRequest output_field in output_fields Length({len(output_field)}) is Invalid and must be in [1, 32]")

                    if re.search('^[a-zA-Z][a-zA-Z0-9_]{0,32}$', output_field) is None:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK QueryDocRequest output_field in output_fields Characters({output_field}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")
                    
                self.output_fields = output_fields
            else:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK QueryDocRequest output_fields Type({type(output_fields)}) is Invalid")
        if self.output_fields is not None:
            query_request.query_fields.extend(self.output_fields)

        super().__init__(request=query_request)

    @property
    def collection_meta(self):
        return self._collection_meta

    @property
    def collection_name(self):
        return self._collection_name

    @property
    def include_vector(self):
        return self._include_vector
