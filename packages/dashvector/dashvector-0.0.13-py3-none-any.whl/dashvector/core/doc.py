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

import json
import numpy as np
import base64

from typing import List, Dict, Union, Optional
from dashvector.common.constants import DASHVECTOR_VECTOR_NAME
from dashvector.common.error import DashVectorException
from dashvector.common.types import DashVectorCode, DataType, CollectionMeta
from dashvector.common.types import DataParser
from dataclasses import dataclass

__all__ = ["DocBuilder", "Doc"]


@dataclass(frozen=True)
class Doc(object):
    """
    A Doc Instance.

    Args:
        id (Union[str, int]): a primary key for a unique doc.
        vector (Union[List[Union[int, float, bool]]): a vector for a doc.
        fields (Optional[Dict[str, Union[str, int, float, bool]]]): additional attributes of a doc. [optional]
        score (float): a correlation score when use doc query api, default is 0.0.

    Examples
        a_doc_with_float = Doc(id="a", vector=[0.1, 0.2])
        a_doc_with_int = Doc(id="a", vector=[1, 2])
        a_doc_with_nparray = Doc(id="a", vector=np.array([0.1, 0.2, 0.3, 0.4]))
        a_doc_with_nparray_fp16 = Doc(id="a", vector=np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float16))
        a_doc_with_fields = Doc(id="a", vector=[0.1, 0.2], fields={'price': 100, 'type': "dress"})
    """

    id: Union[str, int]
    vector: Union[List[Union[int, float]], np.ndarray]
    fields: Optional[Dict[str, Union[str, int, float, bool]]] = None
    score: float = 0.0

    def __dict__(self):
        meta_dict = {}
        if self.id is not None:
            meta_dict['id'] = self.id
        if self.vector is not None:
            meta_dict['vector'] = []
            for vector_i in self.vector:
                meta_dict['vector'].append(vector_i)
        if self.fields is not None:
            meta_dict['fields'] = self.fields
        if self.score is not None:
            meta_dict['score'] = self.score
        return meta_dict

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()


class DocBuilder(object):
    @staticmethod
    def from_meta(doc_meta: Dict,
                  *,
                  collection_meta: Optional[CollectionMeta] = None,
                  include_vector: bool = False,
                  id_is_int: bool = False):
        id = ""
        vector = []
        fields = {}
        score = 0.0
        data_type = DataType.VECTOR_FP32
        dimension = -1
        if isinstance(collection_meta, CollectionMeta):
            data_type = collection_meta.dtype
            dimension = collection_meta.dimension
        if dimension < 0:
            include_vector = False

        '''
        id: IdType
        '''
        if 'pk' in doc_meta:
            id = int(doc_meta['pk']) if id_is_int else str(doc_meta['pk'])
        elif 'primary_key' in doc_meta:
            id = int(doc_meta['primary_key']) if id_is_int else str(doc_meta['primary_key'])
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="Invalid Collection Doc Meta")

        '''
        fields: FieldDataType
        '''
        if 'fields' in doc_meta:
            for field in doc_meta['fields']:
                field_name = field['name']
                if field_name == DASHVECTOR_VECTOR_NAME and not include_vector:
                    continue

                field_value = None
                if 'value' in field and len(field['value']) > 0:
                    field_value_list = list(field['value'].values())
                    field_value = field_value_list[0]

                if field_value and field_name == DASHVECTOR_VECTOR_NAME:
                    vector = list(DataParser.unpack_feature(base64.b64decode(field_value), data_type, dimension))
                    for v_idx in range(len(vector)):
                        if data_type == DataType.VECTOR_FP16 \
                                or data_type == DataType.VECTOR_FP32 \
                                or data_type == DataType.VECTOR_FP64:
                            vector[v_idx] = float(vector[v_idx])
                        elif data_type == DataType.VECTOR_INT8 \
                                or data_type == DataType.VECTOR_INT16:
                            vector[v_idx] = int(vector[v_idx])
                        else:
                            vector[v_idx] = str(vector[v_idx])
                    continue

                fields[field_name] = field_value

        '''
        fields: float
        '''
        if 'score' in doc_meta:
            score = float(doc_meta['score'])
        return Doc(id, vector, fields, score)
