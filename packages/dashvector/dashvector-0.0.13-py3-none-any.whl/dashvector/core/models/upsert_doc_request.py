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
from dashvector.core.doc import Doc


class UpsertDocRequest(RPCRequest):
    def __init__(self, *,
                 collection_meta: CollectionMeta,
                 docs: Union[Doc, Tuple, List[Doc], List[Tuple]],
                 partition: Optional[str] = None,
                 action: str = "upsert"):

        """
        collection_meta: CollectionMeta
        """
        self._collection_meta = collection_meta
        self._collection_name = collection_meta.name
        self._collection_field_map = {field.field_name: field for field in collection_meta.fields}
        self._collection_feature_schema = collection_meta.vector_field
        if self._collection_feature_schema.data_type not in DataParser.data_type_to_format:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest Invalid vector Type({self._collection_feature_schema.data_type}) to Format")
        self._collection_feature_format = DataParser.data_type_to_format[self._collection_feature_schema.data_type]

        """
        partition: Optional[str]
        """
        self._partition = None
        if partition is not None:
            if not isinstance(partition, str):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest partition Type({type(partition)}) is Invalid")

            if len(partition) < 3 or len(partition) > 32:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest partition Length({len(partition)}) is Invalid and must be in [3, 32]")

            if re.search('^[a-zA-Z][a-zA-Z0-9_]{0,32}$', partition) is None:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest partition Characters({partition}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")

            self._partition = partition

        """
        action: str
        """
        self._action = ""
        if not isinstance(action, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest action Type({type(pt)}) is Invalid")
        if action != "upsert" and action != "insert" and action != "update":
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest action Value({action}) is Invalid and must be in ['insert', 'update', 'upsert']")
        self._action = action

        """
        InsertDocRequest: google.protobuf.Message
        UpdateDocRequest: google.protobuf.Message
        UpsertDocRequest: google.protobuf.Message
        """
        if self._action == "upsert":
            upsert_request = centaur_pb2.UpsertDocRequest()
        elif self._action == "insert":
            upsert_request = centaur_pb2.InsertDocRequest()
        else:
            upsert_request = centaur_pb2.UpdateDocRequest()
        upsert_request.collection_name = self._collection_name
        if self._partition is not None:
            upsert_request.partition = self._partition

        """
        docs: Union[Doc, Tuple, List[Doc], List[Tuple]]
        """
        id_list = []
        vector_list = []
        fields_list = []

        if isinstance(docs, Doc):
            id, vector, fields = self._format_input(doc=docs)
            id_list.append(id)
            vector_list.append(vector)
            fields_list.append(fields)
        elif isinstance(docs, tuple):
            id, vector, fields = self._format_input(tup=docs)
            id_list.append(id)
            vector_list.append(vector)
            fields_list.append(fields)
        elif isinstance(docs, list):
            if len(docs) <= 0 or len(docs) > 1024:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest Input docs Length({len(docs)}) is Invalid and must be in [1, 1024]")

            for doc in docs:
                id, vector, fields = None, None, None
                if isinstance(doc, Doc):
                    id, vector, fields = self._format_input(doc=doc)
                elif isinstance(doc, tuple):
                    id, vector, fields = self._format_input(tup=doc)
                else:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest Invalid doc Type({type(doc)}) in docs")
                id_list.append(id)
                vector_list.append(vector)
                fields_list.append(fields)
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest Input Type({type(docs)}) is Invalid and must be in [Doc, Tuple]")

        id_list, vector_list, fields_list = self._format_params(id_list, vector_list, fields_list)

        for _list_id in range(len(id_list)):
            id = id_list[_list_id]
            vector = vector_list[_list_id]
            attr_value = fields_list[_list_id]

            new_doc = upsert_request.doc_list.docs.add()
            new_doc.pk = id if isinstance(id, str) else str(id)
            new_field = new_doc.fields.add()
            new_field.name = DASHVECTOR_VECTOR_NAME
            if isinstance(vector, bytes):
                new_field.value.bytes_value = vector
            elif isinstance(vector, str):
                new_field.value.string_value = vector
            else:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest vector Type({type(vector)}) in invalid")

            if attr_value is None:
                continue

            for field_name, filed_value in attr_value.items():
                if not isinstance(field_name, str):
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest field name Type({type(field_name)}) is Invalid")

                if len(field_name) < 1 or len(field_name) > 32:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest field name Length({len(field_name)}) is Invalid and must be in [1, 32]")

                if re.search('^[a-zA-Z][a-zA-Z0-9_]{0,32}$', field_name) is None:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest field name Characters({field_name}) is Invalid and must be in [a-zA-Z0-9] and symbols[_]")

                new_field = new_doc.fields.add()
                new_field.name = field_name

                if field_name in self._collection_field_map:
                    field_schema = self._collection_field_map[field_name]
                    field_schema_is_invalid = False
                    try:
                        if field_schema.data_type == DataType.BOOL:
                            new_field.value.bool_value = filed_value
                        elif field_schema.data_type == DataType.INT32:
                            new_field.value.int32_value = filed_value
                        elif field_schema.data_type == DataType.INT64:
                            new_field.value.int64_value = filed_value
                        elif field_schema.data_type == DataType.UINT32:
                            new_field.value.uint32_value = filed_value
                        elif field_schema.data_type == DataType.UINT64:
                            new_field.value.uint64_value = filed_value
                        elif field_schema.data_type == DataType.FLOAT:
                            new_field.value.float_value = filed_value
                        elif field_schema.data_type == DataType.DOUBLE:
                            new_field.value.double_value = filed_value
                        elif field_schema.data_type == DataType.STRING:
                            new_field.value.string_value = filed_value
                        elif field_schema.data_type == DataType.BINARY:
                            new_field.value.bytes_value = filed_value
                        else:
                            field_schema_is_invalid = True
                    except Exception as e:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK UpsertDocRequest Field key({field_name}) is Invalid")

                    if field_schema_is_invalid:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK UpsertDocRequest Field key({field_name}) is Invalid")
                else:
                    if isinstance(filed_value, str):
                        new_field.value.string_value = filed_value
                    elif isinstance(filed_value, int):
                        new_field.value.int32_value = filed_value
                    elif isinstance(filed_value, float):
                        new_field.value.float_value = filed_value
                    elif isinstance(filed_value, bool):
                        new_field.value.bool_value = filed_value
                    else:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason=f"DashVectorSDK UpsertDocRequest Field key({field_name}) is Invalid")

        super().__init__(request=upsert_request)

    def _format_input(self,
                      *,
                      doc: Optional[Doc] = None,
                      tup: Optional[Tuple] = None):
        if doc is not None:
            return doc.id, doc.vector, doc.fields
        if tup is not None:
            if len(tup) == 2:
                return tup[0], tup[1], None
            elif len(tup) == 3:
                return tup[0], tup[1], tup[2]
            else:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest doc tuple Length({len(tup)}) is Invalid")
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason="DashVectorSDK UpsertDocRequest Input is Empty")

    def _format_params(self,
                       id_list: List[IdType],
                       vector_list: List[VectorValueType],
                       fields_list: Optional[List[FieldValueType]] = None):

        batch_size = len(id_list)

        for id in id_list:
            if isinstance(id, int):
                _id_str = str(id)
                if len(_id_str) < 1 or len(_id_str) > 64:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest id Length({len(_id_str)}) is Invalid and must be in [1, 64]")
            elif isinstance(id, str):
                if len(id) < 1 or len(id) > 64:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest id Length({len(id)}) is Invalid and must be in [1, 64]")

                if re.search('^[a-zA-Z0-9_\-!@#$%+=.]{0,64}$', id) is None:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest id Characters({id}) is Invalid and must be in [a-zA-Z0-9] and symbols[_-!@#$%+=.]")
            else:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest id Type({type(id)}) Invalid")

        if batch_size != len(vector_list):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest batch size({batch_size}) is Different between id and vector")

        for vector_idx in range(len(vector_list)):
            vector = vector_list[vector_idx]
            if isinstance(vector, list):
                if len(vector) != self._collection_feature_schema.dimension:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest vector List Length({len(vector)}) is Invalid and must be same with Collection Dimension({self._collection_feature_schema.dimension})")
                if self._collection_feature_schema.data_type == DataType.VECTOR_INT8:
                    for v_idx in range(len(vector)):
                        vector[v_idx] = bytes(str(vector[v_idx]), encoding='utf-8')
                try:
                    vector_list[vector_idx] = DataParser.pack_feature(vector, self._collection_feature_schema.data_type, self._collection_feature_schema.dimension)
                except Exception as e:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest vector Value({vector}) is Invalid")
            elif isinstance(vector, np.ndarray):
                if vector.ndim != 1:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest vector NumPy Dimension({vector.ndim}) is Invalid and must be 1")
                if vector.shape[0] != self._collection_feature_schema.dimension:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest vector NumPy Shape[0]({vector.shape[0]}) is Invalid and must be same with Collection Dimension({self._collection_feature_schema.dimension})")
                try:
                    vector_list[vector_idx] = np.ascontiguousarray(vector, dtype=f'<{self._collection_feature_format}').tobytes()
                except Exception as e:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason=f"DashVectorSDK UpsertDocRequest vector Value({vector}) is Invalid")
            else:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest vector Type({type(vector)}) is Invalid")

        if batch_size != len(fields_list):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK UpsertDocRequest batch size({batch_size}) is Different between id and fields")

        for fields_one in fields_list:
            if fields_one is None:
                continue

            if not isinstance(fields_one, dict):
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest fields Type({type(fields_one)}) is Invalid")

            if len(fields_one) > 1024:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK UpsertDocRequest fields Length({len(fields_one)}) is Invalid and must be in [1, 1024]")

        return id_list, vector_list, fields_list

    @property
    def collection_name(self):
        return self._collection_name